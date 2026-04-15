import streamlit as st
from storage import init_storage, load_data

st.set_page_config(
    page_title="FoundationPro",
    page_icon="FP",
    layout="wide"
)

init_storage()

materials = load_data("materials")
suppliers = load_data("suppliers")
bills = load_data("bills")
price_history = load_data("price_history")

st.title("FoundationPro")
st.subheader("Construction Material Wholesale Business Manager")

st.markdown("""
Welcome to FoundationPro.

Use the sidebar to manage:
- Materials
- Suppliers
- Billing
- Analytics
- Prediction
""")

st.info("Open the pages from the sidebar.")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Total Materials", len(materials))

with col2:
    st.metric("Total Suppliers", len(suppliers))

with col3:
    st.metric("Total Bills", len(bills))

with col4:
    st.metric("Price Records", len(price_history))

st.markdown("### System Features")
st.markdown("""
- Full CRUD for materials
- Full CRUD for suppliers
- Billing with stock updates
- PDF invoice generation
- Price analytics charts
- Price prediction
""")