from pathlib import Path
import uuid
import numpy as np
import cv2


def save_debug(img: np.ndarray, label: str = "debug") -> str:
    """
    Saves a debug image with a unique UUID filename.
    """

    debug_dir = Path("debug")
    debug_dir.mkdir(parents=True, exist_ok=True)

    unique_id = uuid.uuid4().hex

    filename = f"{label}-{unique_id}.png"

    path = debug_dir / filename

    cv2.imwrite(str(path), img)

    return str(path)