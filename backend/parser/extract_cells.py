from models.cell import Cell
from pathlib import Path
import cv2
import numpy as np
import os


# =====================================================
# BOARD COORDINATES
# =====================================================

left = 550
top = 90
right = 1370
bottom = 991


# =====================================================
# TEMP PATHS
# =====================================================

temp_folder = Path("temp")
temp_cell_folder = temp_folder / "cells"


# =====================================================
# GENERATE BOARD CELLS
# =====================================================

def generate_cells(img_arr: np.ndarray) -> list[Cell]:

    temp_cell_folder.mkdir(
        parents=True,
        exist_ok=True
    )

    cell_padding = 3

    # -------------------------------------------------
    # CROP BOARD
    # -------------------------------------------------

    board = img_arr[top:bottom, left:right]

    # Save debug board image
    board_path = f"{os.getcwd()}/{temp_folder}/board.png"

    image_rgb = board[:, :, ::-1]

    cv2.imwrite(board_path, image_rgb)

    # -------------------------------------------------
    # COMPUTE CELL SIZE
    # -------------------------------------------------

    board_height, board_width = board.shape[:2]

    cell_width = board_width // 9
    cell_height = board_height // 9

    cells = []

    # -------------------------------------------------
    # SPLIT INTO 9x9 GRID
    # -------------------------------------------------

    for row in range(9):

        for col in range(9):

            x1 = col * cell_width
            y1 = row * cell_height

            x2 = x1 + cell_width
            y2 = y1 + cell_height

            # -----------------------------------------
            # APPLY PADDING + CROP CELL
            # -----------------------------------------

            cell_img = board[
                y1 + cell_padding : y2 - cell_padding,
                x1 + cell_padding : x2 - cell_padding
            ]

            # -----------------------------------------
            # SAVE CELL
            # -----------------------------------------

            cell_path = (
                f"{os.getcwd()}/"
                f"{temp_cell_folder}/"
                f"{row}_{col}.png"
            )

            image_rgb = cell_img[:, :, ::-1]
            cv2.imwrite(cell_path, image_rgb)

            # -----------------------------------------
            # CREATE CELL MODEL
            # -----------------------------------------

            cell = Cell(x=row, y=col, piece=None, image=cell_img)

            cells.append(cell)

    return cells