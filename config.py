from pathlib import Path

# Base directory of the project
BASE_DIR = Path(__file__).resolve().parent

# Database
DATABASE_URL = "sqlite:///invoice_system.db"

# PDF Configuration
PDF_OUTPUT_DIR = BASE_DIR / "pdfs"
if not PDF_OUTPUT_DIR.exists():
    PDF_OUTPUT_DIR.mkdir(parents=True)

# Application settings
INVOICE_DUE_DAYS = 30
COMPANY_NAME = "Your Company Name"
COMPANY_ADDRESS = "Your Company Address"
COMPANY_PHONE = "Your Company Phone"
COMPANY_EMAIL = "your@email.com"
COMPANY_WEBSITE = "www.yourcompany.com"

# Logging Configuration
LOG_DIR = BASE_DIR / "logs"
if not LOG_DIR.exists():
    LOG_DIR.mkdir(parents=True)

LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "standard": {"format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s"},
    },
    "handlers": {
        "file": {
            "class": "logging.FileHandler",
            "filename": LOG_DIR / "invoice_generator.log",
            "formatter": "standard",
        },
        "console": {"class": "logging.StreamHandler", "formatter": "standard"},
    },
    "loggers": {
        "": {  # root logger
            "handlers": ["console", "file"],
            "level": "INFO",
            "propagate": True,
        }
    },
}

# Email Configuration (if needed)
EMAIL_HOST = "smtp.yourserver.com"
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = "your@email.com"
EMAIL_HOST_PASSWORD = "your-password"
