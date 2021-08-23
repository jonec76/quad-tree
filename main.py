import pygame
from random import randint
from quadtree import Point, Rectangle, QuadTree, Center
from grid import Grid
from matplotlib import pyplot as plt
import time

width = 1000
height = 600
max_v = 2
new_points = 5 # 每個 frame 新增多少點數
limit_time = 10 # program 執行時間
q_capacity = 5 
q_limit_depth = 5
g_cell_size = 100

pygame.init()
pygame.display.set_caption("Test")
domain = Rectangle(Center(width/2, height/2), width/2, height/2)
qtree = QuadTree(domain, capacity=q_capacity, limit_depth=q_limit_depth)
grid = Grid(domain, cell=g_cell_size)

# change the structure: grid/qtree
tree = grid

screen = pygame.display.set_mode((width,height))
clock = pygame.time.Clock()
points = []
fps = []
insert_time = []
run = True

def agents(num):
    for i in range(num):
        if randint(0, 1) == 0:
            coef = -1
        else:
            coef = 1

        x, y, xv, yv = randint(1,width), randint(1,height), coef*randint(1,max_v), coef*randint(1,max_v)
        x, y, xv, yv = randint(1,width), randint(1,height), coef*randint(1,max_v), coef*randint(1,max_v)
        points.append(Point(x, y, xv, yv))

def output(datas, title): # 將結果輸出成圖片
    plt.xlabel("frame")
    plt.ylabel(title)
    plt.plot(list(range(len(datas))), datas) # 從 11 開始取是因為 fps 前 10 個 frame 都是 0，這在官方文件有記載
    plt.savefig(title + ".png")
    plt.clf()

start_ticks=pygame.time.get_ticks() #starter tick
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            print("... Output the fps result ...")
            output(fps[11:], tree.name+"_fps")
            output(insert_time, tree.name+"_insert")
            run = False
            break
    seconds=(pygame.time.get_ticks()-start_ticks)/1000 #calculate how many seconds
    if seconds > limit_time: # if more than limit_time seconds close the game
        print("... Output the fps result ...")
        output(fps[11:], tree.name+"_fps")
        output(insert_time, tree.name+"_insert")
        break
    if not run:
        break
    screen.fill((0,0,0))

    fps.append(int(clock.get_fps()))

    for point in points: # 讓所有的點都移動
        point.move(width, height)
    
    agents(new_points)

    start = time.time() # 記錄下 insert 所有點數的時間
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