# Enterprise Account Research Dashboard

### Live Demo
https://enterprise-account-research-dashboard-cqgaffjrmwjzykxye9otuu.streamlit.app/

## Overview

The **Enterprise Account Research Dashboard** is an AI-powered sales intelligence application that helps Business-to-Business (B2B) sales teams prepare for customer meetings by automatically gathering and summarizing publicly available company information.

The application discovers a company's official website, retrieves recent enterprise news, classifies business developments into meaningful categories, and generates an executive briefing using Google's Gemini 2.5 Flash model.

The project is built with Python and Streamlit and demonstrates the integration of web search, news intelligence, natural language processing, and large language models into a unified enterprise research workflow.

---


## Features

* Automatic company website discovery
* Company website analysis
* Enterprise news collection using NewsAPI
* Intelligent article scoring and filtering
* Classification of business events
* AI-generated executive briefing
* Interactive Streamlit dashboard
* Enterprise-focused news prioritization

---

## Technology Stack

### Frontend

* Streamlit

### Backend

* Python

### APIs

* NewsAPI
* Google Gemini 2.5 Flash API
* DuckDuckGo Search (DDGS)

### Libraries

* requests
* BeautifulSoup4
* python-dotenv
* google-genai
* tldextract
* lxml

---

## Project Structure

```
Enterprise-Account-Research-Dashboard/
│
├── app.py
├── requirements.txt
├── README.md
├── .env
│
├── services/
│   ├── company_discovery.py
│   ├── website_parser.py
│   ├── news_service.py
│   ├── intelligence.py
│   ├── pdf_generator.py
│   └── llm_service.py
├── test.py
└── pipeline_test.py
```

---

## Workflow

1. Enter a company name.
2. Discover the official company website.
3. Extract publicly available company information.
4. Retrieve recent enterprise news.
5. Filter and score relevant articles.
6. Classify articles into business intelligence categories.
7. Generate an AI-powered executive briefing.
8. Display results through an interactive dashboard.

---

## Business Intelligence Categories

* AI Initiatives
* Cloud
* Partnerships
* Acquisitions
* Funding
* Product Launches
* Product Updates
* Financial Results
* Hiring
* General Updates

---

## AI Executive Brief Includes

* Executive Summary
* Key Developments
* Opportunities
* Risks
* Talking Points
* Recommended Next Actions

---

## Installation

Clone the repository:

```bash
git clone <repository-url>
cd Enterprise-Account-Research-Dashboard
```

Create a virtual environment:

```bash
python -m venv venv
```

Activate the environment:

### Windows

```bash
venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Create a `.env` file in the project root:

```env
NEWS_API_KEY=your_newsapi_key
LLM_API_KEY=your_gemini_api_key
```

Run the application:

```bash
streamlit run app.py
```

---

## Future Enhancements

* PDF report generation
* Personalized sales outreach generation
* CRM integration
* Multi-company comparison dashboard
* Historical trend analysis
* Interactive visual analytics

---

## Author

Developed as an AI-powered Enterprise Account Research Dashboard project using Python, Streamlit, NewsAPI, DuckDuckGo Search, and Google Gemini 2.5 Flash.
