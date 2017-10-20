#!/usr/bin/env python3
# -*- coding: utf-8 -*

"""
COMS W4701 Artificial Intelligence - Programming Homework 2

An AI player for Othello. This is the template file that you need to  
complete and submit. 

@author: Jiahe Chen AND jc4833 
"""

import random
import sys
import time

# You can use the functions in othello_shared to write your AI 
from othello_shared import find_lines, get_possible_moves, get_score, play_move
from heapq import heappush
from heapq import heappop
cache = {}
maxSafeDepth  = 5
def compute_utility(board, color):
    p1,p2 = get_score(board)
    #dark1, light 2
    if color == 1:
        return p1-p2
    elif color == 2:
        return p2-p1
    return -1


############ MINIMAX ###############################

def minimax_min_node(board, color):
    next_color = 3-color
    next_moves = get_possible_moves(board,next_color)
    minU = float("inf")
    if len(next_moves) == 0:
        cache[board] = compute_utility(board,color)
        return cache[board]
    for move in next_moves:
        next_board = play_move(board,next_color,move[0],move[1])
        if cache.__contains__(next_board):
            minU = min(minU, cache[next_board])
        else:
            minU = min(minU,minimax_max_node(next_board, color))
    return minU


def minimax_max_node(board, color):
    next_moves = get_possible_moves(board,color)
    maxU = float("-inf")
    if len(next_moves) == 0:
        cache[board] = compute_utility(board,color)
        return cache[board]
    for move in next_moves:
        next_board = play_move(board,color,move[0],move[1])
        if cache.__contains__(next_board):
            maxU = max(maxU, cache[next_board])
        else:
            maxU = max(maxU,minimax_min_node(next_board, color))
    return maxU

    
def select_move_minimax(board, color):
    """
    Given a board and a player color, decide on a move. 
    The return value is a tuple of integers (i,j), where
    i is the column and j is the row on the board.  
    """
    next_moves = get_possible_moves(board,color)
    maxU = float("-inf")
    i = 0
    j = 0
    for move in next_moves:
        next_board = play_move(board,color,move[0],move[1])
        if cache.__contains__(next_board):
            nu = cache[next_board]
        else:
            nu = minimax_min_node(next_board, color)
        if nu > maxU:
            i = move[0]
            j = move[1]
            maxU = nu
    return i, j
    
############ ALPHA-BETA PRUNING #####################

# def alphabeta_min_node(board, color, alpha, beta, level, limit)
def alphabeta_min_node(board, color, alpha, beta, level, limit):
    next_color = 3-color
    next_moves = get_possible_moves(board,next_color)
    minU = float("inf")
    next_moves_h = []
    for move in next_moves:
        next_b = play_move(board,next_color,move[0],move[1])
        heappush(next_moves_h,(compute_utility(next_b,next_color),next_b))
    if len(next_moves) == 0 or level > limit:
        cache[board] = compute_utility(board,color)
        return cache[board]
    while next_moves_h:
        next_board = heappop(next_moves_h)[1]
        if cache.__contains__(next_board):
            minU = min(minU, cache[next_board])
        else:
            minU = min(minU,alphabeta_max_node(next_board, color,alpha,beta,level+1,limit))
        if minU <= alpha:
            return minU
        beta = min(beta, minU)
    return minU

# def alphabeta_min_node(board, color, alpha, beta): 
#     next_color = 3-color
#     next_moves = get_possible_moves(board,next_color)
#     minU = float("inf")
#     next_moves_h = []
#     for move in next_moves:
#         next_b = play_move(board,next_color,move[0],move[1])
#         heappush(next_moves_h,(compute_utility(next_b,next_color),next_b))
#     if len(next_moves) == 0:
#         cache[board] = compute_utility(board,color)
#         return cache[board]
#     while next_moves_h:
#     # for move in next_moves:
#         # next_board = play_move(board,next_color,move[0],move[1])
#         next_board = heappop(next_moves_h)[1]
#         if cache.__contains__(next_board):
#             minU = min(minU, cache[next_board])
#         else:
#             minU = min(minU,alphabeta_max_node(next_board, color,alpha,beta))
#         if minU <= alpha:
#             return minU
#         beta = min(beta, minU)
#     return minU


