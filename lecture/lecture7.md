# 第7回 pandas によるデータ分析の基礎

ver1.0.1  
最終更新日: 2025年11月10日

---

## 目次

- pandas とは
- Series と DataFrame
- データの読み込みと保存
- データの操作
  - データの確認
  - データの参照・代入
  - データの加工
- 基本統計量の算出
- グルーピング
- データの結合
- 前半レポート
- （参考）pandas による可視化

---

## pandas とは

### pandas の概要

pandas は、Pythonにおけるデータ分析・機械学習を支援する機能を提供するライブラリである。複雑なソースコードを書かなくても、高度なデータ分析ができる。

- **名前の由来**: 「panel data」
- **主な機能**: 数表や時系列データ処理を容易にするデータ構造、あるいは演算を提供する

### pandas でできること

#### 数表 (テーブル) データのシンプルかつ効率的な取り扱い

- DataFrame型/Series型による数表データの取り扱い
- 数表データのサブセット化 (特定条件に当てはまるデータの取り出し)
- 数表データ同士の連結や、一般的なSQLベースのデータベースで使用可能なその他の関数演算
- 数表データの統計量の確認・欠損値処理
- 時系列データの効率的な取り扱い

#### 様々な形式でのデータの読み込みや書き出し

- csv、json、htmlといった様々な形式のデータの読み込み・出力

### ライブラリの読み込み

pandas をインポートするには、以下のコードを実行する:

```python
import pandas as pd
import numpy as np
```

> **注意**: pandasはエイリアスを `pd` でインポートすることが慣例となっている。NumPy など、他のライブラリとともに使われることが多い。

> **非推奨**: `from pandas import *` のように入力して実行することもできるが、同じ名前の変数・関数を上書きしてしまうリスクがあるため非推奨

---

## Series と DataFrame

### Series型とは

- 一次元データの格納に使用
- NumPyの一次元配列に似ているが、インデックスに名前をつけることができる

### DataFrame型とは

- 二次元データの格納に使用
- NumPyの二次元配列に似ているが、インデックス、カラムに名前をつけることができる
- 一次元データの格納も可能でSeries型を兼ねることもできる

### DataFrame型で扱われるデータ例 (メンバーごとのテスト結果)

| index | 氏名 | 性別 | 数学 | 英語 |
|-------|-----|------|-----|-----|
| 0 | A | 女性 | 80 | 100 |
| 1 | B | 男性 | 65 | 56 |
| 2 | C | 女性 | 52 | 54 |

- **axis=0**: 列方向を意味
- **axis=1**: 行方向を意味
- **インデックスラベル**: 行名
- **カラムラベル**: 列名

### Series型、DataFrame型のメリット

- 数表データにインデックスラベル (行名)、カラムラベル (列名) を付与することができる
- データの取り扱いがシンプルにでき、下記のようなエラーも未然に防ぐことができる
  - 誤って整形されたデータに起因するエラー
  - 別々のデータソースから別々にラベル付けされたデータを用いることで発生するエラー

### Series の作成

Series は一次元データの格納に使用される。

**構文:**
```python
pd.Series(データやデータの型, インデックスラベルなどを引数で設定)
```

**使用例:**
```python
idx = ['クラス', '性別', '国語', '数学', '英語', '物理', '化学']
person_A = ['1組', '男性', 55, 80, 100, 33, 54]

s_score = pd.Series(data=person_A, index=idx)
s_score
```

**実行結果:**
```
クラス     1組
性別      男性
国語       55
数学       80
英語      100
物理       33
化学       54
dtype: object
```

> `dtype` はデータ型を表示している

### DataFrame の作成

DataFrame は二次元データの格納に使用される。

**構文:**
```python
pd.DataFrame(データやデータの型, ラベル名などを引数で設定)
```

