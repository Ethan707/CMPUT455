from typing import Tuple
from board_util import GoBoardUtil
from board import GoBoard
from ZobristHash import ZobristHash
from transposition import TranspositionTable
import math


def storeResult(tt: TranspositionTable, code, result):
    tt.store(code, result)
    return result


def alphabeta(state: GoBoard, alpha, beta, tt: TranspositionTable,
              hasher: ZobristHash):
    code = hasher.hash(GoBoardUtil.get_oneD_board(state))
    result = tt.lookup(code)

    if result != None:
        return result

    if state.endOfGame():
        result = (state.staticallyEvaluateForToPlay(), -1)
        return storeResult(tt, code, result)

    bestMoves = state.bestMoves()
    move = bestMoves[0]
    for m in bestMoves:
        state.play_move(m, state.current_player)
        (value, _) = alphabeta(state, -beta, -alpha, tt, hasher)
        value = -value
        if value > alpha:
            alpha = value
        state.undoMove(m)
        if value >= beta:
            result = (alpha, move)
            storeResult(tt, code, result)
            return result  # or value in failsoft (later)
    result = (alpha, move)
    return storeResult(tt, code, result)