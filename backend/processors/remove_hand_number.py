import cv2
import numpy as np


def remove_hand_number(img: np.ndarray) -> np.ndarray:

    # Connected components
    num_labels, labels, stats, centroids = (
        cv2.connectedComponentsWithStats(img)
    )

    output = img.copy()

    height = img.shape[0]

    for i in range(1, num_labels):

        area = stats[i, cv2.CC_STAT_AREA]

        x = stats[i, cv2.CC_STAT_LEFT]
        y = stats[i, cv2.CC_STAT_TOP]
        w = stats[i, cv2.CC_STAT_WIDTH]
        h = stats[i, cv2.CC_STAT_HEIGHT]

        cx, cy = centroids[i]

        # -----------------------------------------
        # REMOVE SMALL LOW COMPONENTS
        # -----------------------------------------

        if area < 200 and cy > height * 0.70:

            output[labels == i] = 0

    return output