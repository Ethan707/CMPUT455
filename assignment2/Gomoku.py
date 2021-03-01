#!/usr/local/bin/python3
# /usr/bin/python3
# Set the path to your python3 above

from gtp_connection import GtpConnection
from board_util import BLACK, WHITE, GoBoardUtil
from board import GoBoard
from Alphabeta import alphabeta
import math
import signal


class Gomoku():
    def __init__(self):
        """
        Gomoku player that selects moves randomly from the set of legal moves.
        Passes/resigns only at the end of the game.

        Parameters
        ----------
        name : str
            name of the player (used by the GTP interface).
        version : float
            version number (used by the GTP interface).
        """
        self.name = "GomokuAssignment2"
        self.version = 1.0

    def get_move(self, board, color, time_limit, tt, hash):
        _, move = self.solve(board, time_limit, tt, hash)
        if move != -1:
            return move
        else:
            return GoBoardUtil.generate_random_move(board, color)

    def solve(self, board: GoBoard, time_limit, tt, hasher):
        def timeout_handler(sig, frame):
            raise TimeoutError

        signal.signal(signal.SIGALRM, timeout_handler)
        signal.alarm(time_limit)

        board_copy = board.copy()
        try:
            (value, move) = alphabeta(board_copy, -math.inf, math.inf, tt,
                                      hasher)
            # print(value, move)
            if value == 0:
                # draw
                return "draw", move
            if value > 0:
                # win
                if board.current_player == BLACK:
                    return 'b', move
                if board.current_player == WHITE:
                    return 'w', move
            else:
                opponent = GoBoardUtil.opponent(board.current_player)
                if opponent == BLACK:
                    return 'b', None
                if opponent == WHITE:
                    return 'w', None
        except Exception:
            return "unknown", None
        finally:
            signal.alarm(0)


def run():
    """
    start the gtp connection and wait for commands.
    """
    board = GoBoard(7)
    con = GtpConnection(Gomoku(), board)
    con.start_connection()


if __name__ == "__main__":
    run()
