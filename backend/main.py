import keyboard
import traceback
from parser.board_parser import parse_board
from parser.board_to_sfen_converter import board_to_sfen
from parser.board_to_text import render_board
from engine.yaneuraou_client import YaneuraOuClient
from tools.capture_process_screenshot import screenshot
from parser.generate_template_cache import generate_cache
from parser.compare_cells import compare_cell
from parser.turn_count_parser import parse_turn_count
from parser.parse_hands import generate_hands
from models.cell import Cell
from parser.translate_best_move import translate_move_perspective
from processors.preprocess_static_templates import process_static_templates
from parser.compare_cells import compare_cell
from tools.file_logger import Logger
import cv2


PROCESS_NAME = "likeadragon8.exe"


def analyze_board(client):
    print("\n=== Capturing board ===")

    img = screenshot(PROCESS_NAME)

    if img is None:
        print("Screenshot failed")
        return

    try:
        # Parse board
        board = parse_board(img)
        turn_count = parse_turn_count(img)

        if turn_count % 2 == 0:
            player_is_sente = False
        else:
            player_is_sente = True

        bgr_img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
        hands = generate_hands(bgr_img)
        print(hands.player_hand)

        # Convert to SFEN
        sfen = board_to_sfen(board, player_is_sente, turn_count, hands)

        print(f"SFEN: {sfen}")

        # Get best move
        move = client.get_best_move(sfen)

        move = translate_move_perspective(move, player_is_sente)

        board.best_move = move

        # Draw board
        render_board(board, player_is_sente)
        #render_board(board, player_is_sente)

        print(f"Best move: {move}")

    except Exception as e:
        print("\n=== FULL ERROR ===")
        traceback.print_exc()


def main():
    Logger.initialize()
    process_static_templates()
    Logger.info("Application started")


    print("Starting Yakuza Shogi Assistant...")

    client = YaneuraOuClient()

    # Hotkey
    HOTKEY = "f4"

    print(f"Press {HOTKEY} to analyze the board")
    print("Press ESC to quit")

    # Register hotkey
    keyboard.add_hotkey(
        HOTKEY,
        lambda: analyze_board(client)
    )

    # Wait forever
    keyboard.wait("esc")

    print("Closing assistant...")

    client.close()

    #compare_cell(Cell(0,0, None, "temp/cells/8_8.png"))

    # img = cv2.imread(r"F:\Downloads\2072450_470.jpg")
    
    # hands = generate_hands(img)

    # for pieces in hands.enemy_hand.pieces:
    #     print(pieces)

    # for pieces in hands.player_hand.pieces:
    #     print(pieces)

    # board = parse_board(img)
    # turn_count = parse_turn_count(img)

    # if turn_count % 2 == 0:
    #     player_is_sente = False
    # else:
    #     player_is_sente = True

    # hands = generate_hands(img)

    # # Convert to SFEN
    # sfen = board_to_sfen(board, player_is_sente, turn_count, hands)

    # print(f"SFEN: {sfen}")

    #process_static_templates()

    # result = compare_cell(cell)
    # print(result)

    # img = cv2.imread(r"F:\Downloads\2072450_470.jpg")
    
    # hands = generate_hands(img)

    # for pieces in hands.enemy_hand.pieces:
    #     print(pieces)

    # for pieces in hands.player_hand.pieces:
    #     print(pieces)

if __name__ == "__main__":
    main()