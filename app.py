import streamlit as st
from storage import init_storage, load_data

# Set the page title, icon, and layout once at the top.
# Wide layout works better here because the app has metrics, tables, and charts.
st.set_page_config(
    page_title="FoundationPro",
    page_icon="FP",
    layout="wide"
)

# Make sure the data folder and JSON files exist before we try to read anything.
init_storage()

# Load all main datasets so we can show quick summary numbers on the home page.
materials = load_data("materials")
suppliers = load_data("suppliers")
bills = load_data("bills")
price_history = load_data("price_history")

# Main title and short description for the homepage.
st.title("FoundationPro")
st.subheader("Construction Material Wholesale Business Manager")

# Simple welcome text so users know what the app does.
st.markdown("""
Welcome to FoundationPro.

Use the sidebar to manage:
- Materials
- Suppliers
- Billing
- Analytics
- Prediction
""")

# Quick instruction for first-time users.
st.info("Open the pages from the sidebar.")

# These four cards give a quick snapshot of the system.
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Total Materials", len(materials))

with col2:
    st.metric("Total Suppliers", len(suppliers))

with col3:
    st.metric("Total Bills", len(bills))

with col4:
    st.metric("Price Records", len(price_history))

# Short feature list for presentation/demo purposes.
st.markdown("### System Features")
st.markdown("""
- Full CRUD for materials
- Full CRUD for suppliers
- Billing with stock updates
- PDF invoice generation
- Price analytics charts
- Price prediction
""")