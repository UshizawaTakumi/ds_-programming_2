import pandas as pd
df = pd.read_csv('helth_check.csv')
# 欠損値を含む行を削除
df = df.dropna()
from datetime import datetime

# "起床時間"のカラムを整えるための関数を用意
def convert_to_time(time_str):
    if pd.isna(time_str):
        return None  
    try:
        return datetime.strptime(str(time_str), "%H:%M").time()
    except ValueError:
        try:
            return datetime.strptime(str(time_str), "%H時").time()
        except ValueError:
            try:
                return datetime.strptime(str(time_str), "%H時%M").time()
            except ValueError:
                try:
                    # "9" のような形式を datetime に変換（例：9:00に変換）
                    return datetime.strptime(str(time_str), "%H").time()
                except ValueError:
                    try:
                        # "8時30分" のような形式を datetime に変換（例：8:30に変換）
                        return datetime.strptime(str(time_str), "%H時%M分").time()
                    except ValueError:
                        return None  # 不正なデータは None（欠損値）に変換

# 起床時間のカラムを変換
df['起床時間'] = df['起床時間'].apply(convert_to_time)

df = df.rename(columns={
    'タイムスタンプ': 'date',
    '体温': 'body_temperature',
    '起床時間': 'Wake_up_time',
    '睡眠時間': 'time of sleeping',
    '頭痛の有無': 'headache level',
    '腹痛の有無': 'abdominal pain level',
    '喉の痛みの有無': 'sore throat level',
    '吐き気の有無' : 'nausea level',
    '鼻水の有無' : 'runny nose level',
    '咳の有無' : 'cough level',
    '名前' : 'name' 
})

# データをCSVファイルに保存
df.to_csv('helth_data.csv', index=False)

import sqlite3

# DBファイルを保存するためのファイルパス

# pathを設定
path = '/Users/u_t/Lecture/ds_programing/ds_programming_2/git_connect/ds_-programming_2'

# DBファイル名
db_name = 'health_check_sheet.sqlite'

# DBに接続する（指定したDBファイル存在しない場合は，新規に作成される）
con = sqlite3.connect(path + db_name)


# SQLを実行するためのオブジェクトを取得
cur = con.cursor()

# 3．実行したいSQLを用意する
# テーブルを作成するSQL
# CREATE TABLE テーブル名（カラム名 型，...）;
sql_create_table_helth_check = 'CREATE TABLE helth_check(id INTEGER PRIMARY KEY AUTOINCREMENT, date TEXT, body_temperature FLOAT, Wake_up_time TEXT, time_of_sleeping TEXT, headache_level INT,	abdominal_pain_level INT,	sore_throat_level	INT, nausea_level INT,	runny_nose_level INT,	cough_level INT,	name TEXT);'

# 4．SQLを実行する
cur.execute(sql_create_table_helth_check)

# DataFrameをデータベースに挿入
df.to_sql('helth_check', con, if_exists='replace', index=False)

# 5．コミット処理（データ操作を反映させる）
con.commit()

# 6．DBへの接続を閉じる
con.close()