# def alphabeta_max_node(board, color, alpha, beta, level, limit)
def alphabeta_max_node(board, color, alpha, beta, level, limit):
    next_moves = get_possible_moves(board,color)
    maxU = float("-inf")
    if len(next_moves) == 0 or level > limit:
        cache[board] = compute_utility(board,color)
        return cache[board]
    next_moves_h = []
    for move in next_moves:
        next_b = play_move(board,color,move[0],move[1])
        heappush(next_moves_h, (compute_utility(next_b,3-color),next_b))
    while next_moves_h:
        next_board = heappop(next_moves_h)[1]
        if cache.__contains__(next_board):
            maxU = max(maxU, cache[next_board])
        else:
            maxU = max(maxU,alphabeta_min_node(next_board, color,alpha,beta,level+1,limit))
        if maxU >= beta:
            return maxU
        alpha = max(alpha, maxU)
    return maxU

# def alphabeta_max_node(board, color, alpha, beta):
#     next_moves = get_possible_moves(board,color)
#     maxU = float("-inf")
#     if len(next_moves) == 0:
#         cache[board] = compute_utility(board,color)
#         return cache[board]
#     next_moves_h = []
#     for move in next_moves:
#         next_b = play_move(board,color,move[0],move[1])
#         heappush(next_moves_h, (compute_utility(next_b,3-color),next_b))
#     while next_moves_h:
#     # for move in next_moves:
#         # next_board = play_move(board,color,move[0],move[1])
#         next_board = heappop(next_moves_h)[1]
#         if cache.__contains__(next_board):
#             maxU = max(maxU, cache[next_board])
#         else:
#             maxU = max(maxU,alphabeta_min_node(next_board, color,alpha,beta))
#         if maxU >= beta:
#             return maxU
#         alpha = max(alpha, maxU)
#     return maxU

def select_move_alphabeta(board, color): 
    next_moves = get_possible_moves(board,color)
    maxU = float("-inf")
    alpha = float("-inf")
    beta = float("inf")
    i = 0
    j = 0
    for move in next_moves:
        next_board = play_move(board,color,move[0],move[1])
        if cache.__contains__(next_board):
            nu = cache[next_board]
        else:
            # nu = alphabeta_min_node(next_board, color, alpha,beta)
            # for part V Depth Limit
            nu = alphabeta_min_node(next_board, color, alpha,beta,0,maxSafeDepth)
        if nu > maxU:
            i = move[0]
            j = move[1]
            maxU = nu
        alpha = max(alpha,maxU)
    return i, j


####################################################
def run_ai():
    """
    This function establishes communication with the game manager. 
    It first introduces itself and receives its color. 
    Then it repeatedly receives the current score and current board state
    until the game is over. 
    """
    print("Minimax AI") # First line is the name of this AI  
    color = int(input()) # Then we read the color: 1 for dark (goes first), 
                         # 2 for light. 

    while True: # This is the main loop 
        # Read in the current game status, for example:
        # "SCORE 2 2" or "FINAL 33 31" if the game is over.
        # The first number is the score for player 1 (dark), the second for player 2 (light)
        next_input = input() 
        status, dark_score_s, light_score_s = next_input.strip().split()
        dark_score = int(dark_score_s)
        light_score = int(light_score_s)

        if status == "FINAL": # Game is over. 
            print 
        else: 
            board = eval(input()) # Read in the input and turn it into a Python
                                  # object. The format is a list of rows. The 
                                  # squares in each row are represented by 
                                  # 0 : empty square
                                  # 1 : dark disk (player 1)
                                  # 2 : light disk (player 2)
                    
            # Select the move and send it to the manager 
            # movei, movej = select_move_minimax(board, color)
            movei, movej = select_move_alphabeta(board, color)
            print("{} {}".format(movei, movej)) 


if __name__ == "__main__":
    run_ai()
