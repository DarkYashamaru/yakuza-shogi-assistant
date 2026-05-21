import numpy as np
import cv2


def binary_threshold(img: np.array) -> np.array:
    # Normalize size
    img = cv2.resize(img, (94, 85))

    # Remove borders
    padding = 5
    img = img[padding:-padding, padding:-padding]

    # Convert from BGR color to Grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Binary threshold (now safely operating on a single channel)
    _, binary_img = cv2.threshold(gray, 80, 255, cv2.THRESH_BINARY_INV)

    return binary_img