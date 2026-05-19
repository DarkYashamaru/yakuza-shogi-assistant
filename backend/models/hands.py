from dataclasses import dataclass
from models.piece import Piece

@dataclass
class HandPiece:
    piece: Piece
    amount: int

@dataclass
class Hand:
    pieces: list[HandPiece]

    def to_sfen(self) -> str:
        # Strict SFEN piece value priority ordering
        piece_order = ['rook', 'bishop', 'gold', 'silver', 'knight', 'lance', 'pawn']
        
        # Map names to their standard SFEN single-letter symbols
        sfen_symbols = {
            'pawn': 'P', 'lance': 'L', 'knight': 'N', 'silver': 'S', 
            'gold': 'G', 'bishop': 'B', 'rook': 'R'
        }

        # Tracks totals for this specific hand
        counts = {p: 0 for p in piece_order}

        if not self.pieces:
            return ""

        # 1. Tally up the pieces in this hand
        for hp in self.pieces:
            if hp.piece.name == 'empty':
                continue

            # Rule: If name is not empty but amount is 0, assume it's 1
            actual_amount = hp.amount if hp.amount > 0 else 1
            name = hp.piece.name
            
            counts[name] += actual_amount

        sfen_parts = []

        # 2. Build the string segment
        for name in piece_order:
            count = counts[name]
            if count > 0:
                symbol = sfen_symbols[name].upper()
                sfen_parts.append(f"{count if count > 1 else ''}{symbol}")

        return "".join(sfen_parts)

@dataclass
class Hands:
    enemy_hand: Hand
    player_hand: Hand