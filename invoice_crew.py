import sys
import os

# Force Python to recognize the current directory as a package path
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.append(current_dir)

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
