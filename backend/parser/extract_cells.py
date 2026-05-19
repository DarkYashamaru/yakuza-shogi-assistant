from PIL import Image
from models.cell import Cell
from pathlib import Path
import numpy as np
import os

# Approximate board coordinates
left = 550
top = 90
right = 1370
bottom = 991

temp_folder = Path("temp")
temp_cell_folder = temp_folder / "cells"

def generate_cells(img_arr):

    img = Image.fromarray(img_arr)

    temp_cell_folder.mkdir(parents=True, exist_ok=True)

    cell_padding = 3

    board = img.crop((left, top, right, bottom))

    board.save(f"{os.getcwd()}/{temp_folder}/board.png")

    cell_width = board.width / 9
    cell_height = board.height / 9

    cells = []

    for row in range(9):
        for col in range(9):
            x1 = col * cell_width
            y1 = row * cell_height

            x2 = x1 + cell_width
            y2 = y1 + cell_height

            cell = board.crop((x1+cell_padding, y1+cell_padding, x2-cell_padding, y2-cell_padding))
            cell_path = f"{os.getcwd()}/{temp_cell_folder}/{row}_{col}.png"
            cell.save(cell_path)

            cell = Cell(row, col, None, cell_path)

            cells.append(cell)

    return cells
