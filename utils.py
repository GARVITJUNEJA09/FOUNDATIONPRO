import os
from fpdf import FPDF


def generate_invoice_pdf(bill):
    os.makedirs("invoices", exist_ok=True)
    file_path = f"invoices/invoice_{bill['bill_id']}.pdf"

    pdf = FPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)

    pdf.set_font("Arial", "B", 16)
    pdf.cell(0, 10, "FoundationPro Invoice", new_x="LMARGIN", new_y="NEXT", align="C")

    pdf.ln(4)
    pdf.set_font("Arial", "", 12)
    pdf.cell(0, 8, f"Bill ID: {bill['bill_id']}", new_x="LMARGIN", new_y="NEXT")
    pdf.cell(0, 8, f"Customer Name: {bill['customer_name']}", new_x="LMARGIN", new_y="NEXT")
    pdf.cell(0, 8, f"Customer Phone: {bill['customer_phone']}", new_x="LMARGIN", new_y="NEXT")
    pdf.cell(0, 8, f"Bill Date: {bill['bill_date']}", new_x="LMARGIN", new_y="NEXT")

    pdf.ln(6)
    pdf.set_font("Arial", "B", 11)
    pdf.cell(70, 10, "Material", border=1)
    pdf.cell(25, 10, "Qty", border=1)
    pdf.cell(40, 10, "Unit Price", border=1)
    pdf.cell(45, 10, "Line Total", border=1, new_x="LMARGIN", new_y="NEXT")

    pdf.set_font("Arial", "", 11)
    for item in bill["items"]:
        pdf.cell(70, 10, str(item["material_name"])[:32], border=1)
        pdf.cell(25, 10, str(item["quantity"]), border=1)
        pdf.cell(40, 10, f"Rs. {item['unit_price']}", border=1)
        pdf.cell(45, 10, f"Rs. {item['line_total']}", border=1, new_x="LMARGIN", new_y="NEXT")

    pdf.ln(6)
    pdf.set_font("Arial", "B", 13)
    pdf.cell(0, 10, f"Total Amount: Rs. {bill['total_amount']}", new_x="LMARGIN", new_y="NEXT")

    pdf.output(file_path)
    return file_path