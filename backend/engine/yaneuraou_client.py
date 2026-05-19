import subprocess
import threading
import queue
import time

from pathlib import Path


ENGINE_PATH = Path(
    r"D:\Repositories\yakuza-shogi-assistant\backend\engine\YaneuraOu2018KPPT_avx2.exe"
)


class YaneuraOuClient:

    def __init__(self):

        self.output_queue = queue.Queue()

        self.engine = subprocess.Popen(
            [str(ENGINE_PATH)],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1,
            cwd=str(ENGINE_PATH.parent)
        )

        self.thread = threading.Thread(
            target=self.enqueue_output,
            args=(self.engine.stdout, self.output_queue),
            daemon=True
        )

        self.thread.start()

        self.initialize_engine()

    # -------------------------------------------------
    # Output reader
    # -------------------------------------------------

    def enqueue_output(self, pipe, q):

        while True:

            line = pipe.readline()

            if not line:
                break

            q.put(line.strip())

    # -------------------------------------------------
    # Send command
    # -------------------------------------------------

    def send(self, command: str):

        print(f">>> {command}")

        if self.engine.stdin:
            self.engine.stdin.write(command + "\n")
            self.engine.stdin.flush()

    # -------------------------------------------------
    # Wait for response
    # -------------------------------------------------

    def wait_for(self, keyword: str, timeout=15):

        start = time.time()

        while time.time() - start < timeout:

            try:

                line = self.output_queue.get(timeout=0.1)

                print(line)

                if keyword in line:
                    return line

            except queue.Empty:
                continue

        raise TimeoutError(
            f"Did not receive '{keyword}'"
        )

    # -------------------------------------------------
    # Initialize USI
    # -------------------------------------------------

    def initialize_engine(self):

        self.send("usi")
        self.wait_for("usiok")

        self.send("setoption name BookFile value no_book")

        self.send("isready")
        self.wait_for("readyok")

    # -------------------------------------------------
    # Get best move
    # -------------------------------------------------

    def get_best_move(self, sfen: str, depth=10):

        self.send(f"position sfen {sfen}")

        self.send(f"go depth {depth}")

        bestmove_line = self.wait_for("bestmove")

        return self.parse_bestmove(bestmove_line)

    # -------------------------------------------------
    # Parse engine output
    # -------------------------------------------------

    def parse_bestmove(self, line: str):

        # Example:
        # bestmove 7g7f ponder 3c3d

        parts = line.split()

        if len(parts) < 2:
            return None

        return parts[1]

    # -------------------------------------------------
    # Shutdown
    # -------------------------------------------------

    def close(self):

        try:
            self.send("quit")
        except Exception:
            pass

        self.engine.wait(timeout=5)