# -*- coding: utf-8 -*-

# 生成AI使用情報
# 本レポート作成において、2025年11月27日にClaude Opus 4.5を参考資料として使用しました。


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


# (1) cycle.csv を読み込み、df_cycle という変数に格納し、最初の5行を表示


print("(1) データの読み込みと最初の5行の表示")

# csvファイルの読み込み
df_cycle = pd.read_csv("cycle.csv")

# 最初の5行を表示
print(df_cycle.head())
print()


# (2) df_cycle の行数と列数を確認


print("(2) 行数と列数の確認")


# shapeで行数と列数を確認
print("行数:", df_cycle.shape[0])
print("列数:", df_cycle.shape[1])
print()


# (3) df_cycle の基本統計量を算出


print("(3) 基本統計量")


# describe()で基本統計量を算出
print(df_cycle.describe())
print()


# (4) 欠損値の有無を確認し、欠損値がある場合には補完・削除などの処理


print("(4) 欠損値の確認と処理")


# isnull()で欠損値の確認
print("各列の欠損値の数:")
print(df_cycle.isnull().sum())
print()

# 欠損値の合計を計算
missing_total = df_cycle.isnull().sum().sum()
print("欠損値の合計:", missing_total)
print()

# 欠損値がある場合の処理
if missing_total > 0:
    # 欠損値を含む行を表示
    print("欠損値を含む行:")
    print(df_cycle[df_cycle.isnull().any(axis=1)])
    print()
    
    # hr（時間）列に欠損値があるため削除
    # 理由: 時間は0~23の離散値であり、補完すると不正確になる可能性がある
    print("欠損値を含む行を削除します。")
    df_cycle = df_cycle.dropna()
    print("削除後の行数:", df_cycle.shape[0])
    print()
else:
    print("欠損値はありません。")
    print()


# (5) 時間別の利用数合計を集計し、棒グラフで表示


print("(5) 時間別の利用数合計の集計と可視化")


# groupbyで時間別に集計
hourly_cnt = df_cycle.groupby("hr")["cnt"].sum()
print("時間別の利用数合計:")
print(hourly_cnt)
print()

# 棒グラフの作成
fig, ax = plt.subplots(figsize=(12, 6))
ax.bar(hourly_cnt.index, hourly_cnt.values, color="steelblue")
ax.set_xlabel("Hour")
ax.set_ylabel("Total Count")
ax.set_title("Hourly Rental Count")
ax.set_xticks(range(0, 24))
ax.grid(axis="y", alpha=0.3)
fig.savefig("hourly_count.png")
plt.show()

print()
print("【グラフから読み取れること】")
print("1. 朝8時と夕方17-18時に利用数のピークがある。")
print("   これは通勤・通学の時間帯と一致しており、レンタサイクルが")
print("   日常の移動手段として利用されていることがわかる。")
print()
print("2. 深夜から早朝（0-5時）は利用数が非常に少ない。")
print("   この時間帯は人の活動が少ないため、自然な結果である。")
print()
print("3. 夕方のピーク（17-18時）は朝のピーク（8時）よりも高い。")
print("   これは帰宅時間が分散しにくいこと、また仕事帰りに")
print("   買い物や寄り道をする人がいるためと考えられる。")
print()


# (6) (5)以外の集計・可視化と考察


print("(6) 追加の分析と考察")





# 分析1: 季節と時間帯による利用パターンの違い
# 仮説: 季節によって利用数が異なるのではないか

print()
print("【分析4: 季節と時間帯による利用パターンの違い】")

print("仮説: 季節によって利用数が異なるのではないか")
print()

# 季節のラベル
season_labels = {1: "Spring", 2: "Summer", 3: "Fall", 4: "Winter"}

# pivot_tableで季節別・時間別の平均を計算
season_hourly = df_cycle.pivot_table(values="cnt", index="hr", 
                                      columns="season", aggfunc="mean")

# 結果を表示
print("季節別・時間別の平均利用数:")
print(season_hourly.round(1))
print()

# 折れ線グラフの作成
fig, ax = plt.subplots(figsize=(12, 6))
colors_season = ["lightgreen", "tomato", "orange", "skyblue"]

for i in range(4):
    season = i + 1
    if season in season_hourly.columns:
        ax.plot(season_hourly.index, season_hourly[season], 
                marker="o", markersize=4,
                label=season_labels[season], color=colors_season[i])

ax.set_xlabel("Hour")
ax.set_ylabel("Average Count")
ax.set_title("Hourly Rental Pattern by Season")
ax.set_xticks(range(0, 24))
ax.legend()
ax.grid(alpha=0.3)
fig.savefig("season_hourly.png")
plt.show()

print("【考察4】")
print("すべての季節で通勤時間帯（8時、17-18時）にピークがある点は共通している。")
print("夏と秋は利用数が多く、冬と春は相対的に少ない。")
print("特に夏と秋は日中の利用も活発で、レジャー目的の利用が")
print("増加していると考えられる。冬は気温が低いため利用が減少している。")
print()


# 分析2: 気温と利用数の関係（相関分析）
# 仮説: 気温が高いほど利用数が増えるのではないか

print()
print("【分析5: 気温と利用数の関係】")

print("仮説: 気温が高いほど利用数が増えるのではないか")
print()

# 相関係数を計算
corr_temp = df_cycle["temp"].corr(df_cycle["cnt"])
corr_atemp = df_cycle["atemp"].corr(df_cycle["cnt"])

print("気温(temp)と利用数の相関係数:", round(corr_temp, 4))
print("体感気温(atemp)と利用数の相関係数:", round(corr_atemp, 4))
print()

# 散布図の作成（subplotsで複数グラフ）
fig, ax = plt.subplots(1, 2, figsize=(10, 5))

ax[0].scatter(df_cycle["temp"], df_cycle["cnt"], alpha=0.1, s=5, c="steelblue")
ax[0].set_xlabel("Temperature (Normalized)")
ax[0].set_ylabel("Count")
ax[0].set_title("Temperature vs Count (r=" + str(round(corr_temp, 3)) + ")")
ax[0].grid(alpha=0.3)

ax[1].scatter(df_cycle["atemp"], df_cycle["cnt"], alpha=0.1, s=5, c="coral")
ax[1].set_xlabel("Feeling Temperature (Normalized)")
ax[1].set_ylabel("Count")
ax[1].set_title("Feeling Temperature vs Count (r=" + str(round(corr_atemp, 3)) + ")")
ax[1].grid(alpha=0.3)

fig.tight_layout()
fig.savefig("temp_correlation.png")
plt.show()

print("【考察5】")
print("仮説は正しかった。気温と利用数には正の相関がある（r ≈ 0.4）。")
print("気温が高いほど利用数が増加する傾向がある。")
print("ただし相関係数は中程度であり、気温だけでなく")
print("時間帯や天気など他の要因も利用数に影響していると考えられる。")
print()





# まとめ


print("まとめ")


print("季節変動との関連性。夏・秋に利用が多く、冬は減少")
print("気温との相関について、正の相関があり、暖かい日ほど利用が増える")
print()
