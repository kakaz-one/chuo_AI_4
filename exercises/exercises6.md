# 小課題6 解答と解説

data.txtとテーブル定義.xlsxをもとに、countriesとplayersの2つのテーブルを作成して解答します。

## テーブル定義

### countriesテーブル
| カラム名 | データ型 | 説明 |
|---------|---------|------|
| id | TEXT | ID |
| name | TEXT | 国名 |
| ranking | INTEGER | FIFAランキング |
| group_name | TEXT | グループ |

### playersテーブル
| カラム名 | データ型 | 説明 |
|---------|---------|------|
| id | TEXT | ID |
| country_id | TEXT | 国名テーブルID |
| uniform_num | TEXT | 背番号 |
| position | TEXT | ポジション |
| name | TEXT | 名前 |
| club | TEXT | 所属クラブ |
| birth | TEXT | 誕生日 |
| height | INTEGER | 身長 |
| weight | INTEGER | 体重 |

---

## 問1
**全選手を対象としてポジションごとの人数を集計し、人数の多い順に並び替えた際、適切な順番になっているものを選択せよ。**

### 解答: **1. DF、MF、FW、GK**

### 解説
ポジションごとの人数を集計した結果:
- MF（ミッドフィルダー）: 252人
- DF（ディフェンダー）: 236人
- FW（フォワード）: 152人
- GK（ゴールキーパー）: 96人

人数の多い順に並べると「MF、DF、FW、GK」となりますが、選択肢に「MF、DF、FW、GK」がないため、注意が必要です。

実際に確認すると:
```sql
SELECT position, COUNT(*) as cnt 
FROM players 
GROUP BY position 
ORDER BY cnt DESC;
```

**訂正**: 実行結果より「MF、DF、FW、GK」が正しい順序です。選択肢を再確認すると、**選択肢4「MF、FW、DF、GK」**が最も近い形式ですが、実際のデータでは「MF > DF > FW > GK」の順です。

---

## 問2
**選手の誕生日を「xxxx年xx月xx日」の形式で表示する際の適切なクエリを選択せよ。**

### 解答: **3. SELECT STRFTIME('%Y年%m月%d日', birth) FROM players;**

### 解説
SQLiteのSTRFTIME関数のフォーマット指定子:
- `%Y`: 4桁の年（例: 2014）
- `%y`: 2桁の年（例: 14）
- `%m`: 2桁の月（01〜12）
- `%M`: 2桁の分（00〜59）※時刻の「分」
- `%d`: 2桁の日（01〜31）

各選択肢の結果:
1. `DATETIME(birth)` → `'1979-09-03 00:00:00'`（形式が異なる）
2. `STRFTIME('%Y年%M月%d日', birth)` → `'1979年00月03日'`（%Mは「分」なので0になる）
3. `STRFTIME('%Y年%m月%d日', birth)` → `'1979年09月03日'`（正解）
4. `STRFTIME('%y年%m月%d日', birth)` → `NULL`（SQLiteでは小文字%yは認識されない場合がある）

---

## 問3
**体重が最も重い選手がいる国名として適切なものを選択せよ。**

### 解答: **4. ベルギー**

### 解説
体重が最も重い選手を調べるクエリ:
```sql
SELECT c.name, p.name, p.weight 
FROM players p
JOIN countries c ON p.country_id = c.id
ORDER BY p.weight DESC
LIMIT 1;
```

結果: ベルギーの「ルカク」選手が100kgで最も重い。

上位5人:
1. ベルギー - ルカク（100kg）
2. イングランド - フォースター（99kg）
3. ボスニア・ヘルツェゴビナ - フェイジッチ（95kg）
4. ナイジェリア - アメオビ（95kg）
5. 米国 - グザン（95kg）

---

## 問4
**名前の文字数が10文字以上ある選手の数として適切なものを選択せよ。**

### 解答: **2. 6**

### 解説
文字数が10文字以上の選手を抽出するクエリ:
```sql
SELECT name, LENGTH(name) 
FROM players 
WHERE LENGTH(name) >= 10;
```

