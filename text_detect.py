import pytesseract

def to_text(image):
    config = ("-l eng --oem 1 --psm 7")
    text = pytesseract.image_to_string(image, config=config)
    return text