**使用例:**
```python
idx = ['氏名', 'クラス', '性別', '国語', '数学', '英語', '物理', '化学']
person_A = ['A', '1組', '男性', 55, 80, 100, 33, 54] 
person_B = ['B', '1組', '男性', 95, 84, 40, np.nan, 74]
person_C = ['C', '1組', '女性', 91, 84, 43, 95, 94]
person_D = ['D', '2組', '女性', 73, 94, 60, 75, np.nan]
person_E = ['E', '2組', '女性', 83, 44, 47, 95, 84]

df_score = pd.DataFrame(data=[person_A, person_B, person_C, person_D, person_E], columns=idx)
```

**ポイント:**
- `data=` で要素の設定、`columns=` でカラムラベルの設定
- `np.nan` はデータが欠けていることを表す
- カラムラベル、インデックスラベルは指定しなければ0から始まる連番になる

---

## データの読み込みと保存

作成したデータの保存や、外部データの読み込みができる。

### データの保存

```python
データフレーム.to_csv(ファイルパス/ファイル名)
```

### データの読み込み

```python
pd.read_csv(ファイルパス/ファイル名)
```

### 使用例

```python
# 保存
df_score.to_csv('test_result.csv', index=False)

# 読み込み
df_score = pd.read_csv('test_result.csv')
```

**ポイント:**
- メソッドの第一引数にファイルパスを入力する
- ファイル名のみの場合はソースコードファイルと同レベルに保存される
- `index=False` と指定すると、インデックスを含めずに保存される
- csv 以外にも json、html、SQL など様々な形式に対応している

### 練習問題

tips.csv を読み込んで、tips という変数に格納せよ

---

## データの操作

### データの確認 (1/3)

#### データフレームの確認

```python
display(df_score)
```

- データフレームの確認は `display(データフレーム)` で行う
- Jupyter Notebook 使用時で、最後の行になる場合は `display()` は省略可能

#### データ型の確認

```python
df_score.dtypes
```

- データ型は指定しなくても自動付与され、カラム単位で共通となる
- データ型 (dtype) の確認は `データフレーム.dtypes` で行い、カラムごとのデータ型が返される

**主なデータ型:**
- `object`: 文字列型
- `int64`: 整数型
- `float64`: 浮動小数点型（※欠損値が含まれているため整数型にならないことがある）

### データの確認 (2/3)

大規模なデータを確認するときに便利な方法。

#### 先頭から範囲を指定

```python
df_score.head(3)
```

#### 最後から範囲を指定

```python
df_score.tail(2)
```

- `head()` メソッドも `tail()` メソッドもデフォルトは5行の取得となる

### データの確認 (3/3)

インデックス、カラム、要素を別々に確認することもできる。

```python
df_score.index      # インデックスの確認
df_score.columns    # カラムの確認
df_score.values     # 要素の確認
```

**実行結果:**
```python
# index
RangeIndex(start=0, stop=5, step=1)

# columns
Index(['氏名', 'クラス', '性別', '国語', '数学', '英語', '物理', '化学'], dtype='object')

# values
array([['A', '1組', '男性', 55, 80, 100, 33.0, 54.0],
       ['B', '1組', '男性', 95, 84, 40, nan, 74.0],
       ...], dtype=object)
```

**ポイント:**
- カラムの要素が異なる dtype を持つ場合、より汎用性の高い dtype が使われる（アップキャスト）
- インデックスラベルは RangeIndex オブジェクト、カラムラベルは Index オブジェクト、要素は ndarray 形式で格納されている

---

### データの参照・代入

#### 添字で指定する方法

```python
データフレーム[インデックス選択][カラム選択]
```

- インデックスのみ、あるいはカラムのみの指定も可能
- インデックスの選択にはスライスのみ使用でき、ラベル、番号どちらも使用可
- カラムの選択にはカラムラベル（番号は使用不可）をリストで記載する（スライスは使用できない）
- 1カラムのみ選択する場合、リストで記載する必要はないがSeriesが戻り値となる

**使用例:**
```python
df_score['国語']                    # カラムの取得（Seriesが返される）
df_score[['国語', '英語']]          # 複数カラムの取得（DataFrameが返される）
df_score[1:3]                       # インデックスの取得（スライス）
df_score[0:2][['国語', '化学']]     # インデックスとカラム両方を指定
```

