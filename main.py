from invoice_generator import InvoiceGenerator
from database import init_db, Session, Customer, Invoice
import logging
import sys

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def print_menu():
    print("\n=== Invoice Generator System ===")
    print("1. Add Customer")
    print("2. Create Invoice")
    print("3. Generate PDF for Invoice")
    print("4. List All Customers")
    print("5. List All Invoices")
    print("6. Exit")
    print("==============================")

def get_customer_input():
    print("\nEnter Customer Details:")
    name = input("Name: ")
    email = input("Email: ")
    address = input("Address: ")
    phone = input("Phone: ")
    return name, email, address, phone

def list_customers():
    session = Session()
    try:
        customers = session.query(Customer).all()
        if not customers:
            print("\nNo customers found in the database.")
            return False
        
        print("\nAvailable Customers:")
        print("ID  | Name                 | Email")
        print("-" * 50)
        for customer in customers:
            print(f"{customer.id:<3} | {customer.name[:20]:<20} | {customer.email}")
        return True
    finally:
        session.close()

def get_invoice_items():
    items = []
    while True:
        print("\nAdd Invoice Item:")
        description = input("Description (or press enter to finish): ")
        if not description:
            break
            
        try:
            quantity = int(input("Quantity: "))
            if quantity <= 0:
                print("Quantity must be greater than 0")
                continue
                
            unit_price = float(input("Unit Price: $"))
            if unit_price <= 0:
                print("Price must be greater than 0")
                continue
                
            items.append({
                'description': description,
                'quantity': quantity,
                'unit_price': unit_price
            })
            print(f"Item added: {quantity} x {description} at ${unit_price:.2f} each")
            
            add_more = input("\nAdd another item? (y/n): ").lower()
            if add_more != 'y':
                break
                
        except ValueError:
            print("Invalid input. Please enter numbers for quantity and price.")
            continue
            
    return items

def main():
    init_db()
    generator = InvoiceGenerator()

    while True:
        print_menu()
        choice = input("Enter your choice (1-6): ")

        try:
            if choice == '1':
                # Add Customer
                name, email, address, phone = get_customer_input()
                customer_id = generator.create_customer(name, email, address, phone)
                print(f"\nCustomer created successfully! ID: {customer_id}")

            elif choice == '2':
                # Create Invoice
                if not list_customers():
                    print("Please add a customer first.")
                    continue
                    
                try:
                    customer_id = int(input("\nEnter Customer ID from the list above: "))
                except ValueError:
                    print("Invalid input. Please enter a number.")
                    continue
                
                items = get_invoice_items()
                if not items:
                    print("\nNo items added. Invoice creation cancelled.")
                    continue
                    
                try:
                    invoice_id = generator.create_invoice(customer_id, items)
                    print(f"\nInvoice created successfully! ID: {invoice_id}")
                    print("You can now generate a PDF for this invoice using option 3.")
                except ValueError as e:
                    print(f"\nError: {str(e)}")

            elif choice == '3':
                # Generate PDF
                session = Session()
                invoices = session.query(Invoice).all()
                session.close()
                
                if not invoices:
                    print("\nNo invoices found. Create an invoice first.")
                    continue
                    
                print("\nAvailable Invoices:")
                print("ID  | Invoice Number    | Customer Name        | Total Amount")
                print("-" * 65)
                for invoice in invoices:
                    print(f"{invoice.id:<3} | {invoice.invoice_number:<16} | "
                          f"{invoice.customer.name[:18]:<18} | ${invoice.total_amount:,.2f}")
                
                try:
                    invoice_id = int(input("\nEnter Invoice ID from the list above: "))
                    filename = generator.generate_pdf(invoice_id)
                    print(f"\nPDF generated successfully: {filename}")
                except ValueError as e:
                    print(f"\nError: {str(e)}")

            elif choice == '4':
                # List Customers
                list_customers()

            elif choice == '5':
                # List Invoices
                session = Session()
                invoices = session.query(Invoice).all()
                if not invoices:
                    print("\nNo invoices found.")
                else:
                    print("\nInvoices:")
                    print("ID  | Invoice Number    | Customer Name        | Total Amount")
                    print("-" * 65)
                    for invoice in invoices:
                        print(f"{invoice.id:<3} | {invoice.invoice_number:<16} | "
                              f"{invoice.customer.name[:18]:<18} | ${invoice.total_amount:,.2f}")
                session.close()

            elif choice == '6':
                print("\nGoodbye!")
                break

            else:
                print("\nInvalid choice. Please try again.")

        except ValueError as e:
            print(f"\nError: {str(e)}")
        except Exception as e:
            print(f"\nAn error occurred: {str(e)}")
            logger.exception("An error occurred")

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\nProgram terminated by user.")
        sys.exit(0)
    except Exception as e:
        logger.exception("Fatal error occurred")
        print(f"\nA fatal error occurred: {str(e)}")
        sys.exit(1)
