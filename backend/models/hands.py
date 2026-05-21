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
            'pawn': 'P',
            'lance': 'L',
            'knight': 'N',
            'silver': 'S',
            'gold': 'G',
            'bishop': 'B',
            'rook': 'R'
        }

        # Maximum legal amounts in a player's hand
        max_counts = {
            'rook': 1,
            'bishop': 1,
            'gold': 4,
            'silver': 4,
            'knight': 4,
            'lance': 4,
            'pawn': 18
        }

        # Tracks totals for this specific hand
        counts = {p: 0 for p in piece_order}

        if not self.pieces:
            return ""

        # 1. Tally up the pieces in this hand
        for hp in self.pieces:
            if hp.piece.name == 'empty':
                continue

            name = hp.piece.name

            # Ignore unknown piece names safely
            if name not in counts:
                continue

            # If amount is invalid (0 or negative), assume 1
            actual_amount = hp.amount if hp.amount > 0 else 1

            counts[name] += actual_amount

        # 2. Clamp counts to legal maximums
        for name in counts:
            counts[name] = min(counts[name], max_counts[name])

        sfen_parts = []

        # 3. Build the string segment
        for name in piece_order:
            count = counts[name]

            if count > 0:
                symbol = sfen_symbols[name]
                sfen_parts.append(f"{count if count > 1 else ''}{symbol}")

        return "".join(sfen_parts)

@dataclass
class Hands:
    enemy_hand: Hand
    player_hand: Hand