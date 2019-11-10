#!/usr/local/bin/python3

"""
This is where you should write your AI code!

Authors: PLEASE ENTER YOUR NAMES AND USER ID'S HERE

Based on skeleton code by Abhilash Kuhikar, October 2019
"""

from logic_IJK import Game_IJK
import random
import copy
import math

# Suggests next move to be played by the current player given the current game
#
# inputs:
#     game : Current state of the game 
#
# This function should analyze the current state of the game and determine the 
# best move for the current player. It should then call "yield" on that move.

def empty_space_heuristic(board):

    empty_space = 0

    for i in board:
        for j in i:
            if j == ' ':
                empty_space += 1

    return empty_space

def corner_heuristic(board,player):

    gradient = [[[5,4,3,2,1,0],[4,3,2,1,0,-1],[3,2,1,0,-1,-2],[2,1,0,-1,-2,-3],[1,0,-1,-2,-3,-4],[0,-1,-2,-3,-4,-5]],
                [[0,1,2,3,4,5],[-1,0,1,2,3,4],[-2,-1,0,1,2,3],[-3,-2,-1,0,1,2],[-4,-3,-2,-1,0,1],[-5,-4,-3,-2,-1,0]],
                [[-5,-4,-3,-2,-1,0],[-4,-3,-2,-1,0,1],[-3,-2,-1,0,1,2],[-2,-1,0,1,2,3],[-1,0,1,2,3,4],[0,1,2,3,4,5]],
                [[0,-1,-2,-3,-4,-5],[1,0,-1,-2,-3,-4],[2,1,0,-1,-2,-3],[3,2,1,0,-1,-2],[4,3,2,1,0,-1],[5,4,3,2,1,0]]
                ]

    cost = 0

    if player == '-':        
        for l in range(4):
            
            temp_cost = 0

            for i in range(len(board)):
                for j in range(i):
                    if board[i][j].islower():
                        temp_cost += gradient[l][i][j]*(ord(board[i][j])-96)

            if temp_cost > cost:
                cost = temp_cost

    else:
        for l in range(4):
            
            temp_cost = 0

            for i in range(len(board)):
                for j in range(i):
                    if board[i][j].isupper():
                        temp_cost += gradient[l][i][j]*(ord(board[i][j])-64)

            if temp_cost > cost:
                cost = temp_cost

    return cost

def monotonic_heuristic(board):

    return

def highest_move_heuristic(board,player):
    max_cost = 0
    min_cost = 0
    cost = 0
    for i in board:
        for j in i:
            if j.isupper():
                if max_cost< ord(j):
                    max_cost = ord(j)

            else:
                if min_cost<ord(j):
                    min_cost = ord(j)
    
    if player == '-':
        cost = min_cost - max_cost

    else: 
        cost = max_cost - min_cost

    return cost

def future():
    return

def successor(game):
    move = ['U', 'D', 'L', 'R']
    return [(copy.deepcopy(game).makeMove(i),i) for i in move]

def min_value(current,future_step,alpha,beta):

    min_val = math.inf

    board = current[0].getGame()

    if future_step > 1:
        future_step -= 1

        succ = successor(current[0])

        for i in succ:
            temp,beta_new = max_value(i,future_step,alpha,beta)
            if min_val > temp[0]:
                min_val = temp[0]
                move = temp[1]
                beta = beta_new

            if alpha >= beta:
                break

        return [min_val,move],beta
        #return min(max_value(i,future_step) for i in succ)

    cost = corner_heuristic(board,current[0].getCurrentPlayer)
    return [cost,current[1]],cost
    #return [highest_move_heuristic(board,current[0].getCurrentPlayer),current[1]]
    #return [empty_space_heuristic(board),current[1]]

def max_value(current,future_step,alpha,beta):

    max_val = -math.inf

    board = current[0].getGame()

    if future_step > 1:
        future_step -= 1

        succ = successor(current[0])

        for i in succ:
            temp,alpha_new = min_value(i,future_step,alpha,beta)
            if max_val < temp[0]:
                max_val = temp[0]
                move = temp[1]
                alpha = alpha_new

            if alpha > beta:
                break

        return [max_val,move],alpha
        #return max(min_value(i,future_step) for i in succ)

    cost = corner_heuristic(board,current[0].getCurrentPlayer)
    return [cost,current[1]],cost
    #return [highest_move_heuristic(board,current[0].getCurrentPlayer),current[1]]
    #return [empty_space_heuristic(board),current[1]] 

def next_move(game: Game_IJK)-> None:

    '''board: list of list of strings -> current state of the game
       current_player: int -> player who will make the next move either ('+') or -'-')
       deterministic: bool -> either True or False, indicating whether the game is deterministic or not
    '''

    beta = math.inf
    alpha = -math.inf

    future_step = 4

    board = game.getGame()
    player = game.getCurrentPlayer()
    deterministic = game.getDeterministic()

    if deterministic:

        # succ = [game,'move']
        succ = successor(game)

        best,c = max(min_value(i,future_step,alpha,beta) for i in succ)
        print(best[1])
        yield best[1]


    else:

        yield random.choice(['U', 'D', 'L', 'R'])


