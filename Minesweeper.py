import random, pygame

x=20 #Width of grid
y=20 #Height of grid
size=25 #Size of box
numberOfMines=40 #Number of mines
width=(x+2)*size
height=(y+3)*size
end=False
pygame.init()
pygame.font.init()
window = pygame.display.set_mode((width, height))
class Cell():
    def __init__(self,state,revealed,x,y,flag):
        self.state=state
        self.revealed=revealed
        self.x=x
        self.y=y
        self.flag=flag
    def flood(self):
        if self.state==0:
            for i in cells:
                if abs(i.x-self.x)<=1 and abs(i.y-self.y)<=1 and i.revealed==False:
                    if self.state==0:
                        i.revealed=True
                        i.flag=False
                        i.flood()
        
def win():
    global end
    end=True
    myfont = pygame.font.SysFont('Calibri', int(size*1.5))
    #pygame.draw.rect(window,(255,255,255),(int(width//2-size*3.75), int(height//2-size*1.25),int(size*8),int(size*2.5)))
    window.blit(myfont.render("You Win", False, (0, 0, 0)),(int(width//2-size*2.5), int(height-size*1.5)))
def grid(dimentions):
    b=0
    for i in cells:
        if i.revealed==False:
            pygame.draw.rect(window,(128,128,128),(dimentions[0]+size*i.x,dimentions[1]+size*i.y,size,size),0)
            b+=1
    for i in cells:
        pygame.draw.rect(window,(0,0,0),(dimentions[0]+size*i.x,dimentions[1]+size*i.y,size,size),3)
    return b
def show():
    global end
    end=False
    window.fill((255,255,255))
    b=grid(((width-size*x)/2,(height-size*y)/2))
    myfont = pygame.font.SysFont('Calibri', size)
    text=[]
    for i in cells:
        if i.flag==True:
            text.append(myfont.render("P", False, (0, 0, 0)))
        elif i.state==-1:
            text.append(myfont.render("M", False, (0, 0, 0)))
            if i.revealed==True:
                end=True
        else:
            text.append(myfont.render(str(i.state), False, (0, 0, 0)))
    a=0
    if end:
        for i in cells:
            if not i.state==0:
                if i.revealed==True or i.flag==True or i.state==-1:
                    window.blit(text[a],(((width-size*x)/2+size*i.x),((height-size*y)/2+size*i.y)))
            a+=1
        endgame()
    else:
        for i in cells:
            if not i.state==0:
                if i.revealed==True or i.flag==True:
                    window.blit(text[a],(((width-size*x)/2+size*i.x),((height-size*y)/2+size*i.y)))
                
            a+=1
    

        if b==numberOfMines:
            win()
    
    pygame.display.flip()
def endgame():
    myfont = pygame.font.SysFont('Calibri', int(size*1.5))
    window.blit(myfont.render("You Lost", False, (0, 0, 0)),(int(width//2-size*2.5), int(height-size*1.5)))
        
def leftClick(pos):
    for i in cells:
        if -1*size<((width-size*x)/2+size*i.x)-pos[0]<0 and -1*size<((height-size*y)/2+size*i.y)-pos[1]<0 and i.flag==False:
            i.revealed=True
            i.flood()           
    show()
    
def rightClick(pos):
    for i in cells:
        if -1*size<((width-size*x)/2+size*i.x)-pos[0]<0 and -1*size<((height-size*y)/2+size*i.y)-pos[1]<0 and i.revealed==False:
            if i.flag==False: i.flag=True
            else: i.flag=False
    show()
                
            

                

def click(event, end):
    if not end:
        event=[event.pos, event.button]
        if event[1]==1:
            leftClick(event[0])
        elif event[1]==3:
            rightClick(event[0])

cells=[Cell(0,False,i%x,i//x,False) for i in range(x*y)]
a=0
while a<numberOfMines:
    b=random.randint(0,y-1)
    c=random.randint(0,x-1)
    if cells[b*y+c].state>-1:
        cells[b*y+c].state=-1
        for j in cells:
            if not j.state==-1:
                if abs(j.x-cells[b*y+c].x)<=1 and abs(j.y-cells[b*y+c].y)<=1:
                    j.state+=1
        a+=1

        


end=False
show()
while True:
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN:
            click(event, end)
        if event.type == pygame.QUIT : 
            pygame.quit() 
