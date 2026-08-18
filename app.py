import streamlit as st
import os
from invoice_crew import build_invoice_crew
from main import load_invoice_text

st.title("🏗️ Invoice Auditor Pro")
st.write("Upload a subcontractor invoice to instantly verify math and check for lien waivers.")

uploaded_file = st.file_uploader("Drop your PDF invoice here", type="pdf")

if uploaded_file is not None:
    if st.button("Run AI Audit"):
        with st.spinner("AI is reading the document..."):
            temp_path = uploaded_file.name
            with open(temp_path, "wb") as f:
                f.write(uploaded_file.getbuffer())
                
            invoice_text = load_invoice_text(temp_path)
            crew = build_invoice_crew()
            result = crew.kickoff(inputs={"invoice_text": invoice_text})
            
            st.success("Audit Complete!")
            st.write(str(result).replace("$", "\\$"))
            
            os.remove(temp_path)
