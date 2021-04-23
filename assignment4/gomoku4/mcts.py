from typing import List, Tuple
import random

from board_util import GoBoardUtil, EMPTY
from simple_board import SimpleGoBoard

NUM_SIMULATION = 3000

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


    def getMove(self, board: SimpleGoBoard) -> int:
        # if already done, pass
        legal_moves = GoBoardUtil.generate_legal_moves_gomoku(board)
        if len(legal_moves) == 0:
            return 0
        if len(legal_moves) == 49:  # empty board
            return 36 # D4, the center
        isEnd, winner = board.check_game_end_gomoku()
        if isEnd:
            return 0
        
        return self.runSimulation(board)


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
        firstMoves, winner = self.computeMoves(board)
        toplay = board.current_player
        if winner != -1:
            return random.choice(firstMoves)
        if len(firstMoves) == 1:
            return firstMoves[0]
        
        toPlay = board.current_player
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

        highest = 0
        bestMove = 0 # TODO: 0 for debugging, replace with -> random.choice(firstMoves)
        for move in firstMoves:
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
        return bestMove


    def simulate(self, board: SimpleGoBoard) -> int:
        while True:
            hashKey = hash(board)
            toPlay = board.current_player
            if hashKey not in self.table:
                self.table[hashKey] = [None, None, None]
            if self.table[hashKey][toPlay] == None:
                moves, winner = self.computeMoves(board)
                data = NodeData(winner, moves)
                self.table[hashKey][toPlay] = data

            data = self.table[hashKey][toPlay]
            if data.winner == -1:   # not win yet
                # randomly make a move
                move = random.choice(data.moves)
                board.board[move] = toPlay
                board.current_player = GoBoardUtil.opponent(toPlay)
            else:   # winner can be determined
                return data.winner


    def computeMoves(self, board: SimpleGoBoard) -> Tuple[List[int], int]:
        legal_moves = GoBoardUtil.generate_legal_moves_gomoku(board)
        if len(legal_moves) == 0:
            return [], EMPTY    # draw
        isEnd, winner = board.check_game_end_gomoku()
        if isEnd:
            return [], winner
        # TODO: implement filters
        return legal_moves, -1


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
    
