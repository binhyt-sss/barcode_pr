"""
QR Code Service
Xử lý tạo QR code và thêm text
"""
from PIL import Image, ImageDraw, ImageFont
import qrcode
from pathlib import Path
from ..config.settings import FONT_PATH, FONT_PATH_BOLD, FONT_SIZE, FONT_SIZE_BARCODE, FONT_SIZE_ITEMCODE, MAX_TEXT_LENGTH


class QRCodeService:
    """Service để tạo và xử lý QR code"""

    def __init__(self):
        """Initialize QR Code Service với font"""
        self.font = ImageFont.truetype(str(FONT_PATH), FONT_SIZE)
        self.font_bold = ImageFont.truetype(str(FONT_PATH_BOLD), FONT_SIZE_BARCODE)
        self.font_itemcode = ImageFont.truetype(str(FONT_PATH), FONT_SIZE_ITEMCODE)
    
    def create_qr_image(self, text: str, output_path: str) -> None:
        """
        Tạo QR code cơ bản từ text
        
        Args:
            text: Nội dung QR code
            output_path: Đường dẫn lưu file ảnh QR
        """
        barcode_image = qrcode.make(text)
        barcode_image.save(output_path)
        print(f"✓ Created QR code: {output_path}")
    
    def add_vertical_text_to_qr(self, qr_path: str, text: str) -> None:
        """
        Thêm text nằm dọc bên trái QR code (LAYOUT GỐC - giữ nguyên)
        
        Args:
            qr_path: Đường dẫn file QR code
            text: Text cần thêm (tối đa MAX_TEXT_LENGTH ký tự)
        """
        # Giới hạn độ dài text
        text = text[:MAX_TEXT_LENGTH]
        
        # Load QR code
        qr_img = Image.open(qr_path).convert("RGBA")
        w, h = qr_img.size
        
        # Tạo ảnh chữ nằm ngang để xoay (GIỮ NGUYÊN KÍCH THƯỚC CŨ)
        text_img = Image.new("RGBA", (h, 20), "white")  # Giữ nguyên 20
        draw = ImageDraw.Draw(text_img)
        
        # Căn giữa text
        text_width = draw.textbbox((0, 0), text, font=self.font)[2]
        draw.text(((h - text_width) // 2, 0), text, fill="black", font=self.font)  # Giữ nguyên offset 0
        
        # Xoay ảnh chữ 90 độ để nằm dọc
        text_img = text_img.rotate(90, expand=True)
        
        # Tạo canvas mới để ghép (GIỮ NGUYÊN LAYOUT CŨ)
        new_w = w + text_img.width + 6  # Giữ nguyên khoảng cách 6px
        new_h = max(h, text_img.height)
        canvas = Image.new("RGBA", (new_w, new_h), "white")
        
        # Dán text bên trái và QR bên phải (LAYOUT CŨ)
        canvas.paste(text_img, (0, (new_h - text_img.height) // 2))
        canvas.paste(qr_img, (text_img.width + 5, (new_h - h) // 2))  # Giữ nguyên 5px
        
        # Ghi đè lại file QR gốc
        canvas.save(qr_path)
        print(f"✓ Added vertical text to QR: {qr_path}")

    def add_vertical_text_to_qr_large(self, qr_path: str, text: str) -> None:
        """
        Thêm text nằm dọc bên trái QR code (LAYOUT MỚI - QR to hơn, FONT THƯỜNG)

        Args:
            qr_path: Đường dẫn file QR code
            text: Text cần thêm (tối đa MAX_TEXT_LENGTH ký tự)
        """
        # Giới hạn độ dài text
        text = text[:MAX_TEXT_LENGTH]

        # Load QR code
        qr_img = Image.open(qr_path).convert("RGBA")
        w, h = qr_img.size

        # Tạo ảnh chữ nằm ngang để xoay - tăng chiều cao để text to hơn
        text_height = 30  # Text to hơn
        text_img = Image.new("RGBA", (h, text_height), "white")
        draw = ImageDraw.Draw(text_img)

        # Căn giữa text - SỬ DỤNG FONT ITEMCODE (font thường)
        text_width = draw.textbbox((0, 0), text, font=self.font_itemcode)[2]
        draw.text(((h - text_width) // 2, 5), text, fill="black", font=self.font_itemcode)  # Font thường

        # Xoay ảnh chữ 90 độ để nằm dọc
        text_img = text_img.rotate(90, expand=True)

        # Tạo canvas mới để ghép - QR luôn ở bên phải
        padding = 8  # Khoảng cách rộng hơn
        new_w = text_img.width + w + padding
        new_h = max(h, text_img.height)
        canvas = Image.new("RGBA", (new_w, new_h), "white")

        # Dán text bên trái và QR bên phải
        canvas.paste(text_img, (0, (new_h - text_img.height) // 2))
        canvas.paste(qr_img, (text_img.width + padding, (new_h - h) // 2))

        # Ghi đè lại file QR gốc
        canvas.save(qr_path)
        print(f"✓ Added vertical text to QR (Large, Normal Font): {qr_path}")

    def add_vertical_sub_text_to_qr_large(self, qr_path: str, sub_text: str) -> None:
        """
        Thêm text dọc thứ 2 bên cạnh text dọc đầu tiên (LAYOUT LỚN - QR to hơn)
        Text này sử dụng font đậm (Barcode_Text)

        Args:
            qr_path: Đường dẫn file QR code (đã có text dọc đầu tiên)
            sub_text: Text dọc thứ 2 cần thêm (tối đa MAX_TEXT_LENGTH ký tự)
        """
        # Giới hạn độ dài text
        sub_text = sub_text[:MAX_TEXT_LENGTH]

        # Load ảnh hiện tại (đã có text + QR)
        current_img = Image.open(qr_path).convert("RGBA")
        current_w, current_h = current_img.size

        # Tạo ảnh cho sub text dọc - tăng chiều cao để nhất quán
        text_height = 30  # Giống với text chính
        sub_text_img = Image.new("RGBA", (current_h, text_height), "white")
        draw = ImageDraw.Draw(sub_text_img)

        # Căn giữa sub text - SỬ DỤNG FONT BOLD (font đậm cho Barcode_Text)
        sub_text_width = draw.textbbox((0, 0), sub_text, font=self.font_bold)[2]
        draw.text(((current_h - sub_text_width) // 2, 5), sub_text, fill="black", font=self.font_bold)  # Font đậm

        # Xoay sub text 90 độ để nằm dọc
        sub_text_img = sub_text_img.rotate(90, expand=True)

        # Tạo canvas mới để ghép thêm sub text
        padding = 8  # Khoảng cách rộng hơn
        new_w = sub_text_img.width + current_w + padding
        new_h = max(current_h, sub_text_img.height)
        canvas = Image.new("RGBA", (new_w, new_h), "white")

        # Dán sub text bên trái nhất, rồi dán ảnh hiện tại (text + QR) bên phải
        canvas.paste(sub_text_img, (0, (new_h - sub_text_img.height) // 2))
        canvas.paste(current_img, (sub_text_img.width + padding, (new_h - current_h) // 2))

        # Ghi đè lại file QR gốc
        canvas.save(qr_path)
        print(f"✓ Added vertical sub-text to QR (Large, BOLD Font): {qr_path}")
    

    
    def create_qr_with_text(self, text: str, output_path: str) -> None:
        """
        Tạo QR code đã có text dọc bên trái (all-in-one)
        
        Args:
            text: Nội dung QR code và text hiển thị
            output_path: Đường dẫn lưu file
        """
        self.create_qr_image(text, output_path)
        self.add_vertical_text_to_qr(output_path, text)

    def create_qr_with_double_vertical_texts(self, qr_text: str, barcode_text: str, itemcode_text: str, output_path: str) -> None:
        """
        Tạo QR code với 2 text dọc bên trái (LAYOUT LỚN - QR to hơn)
        Layout: [Barcode_Text (FONT ĐẬM)][Itemcode (font thường)][QR_LỚN]

        Args:
            qr_text: Nội dung QR code
            barcode_text: Text Barcode (FONT ĐẬM, xa QR - bên trái cùng)
            itemcode_text: Text Itemcode (font thường, gần QR - ở giữa)
            output_path: Đường dẫn lưu file
        """
        # Tạo QR code cơ bản
        self.create_qr_image(qr_text, output_path)

        # Thêm Itemcode trước (gần QR, font thường)
        self.add_vertical_text_to_qr_large(output_path, itemcode_text)

        # Thêm Barcode_Text sau (xa QR - sẽ được add bên trái, FONT ĐẬM)
        if barcode_text:  # Chỉ thêm nếu có text
            self.add_vertical_sub_text_to_qr_large(output_path, barcode_text)
