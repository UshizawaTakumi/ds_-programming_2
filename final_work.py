#モジュールのインポート
import pandas as pd

#URLを設定(12月分)
url_december = "https://www.data.jma.go.jp/obd/stats/etrn/view/daily_s1.php?prec_no=44&block_no=47662&year=2023&month=12&day=&view=a2"


#スクレイピング
data = pd.read_html(url_december, header = 0)

#リストをデータフレームに変換
data_december_list = data[0]
df_december = pd.DataFrame(data_december_list)


# 最初の3行を列名として使用
df_december.columns = df_december.iloc[:3].astype(str).apply(lambda x: '_'.join(x), axis=0)

# わかりやすくするために最初の列に"12-"を追加
df_december[df_december.columns[0]] = '12-' + df_december[df_december.columns[0]].astype(str)

# 最初の3行を削除
df_december = df_december.iloc[3:]

# インデックスを1から始める
df_december.index = range(1, len(df_december) + 1)

#URLを設定(1月分)
url_january = "https://www.data.jma.go.jp/obd/stats/etrn/view/daily_s1.php?prec_no=44&block_no=47662&year=2024&month=01&day=&view=a2"


#スクレイピング
data = pd.read_html(url_january, header = 0)

#リストをデータフレームに変換
data_january_list = data[0]
df_january = pd.DataFrame(data_january_list)
df_january

# 最初の3行を列名として使用
df_january.columns = df_january.iloc[:3].astype(str).apply(lambda x: '_'.join(x), axis=0)


# わかりやすくするために最初の列に"1-"を追加
df_january[df_january.columns[0]] = '1-' + df_january[df_january.columns[0]].astype(str)

# 最初の3行を削除
df_january = df_january.iloc[3:]

# インデックスを1から始める
df_january.index = range(1, len(df_january) + 1)

# 欠損値処理(12月)
df_december.isnull().sum()

#データの収集開始日に合わせてデータを加工
# 1行目から12行目までを削除
df_december = df_december.drop(index=range(1, 13))



# インデックスをリセット
df_december = df_december.reset_index(drop=True)

# 欠損値処理(1月)
df_january.isnull().sum()

#データの収集開始日に合わせてデータを加工

# 欠損値を含む行を削除
df_january = df_january.dropna()

# 月ごとのデータフレームを連結
df_connected = pd.concat([df_december, df_january], axis=0, ignore_index=True)

# 不要な列の削除
df_connected = df_connected.drop(['海面_最低_値', '海面_最低_時分', '降水量(mm)_最大1時間_時分',
                                  '降水量(mm)_最大10分間_時分', '気温(℃)_最高_時分',
                                  '気温(℃)_最低_時分', '湿度(％)_最小_時分'], axis=1)

# カラムの名前を変更する
df_connected = df_connected.rename(columns={
    '日_日_日': 'date',
    '現地_平均_平均	': 'Local average atmospheric pressure',
    '海面_平均_平均': 'mean pressure at sea level',
    '降水量(mm)_合計_合計': 'total precipitation',
    '降水量(mm)_最大1時間_値': 'Total precipitation for up to 1 hour',
    '降水量(mm)_最大10分間_値': 'Total precipitation for up to 10 minutes',
    '気温(℃)_平均_平均': 'average temperature',
    '気温(℃)_最高_値' : 'Highest temperature',
    '気温(℃)_最低_値' : 'Lowest Temperature',
    '蒸気圧 (hPa)_平均_平均' : 'average vapor pressure',
    '湿度(%)_平均_平均' : 'average humidity' ,
    '湿度(%)_最小_値' : 'minimum humidity'
})

df_connected = df_connected.rename(columns={'現地_平均_平均': 'average atmospheric pressure over land'})

import sqlite3
# DBファイルを保存するためのファイルパス

# pathを設定
path = '/Users/u_t/Lecture/ds_programing/ds_programming_2/git_connect/ds_-programming_2'


# DBファイル名
db_name = 'weather_data_scraping.sqlite'

# DBに接続する（指定したDBファイル存在しない場合は，新規に作成される）
con = sqlite3.connect(path + db_name)

# SQLを実行するためのオブジェクトを取得
cur = con.cursor()


# テーブルを作成するSQL
sql_create_table_scraping_wether = 'CREATE TABLE scraping_wether(id INTEGER PRIMARY KEY AUTOINCREMENT, date TEXT, average_atmospheric_pressure_over_land	FLOAT, mean_pressure_at_sea_level FLOAT, total_precipitation FLOAT, Total_precipitation_for_up_to_1_hour FLOAT,	Total_precipitation_for_up_to_10_minutes FLOAT,	average_temperature	FLOAT, Highest_temperature FLOAT,	Lowest_Temperature FLOAT,	average_vapor_pressure FLOAT,	average_humidity FLOAT,	minimum_humidity FLOAT );'

# 4．SQLを実行する
cur.execute(sql_create_table_scraping_wether)


# DataFrameをデータベースに挿入
df_connected.to_sql('scraping_weather', con, if_exists='replace', index=False)

# 5．コミット処理（データ操作を反映させる）
con.commit()



# DBへの接続を閉じる
con.close()
