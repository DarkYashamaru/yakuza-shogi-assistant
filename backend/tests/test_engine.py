import subprocess
import threading
import queue
import time
from pathlib import Path

ENGINE_PATH = Path(
    r"D:\Repositories\yakuza-shogi-assistant\backend\engine\YaneuraOu2018KPPT_avx2.exe"
)

output_queue = queue.Queue()


def enqueue_output(pipe, q):
    while True:
        line = pipe.readline()

        if not line:
            break

        q.put(line.strip())


engine = subprocess.Popen(
    [str(ENGINE_PATH)],
    stdin=subprocess.PIPE,
    stdout=subprocess.PIPE,
    stderr=subprocess.STDOUT,
    text=True,
    bufsize=1,
    cwd=str(ENGINE_PATH.parent)
)

thread = threading.Thread(
    target=enqueue_output,
    args=(engine.stdout, output_queue),
    daemon=True
)

thread.start()


def send(command: str):
    print(f">>> {command}")

    if engine.stdin:
        engine.stdin.write(command + "\n")
        engine.stdin.flush()


def wait_for(keyword: str, timeout=15):
    start = time.time()

    while time.time() - start < timeout:
        try:
            line = output_queue.get(timeout=0.1)

            print(line)

            if keyword in line:
                return line

        except queue.Empty:
            continue

    raise TimeoutError(f"Did not receive '{keyword}'")


try:
    # --- USI INIT ---

    send("usi")
    wait_for("usiok")
    send("setoption name BookFile value no_book")
    send("isready")
    wait_for("readyok")

    # --- TEST POSITION ---

    send("position startpos")

    # Search
    send("go depth 10")

    bestmove_line = wait_for("bestmove")

    print("\n=== RESULT ===")
    print(bestmove_line)

finally:
    try:
        send("quit")
    except Exception:
        pass

    engine.wait(timeout=5)