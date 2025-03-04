# MathSpaceShip

A fun educational game that combines math practice with space shooting mechanics!

## Building the macOS App

1. First, ensure you have all requirements installed:
```bash
pip install -r requirements.txt
```

2. Clean any previous builds:
```bash
rm -rf build dist
```

3. Build the app:
```bash
python setup.py py2app
```

The finished app will be in the `dist` folder as `MathSpaceShip.app`.

## Distribution

To distribute the app:

1. Navigate to the `dist` folder
2. Right-click on `MathSpaceShip.app` and select "Compress"
3. Share the resulting `MathSpaceShip.app.zip` file

## System Requirements

- macOS 10.10 or later
- 64-bit processor

## Game Controls

- Type numbers to answer math questions
- Press Enter to submit your answer
- Press Backspace to correct your answer

## Features

- Practice math operations (addition, subtraction, multiplication, division)
- Visual feedback for correct/incorrect answers
- Score tracking
- Sound effects and background music
- Progressive difficulty
```bash
uv venv --python 3.10.11
source .venv/bin/activate
uv pip install -r requirements.txt
uv lock
uv export > requirements.txt
```