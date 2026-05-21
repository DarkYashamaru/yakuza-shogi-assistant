from models.cell import Cell
from models.piece import Piece
from models.hands import Hands, Hand, HandPiece
from parser.image_to_number import parse_image
from parser.compare_cells import compare_hand_cell
from processors.binary_threshold import binary_threshold
from pathlib import Path
from parser.check_empty_cell import check_empty
from parser.compare_numbers import compare_number
from tools.save_debug_image import save_debug
import numpy as np
import os
import cv2

temp_folder = Path("temp")
temp_cell_folder = temp_folder / "hand_cells"
hand_witdh_padding = 17
hand_height_padding = 18
player_hand_top_offset = 17
player_hand_bottom_offset = 20

enemy_crop_amount_positions = [
    (440, 353, 464, 384),
    (348, 353, 372, 384),
    (256, 353, 280, 384),
    (440, 262, 464, 293),
    (348, 262, 372, 293),
    (256, 262, 280, 293),
    (440, 173, 464, 202),
    (348, 173, 372, 202),
    (256, 173, 280, 202),
]

player_crop_amount_positions = [
    (1525, 768, 1549, 799),
    (1617, 768, 1641, 799),
    (1709, 768, 1733, 799),
    (1525, 859, 1549, 890),
    (1617, 859, 1641, 890),
    (1709, 859, 1733, 890),
    (1525, 950, 1549, 981),
    (1617, 950, 1641, 981),
    (1709, 950, 1733, 981),
]

import os
import cv2
import numpy as np

from models.cell import Cell


def crop_hand( img: np.ndarray, left: int, top: int, right: int, bottom: int, player: str) -> list[Cell]:

    # -------------------------------------------------
    # CROP HAND REGION
    # -------------------------------------------------

    hand = img[top:bottom, left:right]

    # Save debug image
    hand_path = (
        f"{os.getcwd()}/{temp_cell_folder}/{player}_hand.png"
    )

    #cv2.imwrite(hand_path, hand)

    # -------------------------------------------------
    # COMPUTE CELL SIZE
    # -------------------------------------------------

    hand_height, hand_width = hand.shape[:2]

    cell_width = hand_width // 3
    cell_height = hand_height // 3

    cells = []

    # -------------------------------------------------
    # SPLIT INTO 3x3 GRID
    # -------------------------------------------------

    for row in range(3):

        for col in range(3):

            x1 = col * cell_width
            y1 = row * cell_height

            x2 = x1 + cell_width
            y2 = y1 + cell_height

            # -----------------------------------------
            # CROP CELL
            # -----------------------------------------

            cell_img = hand[y1:y2, x1:x2]

            # -----------------------------------------
            # SAVE CELL
            # -----------------------------------------

            cell_path = (
                f"{os.getcwd()}/"
                f"{temp_cell_folder}/"
                f"{player}_{row}_{col}.png"
            )

            #cv2.imwrite(cell_path, cell_img)

            # -----------------------------------------
            # CREATE CELL MODEL
            # -----------------------------------------

            cell = Cell(
                row,
                col,
                None,
                cell_img
            )

            cells.append(cell)

    return cells

def extract_hand_from_cells(cells, player, img: np.ndarray, positions, reverse_amounts: bool = True) -> Hand:

    pieces = []

    for cell in cells:

        piece = Piece.empty()
        piece_amount = 0

        if not check_empty(cell.image):

            piece = compare_hand_cell(cell.image)
            piece.owner = player
            piece_amount = 1

        pieces.append(
            HandPiece(piece, piece_amount)
        )

    results = []

    for index, (left, top, right, bottom) in enumerate(positions):

        piece_amount = 0
        amount_pos_img = img[top:bottom, left:right]

        save_debug(amount_pos_img, f"{player}_{index}")

        if not check_empty(amount_pos_img):
            piece_amount = compare_number(amount_pos_img)

        results.append(piece_amount)

    if reverse_amounts:
        results.reverse()

    for index, piece in enumerate(pieces):

        piece.amount = results[index]

    return Hand(pieces)


def generate_hands(img: np.array)->Hands:

    enemy_cells = crop_hand(img, 176+hand_witdh_padding, 79+hand_height_padding, 480-hand_witdh_padding, 408-hand_height_padding, "enemy")
    player_cells = crop_hand(img, 1443+hand_witdh_padding, 676+player_hand_top_offset, 1745-hand_witdh_padding, 1005-player_hand_bottom_offset, "player")

    enemy_hand = extract_hand_from_cells(enemy_cells, "enemy", img, enemy_crop_amount_positions)
    player_hand = extract_hand_from_cells(player_cells, "player", img, player_crop_amount_positions, reverse_amounts=False)

    return Hands(enemy_hand, player_hand)
    #return Hands(None, None)