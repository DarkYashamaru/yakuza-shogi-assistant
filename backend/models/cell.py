from dataclasses import dataclass
from models.piece import Piece
import numpy as np

@dataclass
class Cell:
    x: int
    y: int
    piece: Piece
    image: np.array