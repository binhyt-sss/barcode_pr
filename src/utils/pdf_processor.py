"""
PDF Processor Utility
Xử lý stamp ảnh lên PDF
"""
import os
from pathlib import Path
from typing import Tuple
from ..config.settings import PDFSTAMP_JAR, STORAGE_DIR, PDF_TEMPLATE


class PDFProcessor:
    """Utility class để xử lý PDF"""
    
    @staticmethod
    def stamp_image_to_pdf(
        image_path: str, 
        position: Tuple[int, int], 
        rand_id: str, 
        base_pdf: str = None
    ) -> str:
        """
        Stamp ảnh lên PDF tại vị trí cụ thể sử dụng pdfstamp.jar
        
        Args:
            image_path: Đường dẫn file ảnh
            position: Tuple (x, y) vị trí stamp
            rand_id: Random ID cho output file
            base_pdf: PDF gốc (mặc định dùng template)
            
        Returns:
            str: Đường dẫn file PDF output
        """
        if base_pdf is None:
            base_pdf = STORAGE_DIR / PDF_TEMPLATE
        
        x, y = position
        cmdline = f'java -jar "{PDFSTAMP_JAR}" -i "{image_path}" -l "{x}","{y}" -e "{rand_id}" "{base_pdf}"'
        print(f"📄 Stamping PDF: {cmdline}")
        result = os.popen(cmdline).read().rstrip("\n")
        if result:
            print(f"   Result: {result}")
        
        # Return output path
        base_pdf_str = str(base_pdf)
        return base_pdf_str.replace('.pdf', f'_{rand_id}.pdf')
    
    @staticmethod
    def merge_pdfs(pdf_paths: list, output_path: str) -> None:
        """
        Merge nhiều PDF thành 1 file
        
        Args:
            pdf_paths: List đường dẫn các file PDF
            output_path: Đường dẫn file output
        """
        # TODO: Implement PDF merge if needed
        pass
