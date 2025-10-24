"""
Printer Service
Xử lý in ấn qua máy in nhiệt
"""
import os
import shutil
import subprocess


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
            # Try to find Foxit in PATH first, then common install locations
            foxit_exe = shutil.which("FoxitPDFReader.exe")
            common_paths = [
                r"C:\Program Files\Foxit Software\Foxit PDF Reader\FoxitPDFReader.exe",
                r"C:\Program Files (x86)\Foxit Software\Foxit PDF Reader\FoxitPDFReader.exe",
            ]
            if not foxit_exe:
                for p in common_paths:
                    if os.path.exists(p):
                        foxit_exe = p
                        break

            if not foxit_exe:
                print("Error: FoxitPDFReader.exe not found. Please install Foxit Reader or add it to PATH.")
                return False

            # Launch Foxit to print to the specified printer. Use subprocess so we pass the full path.
            try:
                # /t <PDF> <printername> prints the file to the named printer (Foxit CLI)
                subprocess.Popen([foxit_exe, '/t', pdf_path, printer_name], shell=False)
                return True
            except Exception as e:
                print(f"Printing failed: {e}")
                return False
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
