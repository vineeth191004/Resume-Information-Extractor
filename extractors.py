from PyPDF2 import PdfReader
from docx import Document
from PIL import Image
import pytesseract

def extract_text_from_pdf(file):
    reader = PdfReader(file)
    return " ".join([page.extract_text() or "" for page in reader.pages])

def extract_text_from_docx(file):
    doc = Document(file)
    return " ".join([p.text for p in doc.paragraphs])

def extract_text_from_image(file):
    image = Image.open(file)
    return pytesseract.image_to_string(image)
