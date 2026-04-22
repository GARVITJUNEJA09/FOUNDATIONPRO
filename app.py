import streamlit as st
from storage import init_storage, load_data, seed_sample_data

st.set_page_config(
    page_title="FoundationPro",
    page_icon="🏗️",
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
Manage suppliers, materials, billing, analytics, and price prediction from one place.
Use the sidebar to open each module.
""")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Materials", len(materials))
with col2:
    st.metric("Suppliers", len(suppliers))
with col3:
    st.metric("Bills", len(bills))
with col4:
    st.metric("Price Records", len(price_history))

st.markdown("### Quick Actions")
c1, c2 = st.columns(2)

with c1:
    if st.button("Load Demo Data", use_container_width=True):
        seed_sample_data()
        st.success("Demo data loaded successfully.")
        st.rerun()

with c2:
    if st.button("Refresh Dashboard", use_container_width=True):
        st.rerun()

st.markdown("### Features")
st.markdown("""
- Full CRUD for materials and suppliers
- Cart-based billing with stock deduction
- PDF invoice generation
- Price trend analytics
- Basic price forecasting
- Built-in demo dataset
""")

if not materials and not suppliers:
    st.info("Start by clicking **Load Demo Data** or add suppliers/materials from the sidebar.")