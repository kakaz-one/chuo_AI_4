# -*- coding: utf-8 -*-
"""
前半レポート: レンタサイクルデータ分析
作成者: 一色可南子
"""

# =============================================================================
# ライブラリのインポート
# =============================================================================
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# =============================================================================
# (1) cycle.csv を読み込み、df_cycle という変数に格納し、最初の5行を表示
# =============================================================================
print("=" * 60)
print("(1) データの読み込みと最初の5行の表示")
print("=" * 60)

# csvファイルの読み込み
df_cycle = pd.read_csv("cycle.csv")

# 最初の5行を表示
print(df_cycle.head())
print()

# =============================================================================
# (2) df_cycle の行数と列数を確認
# =============================================================================
print("=" * 60)
print("(2) 行数と列数の確認")
print("=" * 60)

# shapeで行数と列数を確認
print("行数:", df_cycle.shape[0])
print("列数:", df_cycle.shape[1])
print()

# =============================================================================
# (3) df_cycle の基本統計量を算出
# =============================================================================
print("=" * 60)
print("(3) 基本統計量")
print("=" * 60)

# describe()で基本統計量を算出
print(df_cycle.describe())
print()

# =============================================================================
# (4) 欠損値の有無を確認し、欠損値がある場合には補完・削除などの処理
# =============================================================================
print("=" * 60)
print("(4) 欠損値の確認と処理")
print("=" * 60)

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

# =============================================================================
# (5) 時間別の利用数合計を集計し、棒グラフで表示
# =============================================================================
print("=" * 60)
print("(5) 時間別の利用数合計の集計と可視化")
print("=" * 60)

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

# =============================================================================
# (6) (5)以外の集計・可視化と考察
# =============================================================================
print("=" * 60)
print("(6) 追加の分析と考察")
print("=" * 60)

# -----------------------------------------------------------------------------
# 分析1: 天気と利用数の関係
# 仮説: 天気が良いほど利用数が多いのではないか
# -----------------------------------------------------------------------------
print()
print("【分析1: 天気と利用数の関係】")
print("-" * 40)
print("仮説: 天気が良いほど利用数が多いのではないか")
print()

# 天気のラベル（1:晴れ, 2:曇り, 3:雨, 4:豪雨・雪）
weather_labels = {1: "Clear", 2: "Cloudy", 3: "Rain", 4: "Heavy Rain"}

# groupbyで天気別の平均利用数を計算
weather_avg = df_cycle.groupby("weathersit")["cnt"].mean()

# 結果を表示
print("天気別の平均利用数:")
for weather_code in weather_avg.index:
    label = weather_labels[weather_code]
    avg = round(weather_avg[weather_code], 1)
    print("  " + label + ": " + str(avg))
print()

# 棒グラフの作成
fig, ax = plt.subplots(figsize=(8, 5))
colors = ["gold", "skyblue", "steelblue", "darkslategray"]
ax.bar(weather_avg.index, weather_avg.values, color=colors[:len(weather_avg)])
ax.set_xlabel("Weather Condition")
ax.set_ylabel("Average Count")
ax.set_title("Average Rental Count by Weather")

# x軸のラベルを設定
x_labels = []
for w in weather_avg.index:
    x_labels.append(weather_labels[w])
ax.set_xticks(weather_avg.index)
ax.set_xticklabels(x_labels)
ax.grid(axis="y", alpha=0.3)
fig.savefig("weather_count.png")
plt.show()

print("【考察1】")
print("仮説は正しかった。晴れの日の利用数が最も多く、")
print("天気が悪化するにつれて利用数が減少する傾向が明確に見られる。")
print("雨の日は晴れの日の約半分程度まで減少している。")
print("これは屋外での移動手段であるレンタサイクルの特性を反映している。")
print()

