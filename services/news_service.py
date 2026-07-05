import os
import re
import requests
from dotenv import load_dotenv

load_dotenv()

NEWS_API_KEY = os.getenv("NEWS_API_KEY")

BASE_URL = "https://newsapi.org/v2/everything"


# Trusted enterprise news sources
GOOD_SOURCES = {
    "Reuters",
    "Bloomberg",
    "CNBC",
    "TechCrunch",
    "The Verge",
    "Business Insider",
    "Fortune",
    "Forbes",
    "Wired",
    "Financial Times",
    "Associated Press",
    "AP News",
    "Yahoo Finance",
    "MarketWatch",
    "ZDNet",
    "VentureBeat",
    "Ars Technica",
    "GeekWire",
    "The Information",
    "TechRadar"
}
GOOD_SOURCES.update({

    "SiliconANGLE News",
    "ComputerWeekly",
    "InfoWorld",
    "VentureBeat",
    "CRN",
    "ZDNet"

})

LOW_QUALITY_SOURCES = {

    "Pypi.org",

    "Biztoc.com",

    "Softpedia.com",

    "BleepingComputer",

    "F1chronicle.com"

}


# Company aliases
ALIASES = {
    "Microsoft": [
        "microsoft",
        "windows",
        "azure",
        "satya nadella"
    ],

    "OpenAI": [
        "openai",
        "chatgpt",
        "sam altman"
    ],

    "Kalvium": [
        "kalvium"
    ]
}

def score_article(company_name, article):

    source = article.get("source", {}).get("name", "").lower()
    for bad in LOW_QUALITY_SOURCES:
        if bad.lower() in source:
            return 0

    title = (article.get("title") or "").lower()

    description = (article.get("description") or "").lower()

    text = title + " " + description

    source_score = 0
    company_score = 0
    business_score = 0

    # -------------------------
    # Trusted Source
    # -------------------------

    for good in GOOD_SOURCES:

        if good.lower() in source.lower():

            source_score = 35
            break
  
    # -------------------------
    # Company aliases
    # -------------------------

    aliases = ALIASES.copy()

    aliases["Microsoft"] = [
        "microsoft",
        "windows",
        "azure",
        "copilot",
        "satya",
        "satya nadella",
        "github",
        "linkedin",
        "msft"
    ]

    aliases["OpenAI"] = [
        "openai",
        "chatgpt",
        "gpt",
        "gpt-4",
        "gpt-5",
        "sam altman",
        "codex"
    ]

    keywords = aliases.get(
        company_name,
        [company_name.lower()]
    )

    company_found = False

    for word in keywords:

        if word in title:

            company_score += 50
            company_found = True

        elif word in description:

            company_score += 25
            company_found = True

    # Reject articles that never mention the company

    if not company_found:
        return 0

    # -------------------------
    # Business keywords
    # -------------------------

    BUSINESS_KEYWORDS = {

        "acquisition": 25,
        "acquire": 25,
        "partnership": 20,
        "partner": 20,
        "collaboration": 20,
        "funding": 25,
        "raises": 25,
        "investment": 20,
        "earnings": 20,
        "revenue": 20,
        "profit": 20,
        "enterprise": 15,
        "ai": 15,
        "artificial intelligence": 15,
        "cloud": 15,
        "launch": 15,
        "announced": 15,
        "introduces": 15,
        "product": 15,
        "security": 10,
        "hiring": 10,
        "expansion": 15,
        "update": 8,
        "updated": 8,
        "upgrade": 8,
        "version": 5,
        "feature": 5,
    }

    for word, value in BUSINESS_KEYWORDS.items():
        if re.search(rf"\b{re.escape(word)}\b", text):

            business_score += value

    # -------------------------
    # Recency bonus
    # -------------------------

    published = article.get("publishedAt", "")

    if published.startswith("2026-07"):
        business_score += 5

    # -------------------------
    # Final Score
    # -------------------------

    score = source_score + company_score + business_score

    return score
    
 

def get_company_news(company_name, page_size=50):

    params = {
        "q": company_name,
        "language": "en",
        "sortBy": "publishedAt",
        "pageSize": page_size,
        "apiKey": NEWS_API_KEY
    }

    try:

        response = requests.get(
            BASE_URL,
            params=params,
            timeout=15
        )

        response.raise_for_status()

        data = response.json()

    except Exception as e:

        return {
            "status": "error",
            "message": str(e),
            "articles": []
        }

    raw_articles = data.get("articles", [])
    seen_titles = set()
    results = []

    for article in raw_articles:
        title = article.get("title", "") or ""

        if title.lower() in seen_titles:
            continue

        seen_titles.add(title.lower())
        
        url = article.get("url", "")
        if "consent.yahoo.com" in url:
            continue
        score = score_article(company_name, article)

        if score < 40:
            continue

        article["score"] = score

        results.append({
            "title": title,

            "source": article.get("source", {}).get("name", ""),

            "published": article.get("publishedAt", ""),

            "description": article.get("description", ""),

            "url": article.get("url", ""),

            "image": article.get("urlToImage", ""),

            "score": score
            })
    
    results.sort(
        key=lambda x: (
            x["score"],
            x["published"]
            ),
        reverse=True
        )

    results = results[:8]

    return {
        "status": "success",
        "total": len(results),
        "articles": results[:page_size]
    }


if __name__ == "__main__":

    print("API Key:", NEWS_API_KEY)

    news = get_company_news("Microsoft")

    print("\nFound", news["total"], "articles\n")

    for article in news["articles"]:

        print("-" * 60)
        print(article["title"])
        print(article["source"])
        print(article["published"])
        print(article["url"])
        