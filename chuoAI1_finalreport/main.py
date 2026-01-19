import pandas as pd
from transformers import AutoTokenizer, BertForSequenceClassification, pipeline
import torch

# === 設定 ===
csv_file = 'data.csv'
model_name = 'koheiduck/bert-japanese-finetuned-sentiment'

# 1. データの読み込みと整形（ここがパワーアップした部分）
print(f"{csv_file} を読み込んでいます...")

try:
    # ヘッダーなし(header=None)として読み込む
    df = pd.read_csv(csv_file, header=None, encoding='utf-8')
except UnicodeDecodeError:
    df = pd.read_csv(csv_file, header=None, encoding='shift_jis')

# データが「横長（1行にたくさん）」になっている場合の補正
if df.shape[0] == 1 and df.shape[1] > 1:
    print("データが横並びのため、縦並びに変換します...")
    df = df.T  # 行と列を入れ替える
    df.columns = ['text'] # 列名をtextにする
elif df.shape[1] >= 1:
    # すでに縦並びの場合でも、1列目を採用する
    df = df.iloc[:, [0]] # 1列目だけ抜き出す
    df.columns = ['text']

# 空行を削除
df = df.dropna()

print(f"データ数: {len(df)}件")
if len(df) != 100:
    print(f"注意: データ数が100件ではありません（{len(df)}件）。コピー漏れがないか確認してください。")

# 2. モデルの準備
print("モデルを読み込んでいます...")
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = BertForSequenceClassification.from_pretrained(model_name)
sentiment_analyzer = pipeline("sentiment-analysis", model=model, tokenizer=tokenizer)

# 3. 分析と集計の実行
print("分析を開始します（数分かかります）...")

labels = []
scores = []

for i, text in enumerate(df['text']):
    # 10件ごとに進捗表示
    if i % 10 == 0:
        print(f"{i}件目完了...")

    # 文字列処理
    text = str(text)
    text = text[:512] # 長すぎる文章はカット
    
    # 感情分析実行
    result = sentiment_analyzer(text)[0]
    labels.append(result['label'])
    scores.append(result['score'])

# 結果を追加
df['label'] = labels
df['score'] = scores

# === 期末レポート回答用データの計算 ===
print("\n" + "="*30)
print("【期末レポート 回答用データ】")
print("="*30)

# ① 感情分析のポジティブの最大スコア
max_pos = df[df['label'].str.upper() == 'POSITIVE']['score'].max()
if pd.isna(max_pos): max_pos = 0.0
print(f"① ポジティブの最大スコア: {max_pos:.3f}")

# ② 感情分析のネガティブの最大スコア
max_neg = df[df['label'].str.upper() == 'NEGATIVE']['score'].max()
if pd.isna(max_neg): max_neg = 0.0
print(f"② ネガティブの最大スコア: {max_neg:.3f}")

# ③ ポジティブ (0 ≦ score ≦ 0.5)
count_pos_low = len(df[
    (df['label'].str.upper() == 'POSITIVE') & 
    (df['score'] >= 0) & (df['score'] <= 0.5)
])
print(f"③ ポジティブ (0 ≦ score ≦ 0.5) の件数: {count_pos_low}")

# ④ ポジティブ (0.5 < score ≦ 1)
count_pos_high = len(df[
    (df['label'].str.upper() == 'POSITIVE') & 
    (df['score'] > 0.5) & (df['score'] <= 1.0)
])
print(f"④ ポジティブ (0.5 < score ≦ 1) の件数: {count_pos_high}")

# ⑤ ネガティブ (0 ≦ score ≦ 0.5)
count_neg_low = len(df[
    (df['label'].str.upper() == 'NEGATIVE') & 
    (df['score'] >= 0) & (df['score'] <= 0.5)
])
print(f"⑤ ネガティブ (0 ≦ score ≦ 0.5) の件数: {count_neg_low}")

# ⑥ ネガティブ (0.5 < score ≦ 1)
count_neg_high = len(df[
    (df['label'].str.upper() == 'NEGATIVE') & 
    (df['score'] > 0.5) & (df['score'] <= 1.0)
])
print(f"⑥ ネガティブ (0.5 < score ≦ 1) の件数: {count_neg_high}")

print("="*30)

# 結果ファイルの保存
output_file = 'final_report_result.csv'
df.to_csv(output_file, index=False, encoding='utf-8-sig')
print(f"結果は {output_file} に保存されました。")