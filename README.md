# Healthcare News Agent

Healthcare News Agent is a multi-agent application for researching current
healthcare news. It searches for relevant articles, scrapes readable article
content, summarizes the findings, and creates a report that can be downloaded.

## Workflow

The workflow is divided into specialized stages:

1. **Research agent** searches for healthcare-related news.
2. **Scraper tool** extracts readable text from article pages.
3. **Fact-checking agent** reviews the collected information.
4. **Summarizer agent** produces a concise summary.
5. **Report agent** prepares the final report.
6. **PDF service** generates a downloadable PDF report.

The project uses Tavily for news search and Groq through LangChain for
language-model processing.

## Requirements

- Python 3.10 or newer
- A [Tavily API key](https://app.tavily.com/)
- A [Groq API key](https://console.groq.com/)

Install the dependencies with:

```bash
pip install -r requirements.txt
```

## Configuration

Create a local environment file from the example:

```bash
copy .env.example .env
```

Then replace the placeholder values in `.env`:

```env
TAVILY_API_KEY=your_tavily_api_key_here
GROQ_API_KEY=your_groq_api_key_here
```

The real `.env` file is ignored by Git and must never be pushed to GitHub.

## Project structure

```text
agents/       Specialized research, fact-checking, summary, and report agents
prompts/      Prompts used by the agents
services/     Workflow orchestration and PDF generation
tools/        News search and article scraping tools
reports/      Locally generated reports (ignored by Git)
config.py     Loads and validates environment variables
```

## Responsible use

This project is for news research and summarization. It is not a medical
diagnosis or treatment tool. Verify important claims against the original
sources and consult qualified healthcare professionals for medical decisions.
