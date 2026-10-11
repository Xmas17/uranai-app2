import urllib.request
from bs4 import BeautifulSoup
import json
import re
from datetime import datetime

# 本日の日付（YYYY-MM-DD）
today = datetime.now().strftime('%Y-%m-%d')
print(f"--- {today} の占い集計を実行中 ---")

# ヘッダー設定（ブラウザからのアクセスに見せかける）
headers = {'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X)'}

def get_goisu_rank():
    """GoisuNetからうお座の順位を取得"""
    try:
        url = "https://goisu.net/daily.html"
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req) as response:
            html = response.read().decode('utf-8')
            soup = BeautifulSoup(html, 'html.parser')
            
            # うお座を探す
            for el in soup.find_all(['div', 'li', 'td', 'p']):
                text = el.get_text()
                if 'うお座' in text or '魚座' in text:
                    match = re.search(r'(\d+)位', text)
                    if match:
                        return int(match.group(1))
    except Exception as e:
        print(f"GoisuNet取得エラー: {e}")
    return None

# 各サイトからの順位取得（現在はGoisuNetから実データ取得、他は準備中）
results = {
    "date": today,
    "line": None,
    "dmenu": None,
    "goisu": get_goisu_rank(),
    "mynavi": None
}

# 平均順位の計算
ranks = [v for v in [results["line"], results["dmenu"], results["goisu"], results["mynavi"]] if v is not None]
results["average"] = round(sum(ranks) / len(ranks), 1) if ranks else None

print(f"取得結果: {results}")

# 結果を JSON ファイルに保存（Web画面表示用）
with open('data.json', 'w', encoding='utf-8') as f:
    json.dump(results, f, ensure_ascii=False, indent=2)

print("data.json に保存完了！")
