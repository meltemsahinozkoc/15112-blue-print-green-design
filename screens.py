# all screens here. draw funcs.
from cmu_graphics import *
from components import *
from utils import *

def drawBg(app):
    drawRect(0,0,app.width, app.height, fill = app.fill)

def draw0HomeScreen(app):    
    buttons = Button(app.height/2, 3, app.width/3, 50,['1. Draw', '2. See', '3. Detail & Calculate'])
    buttons.draw()

    margin = 100
    drawLabel('BLUE PRINT GREEN DESIGN', app.width/2, app.height/8, size=24, fill='white', bold=True, font=app.font)
    drawLabel(app.instruction, app.width/2, app.height/6, size=16, fill='white', bold=True, font=app.font)
    drawLabel('GALLERY', app.width/2, app.height/1.5, size=24, fill='white', bold=True, font=app.font)


def draw1DrawScreen(app):
    buttons1 = Button(20, 4, app.width/4, 50,['PROJECT NAME', 'LOCATION', 'DIMENSIONS', 'HEIGHT'])
    buttons2 = Button(app.height-100, 3, app.width/3, 50,['RESET', 'HELP', 'TOGGLE VIEW'])
    buttons1.draw()
    buttons2.draw()

    

def draw2DetailScreen(app):
    pass

def draw3CalculateScreen(app):
    pass

def draw3_1PopUp(app):
    pass

def draw3_2PopUp(app):
    pass


def onKeyPress(app, key):
    if key == 'right':
        setActiveScreen('game')



