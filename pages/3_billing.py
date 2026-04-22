import streamlit as st
import pandas as pd
from storage import load_data, create_bill
from utils import generate_invoice_pdf

st.title("Billing System")

materials = load_data("materials")

if "cart" not in st.session_state:
    st.session_state.cart = []

if not materials:
    st.warning("Please add materials before creating a bill.")
else:
    material_map = {material["material_id"]: material for material in materials}

    st.subheader("Customer Details")
    c1, c2 = st.columns(2)
    with c1:
        customer_name = st.text_input("Customer Name")
    with c2:
        customer_phone = st.text_input("Customer Phone")

    st.subheader("Add Items to Cart")

    valid_materials = [m for m in materials if m["stock_quantity"] > 0]
    material_options = {
        f"{m['material_name']} | Stock: {m['stock_quantity']} | Price: {m['current_price']}": m["material_id"]
        for m in valid_materials
    }

    if material_options:
        c3, c4 = st.columns([3, 1])
        with c3:
            selected_label = st.selectbox("Select Material", list(material_options.keys()))
        with c4:
            quantity = st.number_input("Quantity", min_value=1, step=1, value=1)

        if st.button("Add to Cart", use_container_width=True):
            selected_material_id = material_options[selected_label]
            existing_item = next(
                (item for item in st.session_state.cart if item["material_id"] == selected_material_id),
                None
            )

            if existing_item:
                existing_item["quantity"] += int(quantity)
            else:
                st.session_state.cart.append({
                    "material_id": selected_material_id,
                    "quantity": int(quantity)
                })

            st.success("Item added to cart.")
            st.rerun()
    else:
        st.info("No materials with available stock.")

    st.subheader("Current Cart")

    if st.session_state.cart:
        merged_cart = {}
        for item in st.session_state.cart:
            merged_cart[item["material_id"]] = merged_cart.get(item["material_id"], 0) + int(item["quantity"])

        cart_display = []
        grand_total = 0.0

        for index, (material_id, qty) in enumerate(merged_cart.items(), start=1):
            material = material_map.get(material_id)
            if material:
                line_total = round(qty * float(material["current_price"]), 2)
                grand_total += line_total
                cart_display.append({
                    "No": index,
                    "Material": material["material_name"],
                    "Quantity": qty,
                    "Unit Price": material["current_price"],
                    "Line Total": line_total
                })

        st.dataframe(pd.DataFrame(cart_display), use_container_width=True)
        st.markdown(f"### Grand Total: Rs. {round(grand_total, 2)}")

        remove_options = {row["Material"]: row["No"] - 1 for row in cart_display}
        selected_remove = st.selectbox("Select cart item to remove", ["None"] + list(remove_options.keys()))

        c5, c6, c7 = st.columns(3)

        with c5:
            if st.button("Remove Selected", use_container_width=True):
                if selected_remove != "None":
                    material_name = selected_remove
                    selected_material_id = next(
                        material["material_id"]
                        for material in materials
                        if material["material_name"] == material_name
                    )
                    st.session_state.cart = [
                        item for item in st.session_state.cart
                        if item["material_id"] != selected_material_id
                    ]
                    st.warning("Item removed from cart.")
                    st.rerun()

        with c6:
            if st.button("Clear Cart", use_container_width=True):
                st.session_state.cart = []
                st.warning("Cart cleared.")
                st.rerun()

        with c7:
            if st.button("Generate Bill", use_container_width=True):
                try:
                    bill = create_bill(customer_name, customer_phone, st.session_state.cart)
                    pdf_path = generate_invoice_pdf(bill)
                    st.success(f"Bill generated successfully. Bill ID: {bill['bill_id']}")

                    with open(pdf_path, "rb") as pdf_file:
                        st.download_button(
                            label="Download Invoice PDF",
                            data=pdf_file,
                            file_name=f"invoice_{bill['bill_id']}.pdf",
                            mime="application/pdf"
                        )

                    st.session_state.cart = []

                except ValueError as error:
                    st.error(str(error))
    else:
        st.info("No items in cart.")