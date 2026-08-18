import os

from crewai import Agent, LLM
from dotenv import load_dotenv

load_dotenv()

llm = LLM(
    model="gemini/gemini-1.5-flash",
    provider="google"
)

extraction_agent = Agent(
    role="Senior Construction Accounts Payable Clerk",
    goal="Extract line items, totals, and vendor data from subcontractor invoices with 100% accuracy.",
    backstory="You have 15 years of experience reading complex commercial construction invoices. You never miss a decimal point.",
    verbose=True,
    allow_delegation=False,
    llm=llm
)

compliance_agent = Agent(
    role="Construction Project Controller",
    goal="Audit extracted invoice data against state compliance laws and flag any missing lien waivers or math errors.",
    backstory="You are a ruthless compliance officer. You protect the general contractor from financial risk by catching errors before payments go out.",
    verbose=True,
    allow_delegation=False,
    llm=llm
)
