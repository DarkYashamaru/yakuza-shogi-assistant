import cv2
import numpy as np

# 1. Load the image
image_path = "D:/Repositories/yakuza-shogi-assistant/backend/temp/cells/2_3 - Copy.png"
img = cv2.imread(image_path)
h_img, w_img, _ = img.shape

# 2. Convert to HSV
hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

# 3. Strict Red Filter (Higher Saturation & Value to ignore the background/border)
lower_red1 = np.array([0, 150, 150])    # Bumped from 100 to 150
upper_red1 = np.array([10, 255, 255])
lower_red2 = np.array([165, 150, 150])  # Narrowed Hue range slightly and bumped to 150
upper_red2 = np.array([180, 255, 255])

mask1 = cv2.inRange(hsv, lower_red1, upper_red1)
mask2 = cv2.inRange(hsv, lower_red2, upper_red2)
red_mask = mask1 + mask2

# 4. Find contours
contours, _ = cv2.findContours(red_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

valid_box = None

if contours:
    # Filter out contours that take up too much of the image (like the whole frame)
    img_area = h_img * w_img
    possible_s_contours = []
    
    for cnt in contours:
        x, y, w, h = cv2.boundingRect(cnt)
        area = w * h
        # The 'S' should be small (e.g., less than 20% of the entire image area)
        if area < (img_area * 0.20):
            possible_s_contours.append(cnt)
            
    if possible_s_contours:
        # Grab the largest one among the valid small candidates
        largest_contour = max(possible_s_contours, key=cv2.contourArea)
        valid_box = cv2.boundingRect(largest_contour)

# 5. Fallback: If color filtering failed/picked up the background, look in the top-left quadrant
if valid_box is None:
    print("Color filter was too strict, falling back to geometric search in top-left...")
    # Grayscale + thresholding just the top-left area where the 'S' resides
    top_left_quadrant = img[0:int(h_img*0.4), 0:int(w_img*0.4)]
    gray = cv2.cvtColor(top_left_quadrant, cv2.COLOR_BGR2GRAY)
    
    # Look for dark/bright contrast changes
    _, thresh = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
    fallback_contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    if fallback_contours:
        largest_fallback = max(fallback_contours, key=cv2.contourArea)
        x, y, w, h = cv2.boundingRect(largest_fallback)
        valid_box = (x, y, w, h)

# 6. Output the results
if valid_box:
    x, y, w, h = valid_box
    print(f"Bounding Box Coordinates: [X: {x}, Y: {y}, Width: {w}, Height: {h}]")
    
    cropped_s = img[y:y+h, x:x+w]
    cv2.imwrite('cropped_S.png', cropped_s)
    
    # Visual check
    cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
    cv2.imwrite('detected_S.png', img)
else:
    print("Could not isolate the 'S'. Check if the image path or format is altering colors.")