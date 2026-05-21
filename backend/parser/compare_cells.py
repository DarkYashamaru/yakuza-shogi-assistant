import os
import cv2
from models.piece import Piece
from processors.template_processor import process_template, process_template_red
from processors.binary_threshold import binary_threshold
from processors.remove_hand_number import remove_hand_number
from tools.file_logger import Logger
from tools.save_debug_image import save_debug
from pathlib import Path
import numpy as np
#from collections import defaultdict

static_templates_folder = "templates/processed/pieces"
static_red_templates_folder = "templates/processed/pieces_red"
template_names = []
static_templates = []
static_red_templates = []

def compare_against_templates(cell_to_compare, templates, x:int = 0, y:int = 0):
    highest_score = 0
    best_match = "empty"
    scores = {}

    index = 0
    for template in templates:

        # --- TEMPLATE MATCHING LOGIC ---
        # We will pick a template to compare against. Let's use index 0 as a test, 
        # but in production, you would loop through all binary_templates to find the highest score.

        # Run template matching using Normalized Cross-Correlation (TM_CCOEFF_NORMED)
        # This gives a clean value ranging from -1.0 to 1.0 (where 1.0 is a perfect match)
        match_result = cv2.matchTemplate(cell_to_compare, template, cv2.TM_CCOEFF_NORMED)
        
        # minMaxLoc extracts the maximum match value and its pixel location
        #_, max_val, _, _ = cv2.minMaxLoc(match_result)
        max_val = match_result[0][0]
        
        # Convert to a human-readable percentage score
        match_percentage = max_val * 100
        scores[template_names[index]] = match_percentage

        Logger.info(f"comparing cell x:{x} y:{y} against: {template_names[index]} score: {match_percentage}")

        index+=1

    scores = dict(sorted(scores.items(), key=lambda item: item[1], reverse=True))

    highest_score = next(iter(scores.values()))
    best_match = next(iter(scores))

    Logger.info(f"Cell x:{x} y:{y} Highest score: {highest_score} best match: {best_match}")

    if highest_score < 45:
        return (Piece.empty(), scores)

    name_without_ext = Path(best_match).stem

    name = name_without_ext.split('_')[0]
    if "enemy" in name_without_ext:
        owner = "enemy"
    else:
        owner = "player"

    if "promoted" in name_without_ext:
        promoted = True
    else:
        promoted = False

    return (Piece(name, owner, promoted), scores)

def load_templates (folder:str):
    templates = []
    for filename in os.listdir(folder):
        path = os.path.join(folder, filename)
        templates.append(cv2.imread(path, cv2.IMREAD_GRAYSCALE))

    return templates


def load_static_templates ():
    global static_templates
    global static_red_templates

    for filename in os.listdir(static_templates_folder):
        template_names.append(filename)            

    if len(static_templates) < 1:
        static_templates = load_templates(static_templates_folder)
    if len(static_red_templates) < 1:
        static_red_templates = load_templates(static_red_templates_folder)
    

def compare_cell(img: np.array, x:int = 0, y:int = 0) -> Piece:

    save_debug(img, f"{x}_{y} To Compare")

    load_static_templates()  

    normalized = process_template(img)
    save_debug(normalized, f"normalized_cell_{x}_{y}")

    match_piece, first_pass_scores = compare_against_templates(normalized, static_templates, x, y)

    highest_score = next(iter(first_pass_scores.values()))

    if highest_score < 63:
        Logger.warning(f"Cell x:{x} y:{y} got a low score {highest_score} for the piece {match_piece.name} performing second pass")

        image_rgb = img[:, :, ::-1]
        red_normalized = process_template_red(image_rgb)
        save_debug(red_normalized, f"normalized_red_cell_{x}_{y}")
        match_piece, second_pass_scores = compare_against_templates(red_normalized, static_red_templates, x, y)

        for key, value in second_pass_scores.items():
            first_pass_scores[key] += value/2

        final_score = dict(sorted(first_pass_scores.items(), key=lambda item: item[1], reverse=True))

        highest_score = next(iter(final_score.values()))
        best_match = next(iter(final_score))

        Logger.warning(f"Second score for Cell x:{x} y:{y} is {highest_score} for the piece {best_match}")
        return match_piece

    return match_piece

def compare_hand_cell(img: np.array) -> Piece:
    
    load_static_templates()

    binary = binary_threshold(img)

    #save_debug(binary, "binary_hand_cell")

    number_removed = remove_hand_number(binary)
    #save_debug(number_removed, "removed_hand_number")

    normalized = process_template(number_removed, apply_binary=False)      

    match_piece, score = compare_against_templates(normalized, static_templates)

    return match_piece