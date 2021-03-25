from typing import List
from board import GoBoard

class LogEngine:
    def __init__(self, filename: str = "temp.log") -> None:
        self.file = open(filename, 'w')

    def log(self, msg: str) -> None:
        self.file.write(msg)
        self.file.write('\n')

    def logPositions(self, board: GoBoard, positions: List[int]) -> None:
        NS = board.size + 1
        moves = []
        for pos in positions:
            move_coord = point_to_coord(pos, board.size)
            moves.append(format_point(move_coord))
        self.file.write("[" + ", ".join(moves) + "]\n")
    
    def printBoard(self, board: GoBoard) -> None:
        self.file.write("current player: " + str(board.current_player) + "\n")
        # print header
        self.file.write("   ")
        i = ord('A')
        for _ in range(board.size):
            self.file.write(chr(i) + " ")
            i += 1
        self.file.write('\n')
        i = 1
        for row in board.rows:
            self.file.write(str(i) + "| ")
            i += 1
            for pos in row:
                self.file.write(str(board.get_color(pos)) + " ")
            self.file.write('\n')
        self.file.write('\n')

    def close(self) -> None:
        self.file.close()


def point_to_coord(point, boardsize):
    """
    Transform point given as board array index 
    to (row, col) coordinate representation.
    Special case: PASS is not transformed
    """
    NS = boardsize + 1
    return divmod(point, NS)


def format_point(move):
    """
    Return move coordinates as a string such as 'A1', or 'PASS'.
    """
    column_letters = "ABCDEFGHJKLMNOPQRSTUVWXYZ"
    row, col = move
    return column_letters[col - 1] + str(row)