# -----------------------------------------------------------------------------
# 分析2: 曜日別の利用パターン（登録ユーザーと非登録ユーザーの比較）
# 仮説: 登録ユーザーは平日中心、非登録ユーザーは週末中心ではないか
# -----------------------------------------------------------------------------
print()
print("【分析2: 曜日別のユーザータイプ比較】")
print("-" * 40)
print("仮説: 登録ユーザーは平日中心、非登録ユーザーは週末中心ではないか")
print()

# 曜日のラベル
weekday_labels = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"]

# groupbyで曜日別の平均を計算
weekday_casual = df_cycle.groupby("weekday")["casual"].mean()
weekday_registered = df_cycle.groupby("weekday")["registered"].mean()

# 結果を表示
print("曜日別の平均利用数:")
print("曜日\t非登録\t登録")
for i in range(7):
    casual = round(weekday_casual[i], 1)
    registered = round(weekday_registered[i], 1)
    print(weekday_labels[i] + "\t" + str(casual) + "\t" + str(registered))
print()

# 積み上げ棒グラフの作成
fig, ax = plt.subplots(figsize=(10, 6))
x = np.arange(7)

# 積み上げ棒グラフ（bottomで開始位置を指定）
ax.bar(x, weekday_registered.values, label="Registered", color="steelblue")
ax.bar(x, weekday_casual.values, bottom=weekday_registered.values, 
       label="Casual", color="coral")

ax.set_xlabel("Day of Week")
ax.set_ylabel("Average Count")
ax.set_title("Average Rental Count by Day of Week")
ax.set_xticks(x)
ax.set_xticklabels(weekday_labels)
ax.legend()
ax.grid(axis="y", alpha=0.3)
fig.savefig("weekday_user_type.png")
plt.show()

print("【考察2】")
print("仮説は正しかった。登録ユーザーは平日の利用が多く、週末は減少している。")
print("これは通勤・通学目的での利用が主であることを示唆している。")
print("一方、非登録ユーザー（観光客等）は土日に増加する傾向がある。")
print("土日は非登録ユーザーの割合が相対的に高くなっている。")
print()

# -----------------------------------------------------------------------------
# 分析3: 平日と休日の時間帯別利用パターンの比較
# 仮説: 平日は通勤時間帯にピークがあり、休日は日中に分散しているのではないか
# -----------------------------------------------------------------------------
print()
print("【分析3: 平日と休日の時間帯別利用パターンの比較】")
print("-" * 40)
print("仮説: 平日は通勤ピークがあり、休日は日中に分散しているのではないか")
print()

# 条件でデータを抽出
workday_data = df_cycle[df_cycle["workingday"] == 1]
holiday_data = df_cycle[df_cycle["workingday"] == 0]

# 時間別の平均を計算
workday_hourly = workday_data.groupby("hr")["cnt"].mean()
holiday_hourly = holiday_data.groupby("hr")["cnt"].mean()

# 結果を表示
print("時間別平均利用数:")
print("時間\t平日\t休日")
for hr in range(24):
    wd = 0
    hd = 0
    if hr in workday_hourly.index:
        wd = round(workday_hourly[hr], 1)
    if hr in holiday_hourly.index:
        hd = round(holiday_hourly[hr], 1)
    print(str(hr) + "時\t" + str(wd) + "\t" + str(hd))
print()

# 折れ線グラフの作成
fig, ax = plt.subplots(figsize=(12, 6))
ax.plot(workday_hourly.index, workday_hourly.values, 
        marker="o", label="Working Day", color="steelblue")
ax.plot(holiday_hourly.index, holiday_hourly.values, 
        marker="s", label="Holiday/Weekend", color="coral")

ax.set_xlabel("Hour")
ax.set_ylabel("Average Count")
ax.set_title("Hourly Rental Pattern: Working Day vs Holiday")
ax.set_xticks(range(0, 24))
ax.legend()
ax.grid(alpha=0.3)
fig.savefig("workday_holiday.png")
plt.show()

