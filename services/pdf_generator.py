from io import BytesIO

from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer


def create_pdf(company_name, executive_brief):

    buffer = BytesIO()

    doc = SimpleDocTemplate(buffer)

    styles = getSampleStyleSheet()

    story = []

    story.append(
        Paragraph(
            f"<b>Enterprise Account Research Report</b>",
            styles["Title"]
        )
    )

    story.append(
        Paragraph(
            f"<b>Company:</b> {company_name}",
            styles["Heading2"]
        )
    )

    story.append(Spacer(1, 20))

    def add_section(title, content):

        story.append(
            Paragraph(
                f"<b>{title}</b>",
                styles["Heading2"]
            )
        )

        story.append(Spacer(1, 8))

        if isinstance(content, list):

            if content:

                for item in content:
                    story.append(
                        Paragraph(f"• {item}", styles["BodyText"])
                    )

            else:

                story.append(
                    Paragraph("None", styles["BodyText"])
                )

        else:

            story.append(
                Paragraph(str(content), styles["BodyText"])
            )

        story.append(Spacer(1, 15))

    add_section(
        "Executive Summary",
        executive_brief.get("executive_summary", "")
    )

    add_section(
        "Key Developments",
        executive_brief.get("key_developments", [])
    )

    add_section(
        "Opportunities",
        executive_brief.get("opportunities", [])
    )

    add_section(
        "Risks",
        executive_brief.get("risks", [])
    )

    add_section(
        "Talking Points",
        executive_brief.get("talking_points", [])
    )

    add_section(
        "Next Actions",
        executive_brief.get("next_actions", [])
    )

    doc.build(story)

    buffer.seek(0)

    return buffer