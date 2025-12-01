# 第6回 Matplotlib によるグラフ作成

2025年11月1日 ver1.0.2

---

## 目次

- 可視化の準備
- Matplotlib を利用した可視化
- 基本的なグラフの作成
  - ヒストグラム
  - 棒グラフ
  - 折れ線グラフ
  - 散布図
  - 円グラフ
- オプションの指定
- グラフの保存
- （参考）グラフの作成 応用編
- （参考）Matplotlib の2つの流儀

---

## 可視化の準備

### データの可視化

ライブラリ（Matplotlib、seaborn）や pandas の plot()メソッドでグラフを描画することができる。

#### Matplotlib

Pythonを利用しグラフを描画するためのライブラリ

- 公式サイト：https://matplotlib.org/
- Matplotlibの色マップ：https://matplotlib.org/examples/color/colormaps_reference.html
- Matplotlibの色の名前：https://matplotlib.org/examples/color/named_colors.html

#### seaborn

Matplotlib をベースとした Python のデータ可視化ライブラリ

- 公式サイト：https://seaborn.pydata.org/

#### pandas の plot()メソッド

pandas の Series もしくは DataFrame を可視化する機能（デフォルトでは、Matplotlibが使用される）

- 公式サイト：https://pandas.pydata.org/pandasdocs/stable/reference/api/pandas.DataFrame.plot.html

---

### ライブラリの読み込み

Matplotlib の pyplot()モジュールを利用してグラフに描画することができる。

```python
import matplotlib.pyplot as plt  # ①
%matplotlib inline                # ②
```

1. Matplotlib の pyplot()モジュールを読み込む
   - pyplot()モジュールは、簡単なグラフを描画するためのインターフェースが集まっている
   - Matplotlib の pyplot()モジュールは、エイリアスを `plt` でインポートすることが慣例となっている
2. Jupyter Notebook 上にグラフを表示するためのコマンド

---

## Matplotlib を利用した可視化

### Matplotlib を利用したグラフ作成

Matplotlib を利用したグラフ作成には大きく４つのステップがある。

#### グラフ作成ステップ

1. 描画するデータを準備する
2. グラフを構成する（Matplotlibのオブジェクトの作成）
3. データの描画の方法を設定する
4. タイトルや軸のラベルなどオプションを加える

#### 使用例

```python
x = np.array(['A','B','C'])      # ①描画するデータの準備
y = np.array([10, 80, 50])

fig, ax = plt.subplots()         # ②オブジェクトの作成
ax.bar(x, y)                     # ③描画の方法設定

ax.set_title('Test Score')       # ④オプション追加
ax.set_xlabel('name')
ax.set_ylabel('score');
```

---

### Matplotlib の構成

Matplotlib は Figureオブジェクトと Axesオブジェクトで構成される。

#### 階層構造

Figure オブジェクト ＞ Axes オブジェクト ＞ Axis

- **Figureオブジェクト**：図全体（初期サイズ：432 x 288 ピクセル = 6.4 x 4.8 インチ）
- **Axesオブジェクト**：座標軸（Axis）を含む

---

### オブジェクトの作成

Matplotlib の関数を利用してオブジェクトを作成する。

#### 使用例

```python
fig = plt.figure()      # ① Figureオブジェクト (fig) を作成する
ax = fig.subplots()     # ② subplots()関数を利用してAxesオブジェクト (ax) を作成する
```

> 引数を指定しない場合、デフォルトで一つのグラフを作成する

#### subplots()関数を利用すると、図 (fig) とサブプロット (ax) のセットを作成できる

```python
fig, ax = plt.subplots()
```

---

### グラフの作成

Matplotlib の関数・メソッドを利用して多様なグラフを作成することができる。

| グラフ名 | 関数・メソッド | 使用例 |
|---------|-------------|--------|
| ヒストグラム | `hist` | `fig, ax = plt.subplots()`<br>`ax.hist(x)` |
| 棒グラフ | `bar` | `fig, ax = plt.subplots()`<br>`ax.bar(x, y)` |
| 折れ線グラフ | `plot` | `fig, ax = plt.subplots()`<br>`ax.plot(x)` |
| 散布図 | `scatter` | `fig, ax = plt.subplots()`<br>`ax.scatter(x, y)` |
| 円グラフ | `pie` | `fig, ax = plt.subplots()`<br>`ax.pie(x)` |

---

## 基本的なグラフの作成

### ヒストグラム

#### ヒストグラム (1/3)

`hist()`関数・メソッドを利用してヒストグラムを作成できる。

