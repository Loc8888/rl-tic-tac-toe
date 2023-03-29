import logging
import numpy as np

class Learner:
    def __init__(self, name, lr=0.2, decay_gamma=0.9, explore_rate=0.3):
        self.name = name
        self.lr = lr
        self.decay_gamma = decay_gamma
        self.explore_rate = explore_rate
        self.states = list()  # record all positions taken
        self.states_value = dict()  # state -> value
        self.BOARD_ROWS = 3
        self.BOARD_COLS = 3
    
        # Speed up learning by flipping and mirroring boards
        self.funcs = [\
            lambda x: np.rot90(x, k=1), \
            lambda x: np.rot90(x, k=2), \
            lambda x: np.rot90(x, k=3), \
            lambda x: np.flip(x), \
            lambda x: np.rot90(np.flip(x), k=1), \
            lambda x: np.rot90(np.flip(x), k=2), \
            lambda x: np.rot90(np.flip(x), k=3)]
        
    def make_hash(self, board):
        return str(board.reshape(self.BOARD_COLS*self.BOARD_ROWS))
    
    def choose_action(self, positions, current_board, symbol, random_moves=True, draw=True):
        logging.debug('chooseAction')
        selected = None
        details = dict()
        
        if draw:
            details['chosen'] = None
            details['options'] = list()
            details['move_num'] = np.sum(current_board==symbol) + 1
        
        value_max = -999
        
        for i,p in enumerate(positions):
            next_board = current_board.copy()
            next_board[p] = symbol
            next_boardHash = self.make_hash(next_board)
            logging.debug('available states_value: ' + str(next_boardHash) + \
                          ' ' + str(self.states_value.get(next_boardHash)))
            value = self.states_value.get(next_boardHash)
            if draw:
                details['options'].append({'next_board': next_board, 'value': value})
            if value is None:
                value = 999
            if value > value_max:
                value_max = value
                selected = i
        
        if random_moves and np.random.uniform(0, 1) <= self.explore_rate:
            logging.debug('learner random action')
            selected = np.random.choice(len(positions))
        
        action = positions[selected]
        
        if draw:
            details['chosen'] = selected
        
        logging.debug('positions: ' + str(positions))
        return [action, details]
    
    def add_state(self, state):
        self.states.append(state)
    
    def update_value(self, st, reward):
        if self.states_value.get(st) is None:
                self.states_value[st] = 0
        delta = self.lr*(self.decay_gamma*reward - self.states_value[st])
        self.states_value[st] += delta
        return delta
    
    def feed_reward(self, reward):
        logging.debug('states: ' + ','.join([self.make_hash(st) for st in self.states]))
        unique_states = []
        orig_reward = reward
        deltas = [] # Changes in value, stored for visualization purposes
        
        reward = orig_reward
        for st in reversed(self.states):
            st = self.make_hash(st)
            delta = self.update_value(st, reward)
            reward = self.states_value[st]
            deltas.append(delta)
        
        num_train_games = 1
            
        # Only learn mirrors/flips once for each last unique state
        unique_states = [self.states[-1].tobytes()]    
        for func in self.funcs:
            state = func(self.states[-1]).tobytes() 
            if state not in unique_states:
                unique_states.append(state)
                reward = orig_reward
                num_train_games += 1
                for st in reversed(self.states):
                    st = self.make_hash(func(st))
                    self.update_value(st, reward)
                    reward = self.states_value[st]
        
        return deltas, num_train_games
            
    def reset(self):
        self.states = list()
        
    def save_policy(self):
        f = open('policy_' + str(self.name), 'wb')
        pickle.dump(self.states_value, f)
        f.close()

    def load_policy(self, file):
        f = open(file,'rb')
        self.states_value = pickle.load(f)
        f.close()