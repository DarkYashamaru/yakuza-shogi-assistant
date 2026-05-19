from models.board import Board
from parser.extract_cells import generate_cells
from parser.compare_cells import compare_cell
from models.piece import Piece
from parser.check_empty_cell import check_empty
from tools.file_logger import Logger
import numpy as np
import cv2

def parse_board(img: np.array)->Board:
    cells = generate_cells(img)

    result = []

    for cell in cells:
        piece = Piece.empty()
        cell_img = cv2.imread(cell.image_path)

        Logger.info(f"Checking Cell x:{cell.x} y:{cell.y}")

        if not check_empty(cell_img):
            piece = compare_cell(cell_img, cell.x, cell.y)
            Logger.info(f"{piece.name} in Cell x:{cell.x} y:{cell.y}") 
        else:
            Logger.info(f"Cell is empty")

        cell.piece = piece

        #print(f"x:{cell.x} y:{cell.y} {piece.owner} {piece.name}")

        result.append(cell)

    board = Board(result, "")

    return board