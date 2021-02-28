from board_util import GoBoardUtil
from board import GoBoard
from ZobristHash import ZobristHash
from transposition import TranspositionTable
import math


class alphabeta:
    def __init__(self, board: GoBoard):
        self.board = board
        self.hasher = ZobristHash(self.board.size)

    def alphabeta(self, state: GoBoard, alpha, beta):
        hash = self.hasher.hash(GoBoardUtil.get_oneD_board(state))
        if state.endOfGame():
            pass
            # return state.staticallyEvaluateForToPlay()

        for m in state.legalMoves():
            state.play_move(m, state.current_player)
            value = -alphabeta(state, -beta, -alpha)
            if value > alpha:
                alpha = value
            state.undoMove(m)
            if value >= beta:
                return beta  # or value in failsoft (later)
        return alpha

    # initial call with full window
    def callAlphabeta(rootState):
        return alphabeta(rootState, -math.inf, math.inf)
