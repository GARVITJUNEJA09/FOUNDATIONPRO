import streamlit as st
import pandas as pd
from storage import load_data, add_material, update_material, delete_material, get_supplier_name

st.title("Materials Management")

materials = load_data("materials")
suppliers = load_data("suppliers")

unit_options = ["Bag", "Kg", "Ton", "Piece", "Box", "Sheet", "Meter", "Litre", "Roll"]

if not suppliers:
    st.warning("Please add suppliers first before adding materials.")
else:
    supplier_map = {supplier["supplier_name"]: supplier["supplier_id"] for supplier in suppliers}

    with st.form("add_material_form"):
        st.subheader("Add Material")
        c1, c2 = st.columns(2)
        with c1:
            material_name = st.text_input("Material Name")
            category = st.text_input("Category")
            unit = st.selectbox("Unit", unit_options)
        with c2:
            stock_quantity = st.number_input("Stock Quantity", min_value=0, step=1)
            current_price = st.number_input("Current Price", min_value=0.0, step=1.0)
            supplier_name = st.selectbox("Supplier", list(supplier_map.keys()))
        submit_add = st.form_submit_button("Add Material")

        if submit_add:
            if not material_name.strip():
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

st.subheader("Material List")

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
            "Updated": material.get("last_updated", "")
        })

    df = pd.DataFrame(display_rows)

    search_term = st.text_input("Search material by name or category")
    if search_term.strip():
        mask = (
            df["Name"].str.contains(search_term, case=False, na=False) |
            df["Category"].str.contains(search_term, case=False, na=False)
        )
        df = df[mask]

    st.dataframe(df, use_container_width=True)

    material_ids = [material["material_id"] for material in materials]
    selected_material_id = st.selectbox("Select Material ID to Edit or Delete", material_ids)

    selected_material = next(
        (material for material in materials if material["material_id"] == selected_material_id),
        None
    )

    if selected_material:
        supplier_names = list(supplier_map.keys())
        current_supplier_name = get_supplier_name(selected_material["supplier_id"])
        current_supplier_index = supplier_names.index(current_supplier_name) if current_supplier_name in supplier_names else 0
        current_unit = selected_material["unit"]
        current_unit_index = unit_options.index(current_unit) if current_unit in unit_options else 0

        with st.form("edit_material_form"):
            st.subheader("Edit Material")
            c1, c2 = st.columns(2)
            with c1:
                edit_name = st.text_input("Material Name", value=selected_material["material_name"])
                edit_category = st.text_input("Category", value=selected_material["category"])
                edit_unit = st.selectbox("Unit", unit_options, index=current_unit_index)
            with c2:
                edit_stock = st.number_input("Stock Quantity", min_value=0, step=1, value=int(selected_material["stock_quantity"]))
                edit_price = st.number_input("Current Price", min_value=0.0, step=1.0, value=float(selected_material["current_price"]))
                edit_supplier_name = st.selectbox("Supplier", supplier_names, index=current_supplier_index)

            c3, c4 = st.columns(2)
            with c3:
                update_button = st.form_submit_button("Update Material")
            with c4:
                delete_button = st.form_submit_button("Delete Material")

            if update_button:
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