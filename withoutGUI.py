import math
import random
import time
from ConnectFourClass import *

C = ConnectFour() #created an instance of the class

board = C.createBoard() #create the board
print("Game Instructions:- The board is an matrix of 6x7 and 0 denotes empty spaces and Your mark will be - 1 and computer will play with mark - 2")
print("Enjoy") #instructions and stuff
time.sleep(3)
C.printBoardAsCF(board)#Initially the element [0][0] would be at top but we need to flip it inorder to bring it to the bottom left

gameFlag = False #flag variable to keep track of game

turn = 0 #turn variable

MAXDEPTH = int(input("Enter the depth you want the minimax to go to : - "))#enter the depth you want to check



turn = C.properTurn()#randomised between player and Computer
while not gameFlag:

    if turn == C.HUMAN_PLAYER:
        column = int(input("Player, Enter which column do you want to drop your mark to: - "))

        if C.isValidLOC(board,column):
            row = C.getNextValidRow(board,column)#get the next open row
            C.dropMark(board,row,column, C.HUMAN_PLAYER_MARK)#drop player's mark
            C.LEGALMOVES[column]-=1#legal moves will keep decreasing as the board fills up
            print(C.LEGALMOVES[column])

            if C.checkIfWinningOrTerminal(board,C.HUMAN_PLAYER_MARK):
                print("You win! Congratulations")
                gameFlag = True#exit the loop if a result has been reached
            turn = turn + 1
            turn = turn % 2
            C.printBoardAsCF(board)

    if turn == C.COMPUTER_PLAYER and not gameFlag:
        print("Computer's turn")
        column,minimaxScore = C.minimax(board,MAXDEPTH,-math.inf,math.inf,True)
        if C.isValidLOC(board,column):
            row = C.getNextValidRow(board,column)#get the next open row
            C.dropMark(board,row,column,C.COMPUTER_PLAYER_MARK)#drop player's mark
            C.LEGALMOVES[column] -= 1#legal moves will keep decreasing as the board fills up

            if C.checkIfWinningOrTerminal(board,C.COMPUTER_PLAYER_MARK):
                print("Computer Wins! Better luck next time")
                gameFlag = True#exit the loop if a result has been reached


            C.printBoardAsCF(board)
            turn = turn + 1
            turn = turn % 2
