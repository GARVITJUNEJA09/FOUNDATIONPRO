import streamlit as st
import pandas as pd
from storage import load_data, add_supplier, update_supplier, delete_supplier

st.title("Suppliers Management")

suppliers = load_data("suppliers")

with st.form("add_supplier_form"):
    st.subheader("Add Supplier")

    supplier_name = st.text_input("Supplier Name")
    contact_person = st.text_input("Contact Person")
    phone = st.text_input("Phone")
    email = st.text_input("Email")
    address = st.text_area("Address")

    submit_add = st.form_submit_button("Add Supplier")

    if submit_add:
        if supplier_name.strip() == "":
            st.error("Supplier name is required.")
        else:
            add_supplier(supplier_name, contact_person, phone, email, address)
            st.success("Supplier added successfully.")
            st.rerun()

st.subheader("All Suppliers")

if suppliers:
    df = pd.DataFrame(suppliers)
    st.dataframe(df, use_container_width=True)

    supplier_ids = [supplier["supplier_id"] for supplier in suppliers]
    selected_supplier_id = st.selectbox("Select Supplier ID to Edit or Delete", supplier_ids)

    selected_supplier = None
    for supplier in suppliers:
        if supplier["supplier_id"] == selected_supplier_id:
            selected_supplier = supplier
            break

    if selected_supplier:
        with st.form("edit_supplier_form"):
            st.subheader("Edit Supplier")

            edit_name = st.text_input("Supplier Name", value=selected_supplier["supplier_name"])
            edit_contact = st.text_input("Contact Person", value=selected_supplier["contact_person"])
            edit_phone = st.text_input("Phone", value=selected_supplier["phone"])
            edit_email = st.text_input("Email", value=selected_supplier["email"])
            edit_address = st.text_area("Address", value=selected_supplier["address"])

            col1, col2 = st.columns(2)
            with col1:
                update_button = st.form_submit_button("Update Supplier")
            with col2:
                delete_button = st.form_submit_button("Delete Supplier")

            if update_button:
                if edit_name.strip() == "":
                    st.error("Supplier name is required.")
                else:
                    update_supplier(
                        selected_supplier_id,
                        edit_name,
                        edit_contact,
                        edit_phone,
                        edit_email,
                        edit_address
                    )
                    st.success("Supplier updated successfully.")
                    st.rerun()

            if delete_button:
                try:
                    delete_supplier(selected_supplier_id)
                    st.warning("Supplier deleted successfully.")
                    st.rerun()
                except ValueError as error:
                    st.error(str(error))
else:
    st.info("No suppliers available.")