print("【考察3】")
print("仮説は正しかった。平日は8時と17-18時に明確なピークがあり、")
print("通勤目的の利用が多いことがわかる。")
print("一方、休日は10時から17時頃まで緩やかな山型となっており、")
print("レジャーや買い物など、時間に縛られない利用が多いことがわかる。")
print("この違いは、利用目的が平日と休日で大きく異なることを示している。")
print()

# -----------------------------------------------------------------------------
# 分析4: 季節と時間帯による利用パターンの違い
# 仮説: 季節によって利用数が異なるのではないか
# -----------------------------------------------------------------------------
print()
print("【分析4: 季節と時間帯による利用パターンの違い】")
print("-" * 40)
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

# -----------------------------------------------------------------------------
# 分析5: 気温と利用数の関係（相関分析）
# 仮説: 気温が高いほど利用数が増えるのではないか
# -----------------------------------------------------------------------------
print()
print("【分析5: 気温と利用数の関係】")
print("-" * 40)
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

# -----------------------------------------------------------------------------
# 分析6: 年度別の月ごとの利用数推移
# 仮説: 2012年は2011年より利用数が増加しているのではないか
# -----------------------------------------------------------------------------
print()
print("【分析6: 年度別の月ごとの利用数推移】")
print("-" * 40)
print("仮説: 2012年は2011年より利用数が増加しているのではないか")
print()

# groupbyで年度・月別の合計を計算
yearly_monthly = df_cycle.groupby(["yr", "mnth"])["cnt"].sum().unstack(level=0)
yearly_monthly.columns = ["2011", "2012"]

# 結果を表示
print("月別の利用数合計:")
print(yearly_monthly)
print()

# 年度別の総利用数を計算
total_2011 = yearly_monthly["2011"].sum()
total_2012 = yearly_monthly["2012"].sum()
increase_rate = (total_2012 / total_2011 - 1) * 100

print("2011年の総利用数:", int(total_2011))
print("2012年の総利用数:", int(total_2012))
print("増加率:", str(round(increase_rate, 1)) + "%")
print()

# 折れ線グラフの作成
fig, ax = plt.subplots(figsize=(10, 6))
ax.plot(yearly_monthly.index, yearly_monthly["2011"], 
        marker="o", label="2011", color="steelblue")
ax.plot(yearly_monthly.index, yearly_monthly["2012"], 
        marker="s", label="2012", color="coral")

ax.set_xlabel("Month")
ax.set_ylabel("Total Count")
ax.set_title("Monthly Rental Count by Year")
ax.set_xticks(range(1, 13))
ax.legend()
ax.grid(alpha=0.3)
fig.savefig("yearly_monthly.png")
plt.show()

print("【考察6】")
print("仮説は正しかった。2012年は2011年と比べてすべての月で利用数が増加している。")
print("増加率は約65%であり、サービスの認知度向上や利用者増加を示している。")
print("両年とも夏から秋（6-10月）の利用数が多く、冬季は減少する傾向がある。")
print("これは気候の良い時期に利用が集中していることを示している。")
print()

# =============================================================================
# まとめ
# =============================================================================
print("=" * 60)
print("【総括】")
print("=" * 60)
print()
print("本分析では、レンタサイクルの利用データを様々な角度から分析した。")
print()
print("主な発見:")
print("1. 利用時間帯: 通勤時間帯（8時、17-18時）にピークがある")
print("2. 天気の影響: 晴れの日は利用が多く、雨の日は大幅に減少")
print("3. ユーザータイプ: 登録ユーザーは平日中心、非登録ユーザーは週末中心")
print("4. 季節変動: 夏・秋に利用が多く、冬は減少")
print("5. 気温との相関: 正の相関があり、暖かい日ほど利用が増える")
print("6. 年次成長: 2012年は2011年より利用数が約65%増加")
print()
print("これらの知見は、レンタサイクルサービスの運営において、")
print("自転車の配置計画やメンテナンススケジュールの最適化、")
print("需要予測モデルの構築などに活用できると考えられる。")