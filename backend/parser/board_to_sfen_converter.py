from models.hands import Hands, Hand
from models.board import Board

PIECE_TO_SFEN = {
    "pawn": "P",
    "lance": "L",
    "knight": "N",
    "silver": "S",
    "gold": "G",
    "bishop": "B",
    "rook": "R",
    "king": "K",
    "empty": "*"
}

PIECE_TO_SFEN_PROMOTED = {
    "pawn": "+P",
    "lance": "+L",
    "knight": "+N",
    "silver": "+S",
    "bishop": "+B",
    "rook": "+R",
}


def board_to_sfen(board: Board, player_is_sente: bool, turn_count: int, hands_data: Hands):
    rows = []

    print(f"Player is Sente: {player_is_sente}")

    if player_is_sente:
        cells = board.cells
    else:
        cells = board.cells[::-1]

    for i in range(9):
        row = ""
        empty = 0
        for j in range(9):
            flat_index = (i * 9) + j
            cell = cells[flat_index]

            if cell.piece.name == "empty":
                empty+=1
            else:
                if empty > 0:
                    row+= str(empty)
                    empty = 0
                if cell.piece.promoted:
                    piece = PIECE_TO_SFEN_PROMOTED[cell.piece.name]
                else:
                    piece = PIECE_TO_SFEN[cell.piece.name]

                if player_is_sente:
                    if cell.piece.owner == "enemy":
                        piece = piece.lower()
                    else:
                        piece = piece.upper()
                else:
                    if cell.piece.owner == "enemy":
                        piece = piece.upper()
                    else:
                        piece = piece.lower()
                
                row+=piece
            #print(cell)
        if empty > 0:
            row+= str(empty)
        print(row)
        rows.append(row)


    board_part = "/".join(rows)

    # Side to move
    side_to_move = "b" if player_is_sente else "w"

    # Hands (captured pieces) - Hand.to_sfen() returns clean uppercase characters
    player_hand_str = hands_data.player_hand.to_sfen()
    enemy_hand_str = hands_data.enemy_hand.to_sfen()

    # Sente (Uppercase) must be concatenated before Gote (Lowercase)
    if player_is_sente:
        hands = player_hand_str + enemy_hand_str.lower()
    else:
        hands = enemy_hand_str + player_hand_str.lower()

    if not hands:
        hands = "-"

    # Perfect SFEN specification order
    return f"{board_part} {side_to_move} {hands} {turn_count}"