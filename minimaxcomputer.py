import logging
import numpy as np
import math

class MiniMaxComputer:
    def __init__(self, name, explore_rate=0.3):
        self.name = name
        self.explore_rate = explore_rate
        self.states_value = dict()
        self.BOARD_ROWS = 3
        self.BOARD_COLS = 3

    def minimax(self, board, player):
        x = self.analyze_board(board)
        if x != 0:
            return x*player
        pos = -1
        value = -2
        for i in range(0,9):
            if board[i] == 0:
                board[i] = player
                score = -self.minimax(board, (player*-1))
                if score > value:
                    value = score
                    pos = i
                board[i]=0
        if pos== -1:
            return 0
        return value

    def analyze_board(self, board):
        cb = [[0,1,2],[3,4,5],[6,7,8],[0,3,6],[1,4,7],[2,5,8],[0,4,8],[2,4,6]]

        for i in range(0,8):
            if(board[cb[i][0]] != 0 and
               board[cb[i][0]] == board[cb[i][1]] and
               board[cb[i][0]] == board[cb[i][2]]):
                return board[cb[i][2]];
        return 0
    
    def choose_action(self, positions, current_board, symbol, random_moves=True, draw=True):
        logging.debug('choose_action')
        
        details = dict()
        details['chosen'] = None
        details['options'] = list()
        details['move_num'] = np.sum(current_board==symbol) + 1
        
        if len(positions) == 9:
            logging.debug('p1 first random action')
            idx = np.random.choice(len(positions))
            action = positions[idx]
            details['chosen'] = idx
            return [action, details]
        
        if random_moves and np.random.uniform(0, 1) <= self.explore_rate:
            logging.debug('p1 random action')
            idx = np.random.choice(len(positions))
            action = positions[idx]
            details['chosen'] = idx
            return [action, details]
        
        board =  current_board.reshape(self.BOARD_COLS*self.BOARD_ROWS).tolist()
        
        if symbol == -1:
            board = [-x for x in board]
        
        pos = -1
        value =-2
        for i in range(0,9):
            if board[i] == 0:
                board[i] = 1
                score = -self.minimax(board, -1)
                board[i] = 0
                if score > value:
                    value = score
                    pos = i
        #board[pos] = 1
        action = (math.floor(pos/3), pos%3)
        return [action, details]
    
    def add_state(self, state):
        pass
    
    def feed_reward(self, reward):
        pass
            
    def reset(self):
        pass
    
    def save_policy(self):
        pass
