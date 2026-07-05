import streamlit as st

from services.company_discovery import find_company
from services.website_parser import build_company_snapshot
from services.news_service import get_company_news
from services.intelligence import build_intelligence
from services.llm_service import generate_executive_brief
from services.pdf_generator import create_pdf

# ==========================================================
# PAGE CONFIG
# ==========================================================

st.set_page_config(
    page_title="Enterprise Account Research Dashboard",
    page_icon="📊",
    layout="wide"
)

st.markdown("""
<style>
a[href^="#"] {
    display: none;
}
</style>
""", unsafe_allow_html=True)
with st.sidebar:

    st.title("Enterprise Dashboard")

    st.markdown("---")

    st.write(
        """
        This dashboard helps sales teams prepare for enterprise meetings by:

        • Discovering the official company website
        • Collecting recent enterprise news
        • Identifying key business developments
        • Generating an AI-powered executive briefing
        """
        )

    st.markdown("---")

    st.caption("Powered by NewsAPI + Gemini 2.5 Flash")


# ==========================================================
# TITLE
# ==========================================================

st.title("📊 Enterprise Account Research Dashboard")

st.markdown(
    """
Analyze a company and automatically generate:

- 🌐 Official Company Information
- 📰 Latest Enterprise News
- 🧠 Enterprise Intelligence
- 🤖 AI Executive Brief
"""
)

st.divider()


# ==========================================================
# INPUT
# ==========================================================

company_name = st.text_input(
    "Enter Company Name",
    placeholder="Microsoft"
)

analyze = st.button(
    "Analyze Company",
    type="primary",
    use_container_width=True
)


# ==========================================================
# MAIN PIPELINE
# ==========================================================

if analyze:

    if not company_name.strip():

        st.error("Please enter a company name.")

        st.stop()

    with st.spinner("Analyzing company..."):

        # ----------------------------------------------------
        # Company Discovery
        # ----------------------------------------------------

        discovery = find_company(company_name)

        website = discovery.get("website")

        # ----------------------------------------------------
        # Website Snapshot
        # ----------------------------------------------------

        if website:

            snapshot = build_company_snapshot(website)

        else:

            snapshot = {
                "status": "error",
                "website": "",
                "title": "",
                "description": "",
                "links": {},
                "errors": [
                    "Official website could not be found."
                ]
            }

        # ----------------------------------------------------
        # News
        # ----------------------------------------------------

        news = get_company_news(company_name)

        # ----------------------------------------------------
        # Enterprise Intelligence
        # ----------------------------------------------------

        intelligence = build_intelligence(
            news["articles"]
        )

        # ----------------------------------------------------
        # Executive Brief
        # ----------------------------------------------------

        executive_brief = generate_executive_brief(
            company_name,
            intelligence
        )

    st.success("Enterprise research completed successfully.")
    
# ==========================================================
# WEBSITE INFORMATION
# ==========================================================

    st.divider()

    st.header("🌐 Company Information")

    col1, col2 = st.columns([2, 1])

    with col1:
        st.subheader(company_name)

        if website:


            st.link_button(
                "Visit Official Website",
                website
                )
        else:

            st.warning("Some sections of the official website could not be accessed because the site blocks automated requests.")

        if snapshot.get("title"):

            st.markdown(f"**Website Title:** {snapshot['title']}")

        if snapshot.get("description"):

            st.write(snapshot["description"])

        elif snapshot.get("status") == "blocked":
            st.info(
                "The company's website blocks automated requests. "
                "Basic company information is still available through news analysis."
                )

    with col2:

        st.metric(
            "Website Confidence",
            discovery.get("confidence", 0)
            )

        st.metric(
            "News Articles",
            len(news["articles"])
        )

        st.metric(
            "Enterprise Insights",
             len(intelligence)
            )


# ==========================================================
# IMPORTANT LINKS
# ==========================================================

    links = snapshot.get("links", {})

    if links:

        st.subheader("Useful Company Links")

        cols = st.columns(3)

        i = 0

        for name, url in links.items():

            with cols[i % 3]:

                st.link_button(name, url)

            i += 1
    
    
# ==========================================================
# LATEST ENTERPRISE NEWS
# ==========================================================

    st.divider()

    st.header("📰 Latest Enterprise News")

    if not news["articles"]:

        st.info("No recent enterprise news found.")

    else:

        for article in news["articles"]:

            with st.expander(article["title"], expanded=False):

                col1, col2, col3 = st.columns(3)

                with col1:
                    st.markdown(f"**Source**")
                    st.write(article["source"])

                with col2:
                    st.markdown(f"**Published**")
                    st.write(article["published"][:10])

                with col3:
                    st.markdown(f"**Relevance Score**")
                    st.write(article["score"])

                if article.get("description"):
                    st.write(article["description"])

                if article.get("url"):

                    st.link_button(
                        "🔗 Read Full Article",
                        article["url"],
                        use_container_width=True
                    )

    
# ==========================================================
# ENTERPRISE INTELLIGENCE
# ==========================================================

    st.divider()

    st.header("🧠 Enterprise Intelligence")

    if not intelligence:

        st.info("No enterprise intelligence generated.")

    else:

        for item in intelligence:

            with st.container(border=True):

                col1, col2, col3 = st.columns([4,2,1])

                with col1:

                    st.subheader(item["title"])

                with col2:

                    st.write(f"**Category**")
                    st.caption(f"Category: {item['category']}")

                    st.write(f"**Priority**")
                    priority = item["priority"]

                    if priority == "High":
                        st.error("🔴 High")

                    elif priority == "Medium":
                        st.warning("🟡 Medium")

                    else:
                        st.success("🟢 Low")

                with col3:

                    st.metric(
                        "Score",
                        item["score"]
                    )
                if item.get("url"):
                    st.link_button(
                        "🔗 View Source",
                        item["url"],
                        use_container_width=True
                    )
                
    
# ==========================================================
# EXECUTIVE BRIEF
# ==========================================================

    st.divider()

    st.header("🤖 AI Executive Brief")

    st.subheader("Executive Summary")

    with st.container(border=True):
        st.write(executive_brief["executive_summary"])

    st.subheader("Key Developments")

    if executive_brief["key_developments"]:
        for item in executive_brief["key_developments"]:
            st.write("•", item)
    else:
        st.info("No key developments identified.")

    st.subheader("Opportunities")

    if executive_brief["opportunities"]:
        for item in executive_brief["opportunities"]:
            st.success(item)
    else:
        st.info("No opportunities identified.")

    st.subheader("Risks")

    if executive_brief["risks"]:

        for item in executive_brief["risks"]:

            st.warning(item)

    else:

        st.success("No significant risks identified.")

    st.subheader("Talking Points")

    if executive_brief["talking_points"]:
        for item in executive_brief["talking_points"]:
            st.write("•", item)
    else:
        st.info("No talking points generated.")

    st.subheader("Next Actions")

    if executive_brief["next_actions"]:
        for item in executive_brief["next_actions"]:
            st.write("✅", item)
    else:
        st.info("No recommended next actions.")
    
    
    pdf = create_pdf(
        company_name,
        executive_brief
        )

    st.download_button(
        label="📄 Download Executive Brief (PDF)",
        data=pdf,
        file_name=f"{company_name}_Executive_Brief.pdf",
        mime="application/pdf",
        use_container_width=True
        )       
    st.divider()

    st.caption(
        "Enterprise Account Research Dashboard | Built using Streamlit, NewsAPI, DuckDuckGo Search and Google Gemini"
        )