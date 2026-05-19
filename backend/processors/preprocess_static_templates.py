import os
import cv2
from processors.template_processor import process_template
from tools.file_logger import Logger

pieces_folder = "templates/pieces"
numbers_folder = "templates/numbers"
processed_numbers_folder = "templates/processed/numbers"
processed_pieces_folder = "templates/processed/pieces"

def process_static_templates():

    process(pieces_folder, processed_pieces_folder)
    process(numbers_folder, processed_numbers_folder)

def process(input_folder:str, output_folder:str):

    for filename in os.listdir(input_folder):
        path = os.path.join(input_folder, filename)
        img = cv2.imread(path)

        result = process_template(img)

        path = f"{output_folder}/{filename}"

        Logger.info("Saved processed static template to {path}")

        cv2.imwrite(path, result)
