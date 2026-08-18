from crewai import Crew, Process

from agents import compliance_agent, extraction_agent
from .tasks import audit_task, extract_task


def build_invoice_crew() -> Crew:
    return Crew(
        agents=[extraction_agent, compliance_agent],
        tasks=[extract_task, audit_task],
        process=Process.sequential,
        verbose=True,
    )
