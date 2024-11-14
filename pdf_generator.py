from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib import colors


class PDFGenerator:
    def __init__(self, filename):
        self.filename = filename
        self.doc = SimpleDocTemplate(
            filename,
            pagesize=letter,
            rightMargin=72,
            leftMargin=72,
            topMargin=72,
            bottomMargin=72,
        )
        self.styles = getSampleStyleSheet()

    def generate_invoice(self, invoice, customer):
        elements = []

        # Add company header
        elements.append(Paragraph("Your Company Name", self.styles["Heading1"]))
        elements.append(Paragraph("123 Business Street", self.styles["Normal"]))
        elements.append(Paragraph("Phone: (555) 555-5555", self.styles["Normal"]))
        elements.append(Spacer(1, 20))

        # Add invoice information
        elements.append(
            Paragraph(f"Invoice #{invoice.invoice_number}", self.styles["Heading2"])
        )
        elements.append(Paragraph(f"Date: {invoice.date}", self.styles["Normal"]))
        elements.append(
            Paragraph(f"Due Date: {invoice.due_date}", self.styles["Normal"])
        )
        elements.append(Spacer(1, 20))

        # Add customer information
        elements.append(Paragraph("Bill To:", self.styles["Heading3"]))
        elements.append(Paragraph(customer.name, self.styles["Normal"]))
        elements.append(Paragraph(customer.address, self.styles["Normal"]))
        elements.append(Paragraph(customer.email, self.styles["Normal"]))
        elements.append(Spacer(1, 20))

        # Create items table
        items_data = [["Description", "Quantity", "Unit Price", "Total"]]
        for item in invoice.items:
            items_data.append(
                [
                    item.description,
                    str(item.quantity),
                    f"${item.unit_price:.2f}",
                    f"${item.total:.2f}",
                ]
            )

        # Add total row
        items_data.append(["", "", "Total:", f"${invoice.total_amount:.2f}"])

        table = Table(items_data, colWidths=[4 * inch, inch, 1.2 * inch, 1.2 * inch])
        table.setStyle(
            TableStyle(
                [
                    ("BACKGROUND", (0, 0), (-1, 0), colors.grey),
                    ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),
                    ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                    ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                    ("FONTSIZE", (0, 0), (-1, 0), 14),
                    ("BOTTOMPADDING", (0, 0), (-1, 0), 12),
                    ("BACKGROUND", (0, -1), (-1, -1), colors.beige),
                    ("TEXTCOLOR", (0, 1), (-1, -1), colors.black),
                    ("FONTNAME", (0, 1), (-1, -1), "Helvetica"),
                    ("FONTSIZE", (0, 1), (-1, -1), 12),
                    ("ALIGN", (-1, 0), (-1, -1), "RIGHT"),
                    ("GRID", (0, 0), (-1, -2), 1, colors.black),
                ]
            )
        )

        elements.append(table)

        # Build PDF
        self.doc.build(elements)
