import math
from quadtree import Point, Rectangle, QuadTree, Center
import pygame
from tree import Tree

class Grid(Tree):
    def __init__(self, boundary, cell=2):
        self.name = "grid"
        width = boundary.width*2
        height = boundary.height*2
        self.cell = cell
        self.table = []
        self.width_size = int(width / self.cell) 
        self.height_size = int(height / self.cell) 
        self.grid_size = self.width_size * self.height_size
        for i in range(self.grid_size): # 初始時需要將所有的空間都先新增好
            self.table.append([]) 
    
    def insert(self, point):
        u = 13 # 使用任意兩個質數
        v = 7
        x = point.x
        y = point.y

        # hash function
        idx = ((math.floor(x/self.cell) * u) ^ (math.floor(y/self.cell) * v))%self.grid_size
        self.table[idx].append(point)
    
    def clear(self):
         for i in range(self.grid_size):
            self.table[i].clear()

    def draw(self, screen, color=(255,255,255), stroke=1):
        for i in range(self.grid_size):
            x = i % self.width_size
            y = int(i / self.width_size)
            pygame.draw.rect(screen, color, pygame.Rect(x*self.cell, y*self.cell, self.cell-1, self.cell-1), stroke)