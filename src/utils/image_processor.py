"""
Image Processor Utility
Xử lý resize và manipulate ảnh
"""
import os


class ImageProcessor:
    """Utility class để xử lý ảnh"""
    
    @staticmethod
    def resize_image(image_path: str, size: int) -> None:
        """
        Resize ảnh sử dụng ImageMagick
        
        Args:
            image_path: Đường dẫn file ảnh
            size: Kích thước mới (width x height)
        """
        cmdline = f'magick "{image_path}" -resize {size}x{size} "{image_path}"'
        print(f"🔧 Resizing image: {cmdline}")
        result = os.popen(cmdline).read().rstrip("\n")
        if result:
            print(f"   Result: {result}")
    
    @staticmethod
    def convert_format(input_path: str, output_path: str, format: str = "PNG") -> None:
        """
        Convert ảnh sang format khác
        
        Args:
            input_path: Đường dẫn file input
            output_path: Đường dẫn file output
            format: Format đích (PNG, JPG, etc.)
        """
        cmdline = f'magick "{input_path}" "{output_path}"'
        print(f"🔧 Converting image: {cmdline}")
        os.popen(cmdline).read()
