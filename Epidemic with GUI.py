import pygame, math, random

width=800 #Screen width
height=800 #Screen height
count=100 #Population
start=1 #Start no of Infected
radius=20 #Spreading radius
chance=0.03 #Chance of spreading per frame
time=150 #Time infected for
isolate=0.2#Fraction which isolate
ICU_capacity=0.4 #Fraction that can fit in ICU
normal_death=0.1 #Fraction that die when infected<ICU_capacity
overcrowded_death=0.5 #Fraction that die when infected>ICU_capacity

#Setup
pygame.init()
pygame.font.init()
window = pygame.display.set_mode((width, height))
log=[]
GUI=True
population=[]

#Do the graph in the background
def clear():
    window.fill((255,255,255)) #Clear screen
    if len(log)/10>width:
        a=0
        for i in range(0,len(log)*width,len(log)):
            i=int(i/width)
            pygame.draw.line(window,(255, 99, 99),(a,height),(a,height-(log[i][1]/count*height)),1) #Show infected proportion
            pygame.draw.line(window,(145, 206, 255),(a,(log[i][2]+log[i][3])/count*height),(a,(log[i][0]+log[i][2]+log[i][3])/count*height),1) #Show susceptable proportion
            pygame.draw.line(window,(128, 255, 138),(a,0),(a,log[i][2]/count*height),1) #Show recovered proportion
            pygame.draw.line(window,(200,200,200),(a,log[i][2]/count*height),(a,(log[i][3]+log[i][2])/count*height),1) #Show deceased proportion
            a+=1
    else:   
        for i in range(0,len(log),10):
            pygame.draw.line(window,(255, 99, 99),(i/10,height),(i/10,height-(log[i][1]/count*height)),1)
            pygame.draw.line(window,(145, 206, 255),(i/10,(log[i][2]+log[i][3])/count*height),(i/10,(log[i][0]+log[i][2]+log[i][3])/count*height),1)
            pygame.draw.line(window,(128, 255, 138),(i/10,0),(i/10,log[i][2]/count*height),1)
            pygame.draw.line(window,(200,200,200),(i/10,log[i][2]/count*height),(i/10,(log[i][2]+log[i][3])/count*height),1)
    #Show R value
    myfont = pygame.font.SysFont('Calibri', int(height/16))
    window.blit(myfont.render('R = '+str(round(R,1)), False, (0, 0, 0)),(0, height-50))
def redraw():
    if GUI:
        GUIsetup()
    else:
        myfont = pygame.font.SysFont('Calibri', int(height/16))
        clear()
        #Draw the dots
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
            #Move at angle self.d
            dx=math.cos(self.d)*(width+height)/1200
            dy=math.sin(self.d)*(width+height)/1200
            self.x+=dx
            self.y+=dy
            self.d+=random.uniform(-math.pi/15,math.pi/15)%2*math.pi
            #Check if off screen
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
        #If susceptable, check if it should be infected
        if self.state>-2:
            self.infect()
        #Ammend time in which it has been infected
        if self.state>-1:
            self.state+=1
        #If it has been infected for long enough it will recover or die
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
        #If it's in the radius of an infected person, become infected
        if self.state<0:
            for i in population:
                if i.state>-1:
                    if ((self.x-i.x)**2+(self.y-i.y)**2)<radius**2 and random.random()<chance:
                        self.state=0
                        i.r+=1
                        break
def ifIsolate():
    if random.random()>isolate: return True
    else: return False

#Move arrow in GUI
def slide(i):
    down=True
    while down:
        for event in pygame.event.get():
            #If mouse if let go of, stop moving it
            if event.type == pygame.MOUSEBUTTONUP:
                down=False
            else:
                #Change the position of the arrow
                x=pygame.mouse.get_pos()[0]
                if x<width//10: x=width//10
                if x>width*9//10:
                    x=width*9//10
                var[i]=x
                redraw()
             
def downClick(event):
    #If the RMB is pressed in a certain area, slide
    global GUI
    if event.button==1 and GUI:
        event=event.pos
        for i in range(8):
            if 0<(i+1)*width//9-event[1]<17:
                if -10<var[i]-event[0]<10:
                    slide(i)
                    break
        #If run button is pressed, begin simulation
        if width*8.5//10<event[0]<width*9.7//10 and height*9//10<event[1]<height*9.7//10:
            GUI=False
            setup()
        

