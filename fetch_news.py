import requests
import os
import pandas as pd
from dotenv import load_dotenv
from datetime import datetime

# 1. 加载 API Key
load_dotenv()
NEWSAPI_KEY = os.getenv("NEWSAPI_KEY")
GNEWS_KEY = os.getenv("GNEWS_KEY")

# 2. 拉取英文新闻
def fetch_english_news():
    url = f"https://newsapi.org/v2/top-headlines?language=en&pageSize=50&apiKey={NEWSAPI_KEY}"
    res = requests.get(url)
    data = res.json()
    articles = data.get("articles", [])
    return [
        {
            "title": a["title"],
            "content": a.get("description") or "",
            "url": a["url"],
            "source": a["source"]["name"],
            "lang": "en"
        } for a in articles
    ]

# 3. 拉取中文新闻
def fetch_chinese_news():
    url = f"https://gnews.io/api/v4/top-headlines?lang=zh&max=50&token={GNEWS_KEY}"
    res = requests.get(url)
    data = res.json()
    articles = data.get("articles", [])
    return [
        {
            "title": a["title"],
            "content": a.get("description") or "",
            "url": a["url"],
            "source": a["source"]["name"],
            "lang": "zh"
        } for a in articles
    ]

# 4. 主程序
if __name__ == "__main__":
    en_news = fetch_english_news()
    zh_news = fetch_chinese_news()
    all_news = en_news + zh_news
    df = pd.DataFrame(all_news)

    # ✅ 新增：创建目录
    output_dir = "news_raw"
    os.makedirs(output_dir, exist_ok=True)

    # ✅ 修改：输出文件路径
    today = datetime.now().strftime("%Y-%m-%d")
    output_path = os.path.join(output_dir, f"news_raw_{today}.json")

    df.to_json(output_path, orient="records", force_ascii=False, indent=2)
    print(f"Saved {len(df)} articles to {output_path}")
