"""
Código creado por Electro de Una
Youtube: Electronica de Una
2021
"""
import max7219
from machine import Pin, SPI, ADC
import framebuf
from time import sleep
import random

spi = SPI(0, baudrate=10000000, polarity=1, phase=0, sck=Pin(2), mosi=Pin(3))
ss = Pin(5, Pin.OUT)

display = max7219.Matrix8x8(spi, ss, 1)

SW_pin=4
xAxis = ADC(Pin(27))
yAxis = ADC(Pin(26))
screenWidth=8
screenHeight=8
snakeSize=1
isGameOver=False
tailX=[]
tailY=[]
direction=""
# setupSnakePosition
snakeX=4
snakeY=4
foodX=6
foodY=6
eat=False
spd=0.2
  
def setupFoodPosition():
    global foodX,foodY
    foodX, foodY = random.randrange(0, 7), random.randrange(0, 7)
    
def initSnake():
    tailX.append(snakeX)
    tailY.append(snakeY)
  
def showGameOverScreen():
    for i in range(screenHeight):
        for j in range(screenWidth):
            showLed(j, i, 1)
            sleep(0.05)
    for i in range(screenHeight):
        for j in range(screenWidth):
            showLed(j, i, 0)
            sleep(0.05)
    resetVariables()

def showLed(row, column, c):
    display.pixel(row, column, c)
    display.show()

def resetVariables():
    global direction, isGameOver, snakeSize, spd
    setupSnakePosition()
    setupFoodPosition()
    direction=""
    isGameOver=False
    snakeSize=1
    tailX.clear()
    tailY.clear()
    spd=0.2
    display.fill(0)
    display.show()
    initSnake()

def setupSnakePosition():
    global snakeX,snakeY
    snakeX=4
    snakeY=4

def startGame():
    manageGameOver()
    setJoystickDirection()
    changeSnakeDirection()
    manageSnakeOutOfBounds()
    manageEatenFood()
    manageSnakeTailCoordinates()
    drawSnake()
    sleep(spd)

def manageGameOver():
    global isGameOver
    for i in range(1, snakeSize-1):
        if tailX[i] == snakeX and tailY[i] == snakeY:
            isGameOver=True
    
def setJoystickDirection():
    xValue = xAxis.read_u16()
    yValue = yAxis.read_u16()
    global direction
    if xValue <= 5000:
        direction="left"
    elif xValue >= 50000:
        direction="right"
    elif yValue <= 5000:
        direction="up"
    elif yValue >= 50000:
        direction="down"
  
def changeSnakeDirection():
    global snakeX, snakeY
    if direction == "left":
        snakeX=snakeX-1
    if direction == "right":
        snakeX=snakeX+1
    if direction == "up":
        snakeY=snakeY-1
    if direction == "down":
        snakeY=snakeY+1

def manageSnakeOutOfBounds():
    global snakeX, snakeY
    if snakeX >= screenWidth:
        snakeX=0
    elif snakeX < 0:
        snakeX=screenWidth-1
  
    if snakeY >= screenHeight:
        snakeY=0
    elif snakeY < 0:
        snakeY=screenHeight-1
  
def manageEatenFood():
    global snakeSize, eat
    if snakeX == foodX and snakeY == foodY:
        snakeSize=snakeSize+1
        setupFoodPosition()
        SpeedUp()
        eat=True
    else:
        eat=False
  
def manageSnakeTailCoordinates():
    tailX.insert(0,snakeX)
    tailY.insert(0,snakeY)
    tailIndex = len(tailX)-1
    if eat==False:
        tailX.pop(tailIndex)
        tailY.pop(tailIndex)
  
def drawSnake():
    for i in range(screenHeight):
        for j in range(screenWidth):
            if i == foodY and j == foodX:
                showLed(foodX, foodY, 1)
            else:
                isShown=False
                for idx, item in enumerate(tailX):
                    if tailX[idx]==j and tailY[idx]==i:
                        showLed(tailX[idx], tailY[idx], 1)
                        isShown=True
                if isShown==False:
                    showLed(j, i, 0)

def SpeedUp():
    global spd
    spd -= 0.01
    if spd<0: spd=0

# setupLedBoard
display.brightness(1)   # ajustar brillo 1 a 15
display.fill(1)
display.show()
sleep(0.5)
display.fill(0)
display.show()
sleep(0.2)
setupFoodPosition()
initSnake()

while True:
    if isGameOver == True:
        showGameOverScreen()
    else:
        startGame()