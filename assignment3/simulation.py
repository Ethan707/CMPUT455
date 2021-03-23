from typing import List, Tuple

def generateRuleBasedMoves(board) -> Tuple[str, List[int]]:
    """
    return: (MoveType, MoveList)
    MoveType: {"Win", "BlockWin", "OpenFour", "BlockOpenFour", "Random"}
    MoveList: an unsorted List[int], each element is a move
    """
    result = checkWin(board)
    if (len(result) > 0):
        return ("Win", result)
    
    result = checkBlockWin(board)
    if (len(result) > 0):
        return ("BlockWin", result)
    
    result = checkOpenFour(board)
    if (len(result) > 0):
        return ("OpenFour", result)
    
    result = checkBlockOpenFour(board)
    if (len(result) > 0):
        return ("BlockOpenFour", result)

    result = [generateRuleBasedMoves(board)]
    return ("Random", result)

def checkWin(board) -> List[int]:
    """
    Check if the current player can win directly, return winning moves if exist, [] otherwise.
    """
    toPlay = board.current_player
    raise NotImplementedError

def checkBlockWin(board) -> List[int]:
    """
    Check if the opponent can win directly, return all blocking moves if exist, [] otherwise.
    e.g.
    oo.oo, .oooo.
    """
    raise NotImplementedError

def checkOpenFour(board) -> List[int]:
    """
    Check if the current player can create an open four, i.e. .xxxx.,
    return all such moves if exist, [] otherwise.
    """
    raise NotImplementedError

def checkBlockOpenFour(board) -> List[int]:
    """
    Check if the opponent can create an open four, return all blocking moves if exist, [] otherwise.
    """
    raise NotImplementedError

def generateRandomMove(board) -> int:
    """
    Run N = 10 simulations for each legal move, return the one with the highest win percentage,
    return -1 if the borad is full.
    """
    raise NotImplementedError
