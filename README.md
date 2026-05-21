# yakuza-shogi-assistant

Native desktop shogi assistant that uses computer vision to detect board states from *Like a Dragon / Yakuza* games and analyze moves using the YaneuraOu shogi engine.

## Current Status

This project is currently a very early proof of concept / prototype.

At the moment, the tool:

- Captures the shogi board directly from the game window
- Uses computer vision and OpenCV to identify pieces
- Converts the detected board into SFEN notation
- Sends the position to YaneuraOu for analysis
- Displays a text-based representation of the board and the recommended best move

The current implementation is highly experimental and currently only supports:

- **Like a Dragon: Infinite Wealth**
- **1920x1080 resolution**
- **Fullscreen or borderless window mode**
- Windows PCs

Puzzle shogi modes are not supported yet.

---

## Running

1. Launch the game and open a normal shogi match

2. Create and activate a Python virtual environment:

### Windows (PowerShell)

```bash
python -m venv venv
venv/Scripts/activate.ps1
```

3. Install dependencies:

```bash
pip install -r backend/requirements.txt
```

4. Run the application:

```bash
python backend/main.py
```

5. Press `F4` while the game is open  
   *(For best results, move the hand cursor outside the board before capturing the screenshot to avoid obstructing the pieces.)*

The tool will:

- Capture the current board
- Analyze the position
- Print a text representation of the board in the terminal
- Show the engine's recommended move

The tool will:

- Capture the current board
- Analyze the position
- Print a text representation of the board in the terminal
- Show the engine's recommended move

### Example Output

```text
    9 8 7 6 5 4 3 2 1

a | l n s g k g s n l
b | * r * * * * * b *
c | p p p p p p p p p
d | * * * * * * * * *
e | * * * * * * * * *
f | * * * * * * *<*>*
g | P P P P P P P[P]P
h | * B * * * * * R *
i | L N S G K G S N L
```

- `[]` indicates the piece to move
- `<>` indicates the engine's suggested destination square

---

## Accuracy / Limitations

Piece recognition is still unreliable in some situations and there are currently false positives during board parsing.

Because of this:

- The generated SFEN may occasionally be incorrect
- The suggested move may sometimes be invalid or suboptimal

Despite this, the current prototype was good enough in testing to beat all ranked shogi opponents in *Infinite Wealth*, including the Shogi King.

---

## Planned Improvements

- Better computer vision accuracy
- Support for promoted pieces and captured pieces
- Overlay UI instead of terminal output
- Real-time board tracking
- Additional resolutions
- Support for older *Yakuza / Like a Dragon* titles
- Puzzle shogi support
- Better move visualization

---

## Technologies Used

- Python
- OpenCV
- YaneuraOu
- SFEN / USI protocols

---

## Disclaimer

This project is intended for educational and experimental purposes.
