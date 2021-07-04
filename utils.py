
class PathTracker():
    def __init__(self, start_cell):
        start_cell.cost_to_cell = start_cell.terrain
        self.path_tree = Tree(start_cell, hzsh=lambda x : x.get_loc())

    def is_tracked(self, cell):
        return self.path_tree.contains(cell)

    def add_cell(self, new_cell):
        # link the new cell
        valid_parents = self.get_valid_parents(new_cell.adj_set)
        best_parent = min(valid_parents, key=lambda x: x.cost_to_cell)
        new_cell.cost_to_cell = best_parent.cost_to_cell + new_cell.terrain
        self.path_tree.link(best_parent, new_cell)

        # check if better paths emerge from linking this new cell
        candidate_parent = new_cell
        propagated_cells = [(cell, candidate_parent) for cell in valid_parents]
        while propagated_cells:
            old_cell, candidate_parent = propagated_cells.pop()
            new_path = candidate_parent.cost_to_cell + old_cell.terrain
            # if the updated/new cell is a better path -> link
            if new_path < old_cell.cost_to_cell:
                old_cell.cost_to_cell = new_path
                self.path_tree.relink_parent(candidate_parent, old_cell)
                # check if better paths emerge from linking this updated cell
                propagated_cells.extend([(cell, old_cell) for cell in self.get_valid_parents(old_cell.adj_set)])

    def get_valid_parents(self, adj_cells):
        valid_parents = [cell for cell in adj_cells if self.path_tree.contains(cell)]
        assert len(valid_parents) > 0
        return valid_parents

    def get_best_path_wrapper(self, start_cell, end_cell):
        if self.path_tree.contains(start_cell) and self.path_tree.contains(end_cell):
            return self.get_best_path(start_cell, end_cell)
        else:
            return None

    def get_best_path(self, start_cell, end_cell):
        path = [end_cell]
        cell = end_cell
        while True:
            parent = self.path_tree.get_parent_of(cell)
            path.append(parent)
            cell = parent
            if parent.get_loc() == start_cell.get_loc():
                return path[::-1]
            if parent is None:
                assert False # this means the start cell cannot be reached from the end cell!

class Tree():
    def __init__(self, root, hzsh=lambda x : hash(x)):
        self.nodes = {hzsh(root): TreeNode(None, set())}
        self.hzsh = hzsh

    def link(self, parent, child):
        assert self.hzsh(parent) in self.nodes
        if self.hzsh(child) in self.nodes:
            self.nodes[self.hzsh(child)].parent = self.nodes[self.hzsh(parent)]
        else:
            self.nodes[self.hzsh(child)] = TreeNode(parent, set())
        self.nodes[self.hzsh(parent)].children.add(self.nodes[self.hzsh(child)])

    def relink_parent(self, new_parent, child):
        assert self.hzsh(child) in self.nodes and self.hzsh(new_parent) in self.nodes
        old_parent = self.nodes[self.hzsh(child)].parent
        self.nodes[self.hzsh(old_parent)].children.remove(self.nodes[self.hzsh(child)])
        self.nodes[self.hzsh(new_parent)].children.add(self.nodes[self.hzsh(child)])
        self.nodes[self.hzsh(child)].parent = new_parent

    def get_parent_of(self, child):
        return self.nodes[self.hzsh(child)].parent

    def contains(self, child):
        return self.hzsh(child) in self.nodes

class TreeNode():
    def __init__(self, parent, children):
        self.parent = parent
        self.children = children

def get_loc(sanitized_cell):
    x,y,_ = sanitized_cell
    return x,y

def get_dist(x,y,N):
    return 0

def calc_score(agent, N, best_path_score, path_score):
    score = 0
    if agent.done:
        score += 50.0
    else:
        x,y = agent.path
        score += (50.0 * get_dist(x,y,N)) / get_dist(0,0,N)
    score += 50.0*best_path_score/path_score
    return score

def get_path(maze, agent):
    if agent.done:
        path = [maze.end_cell.get_loc()]
        path_score = maze.end_cell.terrain
        while maze.entrance_cell.get_loc() not in path:
            cur_loc = path[-1]
            last_loc = agent.backtracking_path[cur_loc]
            assert last_loc in [cell.get_loc() for cell in maze.maze_dict[cur_loc].adj_set]
            path.append(last_loc)
            path_score += maze.maze_dict[last_loc].terrain
        path = path[::-1]
    else:
        path, path_score = [], 0
    return path, path_score