def GUIsetup():
    myfont = pygame.font.SysFont('Calibri', int(height/32))
    window.fill((219,219,219))
    variables=[int(x) for x in var]
    for i in range(8):
        #Show lines, arrow, value and range
        pygame.draw.line(window,(0,0,0),(width//10,(i+1)*width//9),(width//10,(i+0.8)*width//9),5)
        pygame.draw.line(window,(0,0,0),(width//10,(i+1)*width//9),(width*9//10,(i+1)*width//9),5)
        pygame.draw.line(window,(0,0,0),(width*9//10,(i+0.8)*width//9),(width*9//10,(i+1)*width//9),5)
        window.blit(rangeOfGUI[i][0],(width//10-10,(i+0.8)*width//9-25))
        window.blit(rangeOfGUI[i][1],(width*9//10-10,(i+0.8)*width//9-25))
        window.blit(names[i],(width//10-10,(i+0.5)*width//9-25))
        pygame.draw.rect(window,(219,219,219),(variables[i]-15,(i+1)*width//9-40, 50,25))
        if i==0 or i==1 or i==5 or i==6 or i==7:
            window.blit(myfont.render(str(round((variables[i]-width/10)/operation[i],2)), False, (0, 0, 0)),(variables[i]-15,(i+1)*width//9-44))
        elif i==2 or i==4:
            window.blit(myfont.render(str(int(round((variables[i]-width/10)/operation[i],0))), False, (0, 0, 0)),(variables[i]-15,(i+1)*width//9-44))
        else:
            window.blit(myfont.render(str(int(round((variables[i]-width/10)/operation[i]+10,0))), False, (0, 0, 0)),(variables[i]-15,(i+1)*width//9-44))
        pygame.draw.polygon(window,(90,176,127),((variables[i],(i+1)*width//9),(variables[i]-10,(i+1)*width//9-17),(variables[i]+10,(i+1)*width//9-17)))
    #Show run button
    pygame.draw.rect(window,(66,170,245),(width*8.5//10, height*9//10, width*1.2//10, height*0.7//10))
    window.blit(myfont.render('Run', False, (0, 0, 0)),(width*8.6//10, height*9.1//10))
    pygame.display.flip()
def setup():
    #Make each variable what its supposed to be
    global isolate, chance, radius, count, time, ICU_capacity, normal_death, overcrowded_death
    lst=[]
    for i in range(8):
        if i==0 or i==1 or i==5 or i==6 or i==7:
            lst.append(round((var[i]-width/10)/operation[i],2))
        elif i==2 or i==4:
            lst.append(int(round((var[i]-width/10)/operation[i],0)))
        else:
            lst.append(int(round((var[i]-width/10)/operation[i]+10,0)))
    isolate=lst[0]
    chance=lst[1]
    radius=lst[2]
    count=lst[3]
    time=lst[4]*12
    ICU_capacity=lst[5]
    normal_death=lst[6]
    overcrowded_death=lst[7]
    #Create people
    for _ in range(start):
        population.append(Person(0,False,0,0,0,0))
    for _ in range(count-start):
        population.append(Person(-1,False,0,0,0,0))
#Setup
radius=radius*(width+height)/1200
R=0
time*=12
a=width*8/10
myfont = pygame.font.SysFont('Calibri', int(height/32))
operation=[a,a,a/60*(width+height)/1200,a/500,a/250,a,a,a]
names=['Fraction of population that isolate','Chance of spreading - Likeliness of catching', 'Spreading radius - Distance which it can spread','Population - Number of dots','Time infected for - How long it remains contagious',
       'Fraction that receive Intensive Care treatment','Chance of death after receiving Intensive Care treatment','Chance of death without receiving Intensive Care treatment']
names=[myfont.render(x, False, (0, 0, 0)) for x in names]
var=[isolate*a+width/10, chance*a+width/10, radius/60*a+width/10, (count-10)/500*a+width/10, time/3000*a+width/10, ICU_capacity*a+width/10, normal_death*a+width/10, overcrowded_death*a+width/10]
rangeOfGUI=((0,1),(0,1),(0,45),(10,510),(0,250),(0,1),(0,1),(0,1))
rangeOfGUI=[(myfont.render(str(i[0]), False, (0, 0, 0)), myfont.render(str(i[1]), False, (0, 0, 0))) for i in rangeOfGUI]
down=False
while True:
    #Calculate R
    susceptable,infected,immune,killed=0,0,0,0
    redraw()
    R=0
    if not GUI:
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
        #If mouse button pressed, move arrow
        if GUI:
            if event.type == pygame.MOUSEBUTTONDOWN:
                down=True
                downClick(event)
        if event.type == pygame.QUIT : 
            pygame.quit()
