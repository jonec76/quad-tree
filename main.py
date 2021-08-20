import pygame
from random import randint

pygame.init()
width = 1000
length = 600
screen = pygame.display.set_mode((width,length))
clock = pygame.time.Clock()
max_v = 2
running = True
count = 0
xs = []
ys = []
xvs = []
yvs = []


def agents(num, count):
    for i in range(1,num+1):
        x,y,xv,yv = randint(1,width),randint(1,length),randint(1,max_v),randint(1,max_v)
        xs.append(x)
        ys.append(y)
        xvs.append(xv)
        yvs.append(yv)
    count += 1



pygame.display.set_caption("Test")

#test loop
while running:
   for event in pygame.event.get():
       if event.type == pygame.QUIT:
           running = False

   #RGB
   screen.fill((0,0,0))
   agents(100,count)
   print(len(xs))
   for i in range(len(xs)):
       pygame.draw.circle(screen,(255,255,255),(xs[i],ys[i]),1)
       
       xs[i] += xvs[i]
       ys[i] += yvs[i]


       if xs[i] >width or xs[i] < 0:
           xvs[i] = -xvs[i]
       if ys[i] >length or ys[i] < 0:
           yvs[i] = -yvs[i]

   clock.tick(1)
   pygame.time.wait(10)
   pygame.display.update()

pygame.QUIT