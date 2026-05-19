from dataclasses import dataclass
from models.cell import Cell


@dataclass
class Board:
    cells: list[Cell]
    best_move: str
