"""
API Routes
Định nghĩa các endpoints cho Free BARCODE API
"""
from fastapi import APIRouter, HTTPException, Request
import logging
import time
import random
import uuid
from pathlib import Path

from ..models import FreeBARCODEParams, FreeBARCODEDoubleTextParams
from ..services import QRCodeService, PrinterService
from ..utils import ImageProcessor, PDFProcessor
from ..config.settings import (
    STORAGE_DIR, 
    QR_SIZE, 
    QR_SIZE_LARGE,
    QR_POSITIONS
)

# Create router
router = APIRouter()

# Initialize services
qr_service = QRCodeService()
printer_service = PrinterService()
image_processor = ImageProcessor()
pdf_processor = PDFProcessor()


def generate_unique_id() -> str:
    """Tạo unique ID cho mỗi request"""
    timestamp = time.strftime("%Y%m%d%H%M%S")
    random_num = str(random.randint(10000000, 99999999))
    unique_id = str(uuid.uuid4())
    return f"{timestamp}{random_num}_{unique_id}"



async def process_barcode(
    barcode_texts: list,
    printer_name: str
) -> dict:
    """
    Xử lý tạo 3 QR code và in
    
    Args:
        barcode_texts: List 3 text cho 3 QR code
        printer_name: Tên máy in
        
    Returns:
        dict: Kết quả xử lý
    """
    try:
        # Generate unique ID
        rand_id = generate_unique_id()
        current_pdf = STORAGE_DIR / "Thermal_Paper_35_22.pdf"
        
        # Process 3 QR codes
        for idx, (text, position) in enumerate(zip(barcode_texts, QR_POSITIONS), 1):
            
            # Create QR code image path
            qr_image_path = STORAGE_DIR / f"{rand_id}_{idx}.png"
            
            # 1. Create QR code
            qr_service.create_qr_image(text, str(qr_image_path))
            
            # 2. Resize QR code
            image_processor.resize_image(str(qr_image_path), QR_SIZE)
            
            # 3. Add vertical text
            qr_service.add_vertical_text_to_qr(str(qr_image_path), text)
            
            # 4. Stamp to PDF
            output_pdf = pdf_processor.stamp_image_to_pdf(
                str(qr_image_path),
                position,
                rand_id,
                str(current_pdf)
            )
            
            # Update current PDF for next iteration
            current_pdf = Path(output_pdf)
        
        # Rename final PDF
        final_pdf_name = f"Thermal_Paper_35_22_{rand_id}_final.pdf"
        final_pdf_path = STORAGE_DIR / final_pdf_name
        
        # Find the last stamped PDF (with 3 rand_ids)
        import os
        for file in STORAGE_DIR.glob(f"*{rand_id}*{rand_id}*{rand_id}.pdf"):
            os.rename(str(file), str(final_pdf_path))
            break
        
        # Print the PDF
        if printer_name:
            printer_service.print_pdf(str(final_pdf_path), printer_name)
        
        return {"Result": "OK", "File": final_pdf_name, "RequestID": rand_id}
        
    except Exception as e:
        logging.error(f"Error in process_barcode: {str(e)}")
        return {"Result": "ERROR", "Message": str(e)}


@router.post("/freeBARCODEReq")
async def create_barcode(request: Request, params: FreeBARCODEParams):
    """
    Endpoint tạo và in 3 QR code
    
    Request Body:
        - Barcode_Text_1: Text cho QR code thứ 1
        - Barcode_Text_2: Text cho QR code thứ 2 (optional)
        - Barcode_Text_3: Text cho QR code thứ 3 (optional)
        - Printer_Name: Tên máy in (optional)
    
    Returns:
        JSON response với kết quả xử lý
    """
    
    # Prepare barcode texts
    barcode_texts = [
        params.Barcode_Text_1,
        params.Barcode_Text_2 or "",
        params.Barcode_Text_3 or ""
    ]
    
    # Process barcodes
    result = await process_barcode(
        barcode_texts=barcode_texts,
        printer_name=params.Printer_Name
    )
    
    logging.info(f"Result: {result}")
    
    # Return response
    if result.get("Result") == "OK":
        return result
    else:
        raise HTTPException(status_code=500, detail=result.get("Message", "Try Again"))

