import math

from matplotlib.pyplot import quiver
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
    
    def get_hash_idx(self, point):
        u = 13 # 使用任意兩個質數
        v = 7
        x = point.x
        y = point.y

        # hash function
        idx = ((math.floor(x/self.cell) * u) ^ (math.floor(y/self.cell) * v))%self.grid_size
        return idx

    def insert(self, point):
        idx = self.get_hash_idx(point)
        self.table[idx].append(point)
    
    def clear(self):
         for i in range(self.grid_size):
            self.table[i].clear()

    def draw(self, screen, color=(255,255,255), stroke=1):
        for i in range(self.grid_size):
            x = i % self.width_size
            y = int(i / self.width_size)
            pygame.draw.rect(screen, color, pygame.Rect(x*self.cell, y*self.cell, self.cell-1, self.cell-1), stroke)
    
    def get_all_pts(self, wn, es):
        start_x = wn.x
        end_x = es.x
        start_y = wn.y
        end_y = es.y

        pts = []

        while start_x < end_x+self.cell:
            while start_y < end_y:
                pts.append(Center(start_x, start_y))
                start_y += self.cell
            pts.append(Center(start_x, end_y))
            start_y = wn.y
            start_x += self.cell
        return pts

    def query(self, q_domain, found):
        boundary_pts = self.get_all_pts(Center(q_domain.west, q_domain.north), Center(q_domain.east, q_domain.south))
        for b_pt in boundary_pts:
            idx = self.get_hash_idx(b_pt)
            for pt in self.table[idx]:
                if q_domain.containsPoint(pt):
                    found.append(pt)