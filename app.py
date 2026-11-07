import re
from html import escape
from pathlib import Path
from typing import Any

import streamlit as st

from services.pdf_service import generate_pdf
from services.workflow import run_research


APP_ROOT = Path(__file__).parent
STYLESHEET = APP_ROOT / "assets" / "styles.css"


st.set_page_config(
    page_title="Health Research Intelligence",
    page_icon=None,
    layout="wide",
    initial_sidebar_state="collapsed",
)


def load_styles() -> None:
    """Load the application stylesheet from the local assets directory."""
    try:
        stylesheet = STYLESHEET.read_text(encoding="utf-8")
    except OSError as error:
        st.error(f"Unable to load the application stylesheet: {error}")
        return

    st.markdown(f"<style>{stylesheet}</style>", unsafe_allow_html=True)


def render_brand_header() -> None:
    """Render the product header and lightweight navigation."""
    st.markdown(
        """
        <header class="topbar">
            <div class="brand-lockup">
                <div class="brand-mark" aria-hidden="true">
                    <svg viewBox="0 0 42 42" role="img">
                        <rect x="1" y="1" width="40" height="40" rx="12" />
                        <path d="M21 11v20M11 21h20" />
                        <circle cx="21" cy="21" r="13.5" />
                    </svg>
                </div>
                <div>
                    <div class="brand-name">Health Research Intelligence</div>
                    <div class="brand-caption">EVIDENCE-LED HEALTHCARE INSIGHT</div>
                </div>
            </div>
            <div class="topbar-meta">
                <span class="status-dot"></span>
                <span>Research workspace</span>
            </div>
        </header>
        """,
        unsafe_allow_html=True,
    )


def render_hero() -> None:
    """Render the primary product introduction."""
    st.markdown(
        """
        <section class="hero">
            <div class="hero-content">
                <div class="eyebrow">Healthcare intelligence, in one workspace</div>
                <h1>Turn emerging healthcare news into decisions you can trust.</h1>
                <p>
                    Research current developments with a focused multi-agent workflow
                    that gathers source material, checks evidence, and creates a clear
                    report for your team.
                </p>
                <div class="hero-proof">
                    <span><strong>04</strong> specialist agents</span>
                    <span class="proof-divider"></span>
                    <span><strong>01</strong> structured research brief</span>
                </div>
            </div>
            <div class="hero-aside" aria-hidden="true">
                <div class="signal-orbit orbit-large"></div>
                <div class="signal-orbit orbit-small"></div>
                <div class="signal-core">
                    <span class="signal-line"></span>
                    <span class="signal-line"></span>
                    <span class="signal-line"></span>
                </div>
            </div>
        </section>
        """,
        unsafe_allow_html=True,
    )


