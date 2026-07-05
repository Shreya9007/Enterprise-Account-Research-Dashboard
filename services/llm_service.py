import json
import os

from dotenv import load_dotenv
from google import genai

load_dotenv()

client = genai.Client(
    api_key=os.getenv("LLM_API_KEY")
)


def build_prompt(company_name, intelligence):
    """
    Convert enterprise intelligence into a structured prompt
    for Gemini.
    """

    articles = []

    for item in intelligence:

        articles.append(
            f"""
Title: {item.get("title","")}
Category: {item.get("category","")}
Priority: {item.get("priority","")}
Score: {item.get("score", 0)}
Source: {item.get("source","")}
Description: {item.get("description","")}
"""
        )

    articles_text = "\n".join(articles)

    prompt = f"""
You are a Senior Enterprise Account Executive preparing a briefing for a sales meeting with a prospective enterprise customer.

Your task is to analyze the supplied company intelligence and produce an accurate, concise sales briefing.

Base every conclusion ONLY on the supplied intelligence.

If there is not enough evidence for a conclusion, explicitly state that instead of making assumptions.

Your job is to help a B2B sales representative prepare for a meeting with {company_name}.

Rules:

- Use ONLY the supplied enterprise intelligence.
- Never invent facts.
- Never assume partnerships, opportunities or risks unless supported by the articles.
- Ignore duplicate or repeated news.
- Prefer higher priority and higher score articles when summarizing.
- If multiple articles describe the same event, summarize it only once.

Focus on major business developments like:

- AI initiatives
- Cloud
- Enterprise software
- Product launches
- Partnerships
- Acquisitions
- Funding
- Financial performance
- Hiring
- Security

Return ONLY valid JSON.

Output requirements:

- executive_summary: maximum 80 words
- key_developments: 3 to 5 items
- opportunities: maximum 3 items
- risks: maximum 3 items
- talking_points: maximum 5 items
- next_actions: maximum 3 items

Required format:

{{
    "executive_summary": "...",

    "key_developments": [
        "...",
        "..."
    ],

    "opportunities": [
        "...",
        "..."
    ],

    "risks": [
        "...",
        "..."
    ],

    "talking_points": [
        "...",
        "..."
    ],

    "next_actions": [
        "...",
        "..."
    ]
}}
If the supplied intelligence does not contain enough information for a section, 
return an empty list for that section instead of inventing content.


Focus on major business developments like:
Prioritize developments in this order:

1. AI initiatives
2. Enterprise products
3. Cloud strategy
4. Acquisitions
5. Partnerships
6. Funding
7. Financial results
8. Security
9. Hiring

Enterprise Intelligence:

{articles_text}
"""

    return prompt


def clean_response(text):
    """
    Remove markdown code fences if Gemini returns them.
    """

    text = text.strip()

    if text.startswith("```json"):
        text = text.replace("```json", "", 1)

    if text.startswith("```"):
        text = text.replace("```", "", 1)

    if text.endswith("```"):
        text = text[:-3]

    return text.strip()


def generate_executive_brief(company_name, intelligence):

    if not intelligence:

        return {
            "executive_summary": "No recent enterprise updates available.",
            "key_developments": [],
            "opportunities": [],
            "risks": [],
            "talking_points": [],
            "next_actions": []
        }

    prompt = build_prompt(company_name, intelligence)

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )

    text = clean_response(response.text)

    try:

        return json.loads(text)

    except Exception:

        return {
            "executive_summary": text,
            "key_developments": [],
            "opportunities": [],
            "risks": [],
            "talking_points": [],
            "next_actions": []
        }


if __name__ == "__main__":

    sample = [
        {
            "title": "Microsoft launches Frontier Company",
            "category": "AI Initiative",
            "priority": "High",
            "score": 110,
            "source": "Reuters",
            "description": "Microsoft announced a new enterprise AI initiative."
        }
    ]

    result = generate_executive_brief(
        "Microsoft",
        sample
    )

    print(json.dumps(result, indent=4))