# %%
import pygame
from random import randint
from quadtree import Point, Rectangle, QuadTree, Center
from grid import Grid
from matplotlib import pyplot as plt
import time
import numpy as np
from numpy import asarray
from numpy import save
import pandas as pd

width = 1000
height = 600
max_v = 2
new_points = 0 # 每個 frame 新增多少點數
q_capacity = 50
q_limit_depth = 50
g_cell_size = 100

limit_time = 3 # program 執行時間
limit_points = 200

pygame.init()
pygame.display.set_caption("Test")
domain = Rectangle(Center(width/2, height/2), width/2, height/2)
q_domain = Rectangle(Center(500, 300), 350, 270)
qtree = QuadTree(domain, capacity=q_capacity, limit_depth=q_limit_depth)
grid = Grid(domain, cell=g_cell_size)

# change the structure: grid/qtree
tree = qtree

screen = pygame.display.set_mode((width,height))
clock = pygame.time.Clock()
points = []
fps = []
insert_time = []
num_point = []
query_time = []
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

def output_img(datas, title): # 將結果輸出成圖片
    plt.xlabel("frame")
    plt.ylabel(title)
    plt.plot(list(range(len(datas))), datas) # 從 11 開始取是因為 fps 前 10 個 frame 都是 0，這在官方文件有記載
    plt.savefig(title + ".png")
    plt.clf()

def output_excel(fps, insert_time, num_point):
    print(len(num_point))
    data = {'總共點數量': num_point, 'fps':fps, 'insert time':[format(i, '.8f') if i < 10e-5 else i for i in insert_time ]}
    df = pd.DataFrame(data)
    df.to_excel("fps_insert.xlsx", index=False)
  
def record(fps, insert_time, query_time, tree_name, num_point):
    print("... Output the fps result ...")
    output_img(fps, tree_name+"_fps")
    output_img(insert_time, tree_name+"_insert")
    output_excel(fps, insert_time, num_point)
    data = asarray(query_time)
    save(tree_name+'.npy', data)

start_ticks=pygame.time.get_ticks() #starter tick

while run:
    agents(new_points)
    new_points += 1
    screen.fill((0,0,0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            record(fps, insert_time, query_time, tree.name, num_point)
            run = False
            break
    
    keys = pygame.key.get_pressed()

    if keys[pygame.K_DOWN]:
        if q_domain.center.y + q_domain.height + 1 < height:
            q_domain.update(Center(q_domain.center.x, q_domain.center.y + 1))
    elif keys[pygame.K_UP]:
        if q_domain.center.y - q_domain.height - 1 > 0:
            q_domain.update(Center(q_domain.center.x, q_domain.center.y - 1))
    elif keys[pygame.K_RIGHT]:
        if q_domain.center.x + q_domain.width + 1 < width:
            q_domain.update(Center(q_domain.center.x + 1, q_domain.center.y))
    elif keys[pygame.K_LEFT]:
        if q_domain.center.x - q_domain.width - 1 > 0:
            q_domain.update(Center(q_domain.center.x - 1, q_domain.center.y))
    else:
        pass

    q_domain.draw(screen, color=(255,0,0), stroke=4)
    seconds=(pygame.time.get_ticks()-start_ticks)/1000 #calculate how many seconds
    if (new_points % 10) == 0:
        print(new_points)
    
    if seconds > limit_time or new_points > limit_points: # if more than limit_time seconds close the game
        record(fps, insert_time, query_time, tree.name, num_point)
        run = False
        break
    if not run:
        break
    num_point.append(len(points))
    fps.append(int(clock.get_fps()))

    #讓所有的點都移動
    # for point in points:
    #     point.move(width, height)

    start = time.time() # 記錄下 insert 所有點數的時間
    for point in points:
        point.draw(screen)
        tree.insert(point)
    end = time.time()
    insert_time.append(end - start)

    found = []
    start = time.time() # 記錄下 insert 所有點數的時間
    tree.query(q_domain, found)
    end = time.time()
    query_time.append(end - start)

    for p in found:
        p.draw(screen, color=(255,0,0), stroke=2)

    tree.draw(screen)
    tree.clear()
    clock.tick(60)
    pygame.display.flip()
    pygame.time.wait(10)
pygame.QUIT

# %%
# from matplotlib import pyplot as plt

# def output2(datas, datas2, title): # 將結果輸出成圖片
#     plt.xlabel("新增點的個數")
#     plt.ylabel(title)
#     plt.plot(list(range(len(datas))), datas, label = 'grid') # 從 11 開始取是因為 fps 前 10 個 frame 都是 0，這在官方文件有記載
#     plt.plot(list(range(len(datas2))), datas2, label = 'quad') # 從 11 開始取是因為 fps 前 10 個 frame 都是 0，這在官方文件有記載
#     plt.legend()
#     plt.savefig(title)
#     plt.clf()

# from numpy import load
# g = load("grid.npy")
# q = load("quad.npy")

# # 將兩個時間結果做比較
# output2(g, q, "query_cmp.png")


# %%
