from config import MAX_COST, MIN_COST, WINDOW_SIZE, TICK_SPEED

import turtle
import math
UNIT_STEP = 20

class Animator:
    def __init__(self, maze):
        self.N = maze.N
        self.unit_step = WINDOW_SIZE/self.N
        self.screen_dims = (WINDOW_SIZE, WINDOW_SIZE)
        
        self.wn = turtle.Screen()
        self.wn.title("maze soving")
        self.wn.bgcolor('white')
        self.wn.setup(1.5*WINDOW_SIZE, 1.5*WINDOW_SIZE)
        self.wn.tracer(0, 0)
        
        self.pen = turtle.Turtle()
        self.pen.hideturtle()
        self.pen.speed(0)
        
        self.maze = maze
        self.next_cell = maze.entrance_cell
        self.explored_cells = []
        self.candidate_cells = [maze.entrance_cell]
        self.path = []
        
        self.animate()
    
    def reset(self, maze):
        self.N = maze.N
        self.unit_step = WINDOW_SIZE/self.N
        
        self.maze = maze
        self.next_cell = maze.entrance_cell
        self.explored_cells = []
        self.candidate_cells = [maze.entrance_cell]
        self.path = []
    
    def animate(self):
        turtle.resetscreen()
        self.pen.penup()
        
        for cell in self.maze.maze_dict.values():
            self.draw_square(self.get_loc(cell), self.get_color(cell, (0.2,0.2)))
        
        for cell in self.explored_cells:
            self.draw_square(self.get_loc(cell), self.get_color(cell, (1,0)))
        
        for cell in self.candidate_cells:
            self.draw_square(self.get_loc(cell), self.get_color(cell, (0,1)))
        
        for loc in self.path:
            cell = self.maze.maze_dict[loc]
            self.draw_square(self.get_loc(cell), 'pink')
        
        self.draw_square(self.get_loc(self.next_cell), 'pink')
        
        # self.pen.update()
        self.wn.ontimer(self.animate, TICK_SPEED)
    
    def draw_frame(self, next_cell, explored_cells, candidate_cells):
        self.next_cell = next_cell
        self.explored_cells = explored_cells
        self.candidate_cells = candidate_cells
        self.wn.update()
        
    def draw_path(self, path):
        self.path = path
        self.wn.update()
        
        # self.pen.clear()
        # self.pen.reset()
        # self.wn.clear()
        # self.wn.reset()
        # turtle.clearscreen()
    
    def draw_square(self, loc, c):
        self.pen.goto(*loc)
        self.pen.pendown()
        self.pen.pensize(1)
        self.pen.color(c,c)
        self.pen.begin_fill()
        for _ in range(4):
            self.pen.forward(self.unit_step)
            self.pen.left(90)
        self.pen.end_fill()
        self.pen.penup()

    def get_loc(self, cell):
        width, height = self.screen_dims
        return (self.unit_step*cell.x - width/2, self.unit_step*cell.y - height/2)

    def get_color(self, cell, rb_base):
        if cell.is_wall:
            return 'white'
        Red, Blu = rb_base
        cost = (cell.terrain-MIN_COST)/(MAX_COST-MIN_COST)
        Grn = cost
        color = (Red, Grn, Blu)
        return color

# def draw_maze(maze):
    # screen = turtle.Screen()
    # screen.setup(WIDTH*2, WIDTH)
    # unit_step = int(width/(maze.N))
    # width, height = UNIT_STEP*(maze.N), UNIT_STEP*(maze.N)
    # turtle.Screen().setup(1.5*width, 1.5*height)
    # screen_dims = (width, height)
    
    # turtle.hideturtle()
    # turtle.tracer(0, 0)
    # turtle.speed(0)
    # turtle.penup()
    
    # for cell in maze.maze_dict.values():
        # draw_square(get_loc(cell, screen_dims), get_color(cell))
    # turtle.update()

# def get_loc(cell, screen_dims):
    # width, height = screen_dims
    # return (UNIT_STEP*cell.x - width/2, UNIT_STEP*cell.y - height/2)
    
# def get_color(cell):
    # cost = (cell.terrain-MIN_COST)/(MAX_COST-MIN_COST)
    # Red = 1
    # Grn = cost
    # Blu = 0
    # color = (Red, Grn, Blu)
    # return color

# def draw_square(loc, c):
    # turtle.goto(*loc)
    # turtle.pendown()
    # turtle.pensize(1)
    # turtle.color(c,c)
    # turtle.begin_fill()
    # for _ in range(4):
        # turtle.forward(UNIT_STEP)
        # turtle.left(90)
    # turtle.end_fill()
    # turtle.penup()