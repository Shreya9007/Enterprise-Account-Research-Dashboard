
from services.company_discovery import find_company
from services.website_parser import build_company_snapshot
from services.news_service import get_company_news
from services.intelligence import build_intelligence
companies = [
    "Microsoft",
    "Kalvium",
    "OpenAI"
]

for company in companies:

    print("=" * 60)
    print(company)

    discovery = find_company(company)
    print("Discovery:", discovery)

    snapshot = build_company_snapshot(discovery["website"])
    print(snapshot)

    print("\nLatest News")

    news = get_company_news(company)
    print(news)

    intel = build_intelligence(news["articles"])

    print("\nEnterprise Intelligence\n")

    for item in intel: 
        print("-" * 60)
        print("Category :", item["category"])
        print("Priority :", item["priority"])
        print("Score    :", item["score"])
        print("Source   :", item["source"])
        print("Title    :", item["title"])
