from dataclasses import dataclass
from models.piece import Piece

@dataclass
class Cell:
    x: int
    y: int
    piece: Piece
    image_path: str