# init + transition bw screens
from cmu_graphics import *


def onAppStart(app):
    app.fill = 'mediumblue'

    app.screen= 'home' # draw, see, detail_calculate
    app.font = 'monospace'

    app.windows = []
    app.walls = []
    app.doors = []
    app.floors = []
    app.roofs = []
    
    app.instruction = (''' 
    Lorem ipsum dolor sit amet, consectetur adipiscing elit. Pellentesque molestie,                                             
    dui quis condimentum suscipit, neque nulla porttitor augue, ac feugiat lorem turpis ut augue.                                       
    Vivamus sollicitudin, risus quis convallis mattis, velit nunc euismod urna, eget volutpat est sapien vitae metus.                   
    Suspendisse sollicitudin augue ipsum, sit amet consequat lorem congue semper. Nullam ut porta urna, eu tristique ex.                
    Nulla dictum urna ligula, eu sodales massa tristique gravida. Vestibulum in dapibus lacus, eu ullamcorper mi. 
    Donec non mollis eros. Proin iaculis lacus a orci accumsan facilisis. Aliquam accumsan elit sit amet velit commodo
    accumsan eu ac leo. Aenean ut nisl risus. Nunc mollis tellus eu velit auctor aliquet. In ultrices orci id rutrum feugiat.
    Curabitur aliquam turpis est, vel ultrices lorem tempor eget. Suspendisse tincidunt tellus augue, sit amet volutpat enim facilisis at.
''')
    
    app.cx = None
    app.cy = None


def redrawAll(app):
    drawBg(app)
    if app.screen == 'home':
        draw0HomeScreen(app)
    elif app.screen == 'draw':
        draw1DrawScreen(app)
    elif app.screen == 'detail_calculate':
        draw2SeeScreen(app)



    

############################################################
# COMPONENTS
############################################################ 
class Wall:
    def __init__(self, length, width, height, uValue):
        self.length = length
        self.width = width
        self.height = height
        self.uValue = uValue
    
    def calculateArea(self):
        return self.length * self.width
    
    def calculateRValue(self):
        return 1/self.uValue

class Window:
    pass

class Door:
    pass

class Floor:
    pass

class Roof:
    pass


############################################################
# UTILS
############################################################ 
class Button:
    def __init__(self, top, buttonNum, buttonStep, buttonHeight, text):
        self.buttonNum = buttonNum
        self.buttonStep = buttonStep
        self.buttonHeight = buttonHeight
        self.text = text
        self.top = top

    
    def draw(self):
        for i in range(self.buttonNum):
            drawRect(i*self.buttonStep,self.top, (i+1)*self.buttonStep ,
                    self.buttonHeight , border = 'white', fill = 'white', opacity = 40)
            drawLabel(self.text[i], (i+0.5)*self.buttonStep, self.top + self.buttonHeight/2,
                        font = 'monospace', fill='white', bold = True, size = 16)

class Gallery:
    def __init__(self):
        pass
    
    def draw(self):
        # rect
        # image
        # self.name below
        pass

class Project:
    def __init__(self,name,lenght,width):
        self.name = name
        self.length = lenght
        self.width = width
    
    def addWindow(self):
        pass
    
    def addDoor(self):
        pass

    def toggleView(self):
        pass
    


############################################################
# SCREENS
############################################################ 
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
    pass

def draw2SeeScreen(app):
    pass

def draw3DetailCalculateScreen(app):
    pass

def draw3_1PopUp(app):
    pass

def draw3_2PopUp(app):
    pass


def onKeyPress(app, key):
    if key == 'right':
        setActiveScreen('game')

def draw1DrawScreen(app):
    pass



def onKeyPress(app, key):
    if key == 'd':
        app.screen = 'draw'
    elif key == 'd':
        app.screen = 'draw'

def onMousePress(app, mouseX, mouseY):
    app.cx = mouseX
    app.cy = mouseY
    if app.screen == 'home':
        handleClickHomeScreen(app, mouseX, mouseY)

    elif app.screen == 'draw':
        handleClickDrawScreen(app, mouseX, mouseY)
    elif app.screen == 'detail_calculate':
        handleClickDetailCalculateScreen(app, mouseX, mouseY)
        
def handleClickHomeScreen(app, mouseX, mouseY):
    if mouseY > app.height/2 and mouseY < app.height/2 + 50:
            if mouseX > 0 and mouseX < app.width/3:
                app.screen = 'draw'
            elif mouseX > app.width:
                app.screen = 'see'
            elif mouseX > 2*app.width/3:
                app.screen = 'detail_calculate'

def handleClickDrawScreen(app, mouseX, mouseY):
    pass
def handleClickDetailCalculateScreen(app, mouseX, mouseY):
    pass


def main():
    runApp(width=1000, height=1000)

main()
