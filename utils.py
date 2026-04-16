import os
from fpdf import FPDF

def generate_invoice_pdf(bill):
    # Make sure the invoice folder exists before saving the PDF.
    os.makedirs("invoices", exist_ok=True)

    file_path = f"invoices/invoice_{bill['bill_id']}.pdf"

    pdf = FPDF()
    pdf.add_page()

    # Title
    pdf.set_font("Arial", "B", 16)
    pdf.cell(0, 10, "FoundationPro Invoice", ln=True, align="C")

    # Bill details
    pdf.ln(8)
    pdf.set_font("Arial", "", 12)
    pdf.cell(0, 10, f"Bill ID: {bill['bill_id']}", ln=True)
    pdf.cell(0, 10, f"Customer Name: {bill['customer_name']}", ln=True)
    pdf.cell(0, 10, f"Customer Phone: {bill['customer_phone']}", ln=True)
    pdf.cell(0, 10, f"Bill Date: {bill['bill_date']}", ln=True)

    # Table header
    pdf.ln(8)
    pdf.set_font("Arial", "B", 12)
    pdf.cell(70, 10, "Material", 1)
    pdf.cell(25, 10, "Qty", 1)
    pdf.cell(40, 10, "Unit Price", 1)
    pdf.cell(45, 10, "Line Total", 1, ln=True)

    # Table rows
    pdf.set_font("Arial", "", 12)
    for item in bill["items"]:
        pdf.cell(70, 10, str(item["material_name"]), 1)
        pdf.cell(25, 10, str(item["quantity"]), 1)
        pdf.cell(40, 10, str(item["unit_price"]), 1)
        pdf.cell(45, 10, str(item["line_total"]), 1, ln=True)

    # Grand total
    pdf.ln(10)
    pdf.set_font("Arial", "B", 13)
    pdf.cell(0, 10, f"Total Amount: Rs. {bill['total_amount']}", ln=True)

    pdf.output(file_path)
    return file_path