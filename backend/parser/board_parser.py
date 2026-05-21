from concurrent.futures import ThreadPoolExecutor

from models.board import Board
from parser.extract_cells import generate_cells
from parser.compare_cells import compare_cell
from models.piece import Piece
from parser.check_empty_cell import check_empty
from tools.file_logger import Logger

import numpy as np
import cv2
import time


def process_cell(cell):

    piece = Piece.empty()

    if not check_empty(cell.image):

        start = time.perf_counter()
        Logger.info(f"Comparing cell x:{cell.x} y:{cell.y}")

        piece = compare_cell(
            cell.image,
            cell.x,
            cell.y
        )

        Logger.info(
            f"Comparing cell x:{cell.x} y:{cell.y} "
            f"took: {(time.perf_counter() - start)*1000:.2f} ms"
        )

    cell.piece = piece

    return cell


def parse_board(img: np.ndarray) -> Board:

    start = time.perf_counter()

    cells = generate_cells(img)

    Logger.info(
        f"Generate cells took: "
        f"{(time.perf_counter() - start)*1000:.2f} ms"
    )

    Logger.info("Starting cell comparison")

    cell_compare_start = time.perf_counter()

    # Parallel processing
    with ThreadPoolExecutor(max_workers=8) as executor:

        result = list(
            executor.map(
                process_cell,
                cells
            )
        )

    Logger.info(
        f"Comparing cells took: "
        f"{(time.perf_counter() - cell_compare_start)*1000:.2f} ms"
    )

    board = Board(result, "")

    return board