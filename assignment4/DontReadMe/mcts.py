from typing import List, Tuple
import random
import signal

from board_util import GoBoardUtil, EMPTY, BORDER
from simple_board import SimpleGoBoard

# configs
NUM_SIMULATION = 1000
SIMULATION_TIME_LIMIT = 50 # seconds


class NodeData:
    def __init__(self, winner: int = -1, moves: List[int] = [], numVisited: int = 0, numWins: int = 0):
        self.winner = winner # BLACK, WHITE, DRAW if this is a terminal state, -1 otherwise
        self.moves = moves
        self.numVisited = numVisited
        self.numWins = numWins


class MCTSEngine:
    def __init__(self):
        """
        self.table: dict
            key: hashKey: int
            value: List[NodeData] (len 3, index: BLACK or WHITE)
        """
        self.table = dict()
        self.numSimulation = NUM_SIMULATION
        self.initLines()


    def getMove(self, board: SimpleGoBoard) -> int:
        # it is garenteed that there is at least one possible move
        legal_moves = GoBoardUtil.generate_legal_moves_gomoku(board)
        if len(legal_moves) == 49:  # empty board
            return 36 # D4, the center
        
        try:
            signal.alarm(SIMULATION_TIME_LIMIT)
            bestMove = self.runSimulation(board)
            signal.alarm(0)
        except:
            bestMove = self.getBestMove(board, legal_moves)
        return bestMove

    def getBestMove(self, board: SimpleGoBoard, moves: List[int]) -> int:
        highest = 0
        bestMove = 0
        toplay = board.current_player
        for move in moves:
            board.board[move] = toplay
            hashKey = hash(board)
            board.board[move] = EMPTY
            if hashKey not in self.table:
                continue
            data = self.table[hashKey][toplay]
            if data == None:
                continue
            winrate = data.numWins / data.numVisited
            if winrate > highest:
                highest = winrate
                bestMove = move
        if bestMove == 0:
            return random.choice(moves)
        return bestMove


    def saveToDict(self, hashKey: int, toplay: int, data: NodeData) -> None:
        if hashKey not in self.table:
            self.table[hashKey] = [None, None, None]
        self.table[hashKey][toplay] = data


    def getNodeData(self, hashKey: int, toplay: int) -> NodeData:
        if hashKey not in self.table:
            self.table[hashKey] = [None, None, None]
        data = self.table[hashKey][toplay]
        if data == None:
            data = NodeData()
            self.table[hashKey][toplay] = data
        return data

    
    def runSimulation(self, board: SimpleGoBoard) -> None:
        toplay = board.current_player
        firstMoves, winner = self.computeMoves(board, toplay)
        if winner != -1:
            return random.choice(firstMoves)
        if len(firstMoves) == 1:
            return firstMoves[0]
        
        for i in range(self.numSimulation):
            boardCopy = board.copy()
            firstMove = random.choice(firstMoves)
            boardCopy.play_move_gomoku(firstMove, boardCopy.current_player)
            hashKey = hash(boardCopy)
            winner = self.simulate(boardCopy)
            data = self.getNodeData(hashKey, toplay)
            data.numVisited += 1
            if winner == toplay:
                data.numWins += 1
        return self.getBestMove(board, firstMoves)


    def simulate(self, board: SimpleGoBoard) -> int:
        while True:
            hashKey = hash(board)
            toplay = board.current_player
            if hashKey not in self.table:
                self.table[hashKey] = [None, None, None]
            if self.table[hashKey][toplay] == None:
                moves, winner = self.computeMoves(board, toplay)
                data = NodeData(winner, moves)
                self.table[hashKey][toplay] = data

            data = self.table[hashKey][toplay]
            if data.winner == -1:   # not win yet
                # randomly make a move
                move = random.choice(data.moves)
                board.board[move] = toplay
                board.current_player = GoBoardUtil.opponent(toplay)
            else:   # winner can be determined
                data.numVisited += 1
                if toplay == data.winner:
                    data.numWins += 1
                return data.winner


    def computeMoves(self, board: SimpleGoBoard, toplay: int) -> Tuple[List[int], int]:
        legal_moves = GoBoardUtil.generate_legal_moves_gomoku(board)
        if len(legal_moves) == 0:
            return None, EMPTY    # draw
        isEnd, winner = board.check_game_end_gomoku()
        if isEnd:
            return None, winner
        
        opponent = GoBoardUtil.opponent(toplay)
        newMoves = []
        for move in legal_moves:
            board.board[move] = toplay
            lines = self.getCorrespondingLines(board, move)
            if self.computeMovesCanWin(board, toplay, lines):    # can win
                return [move], toplay
            if self.computeMovesCanWin(board, opponent, lines):  # block win
                return [move], -1
            if self.computeMovesHasOpenFour(board, toplay, lines):
                newMoves.append(move)
            if self.computeMovesHasOpenFour(board, opponent, lines): # block open four
                return [move], -1
            board.board[move] = EMPTY

        if len(newMoves) != 0:
            return newMoves, toplay
        return legal_moves, -1


    def computeMovesCanWin(self, board: SimpleGoBoard, toplay: int, lines: List[int]) -> bool:
        for line in lines:
            for i in range(len(line) - 4):
                count = 0
                for j in range(i, i + 5):
                    pos = line[j]
                    if board.board[pos] == toplay:
                        count += 1
                if count == 5:
                    return True
        return False


    def computeMovesHasOpenFour(self, board: SimpleGoBoard, toplay: int, lines: List[int]) -> bool:
        for line in lines:
            for i in range(len(line) - 5):
                if board.board[line[i]] != EMPTY or board.board[line[i + 5]] != EMPTY:
                    continue
                count = 0
                for j in range(i + 1, i + 5):
                    pos = line[j]
                    if board.board[pos] == toplay:
                        count += 1
                if count == 4:
                    return True
        return False


    def initLines(self):
        self.rows = [
            [ 9, 10, 11, 12, 13, 14, 15], 
            [17, 18, 19, 20, 21, 22, 23], 
            [25, 26, 27, 28, 29, 30, 31], 
            [33, 34, 35, 36, 37, 38, 39], 
            [41, 42, 43, 44, 45, 46, 47], 
            [49, 50, 51, 52, 53, 54, 55], 
            [57, 58, 59, 60, 61, 62, 63]
        ]
        self.cols = [
            [ 9, 17, 25, 33, 41, 49, 57], 
            [10, 18, 26, 34, 42, 50, 58], 
            [11, 19, 27, 35, 43, 51, 59], 
            [12, 20, 28, 36, 44, 52, 60], 
            [13, 21, 29, 37, 45, 53, 61], 
            [14, 22, 30, 38, 46, 54, 62], 
            [15, 23, 31, 39, 47, 55, 63]
        ]
        self.diags1 = [ 
            [ 9, 18, 27, 36, 45, 54, 63],
            [10, 19, 28, 37, 46, 55], 
            [11, 20, 29, 38, 47], 
            [12, 21, 30, 39], 
            [13, 22, 31], 
            [14, 23], 
            [15],
            [17, 26, 35, 44, 53, 62], 
            [25, 34, 43, 52, 61], 
            [33, 42, 51, 60], 
            [41, 50, 59], 
            [49, 58], 
            [57]
        ]
        self.diags2 = [
            [9],
            [10, 17],
            [11, 18, 25],
            [12, 19, 26, 33],
            [13, 20, 27, 34, 41],
            [14, 21, 28, 35, 42, 49],
            [15, 22, 29, 36, 43, 50, 57], 
            [23, 30, 37, 44, 51, 58], 
            [31, 38, 45, 52, 59], 
            [39, 46, 53, 60], 
            [47, 54, 61], 
            [55, 62], 
            [63]  
        ]
        self.lines = []
        for row in self.rows:
            self.lines.append(row)
        for col in self.cols:
            self.lines.append(col)
        self.diag1Dict = {}
        for i in range(len(self.diags1)):
            diag = self.diags1[i]
            self.lines.append(diag)
            for p in diag:
                self.diag1Dict[p] = i
        self.diag2Dict = {}
        for i in range(len(self.diags2)):
            diag = self.diags2[i]
            self.lines.append(diag)
            for p in diag:
                self.diag2Dict[p] = i


    def getCorrespondingLines(self, board: SimpleGoBoard, pos: int) -> List[List[int]]:
        """
        Returns the *positions* of the horizontal, vertical, and diagonal lines where pos is located.
        """
        row = self.rows[pos // 8 - 1]
        col = self.cols[pos % 8 - 1]
        diag1 = self.diags1[self.diag1Dict[pos]]
        diag2 = self.diags2[self.diag2Dict[pos]]
        lines = [row, col, diag1, diag2]
        return lines


    def filterMoves(self, board: SimpleGoBoard, legal_moves: List[int], color: int) -> Tuple[int, List[int]]:
        """
        Check if the game can be determined
        """
        if len(legal_moves) == 0:
            return EMPTY, []
        
        isEnd, winner = board.check_game_end_gomoku()
        if isEnd:
            return winner, []
        
        opponent = GoBoardUtil.opponent(color)
        if self.hasOpenFour(board, opponent):
            return opponent, []
        
        for move in legal_moves:
            board.board[move] = color
            if board.point_check_game_end_gomoku(move):
                return color, []
            if self.hasOpenFour(board, color):
                return color, []
            
            board.board[move] = opponent
            if self.hasOpenFour(board, opponent):
                return -1, [move]
        
        return -1, legal_moves
    

    def hasOpenFour(self, board: SimpleGoBoard, color: int) -> bool:
        """
        for line in self.lines:
            for i in range(len(line) - 5):  # get six consecutive positions in a line
                # check if the first and the last are empty
                if board.get_color(line[i]) != EMPTY or board.get_color(line[i + 5]) != EMPTY:
                    continue
                emptyPos = -1
                for pos in line[i + 1: i + 5]:
                    pc = board.get_color(pos)
                    if pc == EMPTY:
                        if emptyPos == -1:
                            emptyPos = pos
                        else:   # more than 1 empty pos in this line
                            emptyPos = -1
                            break
                    elif pc != color:
                        emptyPos = -1
                        break
                if emptyPos != -1:
                    return True
        """
        return False
    
