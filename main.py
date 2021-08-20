import pygame
from random import randint
from quadtree import Point, Rectangle, QuadTree, Center

pygame.init()
width = 1000
height = 600
screen = pygame.display.set_mode((width,height))
clock = pygame.time.Clock()
max_v = 2
running = True
count = 0
points = []

def agents(num, count):
    for i in range(num):
        x, y, xv, yv = randint(1,width), randint(1,height), randint(1,max_v), randint(1,max_v)
        x, y, xv, yv = randint(1,width), randint(1,height), randint(1,max_v), randint(1,max_v)
        points.append(Point(x, y, xv, yv))
    count += 1

def test_agents():
    points.append(Point(20, 20, 0, 0))
    points.append(Point(30, 30, 0, 0))
    points.append(Point(35, 35, 0, 0))
    points.append(Point(60, 60, 0, 0))
    points.append(Point(120, 120, 0, 0))
    points.append(Point(420, 420, 0, 0))
    points.append(Point(600, 120, 0, 0))

pygame.display.set_caption("Test")
# agents(100, count)
test_agents()
domain = Rectangle(Center(width/2, height/2), width/2, height/2)
screen.fill((0,0,0))
qtree = QuadTree(domain)

#test loop
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    #RGB
    # domain.draw(screen)
    
        # xs[i] += xvs[i]
        # ys[i] += yvs[i]
    for point in points:
        point.draw(screen)
        qtree.insert(point)
    qtree.draw(screen)

        # if xs[i] >width or xs[i] < 0:
        #     xvs[i] = -xvs[i]
        # if ys[i] >height or ys[i] < 0:
        #     yvs[i] = -yvs[i]

    clock.tick(60)
    pygame.time.wait(500)
    pygame.display.update()

pygame.QUIT