from utils import get_loc
from config import MIN_COST, MAX_COST, MAX_ITER

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
        random_index = int(random.random())*len(candidate_cells)
        action = candidate_cells[random_index]
        ##############################################################

        assert action in candidate_cells # you must choose from one of the candidate cells!
        if get_loc(action) == (self.N-1,self.N-1):
            self.done = True

        return action
