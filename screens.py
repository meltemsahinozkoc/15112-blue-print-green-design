# all screens here. draw funcs.
from cmu_graphics import *
from components import *
from utils import *

def drawBg(app):
    drawRect(0,0,app.width, app.height, fill = app.fill)

def draw0HomeScreen(app):    
    buttons = Button(app.height/2, 3, app.width/3, 50,['1 "DRAW"', '2 "DETAIL"', '3 "CALCULATE"'])
    buttons.draw()

    margin = 100
    drawLabel('BLUE PRINT GREEN DESIGN', app.width/2, app.height/8, size=24, fill='white', bold=True, font=app.font)
    drawLabel(app.instruction, app.width/2, app.height/6, size=16, fill='white', bold=True, font=app.font)
    drawLabel('GALLERY', app.width/2, app.height/1.5, size=24, fill='white', bold=True, font=app.font)


def draw1DrawScreen(app):
    buttonsTop = Button(0, 4, app.width/4, 50,['PROJECT NAME', 'LOCATION', 'DIMENSIONS', 'HEIGHT'])
    buttonsTop2 = Button(50, 2, app.width/2, 50,['+ADD WINDOW', '+ADD DOOR'])
    buttonsBottom = Button(app.height-50, 3, app.width/3, 50,['RESET', 'TOGGLE VIEW', 'HELP'])
    buttonsTop.draw()
    buttonsTop2.draw()
    buttonsBottom.draw()

    

def draw2DetailScreen(app):
    buttonsTop = Button(app.height/2, 5, app.width/5, 50,['WALLS (W)', 'WINDOWS (G)', 'DOORS (D)', 'FLOOR (F)', 'ROOF (R)'])
    buttonsBottom = Button(app.height-50, 3, app.width/3, 50,['RESET', 'SAVE', 'HELP'])
    buttonsTop.draw()
    buttonsBottom.draw()
    

def draw3CalculateScreen(app):
    drawLabel('TRANSMISSION LOSSES', app.width/2, app.height/8, size=24, fill='white', bold=True, font=app.font)
    buttonsBottom = Button(app.height-50, 3, app.width/3, 50,['RESET', 'SAVE', 'HELP'])
    drawLabel('RETROFIT SUGGESTIONS', app.width/2, app.height-250, size=24, fill='white', bold=True, font=app.font)
    buttonsBottom.draw()


def draw3_1PopUp(app):
    pass

def draw3_2PopUp(app):
    pass


def onKeyPress(app, key):
    if key == 'right':
        setActiveScreen('game')



