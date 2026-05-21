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
import time

PROCESS_NAME = "likeadragon8.exe"


def analyze_board(client):
    board_analysis_start = time.perf_counter()


    print("\n=== Capturing board ===")

    start = time.perf_counter()
    img = screenshot(PROCESS_NAME)
    Logger.info(f"Screenshot took: {(time.perf_counter() - start)*1000:.2f} ms")

    if img is None:
        print("Screenshot failed")
        return

    try:
        # Parse board
        start = time.perf_counter()
        board = parse_board(img)
        Logger.info(f"Board Parsing took: {(time.perf_counter() - start)*1000:.2f} ms")

        start = time.perf_counter()
        turn_count = parse_turn_count(img)
        Logger.info(f"Parse turn count took: {(time.perf_counter() - start)*1000:.2f} ms")

        if turn_count % 2 == 0:
            player_is_sente = False
        else:
            player_is_sente = True

        start = time.perf_counter()
        hands = generate_hands(img)
        Logger.info(f"Parse hands took: {(time.perf_counter() - start)*1000:.2f} ms")

        # Convert to SFEN
        start = time.perf_counter()
        sfen = board_to_sfen(board, player_is_sente, turn_count, hands)
        Logger.info(f"Board to sfen took: {(time.perf_counter() - start)*1000:.2f} ms")

        print(f"SFEN: {sfen}")

        #DEBUG
        print("+++++++++++++ DEBUG BOARD ++++++++++++++++")
        board.best_move = "7g7f"
        render_board(board, player_is_sente)
        print("+++++++++++++ DEBUG BOARD ++++++++++++++++")

        # Get best move
        start = time.perf_counter()
        move = client.get_best_move(sfen)
        Logger.info(f"Get best move took: {(time.perf_counter() - start)*1000:.2f} ms")

        move = translate_move_perspective(move, player_is_sente)

        board.best_move = move

        # Draw board
        start = time.perf_counter()
        render_board(board, player_is_sente)
        Logger.info(f"Render board took: {(time.perf_counter() - start)*1000:.2f} ms")
        #render_board(board, player_is_sente)

        print(f"Best move: {move}")

    except Exception as e:
        print("\n=== FULL ERROR ===")
        traceback.print_exc()

    Logger.info(f"Complete board analisis took: {(time.perf_counter() - board_analysis_start)*1000:.2f} ms")


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