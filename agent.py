from utils import get_loc

import random

class Agent():
    def __init__(self, N):
        self.N = N
        self.backtracking_path = {}
        self.done = False
        random.seed(123)

        ##############################################################
        # add any extra data_structures you need here!
        ##############################################################

    def select_action(self, candidate_cells, adjacent_cells_to_last_cell, last_cell):
        ##############################################################
        # write your algorithm here!
        action = list(candidate_cells)[int(random.random())*len(candidate_cells)]
        ##############################################################

        if get_loc(action) == (self.N-1,self.N-1):
            self.done = True

        return action
