import chess
import time

INF = 10**9

VALUES = {
    chess.PAWN:100,
    chess.KNIGHT:320,
    chess.BISHOP:330,
    chess.ROOK:500,
    chess.QUEEN:900,
    chess.KING:0
}

TT = {}
KILLERS = {}

SEARCH_END = 0


def evaluate(board):

    score = 0

    for p,v in VALUES.items():
        score += len(board.pieces(p,chess.WHITE))*v
        score -= len(board.pieces(p,chess.BLACK))*v

    if len(board.pieces(chess.BISHOP,chess.WHITE)) >= 2:
        score += 30

    if len(board.pieces(chess.BISHOP,chess.BLACK)) >= 2:
        score -= 30

    return score


def order_moves(board, depth):

    moves = list(board.legal_moves)

    def score(move):

        s = 0

        if board.is_capture(move):
            victim = board.piece_at(move.to_square)
            if victim:
                s += VALUES[victim.piece_type]

        if depth in KILLERS and move in KILLERS[depth]:
            s += 900

        if move.promotion:
            s += 800

        return s

    moves.sort(key=score, reverse=True)

    return moves


def quiescence(board, alpha, beta):

    stand = evaluate(board)

    if stand >= beta:
        return beta

    if alpha < stand:
        alpha = stand

    for move in board.generate_legal_captures():

        board.push(move)

        score = -quiescence(board, -beta, -alpha)

        board.pop()

        if score >= beta:
            return beta

        if score > alpha:
            alpha = score

    return alpha


def negamax(board, depth, alpha, beta):

    global SEARCH_END

    if time.time() > SEARCH_END:
        return evaluate(board), None

    key = board._transposition_key()

    if key in TT and TT[key][0] >= depth:
        return TT[key][1], None

    if depth == 0 or board.is_game_over():
        return quiescence(board, alpha, beta), None

    best_move = None
    best_val = -INF

    for move in order_moves(board, depth):

        board.push(move)

        val,_ = negamax(board, depth-1, -beta, -alpha)

        val = -val

        board.pop()

        if val > best_val:
            best_val = val
            best_move = move

        if best_val > alpha:
            alpha = best_val

        if alpha >= beta:

            if depth not in KILLERS:
                KILLERS[depth] = []

            KILLERS[depth].append(move)

            break

    TT[key] = (depth, best_val)

    return best_val, best_move


def choose_move(board, time_limit=3):

    global SEARCH_END

    SEARCH_END = time.time() + time_limit

    best_move = None

    for depth in range(1,8):

        if time.time() > SEARCH_END:
            break

        val,move = negamax(board, depth, -INF, INF)

        if move:
            best_move = move

    return best_move
