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

def get_heuristic(board,player):
    empty_space = empty_space_heuristic(board)
    corner_score = corner_heuristic(board,player)
    monotonic_score = monotonic_heuristic(board)
    adjacent_score = adjacent_heuristic(board)

    max_at_corner = max_corner_heuristic(board,player)
    weighted_score = weighted_heuristic(board,player)
    max_tile_score = maximum_tile_heuristic(board,player)

    return empty_space*10 + corner_score*50 + monotonic_score*50 + adjacent_score*100
    #return corner_score

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

    gradient1 = [[[2**5,2**4,2**3,2**2,2**1,2**0],[2**4,2**3,2**2,2**1,2**0,-2**1],[2**3,2**2,2**1,2**0,-2**1,-2**2],[2**2,2**1,2**0,-2**1,-2**2,-2**3],[2**1,2**0,-2**1,-2**2,-2**3,-2**4],[2**0,-2**1,-2**2,-2**3,-2**4,-2**5]],
                [[2**0,2**1,2**2,2**3,2**4,2**5],[-2**1,2**0,2**1,2**2,2**3,2**4],[-2**2,-2**1,2**0,2**1,2**2,2**3],[-2**3,-2**2,-2**1,2**0,2**1,2**2],[-2**4,-2**3,-2**2,-2**1,2**0,2**1],[-2**5,-2**4,-2**3,-2**2,-2**1,2**0]],
                [[-2**5,-2**4,-2**3,-2**2,-2**1,2**0],[-2**4,-2**3,-2**2,-2**1,2**0,2**1],[-2**3,-2**2,-2**1,2**0,2**1,2**2],[-2**2,-2**1,2**0,2**1,2**2,2**3],[-2**1,2**0,2**1,2**2,2**3,2**4],[2**0,2**1,2**2,2**3,2**4,2**5]],
                [[2**0,-2**1,-2**2,-2**3,-2**4,-2**5],[2**1,2**0,-2**1,-2**2,-2**3,-2**4],[2**2,2**1,2**0,-2**1,-2**2,-2**3],[2**3,2**2,2**1,2**0,-2**1,-2**2],[2**4,2**3,2**2,2**1,2**0,-2**1],[2**5,2**4,2**3,2**2,2**1,2**0]]
                ]

    cost = -100000

    if player == '-':        
        for l in range(4):
            
            temp_cost = 0

            for i in range(len(board)):
                for j in range(i):
                    if board[i][j].islower():
                        temp_cost += gradient1[l][i][j]*(ord(board[i][j])-96)

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

    monotonic_cost = 0

    for i in range(len(board)-1):
        for j in range(len(board)-1):
            if board[i][j] != ' ':
                if board[i][j].lower() == board[i][j+1].lower():
                    monotonic_cost += 1
                if board[i][j].lower() == board[i+1][j].lower():
                    monotonic_cost += 1 

    return monotonic_cost

def adjacent_heuristic(board):

    adjacent_cost = 0

    for i in range(len(board)-1):
        for j in range(len(board)-1):
            if board[i][j] != ' ':
                adjacent_cost += 26 - abs(ord(board[i][j].lower()) - ord(board[i][j+1].lower()))
                adjacent_cost += 26 - abs(ord(board[i][j].lower()) - ord(board[i+1][j].lower()))

    return adjacent_cost

def max_corner_heuristic(board,player):

    max_letter = -1
    idx_i = -1
    idx_j = -1

    if player == '+':
        for i in range(len(board)):
            for j in range(len(board)):
                if board[i][j].isupper():
                    if ord(board[i][j]) > max_letter:
                        max_letter = ord(board[i][j])
                        idx_i = i
                        idx_j = j

    else:
        for i in range(len(board)):
            for j in range(len(board)):
                if board[i][j].islower():
                    if ord(board[i][j]) > max_letter:
                        max_letter = ord(board[i][j])
                        idx_i = i
                        idx_j = j
    if (i == 0 and j == 0) or (i == 5 and j == 0) or (i == 0 and j == 5) or (i == 5 and j == 5):
        return 5000
    else:
        return -5000 

def weighted_heuristic(board,player):
    upper_cost = 0
    lower_cost = 0
    cost = 0
    for i in board:
        for j in i:
            if j.isupper():
                upper_cost += ord(j)-64

            else:
                lower_cost += ord(j)-96
    
    if player == '-':
        cost = lower_cost - upper_cost

    else: 
        cost = upper_cost - lower_cost

    return cost

def maximum_tile_heuristic(board,player):
    
    upper_tile = -1
    lower_tile = -1

    for i in board:
        for j in i:
            if j.isupper():
                if upper_tile < ord(j):
                    upper_tile = ord(j)
            else:
                if lower_tile < ord(j):
                    lower_tile = ord(j)
    
    if player == '-':
        return lower_tile
    else:
        return upper_tile

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

    #cost = corner_heuristic(board,current[0].getCurrentPlayer)
    #cost = weighted_heuristic(board,current[0].getCurrentPlayer)
    cost = get_heuristic(board,current[0].getCurrentPlayer)
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

    #cost = corner_heuristic(board,current[0].getCurrentPlayer)
    #cost = weighted_heuristic(board,current[0].getCurrentPlayer)
    cost = get_heuristic(board,current[0].getCurrentPlayer)
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

    future_step = 3

    board = game.getGame()
    player = game.getCurrentPlayer()
    deterministic = game.getDeterministic()

    if deterministic:

        if player == '+':
            # succ = [game,'move']
            succ = successor(game)

            best,c = max(min_value(i,future_step,alpha,beta) for i in succ)
            #print(best[1])
            yield best[1]
        else:
            yield random.choice(['U', 'D', 'L', 'R'])            

    else:

        yield random.choice(['U', 'D', 'L', 'R'])


