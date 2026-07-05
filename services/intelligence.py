CATEGORY_KEYWORDS = {

    "AI Initiative": {

        "copilot": 5,
        "chatgpt": 5,
        "gpt": 5,
        "llm": 4,
        "agent": 4,
        "artificial intelligence": 3,
        "ai": 1

    },

    "Cloud": {

        "azure": 5,
        "aws": 5,
        "gcp": 5,
        "cloud": 2

    },

    "Partnership": {

        "partnership": 5,
        "collaboration": 5,
        "partner": 4,
        "joins": 3,
        "alliance": 4

    },

    "Acquisition": {

        "acquisition": 5,
        "acquire": 5,
        "buys": 5,
        "purchase": 4,
        "merger": 4

    },

    "Funding": {

        "funding": 5,
        "raises": 5,
        "investment": 4,
        "series a": 5,
        "series b": 5,
        "valuation": 3

    },

    "Product Launch": {

        "launch": 6,
        "launches": 6,
        "launched": 6,
        "introduces": 5,
        "introduced": 5,
        "unveils": 6,
        "unveiled": 6,
        "new platform": 5,
        "new product": 5,
        "new service": 5

    },

    "Product Update": {

        "update": 5,
        "updated": 5,
        "upgrade": 5,
        "upgraded": 5,
        "patch": 4,
        "bug fix": 4,
        "version": 4,
        "edge 150": 4,
        "windows 11": 3,
        "release notes": 4,
        "feature": 3,
        "improvement": 3

   },

    "Hiring": {

        "hire": 5,
        "hiring": 5,
        "recruit": 4,
        "recruiting": 4,
        "expands team": 5

    },

    "Financial Results": {

        "earnings": 5,
        "revenue": 5,
        "profit": 5,
        "quarterly": 4,
        "quarter": 4,
        "fiscal": 4,
        "eps": 5,
        "guidance": 4,
        "operating income": 5,
        "net income": 5,
        "financial results": 5
        }

}

PRIORITY = {

    "AI Initiative": "High",

    "Acquisition": "High",

    "Funding": "High",

    "Financial Results": "High",

    "Cloud": "Medium",

    "Partnership": "Medium",

    "Product Launch": "Medium",
    
    "Product Update": "Medium",

    "Hiring": "Low",

    "General Update": "Low"

}


PRIORITY_ORDER = {

    "High": 3,

    "Medium": 2,

    "Low": 1

}


def classify_article(article):

    title = article.get("title") or ""
    description = article.get("description") or ""

    text = (title + " " + description).lower()

    best_category = "General Update"
    best_score = 0

    for category, keywords in CATEGORY_KEYWORDS.items():

        score = 0

        for word, weight in keywords.items():

            if word in text:
                score += weight

        if score > best_score:
            best_score = score
            best_category = category

    return best_category


def priority(category):

    return PRIORITY.get(category, "Low")


def build_intelligence(news):

    intelligence = []

    for article in news:

        url = article.get("url", "")

        # Skip Yahoo consent pages
        if "consent.yahoo.com" in url:
            continue

        category = classify_article(article)

        intelligence.append({

            "title": article.get("title", ""),

            "category": category,

            "priority": priority(category),

            "score": article.get("score", 0),

            "source": article.get("source", ""),

            "url": url

        })

    intelligence.sort(

        key=lambda x: (

            PRIORITY_ORDER.get(x["priority"], 0),

            x["score"]

        ),

        reverse=True

    )

    return intelligence