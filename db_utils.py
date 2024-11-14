from database import Session, Customer, Invoice, InvoiceItem
from sqlalchemy import text

def print_table_contents():
    session = Session()
    try:
        # Print Customers
        print("\n=== Customers ===")
        customers = session.query(Customer).all()
        for customer in customers:
            print(f"ID: {customer.id}, Name: {customer.name}, Email: {customer.email}")

        # Print Invoices
        print("\n=== Invoices ===")
        invoices = session.query(Invoice).all()
        for invoice in invoices:
            print(f"ID: {invoice.id}, Number: {invoice.invoice_number}, "
                  f"Customer: {invoice.customer.name}, Total: ${invoice.total_amount:.2f}")

            # Print Invoice Items
            print("  Items:")
            for item in invoice.items:
                print(f"    - {item.quantity}x {item.description} "
                      f"@ ${item.unit_price:.2f} = ${item.total:.2f}")

    finally:
        session.close()

def run_custom_query(query):
    session = Session()
    try:
        result = session.execute(text(query))
        for row in result:
            print(row)
    finally:
        session.close()

if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1:
        # If query provided as argument, run it
        query = " ".join(sys.argv[1:])
        print(f"Running query: {query}")
        run_custom_query(query)
    else:
        # Otherwise show all table contents
        print_table_contents()
