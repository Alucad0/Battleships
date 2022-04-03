from ship_forms import *
import pygame

shapes = [S, Z, I, J, L, T]
# color_order: green, red, cyan, violet, orange, blue
shape_colors = [(0, 255, 0), (255, 0, 0), (0, 255, 255), 
                (138,43,226), (255, 165, 0), (0, 0, 255)]

class Ships(object):
    # y - because the rows are going to be stacked ontop of each other
    rows = 20 
    # x - because the columns are going to be stacked besides each other
    columns = 10  

    def __init__(self, column, row, shape):
        self.x = column
        self.y = row
        self.shape = shape
        self.color = shape_colors[shapes.index(shape)]
        
        self.rotation = 0
        pass


class Board:
    pass