#### 番号で指定する方法

**iat**: 要素一つを取り出す
```python
データフレーム.iat[インデックス番号, カラム番号]
```

**iloc**: 複数の要素を取り出す（スライスも利用可能）
```python
データフレーム.iloc[[インデックス番号1, インデックス番号2], [カラム番号1, カラム番号2]]
データフレーム.iloc[インデックス番号1:インデックス番号3, カラム番号1:カラム番号3]
```

**使用例:**
```python
df_score.iat[2, 3]      # 91
df_score.iloc[:2, 3:]   # 複数要素の取得
```

#### ラベルで指定する方法

**at**: 要素一つを取り出す
```python
データフレーム.at[インデックスラベル, カラムラベル]
```

**loc**: 複数の要素を取り出す（スライスも利用可能）
```python
データフレーム.loc[[インデックスラベル1, インデックスラベル2], [カラムラベル1, カラムラベル2]]
データフレーム.loc[インデックスラベル1:インデックスラベル3, カラムラベル1:カラムラベル3]
```

**使用例:**
```python
df_score.at[3, '国語']              # 73
df_score.loc[[0, 2], '性別':'物理']  # 複数要素の取得
```

#### 条件式

DataFrame や Series に対して、条件式を書くことができる。

**使用例:**
```python
df_score['国語'] >= 70                                          # 国語70点以上
(df_score['国語'] >= 70) & (df_score['英語'] >= 45)             # 国語70点以上かつ英語45点以上
df_score.iloc[:, 3:7] > 60                                      # テスト結果が60点より大きい
```

#### 条件を指定してデータを取得

```python
df_score[df_score['国語'] >= 70]                                                    # 国語70点以上のインデックス
df_score[(df_score['国語'] >= 70) & (df_score['英語'] >= 45)][['国語', '英語']]      # 国語70点以上かつ英語45点以上
df_score[['数学', '物理']][(df_score['数学'] >= 90) | (df_score['物理'] >= 90)]      # 数学90点以上または物理90点以上
```

#### 新しいインデックス・カラムの挿入

```python
# カラムを追加する場合
データフレーム[新しく追加するカラム] = 値

# インデックスを追加する場合
データフレーム.loc[新しく追加するインデックス] = 値
```

**使用例:**
```python
df_score['日本史'] = [67, 77, 54, 55, 88]
df_score.loc[5] = ['F', '3組', '男性', 22, 34, 64, 11, 34, 55]
```

#### データの上書き

```python
データの指定 = 新しい値
```

**使用例:**
```python
df_score.at[0, '国語'] = 88
```

### 練習問題

tips のうち、日曜の Dinner のデータを tips2 という変数に格納せよ。また、tips2 の行数と列数を求めよ。

---

### データの加工

#### 軸（インデックス・カラム）に対するソート

`sort_index()` メソッドを使用し、インデックスやカラムに対してソートを行うことができる。

**使用例:**
```python
df_score.sort_index(ascending=False)    # インデックスの降順並び替え
df_score.sort_index(axis=1)              # カラムの並び替え
```

- `ascending=False` で降順を指定
- `axis=1` とするとカラムの並び替え（`axis=0` はインデックス、デフォルト）
- 文字列は文字コードにしたがってソートされる

#### 要素に対するソート

`sort_values()` メソッドを使用し、要素に対するソートを行うことができる。

**使用例:**
```python
df_score.sort_values(by='英語', ascending=False)
```

- `by='英語'` で英語カラムを指定
- `ascending=False` にすると降順で並び替える

#### 転置（インデックスとカラムの入れ替え）

NumPy と同様に、T属性を使用する。

```python
df_score.T
```

データが見やすくなったり、データを新しい角度で見たりすることができる。

#### 欠損値の確認

```python
データフレーム.isnull()
```

**使用例:**
```python
df_score.isnull().any(axis=1)    # 欠損値が含まれるindexがTrueになる
```

