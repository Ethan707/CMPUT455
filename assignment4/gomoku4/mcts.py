from typing import List, Tuple
import random

from board_util import GoBoardUtil, EMPTY
from simple_board import SimpleGoBoard

NUM_SIMULATION = 5000

class NodeData:
    def __init__(self, winner: int, moves: List[int]):
        self.winner = winner
        self.moves = moves

class MCTS:
    def __init__(self, board: SimpleGoBoard):
        self.board = board
        """
        self.table: dict
            key: hashKey: int
            value: List[NodeData] (len 3, index: BLACK or WHITE)
        """
        self.table = dict()
    

    def getMove(self) -> int:
        # if already done, pass
        legal_moves = GoBoardUtil.generate_legal_moves_gomoku(self.board)
        if len(legal_moves) == 0:
            return 0
        isEnd, winner = self.board.check_game_end_gomoku()
        if isEnd:
            return 0
        return self.simulate()


    def simulate(self) -> int:
        scores = {}
        toPlay = self.board.current_player
        firstMoves = self.computeFirstMoves()
        if len(firstMoves) == 0:
            return 0
        for i in range(NUM_SIMULATION):
            boardCopy = self.board.copy()
            move, winner = self.simulateOnce(boardCopy, firstMoves)
            if move not in scores:
                scores[move] = 0
            if winner == EMPTY:
                scores[move] += 1
            elif winner == toPlay:
                scores[move] += 100
            else:
                scores[move] -= 100
        highestScore = -10000000
        bestMove = 0
        for move, score in scores.items():
            if score > highestScore:
                highestScore = score
                bestMove = move
        return bestMove
    
    def computeFirstMoves(self):
        boardCopy = self.board.copy()
        toPlay = boardCopy.current_player
        legal_moves = GoBoardUtil.generate_legal_moves_gomoku(boardCopy)
        winner, moves = self.filterMoves(boardCopy, legal_moves, toPlay)
        return moves
    
    def simulateOnce(self, board: SimpleGoBoard, firstMoves: List[int]) -> int:
        """
        Return (move, winner)
        """
        # randomly make a move
        firstMove = random.choice(firstMoves)
        toPlay = board.current_player
        board.board[firstMove] = toPlay
        board.current_player = GoBoardUtil.opponent(toPlay)

        while True:
            hashKey = hash(board)
            toPlay = board.current_player
            if hashKey not in self.table:
                self.table[hashKey] = [None, None, None]
            if self.table[hashKey][toPlay] == None:
                legal_moves = GoBoardUtil.generate_legal_moves_gomoku(board)
                winner, moves = self.filterMoves(board, legal_moves, toPlay)
                data = NodeData(winner, moves)
                self.table[hashKey][toPlay] = data

            data = self.table[hashKey][toPlay]
            if data.winner == -1:   # not win yet
                # randomly make a move
                move = random.choice(data.moves)
                board.board[move] = toPlay
                board.current_player = GoBoardUtil.opponent(toPlay)
            else:   # winner can be determined
                return firstMove, data.winner


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
    
