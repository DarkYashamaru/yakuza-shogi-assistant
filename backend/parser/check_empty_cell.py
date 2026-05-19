from processors.binary_threshold import binary_threshold

import cv2
import numpy as np


MIN_FOREGROUND_PIXELS = 50


def check_empty(cell_img: np.ndarray) -> bool:

    binary = binary_threshold(cell_img)

    foreground_pixels = cv2.countNonZero(binary)

    return foreground_pixels < MIN_FOREGROUND_PIXELS