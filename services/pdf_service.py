
from pathlib import Path
from datetime import datetime
from xml.sax.saxutils import escape

from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.units import inch
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
)


REPORTS_DIR = Path("reports")
REPORTS_DIR.mkdir(exist_ok=True)


def generate_pdf(report_content: str, topic: str) -> str:

    safe_topic = "".join(
        char if char.isalnum() else "_"
        for char in topic
    ).strip("_")

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    filename = f"healthcare_report_{safe_topic[:40]}_{timestamp}.pdf"
    filepath = REPORTS_DIR / filename

    doc = SimpleDocTemplate(
        str(filepath),
        pagesize=A4,
        rightMargin=0.7 * inch,
        leftMargin=0.7 * inch,
        topMargin=0.7 * inch,
        bottomMargin=0.7 * inch,
    )

    styles = getSampleStyleSheet()

    title_style = ParagraphStyle(
        "ReportTitle",
        parent=styles["Title"],
        alignment=TA_CENTER,
        fontSize=20,
        leading=26,
        spaceAfter=20,
    )

    heading_style = ParagraphStyle(
        "SectionHeading",
        parent=styles["Heading2"],
        fontSize=14,
        leading=19,
        spaceBefore=14,
        spaceAfter=8,
        fontName="Helvetica-Bold",
    )

    subheading_style = ParagraphStyle(
        "SubHeading",
        parent=styles["Heading3"],
        fontSize=12,
        leading=16,
        spaceBefore=10,
        spaceAfter=6,
        fontName="Helvetica-Bold",
    )

    body_style = ParagraphStyle(
        "ReportBody",
        parent=styles["BodyText"],
        fontSize=10,
        leading=15,
        spaceAfter=5,
    )

    story = []

    # Main PDF title
    story.append(
        Paragraph("Healthcare Research Report", title_style)
    )

    story.append(
        Paragraph(
            f"<b>Research Topic:</b> {escape(topic)}",
            body_style
        )
    )

    story.append(
        Paragraph(
            f"<b>Generated:</b> {datetime.now().strftime('%d %B %Y, %I:%M %p')}",
            body_style
        )
    )

    story.append(Spacer(1, 20))

    # Process report content
    for line in report_content.splitlines():

        line = line.strip()

        if not line:
            story.append(Spacer(1, 6))
            continue

        # Main section heading: # Heading
        if line.startswith("# "):
            heading = escape(line[2:])

            story.append(
                Paragraph(heading, heading_style)
            )

        # Subsection heading: ## Heading
        elif line.startswith("## "):
            heading = escape(line[3:])

            story.append(
                Paragraph(heading, subheading_style)
            )

        # Bullet points
        elif line.startswith("- ") or line.startswith("* "):
            content = escape(line[2:])

            story.append(
                Paragraph(
                    f"&bull; {content}",
                    body_style
                )
            )

        # Normal paragraph
        else:
            story.append(
                Paragraph(escape(line), body_style)
            )

    doc.build(story)

    return str(filepath)
