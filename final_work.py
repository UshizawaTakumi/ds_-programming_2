#モジュールのインポート
import pandas as pd

#URLを設定
url = "https://www.data.jma.go.jp/obd/stats/etrn/view/daily_s1.php?prec_no=44&block_no=47662&year=2023&month=12&day=&view=a2"


#スクレイピング
data = pd.read_html(url, header = 0)
data