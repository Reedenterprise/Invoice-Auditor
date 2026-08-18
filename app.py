import os
import streamlit as st
import google.generativeai as genai
from PIL import Image

# Configure Page
st.set_page_config(page_title="Invoice Auditor Pro", page_icon="🧾", layout="wide")

st.title("🧾 Invoice Auditor Pro")
st.markdown("Automated Subcontractor Invoice Extraction & Compliance Auditing")

# Ensure API keys are available
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    try:
        api_key = st.secrets["GEMINI_API_KEY"]
    except Exception:
        pass

if api_key:
    genai.configure(api_key=api_key)

# Streamlit User Interface
uploaded_file = st.file_uploader("Upload Subcontractor Invoice (PDF or Image)", type=["pdf", "png", "jpg", "jpeg"])

if uploaded_file is not None:
    st.image(uploaded_file, caption="Uploaded Invoice", use_container_width=True)
    st.success("Invoice uploaded successfully!")
    
    if st.button("Run Audit"):
        if not api_key:
            st.error("Gemini API key not found in environment or secrets!")
        else:
            with st.spinner("Running AI Extraction and Compliance Audit..."):
                try:
                    # Load model correctly without prefix
                    model = genai.GenerativeModel("gemini-1.5-flash")
                    
                    # Open uploaded image
                    image = Image.open(uploaded_file)
                    
                    prompt = """
                    You are a Senior Construction Accounts Payable Clerk and Construction Project Controller.
                    Analyze this subcontractor invoice:
                    1. Extract all line items, quantities, unit prices, total amounts, and vendor details.
                    2. Audit the extracted data for arithmetic accuracy, matching totals, and flag any missing compliance requirements or math errors.
                    
                    Provide a structured, professional audit report.
                    """
                    
                    response = model.generate_content([image, prompt])
                    
                    st.subheader("Audit Results")
                    st.markdown(response.text)
                except Exception as e:
                    st.error(f"An error occurred during execution: {e}")
