import cv2
import numpy as np


CANVAS_SIZE = 64
TARGET_OBJECT_SIZE = 50

def resize_preserve_aspect(
    img: np.ndarray,
    target_size: int
) -> np.ndarray:

    # Validate image
    if img is None or img.size == 0:
        return np.zeros((target_size, target_size), dtype=np.uint8)

    h, w = img.shape

    # Prevent division by zero
    if h == 0 or w == 0:
        return np.zeros((target_size, target_size), dtype=np.uint8)

    scale = target_size / max(w, h)

    new_w = max(1, int(w * scale))
    new_h = max(1, int(h * scale))

    resized = cv2.resize(
        img,
        (new_w, new_h),
        interpolation=cv2.INTER_NEAREST
    )

    return resized

def center_of_mass_normalize(
    img: np.ndarray,
    canvas_size: int
) -> np.ndarray:

    # Create black canvas
    canvas = np.zeros(
        (canvas_size, canvas_size),
        dtype=np.uint8
    )

    h, w = img.shape

    # -------------------------------------------------
    # PLACE IMAGE ROUGHLY CENTERED FIRST
    # -------------------------------------------------

    start_x = (canvas_size - w) // 2
    start_y = (canvas_size - h) // 2

    canvas[
        start_y:start_y+h,
        start_x:start_x+w
    ] = img

    # -------------------------------------------------
    # COMPUTE CENTER OF MASS
    # -------------------------------------------------

    moments = cv2.moments(canvas)

    if moments["m00"] == 0:
        return canvas

    cx = int(moments["m10"] / moments["m00"])
    cy = int(moments["m01"] / moments["m00"])

    # -------------------------------------------------
    # COMPUTE SHIFT TO TRUE CENTER
    # -------------------------------------------------

    desired_x = canvas_size // 2
    desired_y = canvas_size // 2

    shift_x = desired_x - cx
    shift_y = desired_y - cy

    # -------------------------------------------------
    # APPLY SHIFT
    # -------------------------------------------------

    M = np.float32([
        [1, 0, shift_x],
        [0, 1, shift_y]
    ])

    centered = cv2.warpAffine(
        canvas,
        M,
        (canvas_size, canvas_size)
    )

    return centered

def normalize_piece(img: np.ndarray) -> np.ndarray:

    # Resize object
    resized = resize_preserve_aspect(
        img,
        TARGET_OBJECT_SIZE
    )

    # Center on canvas
    normalized = center_of_mass_normalize(
        resized,
        CANVAS_SIZE
    )

    return normalized