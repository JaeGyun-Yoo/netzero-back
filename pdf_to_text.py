import PyPDF2
import pytesseract
from pdf2image import convert_from_path
from PIL import ImageEnhance
import re
import os
import logging
from fastapi import HTTPException

def extract_text_with_pypdf2(pdf_path): #pypdf2를 이용해 텍스트 추출
    try:
        with open(pdf_path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            text = ""
            for page in reader.pages:
                text += page.extract_text() or ""
        return text
    except Exception as e:
        return f"Error in PyPDF2 processing: {e}"

def preprocess_image(image): #OCR 정확도를 올리기 위해 이미지 전처리과정, 정확도 향상이 미비한 것 같아서 제거해도 상관없을듯?
    enhancer = ImageEnhance.Contrast(image)
    image = enhancer.enhance(2)
    image = image.convert('L')
    image = image.point(lambda x: 0 if x < 128 else 255, '1')
    return image

def extract_text_with_ocr(pdf_path): #OCR(광학문자인식)로 텍스트 추출하기
    try:
        images = convert_from_path(pdf_path, dpi=300)
        text = ""
        for image in images:
            processed_image = preprocess_image(image)
            text += pytesseract.image_to_string(processed_image, lang='kor+eng', config='--psm 6')
        return text
    except Exception as e:
        return f"Error in OCR processing: {e}"

def is_mostly_standard_characters(text, threshold=0.8): #threshold로 임계값 설정, 한글 영어 등이 80%이상이면 True
    standard_chars = re.findall(r"[가-힣a-zA-Z0-9\s!\"#$%&'()*+,-./:;<=>?@\[\\\]^_`{|}~]", text)
    return (len(standard_chars) / len(text)) >= threshold


def pdf_to_text(pdf_name): #pdf를 text로 변환
    print(1)
    pdf_path = find_file(pdf_name)
    if pdf_path is None:
        return "File not found", None
    print(2)
    extracted_text = extract_text_with_pypdf2(pdf_path)
    print(3)
    if not is_mostly_standard_characters(extracted_text):
        print(4)
        extracted_text = extract_text_with_ocr(pdf_path)
        print(5)
        extraction_method = "OCR"
    else:
        extraction_method = "PyPDF2"
    print(6)
    return extracted_text, extraction_method



def find_file(filename):
    directory = 'uploads'
    for root, dirs, files in os.walk(directory):
        if filename in files:
            return os.path.join(root, filename)
    return None

def extract_text(filename: str):
    file_location = find_file(filename)
    if file_location is None:
        return "File not found"
    else:
        extracted_text, extraction_method = pdf_to_text(file_location)
        return {"extracted_text": extracted_text, "extraction_method": extraction_method}
