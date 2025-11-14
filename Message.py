import pdfplumber
import pytesseract
from pdf2image import convert_from_path
from PIL import Image

def extract_text_from_digital_pdf(pdf_path):
    print(f"--- Starting Digital Extraction (pdfplumber) for: {pdf_path} ---")
    all_text = ""
    
    try:
        with pdfplumber.open(pdf_path) as pdf:
            for i, page in enumerate(pdf.pages):
                text = page.extract_text()
                if text:
                    all_text += f"--- Text from Page {i+1} ---\n"
                    all_text += text
                    all_text += "\n\n"
        
        if not all_text:
            print("No text could be extracted. Is this a scanned (image-based) PDF?")
            
        return all_text

    except Exception as e:
        print(f"An error occurred with pdfplumber: {e}")
        return None

def extract_text_from_scanned_pdf(pdf_path):
    print(f"--- Starting Scanned/OCR Extraction (pytesseract) for: {pdf_path} ---")
    all_text = ""
    
    try:
        images = convert_from_path(pdf_path)
        
        for i, img in enumerate(images):
            text = pytesseract.image_to_string(img)
            
            if text:
                all_text += f"--- Text from Page {i+1} (OCR) ---\n"
                all_text += text
                all_text += "\n\n"
        
        if not all_text:
            print("No text was recognized by Tesseract.")
            
        return all_text

    except Exception as e:
        print(f"An error occurred with Tesseract/pdf2image: {e}")
        print("Please ensure Tesseract-OCR and Poppler are installed and in your system's PATH.")
        return None

if __name__ == "__main__":
    resume_file_path = "scan.pdf"

    digital_text = extract_text_from_digital_pdf(resume_file_path)
    
    if digital_text:
        print("--- DIGITAL EXTRACTION RESULTS ---")
        print(digital_text.encode(errors='replace').decode('cp1252'))

    if not digital_text:
        print("\nDigital extraction failed, trying OCR...")
        scanned_text = extract_text_from_scanned_pdf(resume_file_path)
        
        if scanned_text:
            print("--- SCANNED/OCR EXTRACTION RESULTS ---")
            print(scanned_text.encode(errors='replace').decode('cp1252'))
        else:
            print(f"Could not extract text from '{resume_file_path}' using either method.")