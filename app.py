import io
import pandas as pd
import requests
import streamlit as st

st.set_page_config(layout="wide", page_title="PMU Internal Dashboard")

st.title("📊 Portfolios & Project Payments Live Tracker")
st.caption("Auto-syncs live with your Google Drive Excel Master file")

# This is your converted direct link to the Excel file on Google Drive
EXCEL_URL = "https://docs.google.com/spreadsheets/d/19jVwszJtSGMLHhI1nj9Fstyd6DbUC9P4/export?format=xlsx"


# Fetch the data dynamically using an in-memory stream
@st.cache_data(ttl=300)  # Caches for 5 minutes so it stays super fast
def load_data(sheet_name):
    try:
        # Download the file content securely into memory first
        response = requests.get(EXCEL_URL)
        response.raise_for_status()  # Check for download errors
        excel_data = io.BytesIO(response.content)

        # Read the specific sheet from the in-memory data
        return pd.read_excel(excel_data, sheet_name=sheet_name)
    except Exception as e:
        st.error(f"Error fetching data: {e}")
        return None


# 1. Sidebar Setup for Sheet Selection
available_sheets = [
    "Consolidate Sheet",
    "G-Gaiter",
    "Antibiogram",
    "Voice to Text",
    "Citizen Satisfaction Survey",
    "Cervical cancer",
    "Consumer Billing Application",
    "Indoor Navigation System ",
    "Diabetic Retinopathy Phase 2",
    "AI Chatbot for eHealth",
    "Kerala Bone Marrow Registry",
    "Blood Bag Traceability ",
    "AI Based OP Token ",
    "Mobile app KASP-PMJAY-SHA",
    "Facial Recognation",
    "Tissue Culture Traceability",
]

selected_sheet = st.sidebar.selectbox("📂 Select Project Component", available_sheets)

# 2. Load the specific sheet chosen by the user
df = load_data(selected_sheet)

if df is not None:
    st.subheader(f"📑 Current View: {selected_sheet}")

    # Clean up purely empty rows/columns common in Excel exports
    clean_df = df.dropna(how="all").reset_index(drop=True)

    # Simple clean presentation for your internal team
    st.dataframe(clean_df, use_container_width=True)
else:
    st.error(
        "Could not pull live data. Please ensure the Google Drive file share permission is set to 'Anyone with the link'."
    )
