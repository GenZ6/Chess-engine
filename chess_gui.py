import chess
import tkinter as tk
from chess_engine import choose_move

SQUARE = 80
BOARD = SQUARE * 8

LIGHT = "#f0d9b5"
DARK = "#b58863"
HIGHLIGHT = "#f7ec74"
MOVE_DOT = "#4caf50"

UNICODE_PIECES = {
    "P": "♙", "N": "♘", "B": "♗", "R": "♖", "Q": "♕", "K": "♔",
    "p": "♟", "n": "♞", "b": "♝", "r": "♜", "q": "♛", "k": "♚"
}


class ChessGUI:

    def __init__(self, root):

        self.root = root
        self.board = chess.Board()
        self.selected = None
        self.last_move = None
        self.move_number = 1

        frame = tk.Frame(root)
        frame.pack()

        self.canvas = tk.Canvas(frame, width=BOARD, height=BOARD)
        self.canvas.grid(row=0, column=0)

        self.sidebar = tk.Frame(frame, bg="#222")
        self.sidebar.grid(row=0, column=1, sticky="ns")

        self.moves = tk.Text(self.sidebar, width=22, height=28,
                             bg="#1e1e1e", fg="white",
                             font=("Arial", 11))
        self.moves.pack(padx=5, pady=5)

        self.evalbar = tk.Canvas(self.sidebar, width=30, height=BOARD)
        self.evalbar.pack()

        self.canvas.bind("<Button-1>", self.click)

        self.draw()

    # ------------------------

    def draw_board(self):

        for r in range(8):
            for c in range(8):

                color = LIGHT if (r+c) % 2 == 0 else DARK

                x1 = c * SQUARE
                y1 = r * SQUARE
                x2 = x1 + SQUARE
                y2 = y1 + SQUARE

                self.canvas.create_rectangle(x1, y1, x2, y2,
                                             fill=color,
                                             outline="")

    # ------------------------

    def highlight_last_move(self):

        if not self.last_move:
            return

        for sq in [self.last_move.from_square, self.last_move.to_square]:

            col = chess.square_file(sq)
            row = 7 - chess.square_rank(sq)

            x1 = col * SQUARE
            y1 = row * SQUARE
            x2 = x1 + SQUARE
            y2 = y1 + SQUARE

            self.canvas.create_rectangle(
                x1, y1, x2, y2,
                fill=HIGHLIGHT,
                outline=""
            )

    # ------------------------

    def highlight_moves(self, square):

        for move in self.board.legal_moves:

            if move.from_square == square:

                col = chess.square_file(move.to_square)
                row = 7 - chess.square_rank(move.to_square)

                x = col * SQUARE + SQUARE // 2
                y = row * SQUARE + SQUARE // 2

                self.canvas.create_oval(
                    x - 10, y - 10,
                    x + 10, y + 10,
                    fill=MOVE_DOT,
                    outline=""
                )

    # ------------------------

    def draw_pieces(self):

        for sq in chess.SQUARES:

            piece = self.board.piece_at(sq)

            if piece:

                col = chess.square_file(sq)
                row = 7 - chess.square_rank(sq)

                x = col * SQUARE + SQUARE // 2
                y = row * SQUARE + SQUARE // 2

                self.canvas.create_text(
                    x, y,
                    text=UNICODE_PIECES[piece.symbol()],
                    font=("Arial", 44)
                )

    # ------------------------

    def update_eval(self):

        self.evalbar.delete("all")

        score = self.simple_eval()

        score = max(-2000, min(2000, score))

        white = (score + 2000) / 4000

        h = BOARD * white

        self.evalbar.create_rectangle(0, 0, 30, BOARD-h, fill="black")
        self.evalbar.create_rectangle(0, BOARD-h, 30, BOARD, fill="white")

    # ------------------------

    def simple_eval(self):

        values = {
            chess.PAWN: 100,
            chess.KNIGHT: 320,
            chess.BISHOP: 330,
            chess.ROOK: 500,
            chess.QUEEN: 900
        }

        score = 0

        for p, v in values.items():

            score += len(self.board.pieces(p, chess.WHITE)) * v
            score -= len(self.board.pieces(p, chess.BLACK)) * v

        return score

    # ------------------------

    def draw(self):

        self.canvas.delete("all")

        self.draw_board()

        self.highlight_last_move()

        if self.selected:
            self.highlight_moves(self.selected)

        self.draw_pieces()

        self.update_eval()

    # ------------------------

    def click(self, event):

        col = event.x // SQUARE
        row = event.y // SQUARE

        square = chess.square(col, 7-row)

        if self.selected is None:

            piece = self.board.piece_at(square)

            if piece and piece.color == chess.WHITE:
                self.selected = square

        else:

            move = chess.Move(self.selected, square)

            if move in self.board.legal_moves:

                san = self.board.san(move)

                self.board.push(move)

                if self.board.turn == chess.BLACK:
                    self.moves.insert("end",
                                      f"{self.move_number}. {san} ")
                else:
                    self.moves.insert("end", f"{san}\n")
                    self.move_number += 1

                self.last_move = move
                self.selected = None

                self.draw()

                self.root.after(300, self.engine_turn)

            else:
                self.selected = None

        self.draw()

    # ------------------------

    def engine_turn(self):

        if self.board.is_game_over():
            return

        move = choose_move(self.board, time_limit=2)

        if move:

            san = self.board.san(move)

            self.board.push(move)

            self.moves.insert("end", f"{san}\n")

            self.last_move = move

        self.draw()


if __name__ == "__main__":

    root = tk.Tk()
    root.title("Python Chess Engine")

    ChessGUI(root)

    root.mainloop()
