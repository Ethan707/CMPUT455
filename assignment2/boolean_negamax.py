from typing import Tuple

from board import GoBoard
from board_util import (GoBoardUtil, BLACK, WHITE, EMPTY, BORDER)
from transposition import TranspositionTable
from ZobristHash import ZobristHash

def log(msg: str):
    with open("temp.log", 'a') as file:
        file.write(msg)
        file.write('\n')


class BooleanNegamax:
    def __init__(self, board, toPlay) -> None:
        self.board = board
        self.toPlay = toPlay
        self.transpositionTable = TranspositionTable()
        self.hasher = ZobristHash(self.board.size)
    
    def solve(self) -> Tuple[int, int]:
        """
        Returns (winner, move)
        winner: {BLACK, WHITE, BOARD (draw)}
        """
        winner = self.result = self.board.detect_five_in_a_row()
        if winner != EMPTY:
            return winner, -1
        legal_moves = GoBoardUtil.generate_legal_moves(self.board, self.board.current_player)
        assert(len(legal_moves) != 0)
        draw_move = -1
        for m in legal_moves:
            self.board.play_move(m, self.board.current_player)
            winner = self.boolean_negamax_hash()
            if winner == self.toPlay:
                return self.toPlay, m
            if winner == BORDER:
                draw_move = m
            self.board.undo_move(m)
        if draw_move != -1:
            return BORDER, draw_move
        return GoBoardUtil.opponent(self.toPlay), -1

    def boolean_negamax_hash(self) -> int:
        """
        Returns either {BLACK, WHITE, BORDER (indicates a draw)}
        """
        # check in transpositionTable
        hash_code = self.hasher.hash(GoBoardUtil.get_oneD_board(self.board))
        found_in_table = self.transpositionTable.lookup(hash_code)
        if found_in_table != None:
            return found_in_table
        winner = self.boolean_negamax()
        log("winner " + str(winner))
        # store in table
        self.transpositionTable.store(hash_code, winner)
        return winner

    def boolean_negamax(self) -> int:
        # search children
        if self.current_can_win():
            return self.board.current_player
        # TODO: if the opponent may win, the current player must play to block.
        winner = self.board.detect_five_in_a_row()
        if winner != EMPTY:
            return winner

        legal_moves = GoBoardUtil.generate_legal_moves(self.board, self.board.current_player)
        if len(legal_moves) == 0:  
            return BORDER   # BORDER indicates a draw

        hasDraw = False
        for m in legal_moves:
            self.board.play_move(m, self.board.current_player)
            winner = self.boolean_negamax_hash()
            self.board.undo_move(m)
            if winner == BORDER:
                hasDraw = True
            elif winner == self.board.current_player:
                return winner
        if hasDraw:
            return BORDER
        return GoBoardUtil.opponent(self.board.current_player)

    def current_can_win(self) -> int:
        """
        Evaluates if the current player can win.
        Returns move if the current player can win, -1 if the current player cannot.
        """
        result = self.checkImmediateWin()
        return result != -1
    
    def checkImmediateWin(self) -> int:
        """
        Returns (CanImmediateWin, move).
        Patterns:
        - .xxxx
        - x.xxx
        - xx.xx
        - xxx.x
        - xxxx.
        """
        size = self.board.size
        for i in range(len(self.board.rows)):
            row = self.board.rows[i]
            result = self.checkImmediateWinLine(row)
            if result != -1:
                return i * size + result
        for i in range(len(self.board.cols)):
            col = self.board.cols[i]
            result = self.checkImmediateWinLine(row)
            if result != -1:
                return result * size + i
        for i in range(len(self.board.diags)):
            diag = self.board.diags[i]
            result = self.checkImmediateWinLine(row)
            if result != -1:
                return result
        return -1

    def checkImmediateWinLine(self, line) -> Tuple[bool, int]:
        count = 0
        emptyPosition = -1
        for i in range(len(line)):
            point = line[i]
            if point == self.toPlay:
                if count != 0:
                    count += 1
                else:
                    count = 1
            elif point == EMPTY:
                if emptyPosition != -1:
                    count = 0
                emptyPosition = i
            else:
                count = 0
            
            if count == 4:
                return emptyPosition
        return -1


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

