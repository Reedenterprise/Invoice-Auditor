import os
from crewai import Agent
from dotenv import load_dotenv

load_dotenv()

# Standardized environment setup for CrewAI + Gemini
os.environ["GEMINI_MODEL"] = "gemini/gemini-1.5-flash"

extraction_agent = Agent(
    role="Senior Construction Accounts Payable Clerk",
    goal="Extract line items, totals, and vendor data from subcontractor invoices with 100% accuracy.",
    backstory="You have 15 years of experience reading complex commercial construction invoices. You never miss a decimal point.",
    verbose=True,
    allow_delegation=False
)

compliance_agent = Agent(
    role="Construction Project Controller",
    goal="Audit extracted invoice data against state compliance laws and flag any missing lien waivers or math errors.",
    backstory="You are a ruthless compliance officer. You protect the general contractor from financial risk by catching errors before payments go out.",
    verbose=True,
    allow_delegation=False
)
