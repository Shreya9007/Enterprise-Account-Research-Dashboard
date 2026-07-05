from ddgs import DDGS
import tldextract
import re


BLACKLIST = {
    "linkedin.com",
    "facebook.com",
    "instagram.com",
    "youtube.com",
    "github.com",
    "medium.com",
    "wikipedia.org",
    "twitter.com",
    "x.com",
}


BAD_SUBDOMAINS = {
    "blog",
    "community",
    "docs",
    "support",
    "developer",
    "developers",
    "academy",
    "events",
    "news",
    "press",
    "help",
}


SEARCH_QUERIES = [
    "{} official website",
    "{} company",
    "{} homepage",
]


def clean_company_name(name):
    return re.sub(r"[^a-z0-9]", "", name.lower())


def clean_url(url):
    ext = tldextract.extract(url)

    if not ext.domain or not ext.suffix:
        return url

    return f"https://www.{ext.domain}.{ext.suffix}"


def score_result(company_name, result):

    href = result.get("href", "")
    title = result.get("title", "")
    body = result.get("body", "")

    ext = tldextract.extract(href)

    subdomain = ext.subdomain.lower()
    domain = ext.domain.lower()
    suffix = ext.suffix.lower()

    hostname = ".".join(
        part for part in [subdomain, domain, suffix] if part
    )

    company = clean_company_name(company_name)

    score = 0

    # Reject unwanted websites
    if any(site in hostname for site in BLACKLIST):
        return -1000

    # Exact domain
    if domain == company:
        score += 100

    elif domain.startswith(company):
        score += 80

    elif company in domain:
        score += 60

    elif company in hostname:
        score += 40

    # Good TLD
    if suffix in {"com", "io", "ai", "org", "co"}:
        score += 15

    # Prefer root domains
    if subdomain in ("", "www"):
        score += 20

    else:
        for part in subdomain.split("."):
            if part in BAD_SUBDOMAINS:
                score -= 30
            else:
                score -= 15

    combined = (title + " " + body).lower()

    if company_name.lower() in combined:
        score += 20

    if "official" in combined:
        score += 10

    if "homepage" in combined:
        score += 5

    return score


def find_company(company_name):

    candidates = []

    with DDGS() as ddgs:

        for query in SEARCH_QUERIES:

            results = ddgs.text(
                query.format(company_name),
                max_results=5
            )

            for result in results:

                href = result.get("href")

                if not href:
                    continue

                candidates.append({
                    "url": clean_url(href),
                    "score": score_result(company_name, result)
                })

    unique = {}

    for item in candidates:

        url = item["url"]

        if url not in unique or item["score"] > unique[url]:
            unique[url] = item["score"]

    ranked = [
        {"url": url, "score": score}
        for url, score in unique.items()
    ]

    ranked.sort(
        key=lambda x: (x["score"], -len(x["url"])),
        reverse=True,
    )

    if not ranked:
        return {
            "website": None,
            "confidence": 0,
        }

    return {
        "website": ranked[0]["url"],
        "confidence": ranked[0]["score"],
    }