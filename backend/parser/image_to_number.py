import cv2
import pytesseract
import numpy as np

# Added -c tessedit_char_whitelist=0123456789 to strictly force digit recognition
config = r'--oem 3 --psm 7 -c tessedit_char_whitelist=0123456789 outputbase digits'

def parse_image(img) -> int:
    pytesseract.pytesseract.tesseract_cmd = (
        "C:/Program Files/Tesseract-OCR/tesseract.exe"
    )

    # 1. Grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # 2. Upscale (4x)
    gray = cv2.resize(gray, None, fx=4, fy=4, interpolation=cv2.INTER_CUBIC)

    # 3. Adaptive/Otsu Thresholding (handles the blue background automatically)
    # We use THRESH_BINARY_INV if the text is darker than the background to make text white,
    # but Tesseract likes black text on a white background, so standard BINARY + OTSU is perfect.
    _, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    # If the threshold inverted the image (making the number white and bg black), flip it back:
    # Tesseract prefers black text on a white background.
    if np.mean(thresh[:10, :10]) < 127: 
        thresh = cv2.bitwise_not(thresh)

    # 4. Add Padding (Crucial for tight crops!)
    # Adds a 20-pixel solid white border around your upscaled image
    padded = cv2.copyMakeBorder(thresh, 20, 20, 20, 20, cv2.BORDER_CONSTANT, value=255)

    # 5. OCR & Clean String
    text = pytesseract.image_to_string(padded, config=config)
    cleaned_text = text.strip()

    # Safety check in case OCR fails completely to prevent program crash
    if not cleaned_text:
        #print("OCR Failed to detect a number.")
        return 0

    number = int(cleaned_text)
    #print(f"Detected Number: {number}")
    return number