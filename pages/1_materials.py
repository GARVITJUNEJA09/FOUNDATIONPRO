import streamlit as st
import pandas as pd
from storage import (
    load_data,
    add_material,
    update_material,
    delete_material,
    get_supplier_name
)

st.title("Materials Management")

materials = load_data("materials")
suppliers = load_data("suppliers")

if not suppliers:
    st.warning("Please add suppliers first before adding materials.")
else:
    supplier_map = {supplier["supplier_name"]: supplier["supplier_id"] for supplier in suppliers}

    with st.form("add_material_form"):
        st.subheader("Add Material")

        material_name = st.text_input("Material Name")
        category = st.text_input("Category")
        unit = st.selectbox("Unit", ["bag", "kg", "ton", "piece", "box"])
        stock_quantity = st.number_input("Stock Quantity", min_value=0, step=1)
        current_price = st.number_input("Current Price", min_value=0.0, step=1.0)
        supplier_name = st.selectbox("Supplier", list(supplier_map.keys()))

        submit_add = st.form_submit_button("Add Material")

        if submit_add:
            if material_name.strip() == "":
                st.error("Material name is required.")
            else:
                add_material(
                    material_name,
                    category,
                    unit,
                    stock_quantity,
                    current_price,
                    supplier_map[supplier_name]
                )
                st.success("Material added successfully.")
                st.rerun()

st.subheader("All Materials")

if materials:
    display_rows = []
    for material in materials:
        display_rows.append({
            "ID": material["material_id"],
            "Name": material["material_name"],
            "Category": material["category"],
            "Unit": material["unit"],
            "Stock": material["stock_quantity"],
            "Price": material["current_price"],
            "Supplier": get_supplier_name(material["supplier_id"]),
            "Last Updated": material["last_updated"]
        })

    df = pd.DataFrame(display_rows)
    st.dataframe(df, use_container_width=True)

    material_ids = [material["material_id"] for material in materials]
    selected_material_id = st.selectbox("Select Material ID to Edit or Delete", material_ids)

    selected_material = None
    for material in materials:
        if material["material_id"] == selected_material_id:
            selected_material = material
            break

    if selected_material:
        supplier_map = {supplier["supplier_name"]: supplier["supplier_id"] for supplier in suppliers}
        supplier_names = list(supplier_map.keys())
        current_supplier_name = get_supplier_name(selected_material["supplier_id"])

        if current_supplier_name not in supplier_names and supplier_names:
            current_supplier_name = supplier_names[0]

        with st.form("edit_material_form"):
            st.subheader("Edit Material")

            edit_name = st.text_input("Material Name", value=selected_material["material_name"])
            edit_category = st.text_input("Category", value=selected_material["category"])

            unit_options = ["bag", "kg", "ton", "piece", "box"]
            current_unit = selected_material["unit"]
            unit_index = unit_options.index(current_unit) if current_unit in unit_options else 0
            edit_unit = st.selectbox("Unit", unit_options, index=unit_index)

            edit_stock = st.number_input(
                "Stock Quantity",
                min_value=0,
                step=1,
                value=int(selected_material["stock_quantity"])
            )

            edit_price = st.number_input(
                "Current Price",
                min_value=0.0,
                step=1.0,
                value=float(selected_material["current_price"])
            )

            supplier_index = supplier_names.index(current_supplier_name) if current_supplier_name in supplier_names else 0
            edit_supplier_name = st.selectbox("Supplier", supplier_names, index=supplier_index)

            col1, col2 = st.columns(2)
            with col1:
                update_button = st.form_submit_button("Update Material")
            with col2:
                delete_button = st.form_submit_button("Delete Material")

            if update_button:
                if edit_name.strip() == "":
                    st.error("Material name is required.")
                else:
                    update_material(
                        selected_material_id,
                        edit_name,
                        edit_category,
                        edit_unit,
                        edit_stock,
                        edit_price,
                        supplier_map[edit_supplier_name]
                    )
                    st.success("Material updated successfully.")
                    st.rerun()

            if delete_button:
                delete_material(selected_material_id)
                st.warning("Material deleted successfully.")
                st.rerun()
else:
    st.info("No materials available.")