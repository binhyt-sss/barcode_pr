"""
Printer Service
Xử lý in ấn qua máy in nhiệt
"""
import os


class PrinterService:
    """Service để in PDF qua máy in"""
    
    @staticmethod
    def print_pdf(pdf_path: str, printer_name: str) -> bool:
        """
        In PDF qua máy in nhiệt sử dụng FoxitPDFReader
        
        Args:
            pdf_path: Đường dẫn file PDF
            printer_name: Tên máy in
            
        Returns:
            bool: True nếu in thành công, False nếu không
        """
        # Chỉ in nếu là file PDF và máy in nhiệt
        if ".pdf" in pdf_path and "Thermal_Barcode" in printer_name:
            cmdline = f'FoxitPDFReader.exe /t "{pdf_path}" {printer_name}'
            # print(f"🖨️  Printing: {cmdline}")
            os.system(cmdline)
            return True
        else:
            print(f"Skip printing: Invalid file or printer")
            return False
    
    @staticmethod
    def check_printer_available(printer_name: str) -> bool:
        """
        Kiểm tra máy in có sẵn hay không
        """
        # TODO: Implement printer availability check
        return True
