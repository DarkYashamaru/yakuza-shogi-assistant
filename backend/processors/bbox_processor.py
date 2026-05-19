import cv2
import numpy as np
from models.bbox import BoundingBox

def get_bounding_box(img: np.ndarray) -> BoundingBox:
    coords = cv2.findNonZero(img)
    x, y, w, h = cv2.boundingRect(coords)
    return BoundingBox(x,y,w,h)


def get_bbox_and_crop(binary_img: np.ndarray)-> np.ndarray:
    bbox = get_bounding_box(binary_img)
    cropped = binary_img[bbox.y:bbox.y+bbox.height, bbox.x:bbox.x+bbox.width]
    return cropped