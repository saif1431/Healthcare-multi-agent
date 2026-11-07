
from services.pdf_service import generate_pdf

sample_report = """
# Latest Developments in Cancer Treatment

## Executive Summary

This is a sample healthcare research report.

## Key Developments

- Development one: Example research finding.
- Development two: Another example finding.

## Limitations

This is illustrative content, not real medical evidence.

## Sources

- https://example.com/article
"""

pdf_path = generate_pdf(
    report_content=sample_report,
    topic="Latest developments in cancer treatment"
)

print("PDF generated successfully!")
print("PDF Location:", pdf_path)
