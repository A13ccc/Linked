import pytesseract

screenshot_path = "screenshot.png"

def extract_text(image_path):
    # Preprocess the image
    preprocessed_img = image_path
    
    # Perform OCR with no whitelist
    ocr_result = pytesseract.image_to_string(preprocessed_img, config='--psm 4')
    return ocr_result

print(extract_text(screenshot_path))