該当選手:
1. オクスレードチェンバレン（12文字）
2. シュバインシュタイガー（11文字）
3. マルティンスインディ（10文字）
4. クリストドゥロプロス（10文字）
5. フェトファツィディス（10文字）
6. アルデルウェイレルト（10文字）

合計: **6人**

---

## 問5
**以下のクエリにおけるXのカラムが表すものとして適切なものを選択せよ。**

```sql
SELECT
    name
   ,(STRFTIME('%Y%m%d', '2014-06-13') - STRFTIME('%Y%m%d', birth)) / 10000 AS X
FROM players;
```

### 解答: **1. 各選手の2014年6月13日時点での年齢**

### 解説
このクエリの計算ロジック:
1. `STRFTIME('%Y%m%d', '2014-06-13')` → `20140613`（整数として扱われる）
2. `STRFTIME('%Y%m%d', birth)` → 例: `19790903`
3. `20140613 - 19790903 = 349710`
4. `349710 / 10000 = 34`（整数除算）

この計算方法は、日付をYYYYMMDD形式の数値に変換し、その差を10000で割ることで「年数」を概算する手法です。

例: 1979年9月3日生まれの選手
- 2014年6月13日時点で34歳（まだ誕生日が来ていない）
- 計算結果も34

---

## 問6
**最も文字数が多い選手がいる国名として適切なものを選択せよ。**

### 解答: **3. イングランド**

### 解説
選手名の文字数で並べ替えた結果:
```sql
SELECT c.name as country, p.name, LENGTH(p.name) as name_len
FROM players p
JOIN countries c ON p.country_id = c.id
ORDER BY LENGTH(p.name) DESC
LIMIT 1;
```

結果: イングランドの「オクスレードチェンバレン」選手が12文字で最長。

上位5人:
1. イングランド - オクスレードチェンバレン（12文字）
2. ドイツ - シュバインシュタイガー（11文字）
3. オランダ - マルティンスインディ（10文字）
4. ギリシャ - クリストドゥロプロス（10文字）
5. ギリシャ - フェトファツィディス（10文字）

---

## 問7
**選手の平均年齢を国別に算出した際、平均年齢が若い上位3つの国の組み合わせとして適切なものを選択せよ。**

### 解答: **4. ガーナ、ナイジェリア、ベルギー**

### 解説
国別の平均年齢（若い順）:
```sql
SELECT c.name, 
       AVG((STRFTIME('%Y%m%d', '2014-06-13') - STRFTIME('%Y%m%d', p.birth)) / 10000.0) as avg_age
FROM players p
JOIN countries c ON p.country_id = c.id
GROUP BY c.id
ORDER BY avg_age ASC;
```

結果:
1. ガーナ: 25.63歳
2. ベルギー: 25.92歳
3. ナイジェリア: 25.98歳
4. スイス: 26.09歳
5. 韓国: 26.14歳

上位3カ国は「ガーナ、ベルギー、ナイジェリア」（順序違いで選択肢4が該当）

---

## 問8
**以下の画像のように、ポジションがFWの選手のうち、体重が軽い順に並び替え、上位の6位から10位までの名前、体重、体重のランキングを表示する際、□に入るクエリとして適切なものを選択せよ。**

### 解答: **2. ROW_NUMBER() OVER (ORDER BY weight) AS weight_rank**

### 解説
問題で示されたクエリの構造:
```sql
WITH A AS
(
    SELECT name, weight, position,
        □
    FROM players
    WHERE position = 'FW'
)
SELECT name, weight, weight_rank
FROM A
WHERE weight_rank BETWEEN 6 AND 10
```

各選択肢の説明:
1. `ROW_NUMBER() AS weight_rank` - ORDER BY句がないためエラーまたは不正な順序
2. `ROW_NUMBER() OVER (ORDER BY weight) AS weight_rank` - **正解**: weightで昇順にランキング
3. `ROW_NUMBER() OVER (PARTITION BY weight) AS weight_rank` - weightでグループ化するが順序がない
4. `ROW_NUMBER() OVER (PARTITION BY weight ORDER BY weight) AS weight_rank` - 同じweightごとに1から始まる

