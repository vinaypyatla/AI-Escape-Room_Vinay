# The Secret of the Locked Library — AI Escape Room

A Python + Streamlit escape-room assignment with two implementations:
- **Version 1 — AI-led:** Gemini acts as the Game Master and relies on conversation history.
- **Version 2 — Validated:** Python stores structured game state and validates actions before optional AI narration.

## Requirements
- Python 3.10 or newer
- Internet connection only if you want Gemini narration
- A Gemini API key is optional for Version 2 and required for live AI narration in Version 1

## Run locally

1. Open a terminal in this project folder.
2. Create and activate a virtual environment:

   **Windows**
   ```bash
   python -m venv .venv
   .venv\Scripts\activate
   ```

   **macOS / Linux**
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Optional Gemini setup:
   - Create an API key in Google AI Studio.
   - Set `GEMINI_API_KEY` as an environment variable.
   - Optionally set `GEMINI_MODEL` (default: `gemini-2.5-flash`).
   - Do not paste your key into source code or commit it.
5. Start the application:
   ```bash
   streamlit run app.py
   ```
6. Use the sidebar to switch between Version 1 and Version 2.

## How to play
Try natural-language actions:
- `examine the desk`
- `look at the bookshelf`
- `open the drawer with code 2741`
- `examine the painting`
- `unlock the door with code 5832`

You can also type `inventory`, `hint`, or `restart game`.

## Puzzle walkthrough (for developer/testing use)
1. Examine the desk to collect the UV flashlight.
2. Examine the bookshelf to discover drawer code `2741`.
3. Enter `2741` for the drawer. The brass key is collected automatically.
4. Examine the painting while carrying the UV flashlight to reveal `5832`.
5. Enter `5832` at the door while carrying the brass key.

## Tests
Install pytest and run:
```bash
pip install pytest
pytest -q
```

## Version differences
Version 1 asks Gemini to continue the game using recent conversation history. It is intentionally less reliable and does not enforce authoritative state.
Version 2 uses `game_engine.py` as the source of truth. Python checks inventory, puzzle progress, codes, and escape conditions. The model, when configured, only rephrases the validated result.

## Project structure
```text
ai_escape_room_project/
├── app.py
├── game_engine.py
├── tests/
│   └── test_game_engine.py
├── diagrams.md
├── report.md
├── requirements.txt
├── .env.example
└── .gitignore
```