**ポイント:**
- `all()` メソッド: インデックス、カラムごとのすべての要素が欠損値か調べる
- `any()` メソッド: インデックス、カラムごとに一つの要素でも欠損値が含まれるか調べる
- `isnull()` の代わりに `isna()` を用いても良い
- `pd.isnull(データフレーム)` のように関数形式で書くこともできる
- `notnull()` メソッド: 欠損値が含まれていない要素に True が返される

#### 欠損値処理の方法

**削除する場合:**
```python
データフレーム.dropna(引数)
```

- `axis=1` とするとカラム、`axis=0` とするとインデックスの削除
- `how='any'` とすると一つでも欠損値が含まれる場合、`how='all'` とすると全要素が欠損値の場合に削除
- `inplace=True` とすると元のデータフレームが変更される

**使用例:**
```python
df_score.dropna(how='any', axis=1)
```

**補完する場合:**
```python
データフレーム.fillna(引数)
```

**使用例:**
```python
df_score.fillna(0)                                          # 欠損値を0として補完
df_score.fillna({'物理': 70, '化学': 60}, inplace=True)     # カラムごとに補完する値を変える
```

#### 文字列操作

ラベルや要素に対して文字列操作を行うメソッドも用意されている。

**使用例:**
```python
df_score['氏名'].str.lower()              # 小文字変換
df_score['氏名'].str.replace('A', 'a')    # 文字の置換
```

**その他のメソッド:**
- `str.upper()`: 大文字に変換
- `str.strip()`: 文字列から空白を削除

---

## 基本統計量の算出

### describe()メソッド

`describe()` メソッドを使用すると、基本統計量の一覧を確認できる。

```python
df_score.describe()
```

**出力される統計量:**
- `count`: サンプルサイズ
- `mean`: 平均値
- `std`: 標準偏差
- `min`: 最小値
- `25%`: 1/4分位数
- `50%`: 中央値
- `75%`: 3/4分位数
- `max`: 最大値

### 個別の統計量メソッド

`describe()` メソッドで取得するよりも早く計算結果が得られる。

```python
df_score.count()                          # サンプルサイズ
df_score.mean(numeric_only=True)          # 平均値
df_score.std(numeric_only=True)           # 標準偏差
df_score.min(numeric_only=True)           # 最小値
df_score.quantile(numeric_only=True)      # 四分位数
df_score.max(numeric_only=True)           # 最大値
```

### 関数の適用

#### apply()メソッド

インデックス、カラムごとに関数を適用することができる。

```python
データフレーム.apply(関数)
```

**使用例:**
```python
df_score.iloc[:, 3:9].apply(lambda x: max(x) - min(x))           # 科目ごとの最高点と最低点の差
df_score.iloc[:, 3:9].apply(lambda x: max(x) - min(x), axis=1)   # 個人ごとの最高点と最低点の差
```

- デフォルトはカラムごとの適用
- `axis=1` とするとインデックスごとの適用

#### applymap()メソッド

各要素に対して関数を適用させることもできる。

```python
データフレーム.applymap(関数)
```

**使用例:**
```python
df_score.iloc[:, 3:9].applymap(lambda x: '不可' if x < 60 else '可')
```

---

## グルーピング

### グルーピングとは

データをグループ分けすること。グループごとの傾向を見たいときなどに使用する。

`groupby()` メソッドを使用し、以下の3ステップで行われる:
1. データを条件によってグループ分けする
2. 分割したグループごとにメソッドや関数 (max、meanなど) を適用する
3. 結果を結合してデータフレームにする

### 書き方

```python
データフレーム.groupby(ラベル)
```

- グループ分けの軸となる基準をラベルで指定する
- ラベルは複数選択可能であり、その場合はリストでラベルを記載する
- 複数選択した場合、マルチインデックスで出力される

### 使用例

```python
df_score.groupby('性別').mean()                    # 性別でグループ分け
df_score.groupby(['クラス', '性別']).mean()        # クラスと性別でグループ分け
```

### agg()メソッド

`agg()` メソッドを使用してグループごとに集計を行うことができる。ラベルに応じて関数を適用でき、また複数の集計結果を得ることができる。

