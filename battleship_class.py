from ship_forms import *
import pygame

shapes = [S, Z, I, J, L, T]
# color_order: green, red, cyan, violet, orange, blue
shape_colors = [(0, 255, 0), (255, 0, 0), (0, 255, 255), 
                (138,43,226), (255, 165, 0), (0, 0, 255)]

class Shot(object):
    rows = 10  # y
    columns = 10  # x

    def __init__(self, column, row, shape):
        self.x = column
        self.y = row
        self.shape = shape
        self.color = (255, 255, 255)
        # number from 0-3
        self.rotation = 0

class Piece(Shot):
    def __init__(self, column, row, shape):
        super().__init__(column, row, shape)
        self.color = shape_colors[shapes.index(shape)]

