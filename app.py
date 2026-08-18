import os
import streamlit as st
from crewai import Agent, Task, Crew, Process, LLM

# Configure Page
st.set_page_config(page_title="Invoice Auditor Pro", page_icon="🧾", layout="wide")

st.title("🧾 Invoice Auditor Pro")
st.markdown("Automated Subcontractor Invoice Extraction & Compliance Auditing")

# Ensure API keys are available
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    try:
        api_key = st.secrets["GEMINI_API_KEY"]
        os.environ["GEMINI_API_KEY"] = api_key
    except Exception:
        pass

# Initialize explicit Gemini LLM instance for CrewAI
gemini_llm = LLM(model="gemini/gemini-1.5-flash", api_key=api_key)

# Define Agents & Tasks with explicit Gemini LLM
extraction_agent = Agent(
    role="Senior Construction Accounts Payable Clerk",
    goal="Extract line items, totals, and vendor data from subcontractor invoices with 100% accuracy.",
    backstory="You have 15 years of experience reading complex commercial construction invoices. You never miss a decimal point.",
    verbose=True,
    allow_delegation=False,
    llm=gemini_llm
)

compliance_agent = Agent(
    role="Construction Project Controller",
    goal="Audit extracted invoice data against state compliance laws and flag any missing lien waivers or math errors.",
    backstory="You are a ruthless compliance officer. You protect the general contractor from financial risk by catching errors before payments go out.",
    verbose=True,
    allow_delegation=False,
    llm=gemini_llm
)

extract_task = Task(
    description="Analyze the uploaded invoice document and extract all line items, quantities, unit prices, total amounts, and vendor details.",
    expected_output="A structured JSON object containing vendor name, invoice date, line items, and total amount.",
    agent=extraction_agent
)

audit_task = Task(
    description="Review the extracted invoice data for arithmetic accuracy, matching totals, and flag any missing compliance requirements.",
    expected_output="An audit report detailing the validation results, math checks, and compliance status.",
    agent=compliance_agent
)

def build_invoice_crew():
    return Crew(
        agents=[extraction_agent, compliance_agent],
        tasks=[extract_task, audit_task],
        process=Process.sequential,
        verbose=True
    )

# Streamlit User Interface
uploaded_file = st.file_uploader("Upload Subcontractor Invoice (PDF or Image)", type=["pdf", "png", "jpg", "jpeg"])

if uploaded_file is not None:
    st.success("Invoice uploaded successfully!")
    if st.button("Run Audit"):
        with st.spinner("Running AI Extraction and Compliance Audit..."):
            try:
                crew = build_invoice_crew()
                result = crew.kickoff()
                st.subheader("Audit Results")
                st.write(result)
            except Exception as e:
                st.error(f"An error occurred during execution: {e}")
