import streamlit as st
import pandas as pd
from storage import load_data, create_bill
from utils import generate_invoice_pdf

st.title("Billing System")

# Load all materials so we can build the billing form and check stock.
materials = load_data("materials")

# Keep the cart inside session_state so it does not disappear
# every time Streamlit reruns the page.
if "cart" not in st.session_state:
    st.session_state.cart = []

# Small helper so we can quickly find a material by its ID later.
material_map = {material["material_id"]: material for material in materials}

if not materials:
    st.warning("Please add materials before creating a bill.")
else:
    st.subheader("Customer Details")
    customer_name = st.text_input("Customer Name")
    customer_phone = st.text_input("Customer Phone")

    st.subheader("Add Item to Cart")

    # Show a more user-friendly label in the dropdown
    # so the user can see material name, stock, and price together.
    material_options = {
        f"{material['material_name']} | Stock: {material['stock_quantity']} | Price: {material['current_price']}": material["material_id"]
        for material in materials
    }

    selected_label = st.selectbox("Select Material", list(material_options.keys()))
    quantity = st.number_input("Quantity", min_value=1, step=1)

    if st.button("Add to Cart"):
        selected_material_id = material_options[selected_label]
        selected_material = material_map.get(selected_material_id)

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

    # Build a cleaner table for the cart preview.
    for index, cart_item in enumerate(st.session_state.cart, start=1):
        selected_material = material_map.get(cart_item["material_id"])

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
                # This saves the bill and also updates stock in storage.
                bill = create_bill(customer_name, customer_phone, st.session_state.cart)

                # Generate the invoice PDF after the bill is created successfully.
                pdf_path = generate_invoice_pdf(bill)

                st.success("Bill generated successfully.")

                # Give the user a download button for the PDF invoice.
                with open(pdf_path, "rb") as pdf_file:
                    st.download_button(
                        label="Download Invoice PDF",
                        data=pdf_file,
                        file_name=f"invoice_{bill['bill_id']}.pdf",
                        mime="application/pdf"
                    )

                # Clear the cart after a successful bill.
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