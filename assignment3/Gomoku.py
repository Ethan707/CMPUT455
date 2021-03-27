#!/usr/local/bin/python3
# /usr/bin/python3
# Set the path to your python3 above

from typing import List, Tuple
import random

from gtp_connection import GtpConnection
from board_util import GoBoardUtil, EMPTY
from board import GoBoard

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
        self.name = "GomokuAssignment3"
        self.version = 1.0


    def get_move(self, board: GoBoardUtil, color: int) -> int:
        current = board.current_player
        board.current_player = color    # set the current player to the given color
        _, moves = self.generateRuleBasedMoves(board)
        board.current_player = current
        # randomly pick one of these moves
        move = moves[random.randrange(0, len(moves))]
        return move


    def generateRuleBasedMoves(self, board: GoBoard) -> Tuple[str, List[int]]:
        """
        return: (MoveType, MoveList)
        MoveType: {"Win", "BlockWin", "OpenFour", "BlockOpenFour", "Random"}
        MoveList: an unsorted List[int], each element is a move
        """
        self.board = board
        self.lines = self.getLinePositions()
        result = self.checkWin()
        if (len(result) > 0):
            return ("Win", result)

        result = self.checkBlockWin()
        if (len(result) > 0):
            return ("BlockWin", result)

        result = self.checkOpenFour()
        if (len(result) > 0):
            return ("OpenFour", result)

        result = self.checkBlockOpenFour()
        if (len(result) > 0):
            return ("BlockOpenFour", result)

        result = [self.generateRandomMove(board)]
        return ("Random", result)


    def checkWin(self) -> List[int]:
        """
        Check if the current player can win directly, return all winning moves if exist, [] otherwise.
        """
        current = self.board.current_player
        opponent = GoBoardUtil.opponent(current)
        winning_moves = []
        for line in self.lines:
            for i in range(len(line) - 4):
                emptyPos = -1
                for pos in line[i: i + 5]:  # get five consecutive positions in a line
                    color = self.board.get_color(pos)
                    if color == EMPTY:
                        if emptyPos == -1:
                            emptyPos = pos
                        else:   # more than 1 empty pos in this line
                            emptyPos = -1
                            break
                    elif color == opponent:
                        emptyPos = -1
                        break
                if emptyPos != -1 and emptyPos not in winning_moves:
                    winning_moves.append(emptyPos)
        return winning_moves


    def checkBlockWin(self) -> List[int]:
        """
        Check if the opponent can win directly, return all blocking moves if exist, [] otherwise.
        e.g.
        oo.oo, .oooo.
        """
        current = self.board.current_player
        self.board.current_player = GoBoardUtil.opponent(current)    # change to the opponent point of view
        blocking_moves = self.checkWin()
        self.board.current_player = current     # reset the current player
        return blocking_moves


    def checkOpenFour(self) -> List[int]:
        """
        Check if the current player can create an open four, i.e. .xxxx.,
        return all such moves if exist, [] otherwise.
        """
        current = self.board.current_player
        opponent = GoBoardUtil.opponent(current)
        winning_moves = []
        for line in self.lines:
            for i in range(len(line) - 5):  # get six consecutive positions in a line
                # check if the first and the last are empty
                if self.board.get_color(line[i]) != EMPTY or self.board.get_color(line[i + 5]) != EMPTY:
                    continue
                emptyPos = -1
                for pos in line[i + 1: i + 5]:
                    color = self.board.get_color(pos)
                    if color == EMPTY:
                        if emptyPos == -1:
                            emptyPos = pos
                        else:   # more than 1 empty pos in this line
                            emptyPos = -1
                            break
                    elif color == opponent:
                        emptyPos = -1
                        break
                if emptyPos != -1 and emptyPos not in winning_moves:
                    winning_moves.append(emptyPos)
        return winning_moves


    def checkBlockOpenFour(self) -> List[int]:
        """
        Check if the opponent can create an open four, return all blocking moves if exist, [] otherwise.
        """
        current = self.board.current_player
        opponent = GoBoardUtil.opponent(current)
        blocking_moves = []
        for line in self.lines:
            for i in range(len(line) - 5):  # get six consecutive positions in a line
                # check if the first and the last are empty
                if self.board.get_color(line[i]) != EMPTY or self.board.get_color(line[i + 5]) != EMPTY:
                    continue
                emptyPos = -1
                for pos in line[i + 1: i + 5]:
                    color = self.board.get_color(pos)
                    if color == EMPTY:
                        if emptyPos == -1:
                            emptyPos = pos
                        else:   # more than 1 empty pos in this line
                            emptyPos = -1
                            break
                    elif color == current:
                        emptyPos = -1
                        break
                if emptyPos != -1:
                    moves = [emptyPos]
                    if i == 0:
                        # e.g. for |.XX.X., blocking moves can be 0, 3, 5, | indicates the border
                        moves.append(line[5])
                        if emptyPos != line[1]:
                            moves.append(line[0])
                    elif i == len(line) - 6:
                        # e.g. for .XX.X.|, blocking moves can be 0, 3, 5, | indicates the border
                        moves.append(line[i])
                        if emptyPos != line[i + 4]:
                            moves.append(line[i + 5])
                    for move in moves:
                        if move not in blocking_moves:
                            blocking_moves.append(move)

        return blocking_moves


    def generateRandomMove(self, board: GoBoard) -> int:
        """
        Run N = 10 simulations for each legal move, return the one with the highest win percentage,
        return -1 if the borad is full.
        """
        NUM_SIMULATION = 10     # N = 10
        legal_moves = board.get_empty_points()
        highest_winrate = 0
        best_move = 0
        for move in legal_moves:
            result = [0, 0, 0]  # stores the simulation result, [EMPTY (draw), BLACK, WHITE]
            for _ in range(NUM_SIMULATION):
                winner = self.randomSimulate(board, move)
                result[winner] += 1
            winrate = (result[board.current_player] + 0.5 * result[EMPTY]) / NUM_SIMULATION
            if winrate == 1:
                return move
            if winrate > highest_winrate:
                highest_winrate = winrate
                best_move = move
        return best_move


    def randomSimulate(self, board: GoBoard, first_move: int) -> int:
        """
        The current player plays a stone at first_move, then two players play at random till the game is over.
        Returns the winner, either BLACK, WHITE, or EMPTY (draw).

        This function uses random.randrange() to choose a move at random. 
        According to the python docs, randrange() is sophisticated about producing equally distributed (uniformly) values 
        since python 3.2.
        Reference: https://docs.python.org/3/library/random.html#random.randint
        """
        board_copy = board.copy()
        board_copy.play_move(first_move)
        winner = board_copy.detect_five_in_a_row()
        legal_moves = board_copy.get_empty_points()
        while winner == EMPTY and len(legal_moves) != 0: # if the game is not over
            # choose a move at random
            random_move = legal_moves[random.randrange(0, len(legal_moves))]
            board_copy.play_move(random_move, board_copy.current_player)
            # update
            winner = board_copy.detect_five_in_a_row()
            legal_moves = board_copy.get_empty_points()
        return winner


    def getLinePositions(self) -> List[List[int]]:
        """
        Get the positions of each row, col, and diagonal.
        """
        lines = []
        for line in self.board.rows:
            lines.append(line)
        for line in self.board.cols:
            lines.append(line)
        for line in self.board.diags:
            lines.append(line)
        return lines


def run():
    """
    start the gtp connection and wait for commands.
    """
    board = GoBoard(7)
    con = GtpConnection(Gomoku(), board)
    con.start_connection()


if __name__ == "__main__":
    run()
