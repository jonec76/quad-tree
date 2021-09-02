import numpy as np
import math
import pygame
from random import randint
from tree import Tree

class Point:
    def __init__(self, x, y, xv, yv):
        self.x = x
        self.y = y
        self.x_velocity = xv
        self.y_velocity = yv

    def draw(self, screen, color=(255,255,255), stroke=1):
        pygame.draw.circle(screen, color, (self.x, self.y), stroke)

    def move(self, width, height):
        self.x += self.x_velocity
        self.y += self.y_velocity
        if self.x > width or self.x < 0:
            self.x_velocity = -self.x_velocity
        if self.y > height or self.y < 0:
            self.y_velocity = -self.y_velocity

class Center: # 專門給 Rectangle 用的 
    def __init__(self, x, y):
        self.x = x
        self.y = y

class Rectangle:
    def __init__(self, center, width, height):
        self.center = center
        self.width = width
        self.height = height
        self.west = center.x - width
        self.east = center.x + width
        self.north = center.y - height
        self.south = center.y + height

    def containsPoint(self, point): # 用來檢查這個點是否在 cell 裡面
        return (self.west <= point.x < self.east and 
                self.north <= point.y < self.south)
    
    def draw(self, screen, color=(255,255,255), stroke=1):
        pygame.draw.rect(screen, color, pygame.Rect(self.west, self.north, 2*self.width-1, 2*self.height-1), stroke)

class QuadTree(Tree):
    def __init__(self, boundary,  capacity=2, depth=0, limit_depth=2):
        self.name = "quad"
        self.depth = depth
        self.limit_depth = limit_depth
        self.boundary = boundary
        self.capacity = capacity
        self.points = []
        self.divided = False
        self.leaf = True

    def insert(self, point):
        # if the point is in the range of current quadTree
        if not self.boundary.containsPoint(point): # 如果這個點不在目前這個 cell 的話，就不考慮要 insert 他
            return False
        
        # if has not reached capcaity
        if len(self.points) < self.capacity: # 要是 cell 還有空間可以新增點，則新增
            self.points.append(point)
            return True
        
        if self.depth < self.limit_depth and not self.divided: # 如果目前這個 cell 還沒有被切割過，則切割（因為每個 cell 只能被切割一次，所以才會有這個條件）
            self.divide(self.capacity, self.depth+1, self.limit_depth)

        if self.depth == self.limit_depth: # 如果已經達到限制深度了，那就沒有 sub tree，所有的 point 都要新增到這一層
            self.points.append(point)
            return True
        elif self.nw.insert(point):
            return True
        elif self.ne.insert(point):
            return True
        elif self.sw.insert(point):
            return True
        elif self.se.insert(point):
            return True

        return False
    

    def divide(self, capacity, depth, limit_depth):
        center_x = self.boundary.center.x
        center_y = self.boundary.center.y
        new_width = self.boundary.width / 2
        new_height = self.boundary.height / 2

        nw = Rectangle(Center(center_x - new_width, center_y - new_height), new_width, new_height)
        self.nw = QuadTree(nw, capacity=capacity, depth=depth, limit_depth=limit_depth)

        ne = Rectangle(Center(center_x + new_width, center_y - new_height), new_width, new_height)
        self.ne = QuadTree(ne, capacity=capacity, depth=depth, limit_depth=limit_depth)

        sw = Rectangle(Center(center_x - new_width, center_y + new_height), new_width, new_height)
        self.sw = QuadTree(sw, capacity=capacity, depth=depth, limit_depth=limit_depth)

        se = Rectangle(Center(center_x + new_width, center_y + new_height), new_width, new_height)
        self.se = QuadTree(se, capacity=capacity, depth=depth, limit_depth=limit_depth)

        self.divided = True
        self.leaf = False # 如果還可以分割，表示目前這個 cell 不是 leaf

    def __len__(self):
        count = len(self.points)
        if self.divided:
            count += len(self.nw) + len(self.ne) + len(self.sw) + len(self.se) 
        
        return count
    
    def draw(self, screen):
        self.boundary.draw(screen)

        if self.divided:
            self.nw.draw(screen)
            self.ne.draw(screen)
            self.se.draw(screen)
            self.sw.draw(screen)
    
    def clear(self): # 用來將目前的整個樹清除
        if self.leaf == False:
            self.nw.clear()
            self.ne.clear()
            self.se.clear()
            self.sw.clear()
            self.leaf = True
            self.divided = False
        self.points.clear()
