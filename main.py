import pygame
from random import randint
from quadtree import Point, Rectangle, QuadTree, Center
from grid import Grid
from matplotlib import pyplot as plt
import time

width = 1000
height = 600
max_v = 2
new_points = 5

pygame.init()
screen = pygame.display.set_mode((width,height))
clock = pygame.time.Clock()
pygame.display.set_caption("Test")
domain = Rectangle(Center(width/2, height/2), width/2, height/2)
points = []
fps = []
insert_time = []
run = True

qtree = QuadTree(domain)
grid = Grid(domain, cell=100)

tree = grid
def agents(num):
    for i in range(num):
        x, y, xv, yv = randint(1,width), randint(1,height), randint(1,max_v), randint(1,max_v)
        x, y, xv, yv = randint(1,width), randint(1,height), randint(1,max_v), randint(1,max_v)
        points.append(Point(x, y, xv, yv))

def output(datas, title):
    plt.xlabel("frame")
    plt.ylabel(title)
    plt.plot(list(range(len(datas))), datas) # 從 11 開始取是因為 fps 前 10 個 frame 都是 0，這在官方文件有記載
    plt.savefig(title + ".png")
    plt.clf()

while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            print("... Output the fps result ...")
            output(fps[11:], tree.name+"_fps")
            output(insert_time, tree.name+"_insert")
            run = False
            break
    if not run:
        break
    screen.fill((0,0,0))

    fps.append(int(clock.get_fps()))

    for point in points:
        point.move(width, height)
    
    agents(new_points)

    start = time.time()
    for point in points:
        point.draw(screen)
        tree.insert(point)
    end = time.time()
    insert_time.append(end - start)

    tree.draw(screen)
    tree.clear()
    clock.tick(60)
    pygame.time.wait(10)
    pygame.display.flip()
pygame.QUIT