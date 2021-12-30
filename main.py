#----- info -----
#type 0 to create points and enter to start simulation 

import pygame, Global, math, time
from pygame.draw import circle
from pygame.sndarray import samples
clock = pygame.time.Clock()
screen = pygame.display.set_mode((Global.screen_w,Global.screen_h))
pygame.init()

#globals
points = []
sticks = []
gravity = 70  
prevTime = 0
#classes
class Point:
    def __init__(self, position, prevPosition, locked):
        self.position = position
        self.prevPosition = prevPosition
        self.locked = locked
        self.lives = 0

    def draw(self):
        if(self.locked):
            pygame.draw.circle(screen, Global.LOCKED_POINT_COLOR, self.position, Global.point_radius)
        else:
            pygame.draw.circle(screen, Global.POINT_COLOR, self.position, Global.point_radius)

    def clicked(self):
        x = pygame.mouse.get_pos()[0]
        y = pygame.mouse.get_pos()[1]

        sqx = (x - self.position[0])**2
        sqy = (y - self.position[1])**2

        if math.sqrt(sqx + sqy) <  Global.point_safe_area:
            return True
        return False


class Stick():
    def __init__(self, pointA, pointB, length):
        self.pointA = pointA
        self.pointB = pointB
        self.length = length
        self.rectangle = 0
    def draw(self):
        self.rectangle = pygame.draw.line(screen, Global.STICK_COLOR, self.pointA.position, self.pointB.position, Global.stick_width)

    def isMouseOver(self):
        if (self.rectangle):
            if self.rectangle.collidepoint(pygame.mouse.get_pos()):
                #print("mouse is over stick")
                return True
            else:
                #print("mouse is not over stick")
                return False
            

#functions
def Simulate():
    global prevTime
    #clock.tick(60)
    now = time.time()
    deltaTime = now - prevTime
    prevTime = now
    for p in points:
        if(not(p.locked)):
            positionBeforeUpdate = p.position
            p.position.xy += p.position.xy - p.prevPosition.xy
            p.position.xy += 0, 1 * gravity * deltaTime
            p.prevPosition = positionBeforeUpdate

    #for _ in range(0, 10000):
    for stick in sticks:
        dx = stick.pointA.position.x - stick.pointB.position.x
        dy = stick.pointA.position.y - stick.pointB.position.y
        if(dx != 0 and dy != 0):
            distance_between_points = math.sqrt(dx*dx + dy*dy)
            diff = stick.length - distance_between_points
            percent = diff / distance_between_points / 2
            if(not(stick.pointA.locked)):
                stick.pointA.position.x += dx * percent
                stick.pointA.position.y += dy * percent
            if(not(stick.pointB.locked)):
                stick.pointB.position.x -= dx * percent
                stick.pointB.position.y -= dy * percent
            
def Draw(creatingStickStatus, creatingStickPointA, creatingStickPointB):
    for stick in sticks:
        stick.draw()
    if(creatingStickStatus):
        pygame.draw.line(screen, Global.STICK_COLOR, creatingStickPointA, creatingStickPointB, Global.stick_width)
    #for point in points:
        #point.draw()
def CreatePoint(position):
    points.append(Point(pygame.Vector2(position), pygame.Vector2(position), False))
    return points[-1]

def CreateStick(pointA, pointB):
    dx = pointA.position.x - pointB.position.x
    dy = pointA.position.y - pointB.position.y
    distance_between_points = math.sqrt(dx*dx + dy*dy)    
    sticks.append(Stick(pointA, pointB, distance_between_points))

def isClickingPoint():
    for p in points:
        if(p.clicked()):
            return p
    return False

def isOverStick():
    index = 0
    for s in sticks:
        if(s.isMouseOver()):
            return index
        index += 1
    return -1

def createPoints():
    offset = 7
    size = 100
    sizeY = 25
    startingPointX = -offset-50
    startingPointY = -offset
    currentPointX = 0
    prevPointX = 0
    currentPointY = 0
    prevPointY = 0
    for y in range(0, sizeY):
        startingPointX = offset
        for x in range(0, size):
            currentPointX = CreatePoint((startingPointX, startingPointY))
            if(x != 0): #nie skrajny lewy
                #stworz linie pomiedzy x a x-1
                CreateStick(currentPointX, prevPointX)
            #jezeli nie skrajnie gorny
            if(y != 0):
                CreateStick(currentPointX, points[((y-1)*size)+x])       
            startingPointX += offset
            prevPointX = currentPointX
        startingPointY += offset

    for i in range(0, size):
        points[i].locked = True

    # for i in range(0, size):
    #     points[getPos(0,i,size)].locked = True
    co_ile_x = 1000
    co_ile_y = 1500
    #ostatni
    for i in range(0, size):
        if i % co_ile_x == 0:
            points[getPos(size-1,i,size)].locked = True

    for y in range(0,size):
        if(y % co_ile_y  == 0):
            for i in range(0, size):
                if i % co_ile_x == 0:
                    points[getPos(y,i,size)].locked = True

    #dol
    # for i in range(0, size):
    #     points[getPos(i,size-1,size)].locked = True

    #lock one random point
    points[getPos(10,10,size)].locked = True

def getPos(x,y,size):
    return y * size + x
    

def Start():
    global prevTime
    SimulationState = False
    creatingStickStatus = False
    pointA = Point(0,0,0)
    while True:
        #for every frame
        for event in pygame.event.get():
            #wait for end 
            if event.type == pygame.QUIT:
                sys.exit(0)
            #event for creating point // checking if mouse is clicked
            if event.type == pygame.MOUSEBUTTONDOWN:
                if(not(isClickingPoint())):
                    CreatePoint(pygame.mouse.get_pos())
                else:
                    #creating stick
                    creatingStickStatus = True
                    pointA = isClickingPoint()
            #event for creating line when mouseclcikc is up create line
            if event.type == pygame.MOUSEBUTTONUP:
                if(isClickingPoint() and creatingStickStatus):
                    CreateStick(pointA, isClickingPoint())
                creatingStickStatus = False
            #event for locking the points - if space is clicked and above point then lock point 
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if(isClickingPoint()):
                        if(isClickingPoint().locked):
                            isClickingPoint().locked = False
                        else:
                            isClickingPoint().locked = True 
                if event.key == pygame.K_RETURN:
                    if(SimulationState):
                        SimulationState = False
                        print("Simulation off")
                    else:
                        SimulationState = True
                        prevTime = time.time()
                        print("Simulation on")
                if event.key == pygame.K_0:
                    createPoints()
            if event.type == pygame.MOUSEMOTION:
                stickIndex = isOverStick()
                #print(stickIndex)
                if(stickIndex != -1):
                    sticks[stickIndex].pointA.locked = False
                    sticks[stickIndex].pointB.locked = False
                    sticks.pop(stickIndex)

                    # for stick in sticks:
                    #     stick.pointA.lives += 1
                    #     stick.pointB.lives += 1
                    
                    # for point in points:
                    #     if point.lives <= 3:
                    #         point.locked = False

            

        #background
        if(SimulationState):
            screen.fill(Global.C_BACKGROUND)
        else:
            screen.fill(Global.GRAYER)
        if(SimulationState):
            Simulate()
        Draw(creatingStickStatus, pointA.position, pygame.mouse.get_pos())
        #update screen
        pygame.display.flip()
        pygame.time.wait(1)

Start()