import cv2
import numpy as np


def binary_threshold_red(img: np.array, theshold: int = 180) -> np.array:
    # Normalize size
    img = cv2.resize(img, (94, 85))

    # Remove borders
    padding = 5
    img = img[padding:-padding, padding:-padding]

    # 1. Convert the color image from BGR to HSV
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    # 2. Define the TUNED ranges for Red
    # Raised Saturation min from 70 -> 100
    # Raised Value min from 50 -> 100 (This kills the blacks/shadows)
    lower_red1 = np.array([0, theshold, theshold])
    upper_red1 = np.array([10, 255, 255])
    
    lower_red2 = np.array([165, 100, 100])  # Slightly widened hue to 165 to catch deeper reds
    upper_red2 = np.array([180, 255, 255])

    # 3. Create masks for both ranges
    mask1 = cv2.inRange(hsv, lower_red1, upper_red1)
    mask2 = cv2.inRange(hsv, lower_red2, upper_red2)

    # 4. Combine masks
    binary_red = cv2.bitwise_or(mask1, mask2)

    return binary_red