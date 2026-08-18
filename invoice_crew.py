import sys
import os

# Ensure Python can find local modules
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from crewai import Crew, Process
from agents import compliance_agent, extraction_agent
from tasks import audit_task, extract_task

def build_invoice_crew():
    return Crew(
        agents=[extraction_agent, compliance_agent],
        tasks=[extract_task, audit_task],
        process=Process.sequential,
        verbose=True
    )
