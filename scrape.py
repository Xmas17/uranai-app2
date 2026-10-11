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

def fetch_html(url):
    """指定されたURLのHTMLを取得するヘルパー関数"""
    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=10) as response:
            return response.read().decode('utf-8', errors='ignore')
    except Exception as e:
        print(f"取得エラー ({url}): {e}")
        return None

def get_goisu_rank():
    """GoisuNetからうお座の順位を取得"""
    html = fetch_html("https://goisu.net/daily.html")
    if html:
        soup = BeautifulSoup(html, 'html.parser')
        for el in soup.find_all(['div', 'li', 'td', 'p']):
            text = el.get_text()
            if 'うお座' in text or '魚座' in text:
                match = re.search(r'(\d+)位', text)
                if match:
                    return int(match.group(1))
    return None

def get_nifty_rank():
    """nifty占いからうお座の順位を取得"""
    html = fetch_html("https://uranai.nifty.com/kiou/horoscope/")
    if html:
        soup = BeautifulSoup(html, 'html.parser')
        for el in soup.find_all(['div', 'li', 'p', 'section']):
            text = el.get_text()
            if 'うお座' in text or '魚座' in text:
                match = re.search(r'(\d+)位', text)
                if match:
                    return int(match.group(1))
    return None

# 各サイトからの順位取得
goisu_rank = get_goisu_rank()
nifty_rank = get_nifty_rank()

results = {
    "date": today,
    "line": None,
    "dmenu": None,
    "goisu": goisu_rank,
    "mynavi": nifty_rank  # 枠を流用してniftyの順位を入れる
}

# 平均順位の計算（数値が取れたものだけで計算）
ranks = [v for v in [results["goisu"], results["mynavi"]] if v is not None]
results["average"] = round(sum(ranks) / len(ranks), 1) if ranks else None

print(f"最終集計結果: {results}")

# 結果を JSON ファイルに保存
with open('data.json', 'w', encoding='utf-8') as f:
    json.dump(results, f, ensure_ascii=False, indent=2)

print("data.json に保存完了！")

