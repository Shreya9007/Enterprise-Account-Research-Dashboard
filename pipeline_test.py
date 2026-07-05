from services.company_discovery import find_company
from services.website_parser import build_company_snapshot
from services.news_service import get_company_news
from services.intelligence import build_intelligence
from services.llm_service import generate_executive_brief


def print_section(title):
    print("\n" + "=" * 70)
    print(title.upper())
    print("=" * 70)


def run_pipeline(company_name):

    print_section(f"Enterprise Research Report : {company_name}")

    # -------------------------------------------------
    # Discovery
    # -------------------------------------------------

    discovery = find_company(company_name)

    print("\nWebsite Discovery")
    print("-" * 40)
    print(discovery)

    website = discovery.get("website")

    # -------------------------------------------------
    # Website Scraping
    # -------------------------------------------------

    scraped = {
        "status": "error",
        "errors": ["No website found."]
    }

    if website:
        scraped = build_company_snapshot(website)

    print("\nWebsite Information")
    print("-" * 40)
    print(scraped)

    # -------------------------------------------------
    # News
    # -------------------------------------------------

    news = get_company_news(company_name)

    print("\nLatest News")
    print("-" * 40)

    print(f"Articles Found : {news['total']}")

    for i, article in enumerate(news["articles"], start=1):

        print(f"\n{i}. {article['title']}")
        print(f"Source : {article['source']}")
        print(f"Score  : {article['score']}")

    # -------------------------------------------------
    # Intelligence
    # -------------------------------------------------

    intelligence = build_intelligence(news["articles"])

    print_section("Enterprise Intelligence")

    for item in intelligence:

        print(f"\nCategory : {item['category']}")
        print(f"Priority : {item['priority']}")
        print(f"Score    : {item['score']}")
        print(f"Title    : {item['title']}")

    # -------------------------------------------------
    # Executive Brief
    # -------------------------------------------------

    brief = generate_executive_brief(
        company_name,
        intelligence
    )

    print_section("Executive Summary")

    print(brief["executive_summary"])

    print_section("Key Developments")

    for item in brief["key_developments"]:
        print("•", item)

    print_section("Opportunities")

    for item in brief["opportunities"]:
        print("•", item)

    print_section("Risks")

    for item in brief["risks"]:
        print("•", item)

    print_section("Talking Points")

    for item in brief["talking_points"]:
        print("•", item)

    print_section("Next Actions")

    for item in brief["next_actions"]:
        print("•", item)

    print("\n")
    print("=" * 70)
    print("PIPELINE COMPLETED SUCCESSFULLY")
    print("=" * 70)


if __name__ == "__main__":

    company = input("Enter company name: ").strip()

    if company:
        run_pipeline(company)