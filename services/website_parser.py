import requests
import xml.etree.ElementTree as ET
from bs4 import BeautifulSoup
from urllib.parse import urljoin


# ============================================================
# HEADERS
# ============================================================

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/137.0 Safari/537.36"
    ),
    "Accept": (
        "text/html,"
        "application/xhtml+xml,"
        "application/xml;q=0.9,"
        "*/*;q=0.8"
    ),
    "Accept-Language": "en-US,en;q=0.9",
    "Connection": "keep-alive",
    "Upgrade-Insecure-Requests": "1"
}


# ============================================================
# HOMEPAGE PARSER
# ============================================================

def get_html(url):

    session = requests.Session()

    try:

        response = session.get(
            url,
            headers=HEADERS,
            timeout=15,
            allow_redirects=True
        )

        response.raise_for_status()

        return BeautifulSoup(response.text, "lxml")

    except Exception:

        return None


def extract_title(soup):

    if soup is None:
        return ""

    if soup.title:
        return soup.title.get_text(strip=True)

    return ""


def extract_description(soup):

    if soup is None:
        return ""

    checks = [

        ("name", "description"),

        ("property", "og:description"),

        ("name", "twitter:description")

    ]

    for attr, value in checks:

        tag = soup.find(
            "meta",
            attrs={attr: value}
        )

        if tag and tag.get("content"):

            return tag["content"].strip()

    return ""


def extract_navigation_links(soup, base_url):

    if soup is None:
        return {}

    keywords = {
        "About": ["about", "about-us", "company"],
        "Careers": ["career", "careers", "jobs"],
        "Blog": ["blog"],
        "News": ["news", "press"],
        "Contact": ["contact"],
        "Investor": ["investor"],
        "LinkedIn": ["linkedin"]
    }

    links = {}

    candidates = {}

    for a in soup.find_all("a", href=True):

        href = urljoin(base_url, a["href"])

        text = a.get_text(" ", strip=True).lower()

        combined = text + " " + href.lower()

        for section, words in keywords.items():

            if not any(word in combined for word in words):
                continue
            
            if section == "LinkedIn":
                if "/company/" in href.lower():
                    score = 100

                elif "/posts/" in href.lower():
                    score = -100

                else:
                    score = 0

            else:
                score = 0

            score = 0

            # Strong preference for clean URLs
            if "/about" in href.lower():
                score += 40

            if "/about-us" in href.lower():
                score += 50

            if "/company" in href.lower():
                score += 30

            # Penalize blog articles
            if "/blog/" in href.lower():
                score -= 40

            if "utm_" in href.lower():
                score -= 10

            if section not in candidates or score > candidates[section][0]:

                candidates[section] = (score, href)

    for section in candidates:

        links[section] = candidates[section][1]

    return links


# ============================================================
# SITEMAP
# ============================================================

def get_sitemap(base_url):

    try:

        response = requests.get(
            base_url.rstrip("/") + "/sitemap.xml",
            headers=HEADERS,
            timeout=10
        )

        if response.status_code == 200:

            return response.text

    except Exception:

        pass

    return None


def parse_sitemap(xml_text):

    urls = []

    try:

        root = ET.fromstring(xml_text)

        namespace = {
            "sm": "http://www.sitemaps.org/schemas/sitemap/0.9"
        }

        for loc in root.findall(".//sm:loc", namespace):

            if loc.text:

                urls.append(loc.text.strip())

    except Exception:

        return []

    return urls


def find_useful_links(urls):

    keywords = {

        "About": ["about"],

        "Careers": ["career", "careers", "jobs"],

        "Blog": ["blog"],

        "News": ["news", "press"],

        "Contact": ["contact"],

        "Investor": ["investor"]

    }

    found = {}

    for url in urls:

        lower = url.lower()

        for section, words in keywords.items():

            if section in found:
                continue

            if any(word in lower for word in words):

                found[section] = url

    return found


# ============================================================
# MAIN SNAPSHOT BUILDER
# ============================================================

def build_company_snapshot(website):

    snapshot = {

        "status": "success",

        "website": website,

        "title": "",

        "description": "",

        "links": {},

        "errors": []

    }

    soup = get_html(website)

    if soup:

        snapshot["title"] = extract_title(soup)

        blocked_phrases = [

            "request has been blocked",

            "access denied",

            "attention required",

            "verify you are human",

            "forbidden"

        ]

        title = snapshot["title"].lower()

        if any(p in title for p in blocked_phrases):

            snapshot["status"] = "blocked"

            snapshot["errors"].append(
                "Website blocked automated requests."
            )

            snapshot["title"] = ""

            snapshot["description"] = ""

        else:

            snapshot["description"] = extract_description(soup)

            snapshot["links"] = extract_navigation_links(
                soup,
                website
            )

        return snapshot

    # -----------------------------
    # Homepage failed
    # -----------------------------

    snapshot["status"] = "partial"

    snapshot["errors"].append(
        "Homepage unavailable."
    )

    sitemap = get_sitemap(website)

    if sitemap:

        urls = parse_sitemap(sitemap)

        snapshot["links"] = find_useful_links(urls)

    else:

        snapshot["errors"].append(
            "Sitemap unavailable."
        )

    return snapshot