**使用例:**
```python
# グループごとの国語の平均点と最低点を計算
df_score.groupby(['クラス', '性別']).agg({'国語': [np.mean, np.min]})

# グループごとの国語の最低点と数学の最高点と最低点の差を計算
df_score.groupby(['クラス', '性別']).agg({'国語': min, '数学': lambda x: max(x) - min(x)})
```

---

## データの結合

### 結合の方法

結合には連結と結合の2パターンがある。

#### 連結

テーブルを縦方向、あるいは横方向にそのままつなげる。

- `concat()` 関数
- `append()` メソッド

#### 結合

テーブルを共通のラベル（キー）の紐づけによってつなげる。

- `merge()` 関数
- `join()` メソッド

### データの連結

#### concat()関数

```python
pd.concat([df_score, df_gh])
```

- 同時に複数連結させることも可能
- デフォルトは外部結合、縦方向の連結
- 一致しないカラムは欠損値となる
- 引数 `join='inner'` で内部結合を指定
- 引数 `ignore_index=True` とすると、連結後indexを振りなおす

**使用例:**
```python
pd.concat([df_score, df_gh], join='inner', ignore_index=True)
```

### データの結合

#### merge()関数

```python
pd.merge(df_score, df_bio)
```

- キーを軸とした結合が行われる
- デフォルトでは共通のラベルをもつカラムがキーとなり、そのカラム要素に対する内部結合となる

#### キーの指定

```python
pd.merge(df_score, df_bio, on=['氏名', 'クラス'])
```

- キーを複数指定することもできる
- キーになっていない共通のカラムラベルはサフィックス（接尾辞）がつけられる

#### 結合方法の指定

```python
pd.merge(df_score, df_bio, how='outer')     # 外部結合
pd.merge(df_score, df_bio, how='left')      # 左結合
pd.merge(df_score, df_bio, how='right')     # 右結合
pd.merge(df_score, df_bio, how='inner')     # 内部結合（デフォルト）
```

### 章末問題

以下のうち、出力が Series型になるコードの番号を選択せよ:

1. `tips.groupby('day').sum()`
2. `tips.groupby('day').sum()['bill']`
3. `tips.groupby('day').sum()[['bill']]`
4. `tips.groupby('day').sum()['bill'].reset_index()`

---

## （参考）pandas による可視化

### グラフの作成

pandas の `plot()` メソッドを利用して多様なグラフを作成することができる。

| グラフ名 | メソッド | 使用例 |
|---------|---------|--------|
| ヒストグラム | `plot.hist()` / `plot(kind='hist')` | `df.plot.hist()` |
| 棒グラフ | `plot.bar()` / `plot(kind='bar')` | `df.plot.bar('x', 'y')` |
| 折れ線グラフ | `plot()` / `plot(kind='line')` | `df.plot()` |
| 散布図 | `plot.scatter()` / `plot(kind='scatter')` | `df.plot.scatter('x', 'y')` |
| 円グラフ | `plot.pie()` / `plot(kind='pie')` | `df.plot.pie('y')` |

### ヒストグラム・折れ線グラフ

```python
df_random = pd.DataFrame(np.random.normal(10, 5, 100), columns=['random'])
df_random.plot.hist()    # ヒストグラム
df_random.plot()         # 折れ線グラフ
```

### 棒グラフ

```python
tips3 = tips.groupby(['time']).sum()[['bill']].reset_index()
tips3.plot.bar(x='time', y='bill', rot=0)

tips4 = tips.groupby(['time', 'sex']).sum().reset_index().pivot('time', 'sex', 'bill')
tips4.plot.bar(stacked=True)    # 積み上げ棒グラフ
tips4.plot.bar()                # 棒グラフ
```

### 散布図・円グラフ

```python
tips.plot.scatter(x='bill', y='tip')    # 散布図
tips.groupby('sex').size().to_frame('count').plot.pie(y='count', startangle=90)    # 円グラフ
```

---



*Copyright © 2025 Accenture. All rights reserved.*