#!/usr/local/bin/python3
# /usr/bin/python3
# Set the path to your python3 above

from gtp_connection import GtpConnection
from board_util import GoBoardUtil
from board import GoBoard
from alphabeta import compute_winner
import signal
from typing import Tuple


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

    # TODO: Modify the code
    def get_move(self, board, color, time):
        _, move = self.solve(board, time)
        if move != None:
            return move
        else:
            return GoBoardUtil.generate_random_move(board, color)


    def solve(self, board, time_limit: int) -> Tuple[str, int]:
        """
        Attempts to compute the winner of the current position, assuming perfect play by both, 
        within the current time limit.
        Returns: (winner, move).
            winner: either b, w, draw, unknown (if solve runs out of the time)
            move: the first move that achieves the result if the winner is toPlay or it is a draw,
                -1 if the winner is the opponent of toPlay or its unknown
        """
        def timeout_handler(sig, frame):
            raise TimeoutError

        signal.signal(signal.SIGALRM, timeout_handler)
        signal.alarm(time_limit)
        try:
            # TODO: implement compute_winner
            winner, move = compute_winner(board.copy())
        except TimeoutError:
            # if compute_winner() times out
            winner, move = "unknown", -1

        return winner, move


def run():
    """
    start the gtp connection and wait for commands.
    """
    board = GoBoard(7)
    con = GtpConnection(Gomoku(), board)
    con.start_connection()


if __name__ == "__main__":
    run()
