import urllib.request
from bs4 import BeautifulSoup
import json
from datetime import datetime

# 本日の日付（YYYY-MM-DD）
today = datetime.now().strftime('%Y-%m-%d')

print(f"--- {today} の占い集計を実行中 ---")

# ※現在はまだテスト段階のため、仮の順位データをセットしています
# 後ほど実際のサイトから取得するコードにパワーアップしていきます！
results = {
    "date": today,
    "line": 3,          # LINE占い（例: 3位）
    "dmenu": 5,         # dメニュー占い（例: 5位）
    "goisu": 2,         # GoisuNet（例: 2位）
    "mynavi": 4         # マイナビニュース（例: 4位）
}

# 平均順位を計算（数値が入っているものだけ対象）
ranks = [v for v in [results["line"], results["dmenu"], results["goisu"], results["mynavi"]] if v is not None]
if ranks:
    average_rank = sum(ranks) / len(ranks)
    results["average"] = round(average_rank, 1)
else:
    results["average"] = None

print(f"集計結果: {results}")