```python
x = np.random.rand(1000)  # 0以上1未満の連続一様分布に基づく乱数を1000個生成する
fig, ax = plt.subplots()
ax.hist(x)
```

実行結果：それぞれの階級区間 (bin) に含まれるサンプルサイズと階級区間の境界の値が表示される。

---

#### ヒストグラム (2/3)

引数の `bins` で階級区間の数を指定することができる。

```python
x = np.random.rand(1000)
fig, ax = plt.subplots()
ax.hist(x);              # ①デフォルト

fig, ax = plt.subplots()
ax.hist(x, bins=20);     # ②階級区間を20に指定
```

> セミコロンをつけるとグラフだけを表示することができる

---

#### ヒストグラム (3/3)

引数の `range` でデータの範囲を指定することができる。

```python
x = np.random.rand(1000); x[0] = 100  # 極端に大きな値を代入
fig, ax = plt.subplots()
ax.hist(x);                            # ①範囲指定なし

fig, ax = plt.subplots()
ax.hist(x, range=(0, 1));              # ②範囲を0〜1に指定
```

---

### 棒グラフ

#### 棒グラフ (1/3)

`bar()`関数・メソッドを利用して棒グラフを作成できる。

```python
x = np.array(['A', 'B', 'C']); y = np.array([10, 80, 50])
fig, ax = plt.subplots()
ax.bar(x, y);      # ①縦棒グラフ

fig, ax = plt.subplots()
ax.barh(x, y);     # ②横棒グラフ（barhで横棒グラフを作成できる）
```

---

#### 棒グラフ (2/3)

引数の `width` で棒の太さを指定できる。

```python
x = np.array(['A', 'B', 'C']); y = np.array([10, 80, 50])
fig, ax = plt.subplots()
ax.bar(x, y);              # ①デフォルト

fig, ax = plt.subplots()
ax.bar(x, y, width=0.4);   # ②幅を0.4に指定
```

---

#### 棒グラフ (3/3)

昇順または降順に並び替える場合、配列を変更する。

```python
x = np.array(['A', 'B', 'C']); y = np.array([10, 80, 50])
y2 = np.sort(y)[::-1]
x_index = np.argsort(y)[::-1]
x2 = x[x_index]

fig, ax = plt.subplots()
ax.bar(x2, y2);
```

---

### 折れ線グラフ

#### 折れ線グラフ (1/2)

`plot()`関数・メソッドを利用して折れ線グラフを作成できる。

```python
x = np.random.randint(0, 10, 20)  # 0以上10未満の整数を20個生成する
fig, ax = plt.subplots()
ax.plot(x);
```

---

#### 折れ線グラフ (2/2)

引数の `marker` や `linestyle` でマーカーや線の種類を指定できる。

```python
x = np.random.randint(0, 10, 20)
fig, ax = plt.subplots()
ax.plot(x, marker='o');        # ①マーカーを丸に指定

fig, ax = plt.subplots()
ax.plot(x, linestyle=':');     # ②線を点線に指定
```

---

### 散布図

#### 散布図 (1/2)

`scatter()`関数・メソッドを利用して散布図を作成できる。

```python
x = np.random.normal(10, 5, 100)   # 平均10、標準偏差5の正規分布から乱数を100個生成する
y = np.random.normal(10, 10, 100)  # 平均10、標準偏差10の正規分布から乱数を100個生成する
fig, ax = plt.subplots()
ax.scatter(x, y);
```

---

#### 散布図 (2/2)

引数の `marker` や `s` でマーカーや大きさを指定できる。

```python
x = np.random.normal(10, 5, 100); y = np.random.normal(10, 10, 100)
fig, ax = plt.subplots()
ax.scatter(x, y, marker='x');   # ①マーカーをxに指定

fig, ax = plt.subplots()
ax.scatter(x, y, s=50);         # ②サイズを50に指定
```

---

### 円グラフ

#### 円グラフ (1/2)

`pie()`関数・メソッドを利用して円グラフを作成できる。

```python
x = np.array([100, 50])
y = np.array(['A', 'B'])
fig, ax = plt.subplots()
ax.pie(x, labels=y);
```

---

#### 円グラフ (2/2)

引数の `startangle` や `counterclock` で開始位置や順序を指定できる。

```python
x = np.array([100, 50]); y = np.array(['A', 'B'])
fig, ax = plt.subplots()
ax.pie(x, labels=y, startangle=90);                        # ①開始位置を90度に指定

fig, ax = plt.subplots()
ax.pie(x, labels=y, startangle=90, counterclock=False);    # ②時計回りに指定
```

