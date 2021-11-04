import random
import sys
import numpy as np
import math
import random
#Name: Vinit Udasi
#Student:647800
#Subject: COSC 3P71
#Email: vu19pt@brocku.ca


class ConnectFour:
    #initialised numbers in the constructor
    def __init__(self):
        self.ZERO = 0
        self.ONE = 1
        self.TW0 = 2
        self.THREE = 3
        self.FOUR = 4
        self.NUM_ROW = 6
        self.NUM_COLUMN = 7
        self.LEGALMOVES = [6]*7
        self.HUMAN_PLAYER = 0
        self.COMPUTER_PLAYER = 1
        self.HUMAN_PLAYER_MARK = 1
        self.COMPUTER_PLAYER_MARK = 2
        self.WIN_SEQ = 4
        self.BIGPOSITIVE = 99999999999
        self.BIGNEGATIVE = -9999999999
    #decides a proper turn using random
    def properTurn(self):
        turn = random.randint(self.HUMAN_PLAYER,self.COMPUTER_PLAYER)
        return 1 if turn ==1 else  0
    #created an array of zeroes using numpy.
    def createBoard(self):
        board = np.zeros((self.NUM_ROW,self.NUM_COLUMN),dtype=int)
        return board
    #initially, the array[0][0] would be at the top left, We'll flip it by it's axis Pi radians
    def printBoardAsCF(self,board):
        print(np.flip(board,0))
    #get the next open row and drop the player's mark
    def dropMark(self,board,r,c,MARK):
         board[r][c] = MARK
    #is the given location at any time valid?
    def isValidLOC(self,board,c):
        return board[self.NUM_ROW-1][c] == self.ZERO
    #get the next row in which you could drop your mark
    def getNextValidRow(self,board,c):
        for r in range(self.NUM_ROW):
            if board[r][c] == self.ZERO:
                return r
    #vertical Y-axis combinations
    def yAxisWinning(self,board, MARK):
        for c in range(self.NUM_COLUMN):
            for r in range(self.NUM_ROW - 3):
                if board[r][c] == MARK and board[r + 1][c] == MARK and board[r + 2][c] == MARK and board[r + 3][
                    c] == MARK:
                    return True
    #horizontal(x-axis) combinations
    def xAxisWinning(self,board,MARK):
        for c in range(self.NUM_COLUMN - 3):
            for r in range(self.NUM_ROW):
                if board[r][c] == MARK and board[r][c + 1] == MARK and board[r][c + 2] == MARK and board[r][
                    c + 3] == MARK:
                    return True
    #primary diagonal(i.e. diagonal with a positive slope)
    def primaryDiagonal(self,board,MARK):
        for c in range(self.NUM_COLUMN - 3):
            for r in range(self.NUM_ROW - 3):
                if board[r][c] == MARK and board[r + 1][c + 1] == MARK and board[r + 2][c + 2] == MARK and \
                        board[r + 3][c + 3] == MARK:
                    return True
    #secondary diagonal of the array(i.e diagonal with a negative slope)
    def secondaryDiagonal(self,board,MARK):
        for c in range(self.NUM_COLUMN - 3):
            for r in range(3, self.NUM_ROW):
                if board[r][c] == MARK and board[r - 1][c + 1] == MARK and board[r - 2][c + 2] == MARK and \
                        board[r - 3][
                            c + 3] == MARK:
                    return True
    #four cases for checking if a result has been reached(x-axis,y-axis,primary diagonal,secondary diagonal)
    def checkIfWinningOrTerminal(self,board,MARK):
        if self.xAxisWinning(board,MARK):
            return True
        if self.yAxisWinning(board,MARK):
            return True
        if self.primaryDiagonal(board,MARK):
            return True
        if self.secondaryDiagonal(board,MARK):
            return True

    #terminal node means if the board is in winning position or all the valid locations have been exhausted
    def isTerminalNode(self,board):
        return self.checkIfWinningOrTerminal(board,self.HUMAN_PLAYER_MARK) or self.checkIfWinningOrTerminal(board,self.COMPUTER_PLAYER_MARK) or len(self.getValidLocs(board)) == 0
    #Heuristics implemented in evalpos and with the help of countGameScore
    def evalPos(self,board,MARK):
        gameScore = 0
        #any possiblities in the centre
        midArray = self.getScoringArrays(board,None,None,5)#get the scoring array
        midScore = midArray.count(MARK)#check the status of the player's mark on the board
        gameScore += midScore*4#4 is a random number to maintain a score

        for r in range(self.NUM_ROW):
            rowArray = self.getScoringArrays(board,r,None,1)#get the scoring array
            for c in range(self.NUM_COLUMN - 3):
                funcArr = rowArray[c:c + self.WIN_SEQ]# get subarrays of 4
                gameScore = gameScore + self.countGameScore(funcArr, MARK)#get score of the current subarray to determine who's ahead at the time
        #print(gameScore)
        # vertical score
        for c in range(self.NUM_COLUMN):
            col_array = self.getScoringArrays(board,None,c,2)
            for r in range(self.NUM_ROW):
                funcArr = col_array[r:r + self.WIN_SEQ]
                gameScore = gameScore + self.countGameScore(funcArr, MARK)
        # print(gameScore)
        # Primary diagonal
        for r in range(self.NUM_ROW - 3):
            for c in range(self.NUM_COLUMN - 3):
                funcArr = self.getScoringArrays(board,r,c,3)
                gameScore = gameScore + self.countGameScore(funcArr, MARK)
        # print(gameScore)
        # Secondary diagonal
        for r in range(self.NUM_ROW - 3):
            for c in range(self.NUM_COLUMN - 3):
                funcArr = self.getScoringArrays(board,r,c,4)
                gameScore = gameScore + self.countGameScore(funcArr, MARK)
        return gameScore
    #get all the possible scoring arrays
    def getScoringArrays(self,board,r,c,choice):
        if choice == 1:
            return [int(i) for i in list(board[r,:])]
        elif choice == 2:
            return [int(i) for i in list(board[:, c])]
        elif choice == 3:
            return [board[r+i][c+i] for i in range(self.WIN_SEQ)]
        elif choice == 4:
            return [board[r-i+3][c+i] for i in range(self.WIN_SEQ)]
        elif choice == 5:
            return [int(i) for i in list(board[:,math.floor(self.NUM_COLUMN/2)])]
        else:
            return 0
    #keeping track of who's ahead at the moment using gameScore. Scores are random numbers to see which player is leading
    def countGameScore(self,funcArr,MARK):
        gameScore = 0
        #for computer, you're the current opponent
        currentOpp = self.HUMAN_PLAYER_MARK
        #if it's your turn then the current opponent is the computer
        if MARK == self.HUMAN_PLAYER_MARK:
            currentOpp = self.COMPUTER_PLAYER_MARK
        #possible combinations for 4 = 4(maxmising) + 0(minimising) -> best score
        if funcArr.count(MARK) == self.FOUR:
            gameScore = gameScore + 1000
        # 4 = 3(maximising) + 0(minimising) + 1(empty space)
        elif funcArr.count(MARK) == self.THREE and funcArr.count(self.ZERO) == self.ONE:
            gameScore = gameScore + 100
        # 4 = 2 + 2(empty spaces) + 0
        elif funcArr.count(MARK) == self.TW0 and funcArr.count(self.ZERO) == self.TW0:
            gameScore = gameScore + 50
        # if the opponent's got lead. decrease the score
        if funcArr.count(currentOpp) == self.THREE and funcArr.count(self.ZERO) == self.ONE:
            gameScore = gameScore - 800

        return gameScore
    #minimax algorithm implementation with alpha beta pruning using the pseudocode
    def minimax(self,board, depth, alpha, beta, maximizingPlayer):
        val_loc = self.getValidLocs(board)
        isTerminal = self.isTerminalNode(board)
        if depth == 0 or isTerminal:
            if isTerminal:
                if self.checkIfWinningOrTerminal(board, self.COMPUTER_PLAYER_MARK):
                    return (None,self.BIGPOSITIVE )
                elif self.checkIfWinningOrTerminal(board, self.HUMAN_PLAYER_MARK):
                    return (None,self.BIGNEGATIVE )
                else:
                    return (None, 0)
            else:
                return (None, self.evalPos(board, self.COMPUTER_PLAYER_MARK))
        if maximizingPlayer:
            value = -math.inf
            column = random.choice(val_loc)
            for loc in val_loc:
                row = self.getNextValidRow(board, loc)
                newBoard = board.copy()
                self.dropMark(newBoard, row, loc, self.COMPUTER_PLAYER_MARK)
                newScore = self.minimax(newBoard, depth - 1, alpha, beta, False)[1]
                if newScore > value:
                    value = newScore
                    column = loc
                alpha = max(alpha, value)
                if alpha >= beta:
                    break
            return column, value
        else:  # we know we're the minimising player
            value = math.inf
            column = random.choice(val_loc)
            for loc in val_loc:
                row = self.getNextValidRow(board, loc)
                newBoard = board.copy()
                self.dropMark(newBoard, row, loc,self.HUMAN_PLAYER_MARK)
                new_score = self.minimax(newBoard, depth - 1, alpha, beta, True)[1]
                if new_score < value:
                    value = new_score
                    column = loc
                beta = min(beta, value)
                if alpha >= beta:
                    break
            return column, value
    #function to get  the valid locations in an array
    def getValidLocs(self,board):
        validLocs = []

        for column in range(self.NUM_COLUMN):
            if self.isValidLOC(board,column):
                validLocs.append(column)
        return validLocs