async def process_double_text_barcode(
    barcode_data: list,  # [(qr_text, side_text1, side_text2), ...]
    printer_name: str
) -> dict:
    """
    Xử lý tạo 3 QR code với 2 text dọc bên trái mỗi QR
    
    Args:
        barcode_data: List tuple (qr_text, side_text1, side_text2) cho 3 QR
        printer_name: Tên máy in
        
    Returns:
        dict: Kết quả xử lý
    """
    try:
        # Generate unique ID
        rand_id = generate_unique_id()
        
        # Base PDF path
        current_pdf = STORAGE_DIR / "Thermal_Paper_35_22.pdf"
        
        # Process 3 QR codes
        for idx, ((qr_text, side_text1, side_text2), position) in enumerate(zip(barcode_data, QR_POSITIONS), 1):
            print(f"\n--- Processing QR Code {idx}/3 ---")
            print(f"QR Text: {qr_text}")
            print(f"Side Text 1: {side_text1}")
            print(f"Side Text 2: {side_text2}")
            print(f"Position: {position}")
            
            # Create QR code image path
            qr_image_path = STORAGE_DIR / f"{rand_id}_{idx}.png"
            
            # 1. Create QR code with double vertical texts
            qr_service.create_qr_with_double_vertical_texts(qr_text, side_text1, side_text2, str(qr_image_path))
            
            # 2. Resize QR code (SỬ DỤNG KÍCH THƯỚC LỚN)
            image_processor.resize_image(str(qr_image_path), QR_SIZE_LARGE)
            
            # 3. Stamp to PDF
            output_pdf = pdf_processor.stamp_image_to_pdf(
                str(qr_image_path),
                position,
                rand_id,
                str(current_pdf)
            )
            
            # Update current PDF for next iteration
            current_pdf = Path(output_pdf)
        
        # Rename final PDF
        final_pdf_name = f"Triple_Barcode_DoubleText_{rand_id}_final.pdf"
        final_pdf_path = STORAGE_DIR / final_pdf_name
        
        # Find the last stamped PDF (with 3 rand_ids)
        import os
        for file in STORAGE_DIR.glob(f"*{rand_id}*{rand_id}*{rand_id}.pdf"):
            os.rename(str(file), str(final_pdf_path))
            print(f"\n✓ Final PDF created: {final_pdf_name}")
            break
        
        # Print the PDF
        if printer_name:
            printer_service.print_pdf(str(final_pdf_path), printer_name)
        
        return {"Result": "OK", "File": final_pdf_name, "RequestID": rand_id}
        
    except Exception as e:
        logging.error(f"Error in process_double_text_barcode: {str(e)}")
        return {"Result": "ERROR", "Message": str(e)}


@router.post("/freeBARCODEDoubleTextReq")
async def create_barcode_with_double_texts(request: Request, params: FreeBARCODEDoubleTextParams):
    """
    Endpoint tạo và in 3 QR code với 2 text dọc bên trái mỗi QR
    
    Request Body:
        - Barcode_Text_1: Text cho QR code thứ 1 (cũng là text dọc đầu tiên)
        - SideText2_1: Text dọc thứ hai cho QR 1
        - Barcode_Text_2: Text cho QR code thứ 2 (cũng là text dọc đầu tiên) (optional)
        - SideText2_2: Text dọc thứ hai cho QR 2 (optional)
        - Barcode_Text_3: Text cho QR code thứ 3 (cũng là text dọc đầu tiên) (optional)
        - SideText2_3: Text dọc thứ hai cho QR 3 (optional)
        - Printer_Name: Tên máy in (optional)
    
    Layout mỗi QR: [Barcode_Text_X][SideText2_X][QR_Code]
    
    Returns:
        JSON response với kết quả xử lý
    """
    # Logging request info
    logging.info(f"Request URL: {request.url}")
    logging.info(f"Client: {request.client}")
    logging.info(f"User-Agent: {request.headers.get('User-Agent')}")
    logging.info(f"Params: {params}")
    
    # Prepare barcode data với 2 text dọc
    # Layout mong muốn: [Barcode_Text][SideText][QR]
    barcode_data = [
        (params.Barcode_Text_1, params.Barcode_Text_1, params.SideText2_1),  # (qr_content, text_xa_QR, text_gần_QR)
        (params.Barcode_Text_2 or "", params.Barcode_Text_2 or "", params.SideText2_2 or ""),
        (params.Barcode_Text_3 or "", params.Barcode_Text_3 or "", params.SideText2_3 or "")
    ]
    
    # Process barcodes
    result = await process_double_text_barcode(
        barcode_data=barcode_data,
        printer_name=params.Printer_Name
    )
    
    logging.info(f"Result: {result}")
    
    # Return response
    if result.get("Result") == "OK":
        return result
    else:
        raise HTTPException(status_code=500, detail=result.get("Message", "Try Again"))


@router.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "service": "Free BARCODE API",
        "version": "1.0.0"
    }
