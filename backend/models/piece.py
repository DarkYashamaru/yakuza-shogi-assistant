from dataclasses import dataclass

@dataclass
class Piece:
    name: str
    owner: str
    promoted: bool = False

    @staticmethod
    def empty() -> "Piece":
        return Piece("empty", "none", False)