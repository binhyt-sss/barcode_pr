from typing import Optional
from pydantic import BaseModel


class FreeBARCODEParams(BaseModel):
    Barcode_Text_1: str
    Barcode_Text_2: Optional[str] = ""
    Barcode_Text_3: Optional[str] = ""   
    Printer_Name: Optional[str] = None

class FreeBARCODEDoubleTextParams(BaseModel):
    """Model cho API in 3 QR code với 2 text dọc bên trái mỗi QR
    Layout: [Barcode_Text_X][SideText2_X][QR_Code]
    """
    Barcode_Text_1: str
    Itemcode_1: str  
    Barcode_Text_2: Optional[str] = ""
    Itemcode_2: Optional[str] = ""
    Barcode_Text_3: Optional[str] = ""
    Itemcode_3: Optional[str] = ""
    Printer_Name: Optional[str] = None

