#!/usr/local/bin/python3
# /usr/bin/python3
# Set the path to your python3 above

from gtp_connection import GtpConnection
from board_util import GoBoardUtil
from board import GoBoard
from alphabeta import callAlphabeta
import signal
import alphabeta


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

    def get_move(self, board, color, time, alphaBeta: alphabeta):
        _, move = self.solve(board, time, alphaBeta)
        if move != None:
            return move
        else:
            return GoBoardUtil.generate_random_move(board, color)

    def solve(self, board, time_limit, alphaBeta: alphabeta):
        def timeout_handler(sig, frame):
            raise TimeoutError

        signal.signal(signal.SIGALRM, timeout_handler)
        signal.alarm(time_limit)

        board_copy = board.copy()
        try:
            score, move = alphaBeta.callAlphabeta(board_copy)
        except TimeoutError:
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
