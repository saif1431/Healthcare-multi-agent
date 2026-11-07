
from services.workflow import run_research
from services.pdf_service import generate_pdf


def main():

    print("\n===================================")
    print("  HEALTHCARE NEWS RESEARCH SYSTEM")
    print("===================================\n")

    # Get topic from user
    topic = input("Enter your healthcare research topic: ").strip()

    if not topic:
        print("Please enter a valid research topic.")
        return

    print("\nResearch started. Please wait...\n")

    try:
        # Run complete multi-agent workflow
        result = run_research(topic)

        print("\n========== RESEARCH FINDINGS ==========\n")
        print(result["research"])

        print("\n========== FACT CHECKING ==========\n")
        print(result["fact_check"])

        print("\n========== FINAL SUMMARY ==========\n")
        print(result["summary"])

        print("\n========== FINAL REPORT ==========\n")
        print(result["report"])

        # Generate PDF
        print("\nGenerating PDF report...\n")

        pdf_path = generate_pdf(
            report_content=result["report"],
            topic=topic
        )

        print("\n===================================")
        print("       RESEARCH COMPLETED!")
        print("===================================")
        print(f"\nPDF saved at: {pdf_path}\n")

    except Exception as error:
        print(f"\nAn error occurred: {error}")


if __name__ == "__main__":
    main()
