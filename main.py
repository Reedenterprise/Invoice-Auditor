import os
import csv
import pdfplumber
from pathlib import Path
from dotenv import load_dotenv
from crew import build_invoice_crew

def load_invoice_text(source: str) -> str:
    path = Path(source)
    if path.is_file():
        if path.suffix.lower() == '.pdf':
            text = ""
            with pdfplumber.open(source) as pdf:
                for page in pdf.pages:
                    text += page.extract_text() + "\n"
            return text
        return path.read_text(encoding="utf-8")
    return source

def main() -> None:
    load_dotenv()
    
    invoices_folder = Path("invoices")
    csv_file_path = "invoice_audit_summary.csv"
    
    if not invoices_folder.exists():
        print("Could not find the 'invoices' folder!")
        return
        
    crew = build_invoice_crew()
    
    print(f"Opening {csv_file_path} to save results...")
    
    # Open the CSV file and set up our columns
    with open(csv_file_path, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["Invoice File Name", "AI Audit Result"])
        
        # Loop through every single PDF inside the invoices folder
        for pdf_path in invoices_folder.glob("*.pdf"):
            print(f"\n--- Scanning: {pdf_path.name} ---")
            
            invoice_text = load_invoice_text(str(pdf_path))
            result = crew.kickoff(inputs={"invoice_text": invoice_text})
            
            # Write the file name and the AI's final answer to the spreadsheet
            writer.writerow([pdf_path.name, str(result)])
            print(f"Saved {pdf_path.name} to the spreadsheet.")

    print(f"\nAll done! Check your {csv_file_path} file.")

if __name__ == "__main__":
    main()