from typing import List, Tuple

from board import GoBoard
from board_util import GoBoardUtil, EMPTY
# from log_engine import LogEngine

# logEngine = LogEngine()

def generateRuleBasedMoves(board: GoBoard) -> Tuple[str, List[int]]:
    """
    return: (MoveType, MoveList)
    MoveType: {"Win", "BlockWin", "OpenFour", "BlockOpenFour", "Random"}
    MoveList: an unsorted List[int], each element is a move
    """
    # logEngine.printBoard(board)
    lines = getLinePositions(board)
    result = checkWin(board, lines)
    if (len(result) > 0):
        return ("Win", result)
    
    result = checkBlockWin(board, lines)
    if (len(result) > 0):
        return ("BlockWin", result)
    
    result = checkOpenFour(board, lines)
    if (len(result) > 0):
        return ("OpenFour", result)
    
    result = checkBlockOpenFour(board, lines)
    if (len(result) > 0):
        return ("BlockOpenFour", result)

    result = [generateRandomMove(board)]
    return ("Random", result)

def checkWin(board: GoBoard, lines: List[List[int]]) -> List[int]:
    """
    Check if the current player can win directly, return all winning moves if exist, [] otherwise.
    """
    current = board.current_player
    opponent = GoBoardUtil.opponent(current)
    winning_moves = []
    for line in lines:
        for i in range(len(line) - 4):
            emptyPos = -1
            for pos in line[i: i + 5]:  # get five consecutive positions in a line
                color = board.get_color(pos)
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


def checkBlockWin(board: GoBoard, lines: List[List[int]]) -> List[int]:
    """
    Check if the opponent can win directly, return all blocking moves if exist, [] otherwise.
    e.g.
    oo.oo, .oooo.
    """
    current = board.current_player
    board.current_player = GoBoardUtil.opponent(current)    # change to the opponent point of view
    blocking_moves = checkWin(board, lines)
    board.current_player = current  # reset
    return blocking_moves


def checkOpenFour(board: GoBoard, lines: List[List[int]]) -> List[int]:
    """
    Check if the current player can create an open four, i.e. .xxxx.,
    return all such moves if exist, [] otherwise.
    """
    current = board.current_player
    opponent = GoBoardUtil.opponent(current)
    winning_moves = []
    for line in lines:
        for i in range(len(line) - 5):  # get six consecutive positions in a line
            # check if the first and the last are empty
            if board.get_color(line[i]) != EMPTY or board.get_color(line[i + 5]) != EMPTY:
                continue
            emptyPos = -1
            for pos in line[i + 1: i + 5]:
                color = board.get_color(pos)
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


def checkBlockOpenFour(board: GoBoard, lines: List[List[int]]) -> List[int]:
    """
    Check if the opponent can create an open four, return all blocking moves if exist, [] otherwise.
    """
    current = board.current_player
    board.current_player = GoBoardUtil.opponent(current)    # change to the opponent point of view
    blocking_moves = checkOpenFour(board, lines)
    board.current_player = current  # reset
    return blocking_moves


def generateRandomMove(board: GoBoard) -> int:
    """
    Run N = 10 simulations for each legal move, return the one with the highest win percentage,
    return -1 if the borad is full.
    """
    # TODO: to be implemented!
    return 1


def getLinePositions(board: GoBoard) -> List[List[int]]:
    """
    Get the positions of each row, col, and diagonal.
    """
    lines = []
    for line in board.rows:
        lines.append(line)
    for line in board.cols:
        lines.append(line)
    for line in board.diags:
        lines.append(line)
    return lines
