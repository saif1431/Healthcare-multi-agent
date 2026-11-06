
from agents.research_agent import research_agent
from agents.fact_checker_agent import fact_checker_agent
from agents.summarizer_agent import summarizer_agent
from agents.report_agent import report_agent


def get_agent_output(response):
    """Extract the final AI response from an agent."""
    for message in reversed(response["messages"]):
        content = message.content
        if isinstance(content, str) and content.strip():
            return content

    raise RuntimeError("The agent returned no text content.")


def run_research(topic: str) -> dict:
    """
    Execute the complete healthcare research workflow.
    """

    # Step 1: Research
    research_response = research_agent.invoke({
        "messages": [
            {
                "role": "user",
                "content": f"Research this healthcare topic: {topic}"
            }
        ]
    })

    research_output = get_agent_output(research_response)


    # Step 2: Fact Checking
    fact_check_response = fact_checker_agent.invoke({
        "messages": [
            {
                "role": "user",
                "content": f"""
                Research Topic: {topic}

                Fact-check the following research:

                {research_output}
                """
            }
        ]
    })

    fact_check_output = get_agent_output(fact_check_response)


    # Step 3: Summarization
    summary_response = summarizer_agent.invoke({
        "messages": [
            {
                "role": "user",
                "content": f"""
                Research Topic: {topic}

                Summarize these fact-checking results:

                {fact_check_output}
                """
            }
        ]
    })

    summary_output = get_agent_output(summary_response)


    # Step 4: Report Generation
    report_response = report_agent.invoke({
        "messages": [
            {
                "role": "user",
                "content": f"""
                Research Topic: {topic}

                Fact Checking Results:
                {fact_check_output}

                Final Summary:
                {summary_output}

                Prepare the final research report.
                """
            }
        ]
    })

    report_output = get_agent_output(report_response)


    # Return all agent outputs
    return {
        "topic": topic,
        "research": research_output,
        "fact_check": fact_check_output,
        "summary": summary_output,
        "report": report_output
    }
