from sqlalchemy import create_engine, Column, Integer, String, Float, Date, ForeignKey, event
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, scoped_session, sessionmaker
from datetime import datetime
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Create the declarative base
Base = declarative_base()

# Configure the database engine with better connection handling
engine = create_engine(
    'sqlite:///invoice_system.db',
    echo=False,  # Set to True for debugging SQL output
    pool_pre_ping=True,  # Enable automatic reconnection
    pool_recycle=3600,  # Recycle connections after 1 hour
    connect_args={'check_same_thread': False}  # Required for SQLite
)

# Create thread-safe session factory
Session = scoped_session(sessionmaker(
    bind=engine,
    autocommit=False,
    autoflush=False
))

# SQLite Foreign Key Support
@event.listens_for(engine, 'connect')
def set_sqlite_pragma(dbapi_connection, connection_record):
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()

class Customer(Base):
    __tablename__ = 'customers'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False, index=True)
    email = Column(String(255), unique=True)
    address = Column(String(255))
    phone = Column(String(20))
    created_at = Column(Date, default=datetime.now().date(), nullable=False)
    invoices = relationship("Invoice", back_populates="customer", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Customer(id={self.id}, name='{self.name}', email='{self.email}')>"

class Invoice(Base):
    __tablename__ = 'invoices'
    
    id = Column(Integer, primary_key=True)
    invoice_number = Column(String(50), unique=True, nullable=False, index=True)
    date = Column(Date, default=datetime.now().date(), nullable=False)
    due_date = Column(Date)
    customer_id = Column(Integer, ForeignKey('customers.id', ondelete='CASCADE'), nullable=False)
    total_amount = Column(Float, default=0.0, nullable=False)
    status = Column(String(20), default='draft', nullable=False)  # draft, sent, paid, cancelled
    notes = Column(String(500))
    
    customer = relationship("Customer", back_populates="invoices")
    items = relationship("InvoiceItem", back_populates="invoice", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Invoice(id={self.id}, number='{self.invoice_number}', total={self.total_amount})>"

    def calculate_total(self):
        """Calculate total amount from items."""
        self.total_amount = sum(item.total for item in self.items)

class InvoiceItem(Base):
    __tablename__ = 'invoice_items'
    
    id = Column(Integer, primary_key=True)
    invoice_id = Column(Integer, ForeignKey('invoices.id', ondelete='CASCADE'), nullable=False)
    description = Column(String(255), nullable=False)
    quantity = Column(Integer, nullable=False)
    unit_price = Column(Float, nullable=False)
    total = Column(Float, nullable=False)
    
    invoice = relationship("Invoice", back_populates="items")

    def __repr__(self):
        return f"<InvoiceItem(id={self.id}, description='{self.description}', total={self.total})>"

    def calculate_total(self):
        """Calculate total from quantity and unit price."""
        self.total = self.quantity * self.unit_price

def get_session():
    """Get a new session."""
    return Session()

def init_db():
    """Initialize the database by creating all tables."""
    try:
        Base.metadata.create_all(engine)
        logger.info("Database initialized successfully")
    except Exception as e:
        logger.error(f"Error initializing database: {str(e)}")
        raise

def clear_database():
    """Clear all data from the database."""
    try:
        Base.metadata.drop_all(engine)
        Base.metadata.create_all(engine)
        logger.info("Database cleared successfully")
    except Exception as e:
        logger.error(f"Error clearing database: {str(e)}")
        raise

def cleanup_db():
    """Clean up database resources."""
    try:
        Session.remove()
        engine.dispose()
        logger.info("Database resources cleaned up successfully")
    except Exception as e:
        logger.error(f"Error cleaning up database resources: {str(e)}")
        raise

if __name__ == '__main__':
    init_db()
