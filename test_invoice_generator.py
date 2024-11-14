import unittest
from database import Base, engine, Customer, Invoice, InvoiceItem, Session, clear_database
from invoice_generator import InvoiceGenerator

class TestInvoiceGenerator(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        Base.metadata.create_all(engine)

    @classmethod
    def tearDownClass(cls):
        Base.metadata.drop_all(engine)

    def setUp(self):
        clear_database()
        self.generator = InvoiceGenerator()
        self.session = Session()

    def tearDown(self):
        self.session.close()
        Session.remove()

    def test_create_customer(self):
        customer_id = self.generator.create_customer(
            "Test Customer",
            "test@example.com",
            "123 Test St",
            "555-555-5555"
        )
        
        customer = self.session.get(Customer, customer_id)
        self.assertEqual(customer.name, "Test Customer")
        self.assertEqual(customer.email, "test@example.com")

    def test_create_customer_invalid(self):
        with self.assertRaises(ValueError):
            self.generator.create_customer(
                "",
                "test@example.com",
                "123 Test St",
                "555-555-5555"
            )

    def test_create_invoice(self):
        customer_id = self.generator.create_customer(
            "Test Customer",
            "test@example.com",
            "123 Test St",
            "555-555-5555"
        )
        
        items = [
            {
                'description': "Test Item",
                'quantity': 2,
                'unit_price': 10.00
            }
        ]
        
        invoice_id = self.generator.create_invoice(customer_id, items)
        
        invoice = self.session.get(Invoice, invoice_id)
        self.assertEqual(invoice.customer_id, customer_id)
        self.assertEqual(invoice.total_amount, 20.00)
        self.assertEqual(len(invoice.items), 1)

    def test_invoice_calculations(self):
        customer_id = self.generator.create_customer(
            "Test Customer",
            "test@example.com",
            "123 Test St",
            "555-555-5555"
        )
        
        items = [
            {
                'description': "Item 1",
                'quantity': 2,
                'unit_price': 10.00
            },
            {
                'description': "Item 2",
                'quantity': 1,
                'unit_price': 20.00
            }
        ]
        
        invoice_id = self.generator.create_invoice(customer_id, items)
        invoice = self.session.get(Invoice, invoice_id)
        self.assertEqual(invoice.total_amount, 40.00)

    def test_invoice_number_uniqueness(self):
        customer_id = self.generator.create_customer(
            "Test Customer",
            "test@example.com",
            "123 Test St",
            "555-555-5555"
        )
        
        items = [{'description': "Test Item", 'quantity': 1, 'unit_price': 10.00}]
        
        invoice1_id = self.generator.create_invoice(customer_id, items)
        invoice2_id = self.generator.create_invoice(customer_id, items)
        
        invoice1 = self.session.get(Invoice, invoice1_id)
        invoice2 = self.session.get(Invoice, invoice2_id)
        self.assertNotEqual(invoice1.invoice_number, invoice2.invoice_number)

    def test_customer_invoice_relationship(self):
        customer_id = self.generator.create_customer(
            "Test Customer",
            "test@example.com",
            "123 Test St",
            "555-555-5555"
        )
        
        items = [{'description': "Test Item", 'quantity': 1, 'unit_price': 10.00}]
        invoice_id = self.generator.create_invoice(customer_id, items)
        
        customer = self.session.get(Customer, customer_id)
        self.assertEqual(len(customer.invoices), 1)
        self.assertEqual(customer.invoices[0].id, invoice_id)

    def test_invoice_items_relationship(self):
        customer_id = self.generator.create_customer(
            "Test Customer",
            "test@example.com",
            "123 Test St",
            "555-555-5555"
        )
        
        items = [
            {'description': "Item 1", 'quantity': 2, 'unit_price': 10.00},
            {'description': "Item 2", 'quantity': 1, 'unit_price': 20.00}
        ]
        
        invoice_id = self.generator.create_invoice(customer_id, items)
        invoice = self.session.get(Invoice, invoice_id)
        self.assertEqual(len(invoice.items), 2)
        self.assertEqual(invoice.items[0].total, 20.00)
        self.assertEqual(invoice.items[1].total, 20.00)

    def test_generate_pdf(self):
        customer_id = self.generator.create_customer(
            "Test Customer",
            "test@example.com",
            "123 Test St",
            "555-555-5555"
        )
        
        items = [
            {
                'description': "Test Item",
                'quantity': 2,
                'unit_price': 10.00
            }
        ]
        
        invoice_id = self.generator.create_invoice(customer_id, items)
        filename = self.generator.generate_pdf(invoice_id)
        self.assertTrue(filename.endswith('.pdf'))

if __name__ == '__main__':
    unittest.main()