def render_research_form() -> tuple[str, bool]:
    """Render the research input and return the submitted topic."""
    st.markdown(
        """
        <div class="section-intro">
            <div>
                <div class="eyebrow eyebrow-dark">Start a research brief</div>
                <h2>What would you like to understand?</h2>
            </div>
            <p>Enter a focused healthcare topic to begin a new evidence review.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    with st.form("research_form", clear_on_submit=False):
        topic = st.text_input(
            "Research topic",
            placeholder="e.g. Latest developments in cancer treatment",
            label_visibility="collapsed",
        )
        submitted = st.form_submit_button(
            "Generate research report",
            use_container_width=True,
        )

    return topic.strip(), submitted


def parse_research_articles(research: str) -> list[dict[str, str]]:
    """Parse the research agent's documented article format for display."""
    article_pattern = re.compile(
        r"###\s*Article\s*(?P<number>\d+)\s*:\s*(?P<title>.*?)\s*"
        r"\n+[\*_]{0,2}Content:[\*_]{0,2}\s*\n?"
        r"(?P<content>.*?)"
        r"\n+[\*_]{0,2}Source URL:[\*_]{0,2}\s*"
        r"\n?(?P<url>https?://\S+)",
        re.IGNORECASE | re.DOTALL,
    )

    articles = []
    for match in article_pattern.finditer(research):
        content = re.sub(r"\n{3,}", "\n\n", match.group("content").strip())
        url = match.group("url").rstrip(").,;")
        articles.append(
            {
                "number": match.group("number"),
                "title": match.group("title").strip(),
                "content": content,
                "url": url,
            }
        )

    return articles


def render_article(article: dict[str, str]) -> None:
    """Render one research article with distinct content and source areas."""
    with st.container(border=True):
        st.markdown(
            f"""
            <div class="article-kicker">ARTICLE {article["number"].zfill(2)}</div>
            <h3 class="article-title">{escape(article["title"])}</h3>
            """,
            unsafe_allow_html=True,
        )
        st.markdown(article["content"])
        st.markdown('<div class="source-label">SOURCE</div>', unsafe_allow_html=True)
        st.caption(article["url"])
        st.link_button("Open original source", article["url"])


def render_research_findings(research: str) -> None:
    """Render parsed articles, with a safe fallback for unexpected output."""
    articles = parse_research_articles(research)
    if not articles:
        with st.container(border=True):
            st.markdown(research)
        return

    for article in articles:
        render_article(article)


def render_output_section(title: str, description: str, content: str) -> None:
    """Render a polished section for a non-article agent output."""
    st.markdown(
        f"""
        <div class="output-heading">
            <div>
                <div class="eyebrow eyebrow-dark">Workflow output</div>
                <h2>{title}</h2>
            </div>
            <p>{description}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    with st.container(border=True):
        st.markdown(content)


def render_results(result: dict[str, Any], pdf_path: str) -> None:
    """Render all workflow outputs and the generated PDF download."""
    topic = escape(str(result["topic"]))
    st.markdown(
        """
        <div class="results-header">
            <div>
                <div class="eyebrow eyebrow-dark">Research workspace</div>
                <h2>Research brief</h2>
            </div>
            <div class="results-topic">Topic <strong>{}</strong></div>
        </div>
        """.format(topic),
        unsafe_allow_html=True,
    )

    tab_articles, tab_evidence, tab_summary, tab_report = st.tabs(
        ["Research findings", "Evidence review", "Executive summary", "Final report"]
    )

    with tab_articles:
        st.markdown(
            '<p class="tab-intro">Source-led findings collected for this research topic.</p>',
            unsafe_allow_html=True,
        )
        render_research_findings(result["research"])

    with tab_evidence:
        render_output_section(
            "Evidence review",
            "Claims reviewed against the collected source material.",
            result["fact_check"],
        )

    with tab_summary:
        render_output_section(
            "Executive summary",
            "The most important developments, distilled for quick review.",
            result["summary"],
        )

    with tab_report:
        render_output_section(
            "Final research report",
            "A structured report ready to share with your team.",
            result["report"],
        )

    st.markdown(
        """
        <section class="download-panel">
            <div class="download-copy">
                <div class="eyebrow eyebrow-teal">Export your brief</div>
                <h2>Take the research with you.</h2>
                <p>Download a professionally formatted PDF of the final research report.</p>
            </div>
            <div class="download-meta">
                <span>PDF report</span>
                <span>Generated from the final report</span>
            </div>
        </section>
        """,
        unsafe_allow_html=True,
    )

    if Path(pdf_path).exists():
        with open(pdf_path, "rb") as pdf_file:
            st.download_button(
                "Download research report",
                data=pdf_file,
                file_name=Path(pdf_path).name,
                mime="application/pdf",
                use_container_width=True,
            )
    else:
        st.error("The generated PDF file could not be found.")


def run_submitted_research(topic: str) -> None:
    """Run the unchanged backend workflow and persist its outputs."""
    try:
        with st.status("Preparing your research brief", expanded=True) as status:
            st.write(
                "The research workflow is gathering sources, reviewing evidence, "
                "summarizing findings, and preparing the final report."
            )
            result = run_research(topic)
            pdf_path = generate_pdf(result["report"], topic)
            status.update(
                label="Research brief ready",
                state="complete",
                expanded=False,
            )

        st.session_state["research_result"] = result
        st.session_state["research_pdf"] = pdf_path
        st.session_state["research_topic"] = topic
    except Exception as error:
        st.error(f"Unable to complete the research process: {error}")


def render_footer() -> None:
    """Render the product footer."""
    st.markdown(
        """
        <footer class="footer">
            <div class="footer-brand">HEALTH RESEARCH INTELLIGENCE</div>
            <div>AI-assisted healthcare research for informed teams.</div>
            <div class="footer-note">For research and education only. Not medical advice.</div>
        </footer>
        """,
        unsafe_allow_html=True,
    )


load_styles()
render_brand_header()
render_hero()

topic, submitted = render_research_form()
if submitted:
    if not topic:
        st.warning("Enter a healthcare topic to begin your research brief.")
    else:
        run_submitted_research(topic)

if "research_result" in st.session_state:
    render_results(
        st.session_state["research_result"],
        st.session_state["research_pdf"],
    )

render_footer()
