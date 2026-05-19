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

# FIX 1: Shogi files always run from 9 down to 1 (left-to-right on screen display)
FILES = [" ", "9", "8", "7", "6", "5", "4", "3", "2", "1"]
RANKS = ["a", "b", "c", "d", "e", "f", "g", "h", "i"]

# FIX 2: Remap indices so File 9 is the 0th array item (far left) and File 1 is index 8 (far right)
file_to_x = {
    "9": 0, "8": 1, "7": 2, "6": 3, "5": 4, 
    "4": 5, "3": 6, "2": 7, "1": 8,
}

row_to_y = {
    "a": 0, "b": 1, "c": 2, "d": 3, "e": 4, 
    "f": 5, "g": 6, "h": 7, "i": 8,
}

def render_board(board: Board, render_best_move: bool):
    files = ""
    for file in FILES:
        files += f" {file} "

    best_move = board.best_move

    if len(best_move) >= 4 and best_move[1] == "*":
        # Since the piece is dropped from the hand, it doesn't have a 'current' position on the board.
        # We can set its current coordinates to a dummy value like -1
        current_x, current_y = -1, -1
        
        # The destination is at indices 2 and 3
        future_file = best_move[2]
        future_row  = best_move[3]
        
        next_x = file_to_x[future_file]
        next_y = row_to_y[future_row]

    else:
        # This is a normal move (e.g., "6i7h")
        current_file = best_move[0]
        current_row  = best_move[1]
        future_file  = best_move[2]
        future_row   = best_move[3]

        current_x = file_to_x[current_file]
        current_y = row_to_y[current_row]

        next_x = file_to_x[future_file]
        next_y = row_to_y[future_row]

    print(f"current pos x:{current_x} y:{current_y} next pos x:{next_x} y:{next_y}")
    
    print(files)
    print("")

    for x in range(9):
        row = ""
        for y in range(9):

            if y == 0:
                row += f" {RANKS[x]}|"
            
            # Ensure your flat index matches how your parser populates board.cells
            flat_index = (x * 9) + y
            cell = board.cells[flat_index]

            if cell.piece.promoted:
                piece = PIECE_TO_SFEN_PROMOTED[cell.piece.name]
            else:
                piece = PIECE_TO_SFEN[cell.piece.name]

            if cell.piece.owner == "enemy":
                piece = piece.lower()

            # Highlight assignments
            if y == current_x and x == current_y:
                row += f"[{piece}]"
            elif y == next_x and x == next_y:
                row += f"<{piece}>"
            else:
                if cell.piece.promoted:
                    row += f"{piece} "
                else:
                    row += f" {piece} "
            
        print(row)