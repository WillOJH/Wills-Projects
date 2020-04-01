import pygame, math, random

width=800 #Screen width
height=800 #Screen height
count=100 #Population
start=1 #Start no of Infected
radius=10 #Spreading radius
chance=0.03 #Chance of spreading per frame
time=150 #Time infected for
isolate=0.2 #Fraction which isolate
ICU_capacity=0.4 #Fraction that can fit in ICU
normal_death=0.1 #Fraction that die when infected<ICU_capacity
overcrowded_death=0.5 #Fraction that die when infected>ICU_capacity

pygame.init()
pygame.font.init()
window = pygame.display.set_mode((width, height))
log=[]
population=[]
def clear():
    window.fill((255,255,255))
    if len(log)/10>width:
        a=0
        for i in range(0,len(log)*width,len(log)):
            i=int(i/width)
            pygame.draw.line(window,(255, 99, 99),(a,height),(a,height-(log[i][1]/count*height)),1)
            pygame.draw.line(window,(145, 206, 255),(a,(log[i][2]+log[i][3])/count*height),(a,(log[i][0]+log[i][2]+log[i][3])/count*height),1)
            pygame.draw.line(window,(128, 255, 138),(a,0),(a,log[i][2]/count*height),1)
            pygame.draw.line(window,(200,200,200),(a,log[i][2]/count*height),(a,(log[i][3]+log[i][2])/count*height),1)
            a+=1
    else:   
        for i in range(0,len(log),10):
            pygame.draw.line(window,(255, 99, 99),(i/10,height),(i/10,height-(log[i][1]/count*height)),1)
            pygame.draw.line(window,(145, 206, 255),(i/10,(log[i][2]+log[i][3])/count*height),(i/10,(log[i][0]+log[i][2]+log[i][3])/count*height),1)
            pygame.draw.line(window,(128, 255, 138),(i/10,0),(i/10,log[i][2]/count*height),1)
            pygame.draw.line(window,(200,200,200),(i/10,log[i][2]/count*height),(i/10,(log[i][2]+log[i][3])/count*height),1)
    
    window.blit(myfont.render('R = '+str(round(R,1)), False, (0, 0, 0)),(0, height-50))
def redraw():
    clear()
    for i in population:
        if i.state==-1:
            pygame.draw.circle(window, (0,0,255), ((int(i.x)),(int(i.y))), math.ceil(width/125), 0)
        elif i.state==-2:
            pygame.draw.circle(window, (67,222,77), ((int(i.x)),(int(i.y))), math.ceil(width/125), 0)
        elif i.state==-3:
            pygame.draw.circle(window, (128,128,128), ((int(i.x)),(int(i.y))), math.ceil(width/125), 0)
        else:
            pygame.draw.circle(window, (255,0,0), ((int(i.x)),(int(i.y))), math.ceil(width/125), 0)
        pygame.draw.circle(window, (0,0,0), ((int(i.x)),(int(i.y))),math.ceil(width/125),math.ceil(width/1000))
    pygame.display.flip()
def ifIsolate():
    if random.random()<isolate: return False
    else: return True
class Person:
    def __init__(self,state,isolate,x,y,d,r):
        self.state=state
        self.isolate=isolate
        self.x=x
        self.y=y
        self.d=d
        self.r=r
        self.x=random.randint(0,width)
        self.y=random.randint(0,height)
        self.d=random.uniform(0,2*math.pi)
        self.isolate=ifIsolate()
    def move(self):
        if self.isolate and not self.state==-3:
            dx=math.cos(self.d)*(width+height)/1200
            dy=math.sin(self.d)*(width+height)/1200
            self.x+=dx
            self.y+=dy
            self.d+=random.uniform(-math.pi/15,math.pi/15)%2*math.pi
            if self.x<0:
                self.x=0
                self.d=(self.d+math.pi)%2*math.pi
            if self.y<0:
                self.y=0
                self.d=(self.d+math.pi)%2*math.pi
            if self.x>width:
                self.x=width
                self.d=(self.d+math.pi)%2*math.pi
            if self.y>height:
                self.y=height
                self.d=(self.d+math.pi)%2*math.pi
        if self.state>-2:
            self.infect()
        if self.state>-1:
            self.state+=1
        if self.state>time:
            if infected/count<ICU_capacity:
                if random.random()<normal_death:
                    self.state=-3
                else:
                    self.state=-2
            elif random.random()<overcrowded_death:
                self.state=-3
            else:
                self.state=-2
    def infect(self):
        if self.state<0:
            for i in population:
                if i.state>-1:
                    if ((self.x-i.x)**2+(self.y-i.y)**2)**0.5<radius and random.random()<chance:
                        self.state=0
                        i.r+=1
                        break      
for _ in range(start):
    population.append(Person(0,False,0,0,0,0))
for _ in range(count-start):
    population.append(Person(-1,False,0,0,0,0))
radius=radius*(width+height)/1200
R=0
time*=12
myfont = pygame.font.SysFont('Calibri', 50)
clear()
while True:
    susceptable,infected,immune,killed=0,0,0,0
    redraw()
    R=0
    for i in population:
        i.move()
        if i.state==-1:
            susceptable+=1
        elif i.state==-2:
            immune+=1
        elif i.state==-3:
            killed+=1
        else:
            infected+=1
            R+=i.r*time/i.state
    if R>0:
        R=R/infected
    log.append([susceptable,infected,immune,killed])
    for event in pygame.event.get():
        if event.type == pygame.QUIT : 
            pygame.quit() 
