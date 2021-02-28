from typing import Tuple

from board import GoBoard
from board_util import (GoBoardUtil, BLACK, WHITE, EMPTY, BORDER)

class BooleanNegamax:
    def __init__(self, board, toPlay) -> None:
        self.board = board
        self.toPlay = toPlay
        self.move = -1
    
    def solve(self) -> Tuple[int, int]:
        """
        Returns (winner, move)
        winner: {BLACK, WHITE, BOARD (draw)}
        """
        boolean_negamax()
        return self.winner, self.move

    def boolean_negamax(self) -> bool:
        winner = self.board.detect_five_in_a_row()
        if winner != EMPTY:
            self.result = winner
            return winner == self.toPlay
        legal_moves = GoBoardUtil.generate_legal_moves(self.board, self.board.current_player)
        if len(legal_moves) == 0:
            self.result = BORDER    # winner == BORDER indicates a draw
            return True
        for m in legal_moves:
            self.board.play_move(m, self.board.current_player)
            success = not boolean_negamax(self.board)
            self.board.undo_move(m)
            if success:
                if self.move == -1:
                    self.move = m   # record the winning move
                return True
        return False


def compute_winner(board: GoBoard) -> Tuple[str, int]:
    """
    Returns (winner, move)
    """
    toPlay = board.current_player
    winner, move = BooleanNegamax(board, toPlay).solve()
    if winner == BLACK:
        winner_str = "b"
    elif winner == WHITE:
        winner_str = "w"
    else:
        winner_str = "draw"
    return winner_str, move
    

def boolean_negamax(state: GoBoard) -> bool:
    winner = state.detect_five_in_a_row()
    if winner != EMPTY:
        return winner
    legal_moves = GoBoardUtil.generate_legal_moves(state, state.current_player)
    if len(legal_moves) == 0:
        return BORDER   # winner = BORDER indicates a draw
    for m in legal_moves:
        state.play_move(m, state.current_player)
        success = not boolean_negamax(state)
        state.undo_move(m)
        if success:
            return True
    return False
