#モジュールのインポート
import pandas as pd

#URLを設定(12月分)
url_december = "https://www.data.jma.go.jp/obd/stats/etrn/view/daily_s1.php?prec_no=44&block_no=47662&year=2023&month=12&day=&view=a2"


#スクレイピング
data = pd.read_html(url_december, header = 0)

#一時的にリストをデータフレームに変換
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

#一時的にリストをデータフレームに変換
data_january_list = data[0]
df_january = pd.DataFrame(data_january_list)


# 最初の3行を列名として使用
df_january.columns = df_january.iloc[:3].astype(str).apply(lambda x: '_'.join(x), axis=0)


# わかりやすくするために最初の列に"1-"を追加
df_january[df_january.columns[0]] = '1-' + df_january[df_january.columns[0]].astype(str)

# 最初の3行を削除
df_january = df_january.iloc[3:]

# インデックスを1から始める
df_january.index = range(1, len(df_january) + 1)

#12月のデータを処理
# 欠損値処理
df_december.isnull().sum()

#データの収集開始日に合わせてデータを加工
# 1行目から12行目までを削除
df_december = df_december.drop(index=range(1, 13))

# インデックスをリセット
df_december = df_december.reset_index(drop=True)

#1月のデータを処理
# 欠損値処理
df_january.isnull().sum()


#データの収集開始日に合わせてデータを加工

# 欠損値を含む行を削除
df_january = df_january.dropna()

# 月ごとのデータフレームを連結
df_connected = pd.concat([df_december, df_january], axis=0, ignore_index=True)

# 連結したデータフレームをリストに格納
data_list = [df_connected]