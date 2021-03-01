from board import GoBoard
from board_util import GoBoardUtil
from transpositiontable import TranspositionTable
from zobrist import ZobristHash
INFINITY = 10000


def storeResult(tt, code, result):
    tt.store(code, result)
    return result


def alphabeta(state: GoBoard, alpha, beta, tt: TranspositionTable,
              hasher: ZobristHash):
    code = hasher.hash(GoBoardUtil.get_oneD_board(state))
    result = tt.lookup(code)

    if result != None:
        return result

    if state.endOfGame():
        result = (state.evaluate(), None)
        storeResult(tt, code, result)
        return result

    moves = state.get_best_moves()
    move = moves[0]

    for move in moves:
        state.play_move(move, state.current_player)
        (value, _) = alphabeta(state, -beta, -alpha, tt, hasher)
        value = -value
        if value > alpha:
            alpha = value
            move = move
        state.undoMove(move)
        if value >= beta:
            result = (beta, move)
            storeResult(tt, code, result)
            return result

    result = (alpha, move)
    storeResult(tt, code, result)
    return result


# initial call with full window
def call_alphabeta(rootState, tt, hasher):
    return alphabeta(rootState, -INFINITY, INFINITY, tt, hasher)
