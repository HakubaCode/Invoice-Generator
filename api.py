from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel, EmailStr, constr, confloat, conint
from typing import List, Optional
from datetime import date
from invoice_generator import InvoiceGenerator
from database import Session, Customer, Invoice
import uvicorn

app = FastAPI(title="Invoice Generator API", version="1.0.0")
generator = InvoiceGenerator()

class CustomerCreate(BaseModel):
    name: constr(min_length=1, max_length=100)
    email: EmailStr
    address: Optional[str]
    phone: Optional[str]

class InvoiceItemCreate(BaseModel):
    description: constr(min_length=1, max_length=255)
    quantity: conint(gt=0)
    unit_price: confloat(gt=0)

class InvoiceCreate(BaseModel):
    customer_id: int
    items: List[InvoiceItemCreate]

@app.post("/customers/", response_model=dict)
async def create_customer(customer: CustomerCreate):
    try:
        customer_id = generator.create_customer(
            customer.name,
            customer.email,
            customer.address,
            customer.phone
        )
        return {"id": customer_id, "message": "Customer created successfully"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/invoices/", response_model=dict)
async def create_invoice(invoice: InvoiceCreate):
    try:
        items = [dict(item) for item in invoice.items]
        invoice_id = generator.create_invoice(invoice.customer_id, items)
        return {"id": invoice_id, "message": "Invoice created successfully"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/customers/")
async def list_customers():
    session = Session()
    try:
        customers = session.query(Customer).all()
        return [{"id": c.id, "name": c.name, "email": c.email} for c in customers]
    finally:
        session.close()

@app.get("/invoices/")
async def list_invoices():
    session = Session()
    try:
        invoices = session.query(Invoice).all()
        return [{
            "id": i.id,
            "invoice_number": i.invoice_number,
            "customer_name": i.customer.name,
            "total_amount": i.total_amount,
            "date": i.date
        } for i in invoices]
    finally:
        session.close()

@app.get("/invoices/{invoice_id}/pdf")
async def generate_pdf(invoice_id: int):
    try:
        filename = generator.generate_pdf(invoice_id)
        return {"filename": filename, "message": "PDF generated successfully"}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
