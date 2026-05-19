from parser.image_to_number import parse_image
from PIL import Image
import numpy as np

# Approximate turn coordinates
left = 222
top = 560
right = 445
bottom = 624

def parse_turn_count(img_arr)->int:

    img = Image.fromarray(img_arr)
    cropped_image = img.crop((left, top, right, bottom))

    cropped_array = np.array(cropped_image)
    turn_count = parse_image(cropped_array)
    return turn_count