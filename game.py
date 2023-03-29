import os
import sys
import time
import math
import numpy as np
from random import shuffle

from tkinter import Frame, Canvas, Text, StringVar, Tk, Label, Button

from learner import Learner
from minimaxcomputer import MiniMaxComputer

import logging
root = logging.getLogger()
logging.getLogger().setLevel(logging.DEBUG)
handler = logging.StreamHandler(sys.stdout)
handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s', "%H:%M:%S")
handler.setFormatter(formatter)
root.addHandler(handler)

class Tic_Tac_Toe:
    def __init__(self, p1, p2, tester):
        self.learner1 = learner1 # x
        self.learner2 = learner2 # o
        self.tester = tester # x
 
        self.BOARD_ROWS = 3
        self.BOARD_COLS = 3
        
        self.symbol_X_color = 'lavender'
        self.symbol_O_color = 'lavender'
        self.grid_color = 'lavender'
        self.line_color = 'red3'
        self.reward_color_positive = 'chartreuse'
        self.reward_color_negative = 'red'
        
        self.p1 = self.learner1 # Since p1 can either be learner or teacher
        self.p2 = self.learner2
        
        self.frame_w = 1200
        self.frame_h = 500
        
        self.window = Tk()
        self.window.attributes('-fullscreen', True)
        #self.window.wm_attributes('-type', 'splash')
        self.window.title('Tic-Tac-Toe')
        self.window.configure(background='black')
        #self.window.resizable(False, False)
        self.window.minsize(self.frame_w, self.frame_h)
        
        self.board_status = np.zeros(shape=(3, 3))
        self.ready = True
        self.num_train_games = 0
        self.winner = None
        self.all_labels_reset = False
    
        self.size_of_board = self.frame_h
        self.right_side_w = int(self.frame_w/2) #int(2 * self.size_of_board)
        self.stats_values_x = int(self.right_side_w * 0.25) 
        self.choices_w = int(self.right_side_w * 0.5) #int(self.right_side_w / 2)
        self.choices_h = int(self.size_of_board / 2.5)
        self.choices_y = int(self.size_of_board * 0.25)
        self.padding = 20
        self.symbol_size = (self.size_of_board / 3 - self.size_of_board / 8) / 2
        self.symbol_thickness = 15
        self.line_width = 10
        
        self.main_frame  =  Frame(self.window, bg='black', width=self.frame_w, height=self.frame_h)
        self.main_frame.place(relx=0.5, rely=0.5, anchor='center')
        
        self.left_canvas = Canvas(self.main_frame, bg="black", borderwidth=0, highlightthickness=0, \
                                  height=self.size_of_board,  width=self.size_of_board)
        self.left_canvas.place(relx=0.25, rely=0.5, anchor='center')
        
        self.right_canvas = Canvas(self.main_frame, bg="black", borderwidth=0, highlightthickness=0, \
                                   height=self.size_of_board, width=self.right_side_w)
        self.right_canvas.place(relx=0.75, rely=0.5, anchor='center')
        
        self.games_played_key = Text(self.right_canvas, bg='black', \
                                     fg='grey', borderwidth=0, highlightthickness=0, \
                                     font=("cmr", 12, "bold"))
        self.games_played_key.insert("1.0", "Games Played")
        self.games_played_key.place(x=0, y=0)
        
        self.games_played_value = StringVar()
        self.games_played_value_label = Label(self.right_canvas, textvariable=self.games_played_value, \
                                        bg='black', fg='white', justify='left', font=("cmr", 12, "bold"))
        self.games_played_value_label.place(x=self.stats_values_x, y=0)
    
        self.states_seen_key = Text(self.right_canvas, bg='black', \
                                     fg='grey', borderwidth=0, highlightthickness=0, \
                                     font=("cmr", 12, "bold"))
        self.states_seen_key.insert("1.0", "States Seen")
        self.states_seen_key.place(x=0, y=int(self.size_of_board*0.05))
        
        self.states_seen_value = StringVar()
        self.states_seen_value_label = Label(self.right_canvas, textvariable=self.states_seen_value, \
                                       bg='black', fg='white', justify='left', font=("cmr", 12, "bold"))
        self.states_seen_value_label.place(x=self.stats_values_x, y=int(self.size_of_board*0.05))
        
        self.last_test_key = Text(self.right_canvas, bg='black', \
                                     fg='grey', borderwidth=0, highlightthickness=0, \
                                     font=("cmr", 12, "bold"))
        self.last_test_key.insert("1.0", "Last Test")
        self.last_test_key.place(x=0, y=int(self.size_of_board*0.1))
        
        self.last_test_value = StringVar()
        self.last_test_value_label = Label(self.right_canvas, textvariable=self.last_test_value, \
                                     bg='black', fg='white', justify='left', font=("cmr", 12, "bold"))
        self.last_test_value_label.place(x=self.stats_values_x, y=int(self.size_of_board*0.1))
        self.last_test_value.set("None")
        
        self.choices1 = Text(self.right_canvas, bg='black', fg='grey', borderwidth=0, \
                             highlightthickness=0, font=("cmr", 11, "bold"), \
                             height=self.choices_h, width=self.choices_w, state='disabled')
        self.choices1.place(x=0, y=self.choices_y)
        
        self.choices2 = Text(self.right_canvas, bg='black', fg='grey', borderwidth=0, \
                             highlightthickness=0, font=("cmr", 11, "bold"), height=self.choices_h, \
                             width=self.choices_w, state='disabled')
        self.choices2.place(x=self.choices_w, y=self.choices_y)
       
        self.choices3 = Text(self.right_canvas, bg='black', fg='grey', borderwidth=0, \
                             highlightthickness=0, font=("cmr", 11, "bold"), height=self.choices_h, \
                             width=self.choices_w, state='disabled')
        self.choices3.place(x=0, y=self.choices_y+self.choices_h)
        self.choices4 = Text(self.right_canvas, bg='black', fg='grey', borderwidth=0, \
                             highlightthickness=0, font=("cmr", 11, "bold"), height=self.choices_h, \
                             width=self.choices_w, state='disabled')
        self.choices4.place(x=self.choices_w, y=self.choices_y+self.choices_h)
        
        self.all_choices = [self.choices1, self.choices2, self.choices3, self.choices4] 
        
        self.button1 = Button(self.right_canvas, text="Train", bg='black', fg='white', \
                             font="cmr 15 bold", command=self.run_train)
        self.button1.place(x=0, y=self.size_of_board, anchor='sw')
        
        self.button2 = Button(self.right_canvas, text="Test", bg='black', fg='white', \
                             font="cmr 15 bold", command=self.run_test)
        self.button2.place(x=100, y=self.size_of_board, anchor='sw')
        
        # Input from user in form of clicks
        self.left_canvas.bind('<Button-1>', self.click)
    
        self.reset_game()
    
    def available_positions(self):
        positions = []
        for i in range(self.BOARD_ROWS):
            for j in range(self.BOARD_COLS):
                if self.board_status[i, j] == 0:
                    positions.append((i, j))
        return positions
        
    def mainloop(self):
        self.window.mainloop()

    def give_rewards(self, ignore_p1=False, display_p2_rewards=False):
        # backpropagate reward
        if self.winner == 1:
            logging.debug('X wins')
            p1_reward = 1
            p2_reward = 0
        elif self.winner == -1:
            logging.debug('O wins')
            p1_reward = 0
            p2_reward = 1
        elif self.winner == 0:
            logging.debug('Tie')
            p1_reward = 0.1
            p2_reward = 0.5
        else:
            raise Exception('self.winner not valid')
            
        if not ignore_p1:
            self.p1.feed_reward(p1_reward)
        
        deltas, num_train_games = self.p2.feed_reward(p2_reward)
        
        self.num_train_games += num_train_games       
        
        if not display_p2_rewards:
            return 
        
        # Show value change for each choice
        # We use reverse a few times to create the effect of updates propogating backwards
        deltas = reversed(deltas)
        for i,delta in reversed(list(enumerate(deltas))):
            label = self.all_choices[i]
            label.config(state='normal')
            val = str('{0:.3f}'.format(delta))
            if delta >= 0:
                color = self.reward_color_positive
                val = '+' + val
            else:
                color = self.reward_color_negative
            val = 2*' ' + val
            a = str(label.chosen_line) + '.17'
            b = str(label.chosen_line + 1) + '.0'
            label.insert(a, val)
            label.tag_add("score", a, b)
            label.tag_config("score", foreground=color)       
            label.config(state='disabled')
            label.update()
       
    def run_train(self):
        self.p1 = self.learner1
        self.p2 = self.learner2
        self.autoplay(num_iters=1000, redraw_freq=100, random_moves=True)
             
    def run_test(self):
        self.p1 = self.tester
        self.p2 = self.learner2
        self.autoplay(num_iters=50, redraw_freq=2, random_moves=False, test=True)
        
    def autoplay(self, num_iters=1, redraw_freq=1, random_moves=True, test=False):
        x_wins = 0; o_wins = 0; ties = 0
        logging.debug('num_iters: ' + str(num_iters))
        start_time = time.time()
        
        for i in range(num_iters):
            draw = i%redraw_freq == 0
            
            self.reset_game(draw=draw)
        
            while True:
                # Player 1
                self.p1_move(random_moves=random_moves)
                
                self.eval_game(draw=draw)
                if self.winner is not None:
                    break

                # Player 2
                self.p2_move(random_moves=random_moves)

                self.eval_game(draw=draw)
                if self.winner is not None:
                    break
            
            if draw:
                self.window.update()
            
            if not test:
                self.give_rewards()
            
            if self.winner == 1:
                x_wins += 1
            elif self.winner == -1:
                o_wins += 1
            else:
                ties += 1
            
            logging.debug('iter: ' + str(i) + ', num states: ' + str(len(self.p1.states_value)))
        
        logging.info('x_wins: ' + str(x_wins) + ', ' + \
                    'o_wins: ' + str(o_wins) + ', ' + \
                    'ties: ' + str(ties))
        logging.info('duration: ' + str(time.time() - start_time))
        self.reset_game()
        
        if test:
            out = str(o_wins) + ' wins, ' + str(x_wins) + ' losses, ' + str(ties) + ' ties'
            self.last_test_value.set(out)
        
    def reset_game(self, draw=True):
        self.winner = None
        self.p1.reset()
        self.p2.reset()
        
        if draw:
            self.left_canvas.delete("all")
            self.games_played_value.set(str(self.num_train_games))
            self.states_seen_value.set(str(len(self.p2.states_value)))
            self.draw_grid()

        self.board_status = np.zeros(shape=(3, 3))
        
        if not self.all_labels_reset:
            for label in self.all_choices:
                label.config(state='normal')
                label.delete("1.0", "end")  # if you want to remove the old data
                label.config(state='disabled')
                label.update()
            self.all_labels_reset = True
    
    def draw_grid(self):
        x = self.size_of_board / 3    
        for i in range(2):
            a = (i+1)*x
            self.left_canvas.create_line(a, 0, a, self.size_of_board, \
                                         width=self.line_width, fill=self.grid_color) 
            self.left_canvas.create_line(0, a, self.size_of_board, a, \
                                         width=self.line_width, fill=self.grid_color)
    
    def draw_O(self, logical_position):
        grid_position = self.convert_logical_to_grid_position(logical_position)
        self.left_canvas.create_oval(grid_position[0] - self.symbol_size, \
                                grid_position[1] - self.symbol_size,
                                grid_position[0] + self.symbol_size, \
                                grid_position[1] + self.symbol_size, \
                                width=self.symbol_thickness,
                                outline=self.symbol_O_color)

    def draw_X(self, logical_position):
        grid_position = self.convert_logical_to_grid_position(logical_position)
        self.left_canvas.create_line(grid_position[0] - self.symbol_size, \
                                grid_position[1] - self.symbol_size, \
                                grid_position[0] + self.symbol_size, \
                                grid_position[1] + self.symbol_size, \
                                width=self.symbol_thickness,
                                fill=self.symbol_X_color)
        self.left_canvas.create_line(grid_position[0] - self.symbol_size, \
                                grid_position[1] + self.symbol_size, \
                                grid_position[0] + self.symbol_size, \
                                grid_position[1] - self.symbol_size, \
                                width=self.symbol_thickness,
                                fill=self.symbol_X_color)

    def convert_logical_to_grid_position(self, logical_position):
        # logical_position = grid value on the board
        # grid_position = actual pixel values of the center of the grid
        logical_position = [logical_position[1], logical_position[0]]
        logical_position = np.array(logical_position, dtype=int)
        return (self.size_of_board / 3) * logical_position + self.size_of_board / 6

    def convert_grid_to_logical_position(self, grid_position):
        grid_position = [grid_position[1], grid_position[0]]
        grid_position = np.array(grid_position)
        return np.array(grid_position // (self.size_of_board / 3), dtype=int)
    
    def draw_line(self, x1, x2):
        x1 = self.convert_logical_to_grid_position(x1)
        x2 = self.convert_logical_to_grid_position(x2)
        self.left_canvas.create_line(x1[0], x1[1], x2[0], x2[1], \
                                     width=self.line_width, fill=self.line_color)
    
    def eval_game(self, draw=True):
        self.winner = None
        
        # Game can't be over, need at least min 5 moves
        # x x x o o _ _ _ _
        if np.sum(np.absolute(self.board_status)) < 5:
            return
        
       # Diagonals
        if (self.board_status[0][0] == self.board_status[1][1] == self.board_status[2][2]) and \
        (self.board_status[0][0] != 0):
            if draw:
                self.draw_line((0,0), (2,2))
            self.winner = self.board_status[0][0]
            return
        
        if (self.board_status[0][2] == self.board_status[1][1] == self.board_status[2][0]) and \
        (self.board_status[0][2] != 0):
            if draw:
                self.draw_line((0,2), (2,0))
            self.winner = self.board_status[0][2]
            return
        
        # Columns and rows
        for i in range(3):
            if (self.board_status[i][0] == self.board_status[i][1] == self.board_status[i][2]) and \
            (self.board_status[i][0] != 0):
                if draw:
                    self.draw_line((i,0), (i,2))
                self.winner = self.board_status[i][0]
                return 
        
        for i in range(3):
            if (self.board_status[0][i] == self.board_status[1][i] == self.board_status[2][i]) and \
            (self.board_status[0][i] != 0):
                if draw:
                    self.draw_line((0,i), (2,i))
                self.winner = self.board_status[0][i]
                return
        
        # Check if board is full, at this point there are no winners
        r, c = np.where(self.board_status == 0)
        if len(r) == 0:
            self.winner = 0
            return
        
        # Game not over
        return 
    
    def update_options(self, details):
        self.all_labels_reset = False
        
        i = details['move_num'] - 1 
        label = self.all_choices[i]
        
        label.config(state='normal')
        label.delete("1.0", "end")  # remove the old data
        label.insert("1.0", 'Turn ' + str(details['move_num']) + '\n\n')
        label.tag_add("title", "1.0", "2.0")
        label.tag_config("title", foreground="white")
        
        lns = list()
        for option in details['options']:
            next_board = option['next_board']
            # Convert from numpy matrix to a flatten string
            next_board = ''.join(next_board.astype(int).astype(str).flatten().tolist())\
                .replace('-1','O').replace('1','X').replace('0','_')
            value = option['value']
            ln = next_board + ' : ' 
            if value == None:
                ln = ln + str(None) + ' '
            else:
                ln = ln + str('{0:.3f}'.format(value))
            lns.append(ln)
        
        label.insert('3.0', '\n'.join(lns))
        label.config(state='disabled')
        label.update()
        
        time.sleep(0.5) # Mimic the computer making a decision
        
        # Highlight the beginning of chosen line to the beginning of the next.
        # Offset by 3 because need to account for title and space.
        # Store value in object so that we can get it later.
        label.chosen_line = details['chosen'] + 3 
        a = str(label.chosen_line) + '.0'
        b = str(label.chosen_line + 1) + '.0'
        label.tag_add("chosen", a, b)
        label.tag_config("chosen", foreground="white")
        label.update()
     
    def p1_move(self, random_moves=True, draw=True):
        logging.debug('x looking')
        positions = self.available_positions()
        [logical_position, details] = self.p1.choose_action(positions, self.board_status, 1, \
                                                           random_moves, draw)
        if draw:
            self.draw_X(logical_position)
        self.board_status[logical_position[0]][logical_position[1]] = 1
        self.p1.add_state(self.board_status.copy())
    
    def p2_move(self, random_moves=True, draw=True, display_choices=False):
        logging.debug('o looking')
        positions = self.available_positions()
        [logical_position, details] = self.p2.choose_action(positions, self.board_status, -1, \
                                                           random_moves, draw)
        if display_choices:
            self.update_options(details)
        
        if draw:
            self.draw_O(logical_position)
            
        self.board_status[logical_position[0]][logical_position[1]] = -1
        self.p2.add_state(self.board_status.copy())
          
    def click(self, event):
        if not self.ready:
            # Busy, currently not accepting any user input
            return
        
        self.ready = False
        
        # Click to complete a game
        if self.winner is not None:
            self.reset_game()
            self.ready = True
            return
        
        # Human X
        grid_position = [event.x, event.y]
        logical_position = self.convert_grid_to_logical_position(grid_position)
        # Invalid move
        if self.board_status[logical_position[0]][logical_position[1]] != 0:
            self.ready = True
            return
        self.board_status[logical_position[0]][logical_position[1]] = 1
        self.draw_X(logical_position)
        
        self.eval_game()
        
        if self.winner is not None:
            self.give_rewards(ignore_p1=True, display_p2_rewards=True)
            self.ready = True
            return
        
        # Computer O
        self.p2_move(random_moves=False, display_choices=True)
        
        self.eval_game()
        
        if self.winner is not None:
            self.give_rewards(ignore_p1=True, display_p2_rewards=True)
        
        self.ready = True
        return
        
if __name__ == '__main__':
    tester = MiniMaxComputer('tester')
    learner1 = Learner("learner1")
    learner2 = Learner("learner2")

    game_instance = Tic_Tac_Toe(learner1, learner2, tester)
    game_instance.mainloop()