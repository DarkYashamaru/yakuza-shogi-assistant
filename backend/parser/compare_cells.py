import os
import cv2
from models.piece import Piece
from processors.template_processor import process_template
from processors.binary_threshold import binary_threshold
from processors.remove_hand_number import remove_hand_number
from tools.file_logger import Logger
from tools.save_debug_image import save_debug
from pathlib import Path
import numpy as np

static_templates_folder = "templates/processed/pieces"
template_names = []
static_templates = []

def compare_against_templates(cell_to_compare, templates)->Piece:
    highest_score = 0
    best_match = "empty"

    index = 0
    for template in templates:

        # --- TEMPLATE MATCHING LOGIC ---
        # We will pick a template to compare against. Let's use index 0 as a test, 
        # but in production, you would loop through all binary_templates to find the highest score.
        target_template = template
        target_name = template_names[index]

        # Run template matching using Normalized Cross-Correlation (TM_CCOEFF_NORMED)
        # This gives a clean value ranging from -1.0 to 1.0 (where 1.0 is a perfect match)
        match_result = cv2.matchTemplate(cell_to_compare, target_template, cv2.TM_CCOEFF_NORMED)
        
        # minMaxLoc extracts the maximum match value and its pixel location
        _, max_val, _, _ = cv2.minMaxLoc(match_result)
        
        # Convert to a human-readable percentage score
        match_percentage = max_val * 100

        Logger.info(f"comparing against: {target_name} score: {match_percentage}")

        if match_percentage > highest_score:
            highest_score = match_percentage
            best_match = target_name

        index+=1

        #print(f"Comparing with {target_name} -> Match Score: {match_percentage:.2f}%")

        # # --- VISUALIZATION BLOCK ---
        # # Stack the processed cell and the template side-by-side to compare visually
        # visual_stack = cv2.hconcat([cell_to_compare, target_template])
        
        # # Convert back to BGR color space strictly so we can draw colorful text on it
        # visual_output = cv2.cvtColor(visual_stack, cv2.COLOR_GRAY2BGR)
        
        # # Double the size of the visualization window so it's easier to read
        # visual_output = cv2.resize(visual_output, (visual_output.shape[1] * 2, visual_output.shape[0] * 2))

        # # Text setups
        # score_text = f"Score: {match_percentage:.1f}%"
        # name_text = f"Template: {target_name}"
        
        # # Choose text color: Green if highly confident (>80%), Red if poor match
        # text_color = (0, 255, 0) if match_percentage > 80 else (0, 0, 255)

        # # Draw the text overlay onto the display image
        # cv2.putText(visual_output, score_text, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.6, text_color, 2)
        # cv2.putText(visual_output, name_text, (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (255, 255, 255), 1)

        # # Display the results
        # cv2.imshow('Template Matching Evaluation', visual_output)
        # cv2.waitKey(0)
        # cv2.destroyAllWindows()

    #print(f"best match {best_match}, score {highest_score}")

    Logger.info(f"Highest score: {highest_score} best match: {best_match}")

    if highest_score < 50:
        return Piece.empty()

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

    return Piece(name, owner, promoted)


def load_static_templates ():
    global static_templates

    if len(static_templates) < 1:
        for filename in os.listdir(static_templates_folder):
            path = os.path.join(static_templates_folder, filename)
            static_templates.append(cv2.imread(path, cv2.IMREAD_GRAYSCALE))
            template_names.append(filename)

def compare_cell(img: np.array, x:int = 0, y:int = 0) -> Piece:

    load_static_templates()  

    normalized = process_template(img)
    #save_debug(normalized, f"normalized_cell_{x}_{y}")

    match_piece = compare_against_templates(normalized, static_templates)

    return match_piece

def compare_hand_cell(img: np.array) -> Piece:
    
    load_static_templates()

    binary = binary_threshold(img)

    #save_debug(binary, "binary_hand_cell")

    number_removed = remove_hand_number(binary)
    #save_debug(number_removed, "removed_hand_number")

    normalized = process_template(number_removed, apply_binary=False)      

    match_piece = compare_against_templates(normalized, static_templates)

    return match_piece