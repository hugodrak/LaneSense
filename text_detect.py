import pytesseract

def to_text(image):
    config = ("-l eng --oem 1 --psm 7")
    data = pytesseract.image_to_data(image, config=config)
    parsed = data.split('\t')
    conf, text = parsed[-2:]
    return [int(conf), str(text.rstrip(")"))]
