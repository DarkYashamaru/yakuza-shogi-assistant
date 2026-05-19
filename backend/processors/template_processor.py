import numpy as np
import cv2
from processors.binary_threshold import binary_threshold
from processors.bbox_processor import get_bbox_and_crop
from processors.center_of_mass_normalization import normalize_piece
from tools.save_debug_image import save_debug

def process_template(template: np.array, apply_binary:bool = True, apply_bbox:bool = True) -> np.array:

    result = template

    if apply_binary:
        result = binary_threshold(template)
    
    if apply_bbox:
        result = get_bbox_and_crop(result)

    normalized = normalize_piece(result)
    #debug
    #save_debug(normalized)
    return normalized