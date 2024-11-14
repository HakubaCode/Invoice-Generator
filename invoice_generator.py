from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib import colors

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class InvoiceGenerator:
    def create_customer(self, name, email, address, phone):
        """Create a new customer."""
        if not name:
            raise ValueError("Customer name is required")

        session = Session()
        try:
            # Check for existing email
            if email and session.query(Customer).filter_by(email=email).first():
                raise ValueError("Email already exists")

            customer = Customer(name=name, email=email, address=address, phone=phone)

            session.add(customer)
            session.commit()
            # Get the ID before closing the session
            customer_id = customer.id
            return customer_id
        finally:
            session.close()

    def create_invoice(self, customer_id, items):
        """Create a new invoice with items."""
        session = Session()
        try:
            # Verify customer exists
            customer = session.get(Customer, customer_id)
            if not customer:
                raise ValueError("Customer not found")

            # Generate unique invoice number
            invoice_number = f"INV-{uuid.uuid4().hex[:8].upper()}"

            # Create invoice
            invoice = Invoice(
                invoice_number=invoice_number,
                customer_id=customer_id,
                date=datetime.now().date(),
                due_date=datetime.now().date() + timedelta(days=30),
                status="draft",
            )

            # Add items to invoice
            total_amount = 0
            for item_data in items:
                item = InvoiceItem(
                    description=item_data["description"],
                    quantity=item_data["quantity"],
                    unit_price=item_data["unit_price"],
                )
                item.calculate_total()
                total_amount += item.total
                invoice.items.append(item)

            invoice.total_amount = total_amount

            session.add(invoice)
            session.commit()
            # Get the ID before closing the session
            invoice_id = invoice.id
            return invoice_id
        finally:
            session.close()

    def get_invoice(self, invoice_id):
        """Retrieve an invoice by ID."""
        session = Session()
        try:
            invoice = session.get(Invoice, invoice_id)
            if not invoice:
                raise ValueError("Invoice not found")
            return invoice
        finally:
            session.close()

    def get_customer(self, customer_id):
        """Retrieve a customer by ID."""
        session = Session()
        try:
            customer = session.get(Customer, customer_id)
            if not customer:
                raise ValueError("Customer not found")
            return customer
        finally:
            session.close()

    def generate_pdf(self, invoice_id):
        """Generate PDF for an invoice."""
        session = Session()
        try:
            invoice = session.get(Invoice, invoice_id)
            if not invoice:
                raise ValueError("Invoice not found")

            filename = f"invoice_{invoice.invoice_number}.pdf"
            pdf_generator = PDFGenerator(filename)
            pdf_generator.generate_invoice(invoice, invoice.customer)
            return filename
        finally:
            session.close()
