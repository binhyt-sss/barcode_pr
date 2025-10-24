"""
Configuration settings for Free BARCODE application
"""
import os
from pathlib import Path

# Base paths
BASE_DIR = Path(__file__).resolve().parent.parent.parent
STORAGE_DIR = BASE_DIR / "Storage"
FONT_DIR = BASE_DIR / "Font"
PDFSTAMP_JAR = BASE_DIR / "pdfstamp" / "pdfstamp.jar"

# Ensure directories exist
STORAGE_DIR.mkdir(exist_ok=True)
FONT_DIR.mkdir(exist_ok=True)

# Authentication
AUTH_USER = os.getenv("AUTH_USER", "imes")
AUTH_PASSWORD = os.getenv("AUTH_PASSWORD", "AHsguq6663ASgwfQw")

# Font settings
FONT_PATH = FONT_DIR / "arial.ttf"
FONT_PATH_BOLD = FONT_DIR / "arialbd.ttf"  # Font đậm cho Barcode_Text
FONT_SIZE = 22
FONT_SIZE_BARCODE = 28  # Font lớn hơn cho Barcode_Text
FONT_SIZE_ITEMCODE = 22  # Font thường cho Itemcode

# QR Code settings
QR_SIZE = 270  # Kích thước gốc cho API cũ
QR_SIZE_LARGE = 350  # Kích thước lớn cho API mới
QR_POSITIONS = [(22, 0), (124, 0), (226, 0)]
MAX_TEXT_LENGTH = 15

# PDF Template
PDF_TEMPLATE = "Thermal_Paper_35_22.pdf"

# Logging
LOG_FILE = BASE_DIR / "BARCODE.log"
LOG_FORMAT = '%(asctime)s %(levelname)s %(message)s'
LOG_DATE_FORMAT = '%d/%m/%y-%H:%M:%S'

# Server settings
HOST = "0.0.0.0"
PORT = 25000
WORKERS = 1