---

### 練習問題

#### コンビニエンスストア商品別販売額

以下の表をグラフにして、グラフから読み取れることを考えてください。

| 年月 | 合計 |
|------|------|
| 202001 | 971,358 |
| 202002 | 930,834 |
| 202003 | 957,674 |
| 202004 | 891,438 |
| 202005 | 927,068 |
| 202006 | 959,603 |
| 202007 | 990,818 |
| 202008 | 1,034,075 |
| 202009 | 988,740 |
| 202010 | 997,305 |
| 202011 | 970,016 |
| 202012 | 1,023,359 |

出典：e-stat 商業動態統計調査 / 時系列データ

---

## オプションの指定

### グラフタイトル・軸ラベルの設定

`set_○○`でグラフタイトルや軸ラベルを指定することができる。

#### 使い方

```python
Axesオブジェクト.set_title(文字列型のタイトル)
Axesオブジェクト.set_xlabel(文字列型のx軸のラベル)
Axesオブジェクト.set_ylabel(文字列型のy軸のラベル)
```

#### set()関数・メソッドでまとめて指定することもできる

```python
Axesオブジェクト.set(title=タイトル, xlabel=x軸のラベル, ylabel=y軸のラベル)
```

#### 使用例

```python
x = np.array(['A','B','C'])
y = np.array([10, 80, 50])

fig, ax = plt.subplots()
ax.bar(x, y)

ax.set_title('Test Score')
ax.set_xlabel('name')
ax.set_ylabel('score');
```

---

### グラフの凡例の設定

`legend()`関数・メソッドを利用して凡例を表示できる。

#### 使い方

```python
Axesオブジェクト.legend()
```

> 引数 `loc` で表示する場所を指定できる（デフォルトは best）

#### 使用例

```python
x = np.random.randint(0, 10, 20)
fig, ax = plt.subplots()
ax.plot(x, label='random')
ax.legend();
```

---

### 日本語の表示

デフォルトの設定では、日本語を表示することはできない。

日本語を表示する方法は複数存在するが、ここでは japanize-matplotlib を使う方法を紹介する。

```python
!pip install japanize-matplotlib   # ライブラリをインストール
import japanize_matplotlib          # import する際はアンダースコアになることに注意
```

#### 使用例

```python
x = np.array(['A', 'B', 'C']); y = np.array([10, 80, 50])
fig, ax = plt.subplots()
ax.bar(x, y)
ax.set_title('テスト得点');
```

---

## グラフの保存

`savefig()`関数・メソッドを利用してグラフを保存することができる。

#### 使い方

```python
グラフオブジェクト.savefig(保存先/ファイル名)
```

#### 使用例

```python
x = np.array(['A', 'B', 'C']); y = np.array([10, 80, 50])
fig, ax = plt.subplots()
ax.bar(x, y)
fig.savefig('./bar.png');
```

---

### 章末問題

□に入れたときに、エラーになる番号を選択せよ

```python
a = np.random.normal(10, 5, 100)
b = np.random.normal(10, 10, 100)
fig, ax = plt.subplots()
□
```

#### 選択肢

1. `ax.plot(x, y);`
2. `ax.scatter(x, y);`
3. `ax.hist(x, y);`
4. `ax.bar(x, y);`

---

## （参考）グラフの作成 応用編

### 複数のグラフの作成 (1/4)

for文を使うと、同じようなグラフを複数作成できる。

```python
x = np.random.randint(0, 10, (3, 20))  # 0以上10未満の整数を3行20列生成する
for i in range(3):
    fig, ax = plt.subplots()
    ax.plot(x[i])
    ax.set_title(f'row {i}')
```

---

### 複数のグラフの作成 (2/4)

`add_subplot()`関数を使って複数のAxesオブジェクトを作成できる。

```python
fig = plt.figure()                # ① 初期サイズでFigureオブジェクト (fig) を作成する
ax1 = fig.add_subplot(1, 2, 1)    # ② add_subplot()関数を利用してAxesオブジェクト (ax) を作成する
ax2 = fig.add_subplot(1, 2, 2)
```

> 引数：1番目の桁は行数、2番目の桁は列数、3番目の桁はインデックスを指定する
> 引数はコンマ (,) を入力せず `fig.add_subplot(121)` のように書き換えることができる

---

### 複数のグラフの作成 (3/4)

```python
x = np.random.normal(10, 5, 1000)
y = np.random.normal(10, 20, 1000)
fig = plt.figure()
ax1 = fig.add_subplot(1, 2, 1)
ax2 = fig.add_subplot(1, 2, 2)
ax1.hist(x)
ax2.hist(y);
```

