FILES = ["9", "8", "7", "6", "5", "4", "3", "2", "1"]
RANKS = ["a", "b", "c", "d", "e", "f", "g", "h", "i"]

def translate_move_perspective(move: str, player_is_sente: bool) -> str:
    """
    Translates a USI move string to match the player's visual perspective.
    If Sente, the move remains unchanged.
    If Gote, the files and ranks are flipped 180 degrees.
    """
    # If looking from Sente's perspective, the engine's absolute coordinates 
    # already match your screen perfectly.
    if player_is_sente:
        return move

    # Handle Shogi piece drop moves (e.g., 'P*5f')
    if '*' in move:
        piece, rest = move.split('*')
        to_file = int(rest[0])
        to_rank = rest[1]
        
        # Invert target coordinates for Gote
        flipped_file = 10 - to_file
        flipped_rank = RANKS[8 - RANKS.index(to_rank)]
        
        return f"{piece}*{flipped_file}{flipped_rank}"

    # Handle regular moves (e.g., '4a3b' or promoted moves like '4a3b+')
    from_file = int(move[0])
    from_rank = move[1]
    to_file = int(move[2])
    to_rank = move[3]
    promotion = move[4:] if len(move) > 4 else "" # Captures '+' if a piece promotes

    # Flip the files (10 - file)
    flipped_from_file = 10 - from_file
    flipped_to_file = 10 - to_file

    # Flip the ranks (mirroring indices in our RANKS list)
    flipped_from_rank = RANKS[8 - RANKS.index(from_rank)]
    flipped_to_rank = RANKS[8 - RANKS.index(to_rank)]

    return f"{flipped_from_file}{flipped_from_rank}{flipped_to_file}{flipped_to_rank}{promotion}"


# # --- Quick Test ---
# engine_move = "4a3b"

# print(f"Engine Raw Move: {engine_move}")
# print(f"Visualized as Sente: {translate_move_perspective(engine_move, player_is_sente=True)}")
# print(f"Visualized as Gote:  {translate_move_perspective(engine_move, player_is_sente=False)}")