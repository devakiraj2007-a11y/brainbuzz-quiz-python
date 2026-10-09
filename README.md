# BrainBuzz

A desktop quiz game platform built with Python and Tkinter.

## Features
- 5 categories: Python, Science, Technology, General Knowledge, Mixed
- 15-second countdown timer with colour-changing bar
- Points by difficulty, plus time and streak bonuses
- 50/50 lifeline (once per game)
- Persistent leaderboard saved to `leaderboard.json`

## Getting Started

Requires Python 3.10+ (Tkinter is included).

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python main.py
```

## Run tests
```bash
python -m pytest
```

## Project Structure
```
quiz/
├── questions.py   # question bank
├── game.py        # scoring and game logic
├── storage.py     # leaderboard (JSON)
└── ui.py          # Tkinter interface
main.py            # entry point
tests/             # unit tests
```

## Future Ideas
- Add more categories and questions
- Sound effects
- Difficulty modes
- Web version with Flask