---

### 複数のグラフの作成 (4/4)

`subplots()`関数の引数で指定しても、複数のAxesオブジェクトを作成できる。

インデックスで描画するオブジェクトを指定する。

```python
x = np.random.normal(10, 5, 1000)
y = np.random.normal(10, 20, 1000)
fig, ax = plt.subplots(2, 2)
ax[0, 0].hist(x)   # ax[0, 0], ax[0, 1]
ax[1, 1].hist(y);  # ax[1, 0], ax[1, 1]
```

---

### 複数の要素を持つグラフの作成 (1/2)

1つのAxesオブジェクトに複数のグラフを書くこともできる。

```python
x = np.random.normal(10, 5, 1000)
y = np.random.normal(10, 20, 1000)
fig, ax = plt.subplots()
ax.hist(x, color='red', alpha=0.5)
ax.hist(y, color='green', alpha=0.5);
```

---

### 複数の要素を持つグラフの作成 (2/2)

```python
x = np.array(['a', 'b', 'c', 'd']); y = np.array([100, 80, 50, 10])
z = np.cumsum(y) / np.sum(y)
fig, ax1 = plt.subplots()
ax2 = ax1.twinx()
ax1.bar(x, y)
ax2.plot(z, color='red', marker='o')
ax2.set_ylim((0.0, 1.1));
```

---

### 積み上げ棒グラフ

引数の `bottom` で棒グラフの開始位置を指定できる。

```python
x = np.array(['A', 'B', 'C']); y = np.array([10, 80, 50])
z = np.array([30, 50, 30])
fig, ax = plt.subplots()
ax.bar(x, y, label='math')
ax.bar(x, z, bottom=y, label='English')
ax.legend();
```

---

### 複数の棒を持つ棒グラフ

`xticks` の使い方を工夫することで、複数の棒を持つ棒グラフを作成できる。

```python
x = np.array(['A', 'B', 'C']); y = np.array([10, 80, 50]); z = np.array([30, 50, 30])
ticks = np.arange(3); bar_width = 0.4
fig, ax = plt.subplots()
ax.bar(ticks - bar_width/2, y, width=bar_width, label='math')      # 'math'棒の位置 (-0.2)
ax.bar(ticks + bar_width/2, z, width=bar_width, label='English')   # 'English'棒の位置 (+0.2)
ax.set_xticks(ticks)
ax.set_xticklabels(x)   # ticksの値にxでラベリング
ax.legend();
```

---

## （参考）Matplotlib の2つの流儀

### グラフ描画の2つの流儀

Matplotlib にはグラフは「オブジェクト指向インターフェース」と「Pyplot インターフェース」の2つの書き方がある。

2つの方法があることを認識して、これらを混ぜて使用しないようにする。

#### オブジェクト指向インターフェース

`fig, ax = plt.subplots()` を実行後に fig や ax に対して操作を行っていく方法（これまでの授業の中で紹介してきた書き方）

```python
fig, ax = plt.subplots()
ax.plot(x);
```

#### Pyplot インターフェース

`plt.foo` で全てを済ます方法（MATLAB に近い書き方）

```python
plt.plot(x)
```

---

### 2つの流儀の比較

コードの長さとして大きな違いはない。

#### オブジェクト指向インターフェース

```python
x = np.linspace(0, 2*np.pi, 500)
fig = plt.figure()
ax1 = fig.add_subplot(211)
ax1.plot(x, np.sin(x), color='blue')
ax2 = fig.add_subplot(212)
ax2.plot(x, np.cos(x), color='orange')
fig.show()
```

#### Pyplot インターフェース

```python
x = np.linspace(0, 2*np.pi, 500)
plt.figure(1)
plt.subplot(211)
plt.plot(x, np.sin(x), color='blue')
plt.subplot(212)
plt.plot(x, np.cos(x), color='orange')
plt.show()
```

---

### 2つの流儀が混ざっている例

2つの流儀が混ざっても実行できるが、読みにくいコードになってしまう。

自分がどちらの流儀を使っているかを意識して、混在しないようにする。

```python
x = np.linspace(0, 2*np.pi, 500)
fig = plt.figure()
ax1 = fig.add_subplot(211)
plt.plot(x, np.sin(x), color='blue')   # 混在している
ax2 = fig.add_subplot(212)
plt.plot(x, np.cos(x), color='orange') # 混在している
fig.show()
```

---

**Thank you!**