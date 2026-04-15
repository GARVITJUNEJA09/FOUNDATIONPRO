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
    st.subheader("Customer Details")
    customer_name = st.text_input("Customer Name")
    customer_phone = st.text_input("Customer Phone")

    st.subheader("Add Item to Cart")

    material_labels = []
    for material in materials:
        label = f"{material['material_name']} | Stock: {material['stock_quantity']} | Price: {material['current_price']}"
        material_labels.append(label)

    selected_label = st.selectbox("Select Material", material_labels)
    quantity = st.number_input("Quantity", min_value=1, step=1)

    if st.button("Add to Cart"):
        selected_material = None
        for material in materials:
            label = f"{material['material_name']} | Stock: {material['stock_quantity']} | Price: {material['current_price']}"
            if label == selected_label:
                selected_material = material
                break

        if selected_material is not None:
            st.session_state.cart.append({
                "material_id": selected_material["material_id"],
                "quantity": int(quantity)
            })
            st.success("Item added to cart.")
            st.rerun()

st.subheader("Current Cart")

if st.session_state.cart:
    cart_display = []
    grand_total = 0

    for index, cart_item in enumerate(st.session_state.cart, start=1):
        selected_material = None
        for material in materials:
            if material["material_id"] == cart_item["material_id"]:
                selected_material = material
                break

        if selected_material is not None:
            line_total = cart_item["quantity"] * float(selected_material["current_price"])
            grand_total += line_total

            cart_display.append({
                "No": index,
                "Material": selected_material["material_name"],
                "Quantity": cart_item["quantity"],
                "Unit Price": selected_material["current_price"],
                "Line Total": line_total
            })

    st.dataframe(pd.DataFrame(cart_display), use_container_width=True)
    st.markdown(f"### Grand Total: Rs. {grand_total}")

    col1, col2 = st.columns(2)

    with col1:
        if st.button("Generate Bill"):
            try:
                bill = create_bill(customer_name, customer_phone, st.session_state.cart)
                pdf_path = generate_invoice_pdf(bill)

                st.success("Bill generated successfully.")

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

    with col2:
        if st.button("Clear Cart"):
            st.session_state.cart = []
            st.warning("Cart cleared.")
            st.rerun()
else:
    st.info("No items in cart.")