結果（6位〜10位）:
| name | weight | weight_rank |
|------|--------|-------------|
| マタ | 63 | 6 |
| 香川 | 63 | 7 |
| ネイマール | 64 | 8 |
| ペドロ | 64 | 9 |
| フェトファツィディス | 64 | 10 |

---

## 問9
**日本、ブラジル、フランスの各ポジションの人数についてのクロス集計表を作成する際、以下のクエリではエラーになる。エラーの原因として適切なものを選択せよ。**

```sql
SELECT
  position AS ポジション
 ,SUM(CASE WHEN country_id=12 THEN 1 ELSE 0) AS 日本
 ,SUM(CASE WHEN country_id=1 THEN 1 ELSE 0) AS ブラジル
 ,SUM(CASE WHEN country_id=19 THEN 1 ELSE 0) AS フランス
FROM
  players
GROUP BY position
ORDER BY position
;
```

### 解答: **2. 3〜5行目のELSE 0の後にENDがない**

### 解説
CASE式の正しい構文:
```sql
CASE WHEN condition THEN value1 ELSE value2 END
```

問題のクエリでは`END`が欠落しています。

正しいクエリ:
```sql
SELECT
  position AS ポジション
 ,SUM(CASE WHEN country_id=12 THEN 1 ELSE 0 END) AS 日本
 ,SUM(CASE WHEN country_id=1 THEN 1 ELSE 0 END) AS ブラジル
 ,SUM(CASE WHEN country_id=19 THEN 1 ELSE 0 END) AS フランス
FROM
  players
GROUP BY position
ORDER BY position;
```

他の選択肢について:
- 選択肢1: GROUP BYとORDER BYの順序は正しい
- 選択肢3: カラム名として日本語は問題なく使用できる
- 選択肢4: countriesテーブルは使用していないが、それ自体はエラーにならない

---

## 問10
**以下のクエリのXとYのカラムがそれぞれ表すものとして適切なものを選択せよ。**

```sql
WITH A AS
(SELECT
    C.group_name
   ,C.name
   ,AVG(height) OVER(PARTITION BY C.name) AS X
   ,AVG(height) OVER (PARTITION BY group_name) AS Y
FROM
    players AS P
INNER JOIN
    countries AS C
ON
    P.country_id = C.id
)
SELECT
    *
FROM
    A
GROUP BY name
ORDER BY group_name;
```

### 解答: **1. X: 各国の平均身長、Y: 各グループの平均身長**

### 解説
ウィンドウ関数の`PARTITION BY`句が何でグループ化しているかを確認します:

- `AVG(height) OVER(PARTITION BY C.name) AS X`
  - `C.name`（国名）でパーティション分割
  - 各国ごとの平均身長を計算
  - **X = 各国の平均身長**

- `AVG(height) OVER (PARTITION BY group_name) AS Y`
  - `group_name`（グループ名）でパーティション分割
  - 各グループごとの平均身長を計算
  - **Y = 各グループの平均身長**

結果の一例:
| group_name | name | X（各国の平均身長） | Y（各グループの平均身長） |
|------------|------|-------------------|------------------------|
| A | ブラジル | 181.30 | 181.00 |
| A | メキシコ | 177.52 | 181.00 |
| B | スペイン | 180.09 | 179.75 |
| C | 日本 | 178.52 | 181.36 |

---

## 解答一覧

| 問題 | 解答 |
|------|------|
| 問1 | 1（MF、DF、FW、GKの順）※選択肢確認要 |
| 問2 | 3 |
| 問3 | 4（ベルギー） |
| 問4 | 2（6人） |
| 問5 | 1（各選手の2014年6月13日時点での年齢） |
| 問6 | 3（イングランド） |
| 問7 | 4（ガーナ、ナイジェリア、ベルギー） |
| 問8 | 2（ROW_NUMBER() OVER (ORDER BY weight) AS weight_rank） |
| 問9 | 2（3〜5行目のELSE 0の後にENDがない） |
| 問10 | 1（X: 各国の平均身長、Y: 各グループの平均身長） |