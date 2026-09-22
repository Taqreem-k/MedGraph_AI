import base64
import fitz  # PyMuPDF
from io import BytesIO
from typing import List, Dict

def encode_image_to_base64(image_bytes: bytes) -> str:
    return base64.b64encode(image_bytes).decode('utf-8')

def convert_pdf_to_base64_images(pdf_bytes: bytes, dpi: int = 150) -> List[Dict[str, str]]:
    base64_pages = []
    
    # Open the PDF directly from the byte stream
    doc = fitz.open(stream=pdf_bytes, filetype="pdf")
    
    for page_num in range(len(doc)):
        page = doc.load_page(page_num)
        
        # Render the PDF page to an image pixmap
        pix = page.get_pixmap(dpi=dpi)
        
        # Convert pixmap to raw image bytes, then encode to base64
        img_bytes = pix.tobytes("jpeg")
        b64_string = encode_image_to_base64(img_bytes)
        
        base64_pages.append({
            "page": page_num + 1,
            "image_data": b64_string
        })
        
    doc.close()
    return base64_pages

def process_medical_file(file_name: str, file_bytes: bytes, mime_type: str) -> List[Dict[str, str]]:
    if "pdf" in mime_type.lower():
        return convert_pdf_to_base64_images(file_bytes)
    elif mime_type.lower() in ["image/jpeg", "image/png", "image/jpg"]:
        # Wrap single images in the same structure as PDF output for consistency
        b64_string = encode_image_to_base64(file_bytes)
        return [{"page": 1, "image_data": b64_string}]
    else:
        raise ValueError(f"Unsupported file type: {mime_type}")