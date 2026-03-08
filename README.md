# Python Chess Engine with GUI ♟️

A Python-based chess application that combines a **custom chess engine** with a **graphical user interface (GUI)** built using Tkinter. The program allows users to play chess against the computer while visualizing moves, board state, and a basic evaluation of the position.

This project demonstrates how chess logic, graphical interfaces, and simple AI decision-making can be integrated into a single Python application.

---

## Key Features

* Play chess against a computer engine
* Interactive chess board built with Tkinter
* Legal move highlighting for selected pieces
* Last move highlighting on the board
* Move history panel showing the game notation
* Evaluation bar indicating positional advantage
* Clean board colors similar to Chess.com
* Simple engine move generation using a custom `choose_move()` function

---

## Technologies Used

* **Python 3**
* **Tkinter** – for the graphical user interface
* **python-chess** – for chess rules, move validation, and board representation

---

## Installation

### 1. Clone the Repository

```
git clone https://github.com/yourusername/python-chess-engine.git
cd python-chess-engine
```

### 2. Install Dependencies

Install the required Python package:

```
pip install -r requirements.txt
```

If installing manually:

```
pip install python-chess
```

---

## Running the Application

Run the main GUI file:

```
python chess_gui.py
```

A window will open displaying the chess board. You play as **White**, and the engine responds automatically after your move.

---

## Gameplay Instructions

1. Click on one of your pieces to select it.
2. Legal moves will be shown as highlighted indicators on the board.
3. Click a destination square to make your move.
4. The computer engine will calculate and play its move automatically.
5. The move list and evaluation bar update as the game progresses.

---

## Engine Overview

The chess engine uses the **python-chess board representation** to generate legal moves.
A custom `choose_move()` function evaluates possible moves and selects one within a specified time limit.

The current evaluation is based on **material balance**, assigning values to pieces such as:

* Pawn = 100
* Knight = 320
* Bishop = 330
* Rook = 500
* Queen = 900

This evaluation drives the simple position assessment displayed in the evaluation bar.

---

## Possible Improvements

Future enhancements that could make the project stronger include:

* Implementing **minimax with alpha-beta pruning**
* Adding **piece-square tables** for better evaluation
* Creating **opening book support**
* Adding **move animations**
* Implementing **game saving (PGN export)**
* Adding **difficulty levels for the engine**
* Improving GUI styling and layout

---

## Educational Value

This project is useful for learning:

* Game programming in Python
* GUI development using Tkinter
* Chess programming concepts
* Move generation and board evaluation
* Structuring medium-sized Python projects

It serves as a solid starting point for experimenting with **chess engines, AI algorithms, and graphical interfaces**.
