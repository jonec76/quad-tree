import pygame
from random import randint
from quadtree import Point, Rectangle, QuadTree, Center
from matplotlib import pyplot as plt
import time

pygame.init()
width = 1000
height = 600
screen = pygame.display.set_mode((width,height))
clock = pygame.time.Clock()
max_v = 2
running = True
count = 0
points = []

def agents(num):
    for i in range(num):
        x, y, xv, yv = randint(1,width), randint(1,height), randint(1,max_v), randint(1,max_v)
        x, y, xv, yv = randint(1,width), randint(1,height), randint(1,max_v), randint(1,max_v)
        points.append(Point(x, y, xv, yv))

pygame.display.set_caption("Test")
domain = Rectangle(Center(width/2, height/2), width/2, height/2)
qtree = QuadTree(domain)
fps = []
insert_time = []

def output(datas, title):
    plt.xlabel("frame")
    plt.ylabel(title)
    plt.plot(list(range(len(datas))), datas) # 從 11 開始取是因為 fps 前 10 個 frame 都是 0，這在官方文件有記載
    plt.savefig(title + ".png")
    plt.clf()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            print("... Output the fps result ...")
            running = False
            output(fps[11:], "fps")
            output(insert_time, "insert")

    fps.append(int(clock.get_fps()))

    screen.fill((0,0,0))
    for point in points:
        point.move(width, height)
    
    agents(5)

    start = time.time()
    for point in points:
        # point.draw(screen)
        qtree.insert(point)
    end = time.time()
    insert_time.append(end - start)

    qtree.draw(screen)
    clock.tick(60)
    qtree.delete()
    pygame.time.wait(10)
    pygame.display.flip()
pygame.QUIT