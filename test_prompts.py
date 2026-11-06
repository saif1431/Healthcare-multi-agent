
import sys

from services.workflow import run_research


sys.stdout.reconfigure(encoding="utf-8")

topic = "Latest developments in cancer treatment"

print("\nStarting Healthcare Research Workflow...\n")

result = run_research(topic)


print("\n========== RESEARCH ==========\n")
print(result["research"])

print("\n========== FACT CHECK ==========\n")
print(result["fact_check"])

print("\n========== SUMMARY ==========\n")
print(result["summary"])

print("\n========== FINAL REPORT ==========\n")
print(result["report"])
