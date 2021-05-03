import random

class Agent():
    def __init__(self, N):
        self.N = N
        self.backtracking_path = {}
        self.done = False
        random.seed(123)
    
    def select_action(self, adjacent_cells, last_cell):
        idx = int(random.random() * len(adjacent_cells))
        action = adjacent_cells[idx]
        
        if action.get_loc() == (self.N-1,self.N-1):
            self.done = True
        
        if last_cell is not None:
            self.update_backtracking_path(adjacent_cells, last_cell)
            
        return action
    
    def update_backtracking_path(self, adjacent_cells, last_cell):
        for cell in adjacent_cells:
            if cell.get_loc() not in self.backtracking_path:
                self.backtracking_path[cell.get_loc()] = last_cell.get_loc()