# init + transition bw screens
from cmu_graphics import *
from components import *
from web_scraping import *
from screens import *
from utils import *


def onAppStart(app):
    reset(app)

def reset(app):
    app.fill = 'mediumblue'
    app.font = 'monospace'
    app.instruction = ('''BLUE PRINT GREEN DESIGN ia an interactive app for anyone who wants to create and visualize simple building plans
    in 2D and calculate their heat loss. The app allows users to design layouts by defining dimensions and location,
    adding walls, windows, doors, floors, and roofs. The “Detail” and “Calculate” stages allow users to either directly
    input component U-values (thermal transmittance) or enter material layers and thicknesses for each building component.
    The app plans to use web-scraping to fetch thermal conductivity and heating degree day values for heat loss calculations.
    After the heat loss calculations, the “4. Calculate” screen will break down the building’s heat loss, detect the least
    efficient components, and give prioritized retrofit suggestions. This project aims to integrate design and basic sustainability
    evaluation in a user-friendly, visually compelling interface.''')

    app.screen= 'home' # draw, see, detail_calculate
    app.building = None

    app.windows = []
    app.walls = []
    app.doors = []
    app.floors = []
    app.roofs = []

    app.bldgHeight = 0
    app.bldgWidht = 0
    app.bldgLenght = 0
    
    app.cx = None
    app.cy = None

    app.help = False

def redrawAll(app):
    drawBg(app)
    if app.screen == 'home':
        draw0HomeScreen(app)
    elif app.screen == 'draw':
        draw1DrawScreen(app)
    elif app.screen == 'detail':
        draw2DetailScreen(app)
    elif app.screen == 'calculate':
        draw3CalculateScreen(app)

def onKeyPress(app, key):
    if key == '0':
        app.screen = 'home'
    elif key == '1':
        app.screen = 'draw'
    elif key == '2':
        app.screen = 'detail'
    elif key == '3':
        app.screen = 'calculate'

def onMousePress(app, mouseX, mouseY):
    app.cx = mouseX
    app.cy = mouseY
    if app.screen == 'home':
        handleClickHomeScreen(app, mouseX, mouseY)
    elif app.screen == 'draw':
        handleClickDrawScreen(app, mouseX, mouseY)
    elif app.screen == 'detail':
        handleClickDetailScreen(app, mouseX, mouseY)
    elif app.screen == 'calculate':
        handleClickCalculateScreen(app, mouseX, mouseY)
        
def handleClickHomeScreen(app, mouseX, mouseY):
    if mouseY > app.height/2 and mouseY < app.height/2 + 50:
            if mouseX > 0 and mouseX < app.width/3:
                app.screen = 'draw'
            elif mouseX > app.width:
                app.screen = 'see'
            elif mouseX > 2*app.width/3:
                app.screen = 'detail_calculate'

def handleClickDrawScreen(app, mouseX, mouseY):
    name = ''
    location = ''
    app.building = Building(name, location, app.bldgLenght, app.bldgWidth, app.bldgHeight)
    if mouseY > 0 and mouseY < 50:
        if mouseX > 0 and mouseX < app.width/4:
            name = app.getTextInput('Enter project name: ')
        elif mouseX > app.width/4 and mouseX < app.width/2:
            location = app.getTextInput('Enter location: ')
        elif mouseX > app.width/2 and mouseX < 3*app.width/4:
            app.bldgLenght = int(app.getTextInput('Enter building length: '))
            app.bldgWidth = int(app.getTextInput('Enter building width: '))
            if isValidDimension(app, app.bldgWidth) and isValidDimension(app, app.bldgLenght) and hasAllParametersSet(app):
                    app.building.drawRoom()
                    app.building.drawMeasureLines()
            else:
                app.showMessage('Invalid dimension. Please enter a value between 100-600.')
        elif mouseX > 3*app.width/4 and mouseX < app.width:
            app.bldgHeight = int(app.getTextInput('Enter building height: '))
    

    if mouseY > 50 and mouseY < 100:
        if mouseX > 0 and mouseX < app.width/2:
            app.windows.append(Window(5,0,0,0)) # wrong!!!
        elif mouseX > app.width/2 and mouseX < app.width:
            app.doors.append(Door(2.5,0,0,0)) # wrong!!!

    if mouseY > app.height-50:
        if mouseX > 0 and mouseX < app.width/3:
            reset(app)
        elif mouseX > app.width/3 and mouseX < 2*app.width/3:
            app.building.toggleView()
        elif mouseX > 2*app.width/3:
            app.help = True
            app.screen = 'home' # or show message

    
def handleClickDetailCalculateScreen(app, mouseX, mouseY):
    pass

def isValidDimension(app, dimension):
    return dimension > 100 and dimension < 600

def hasAllParametersSet(app):
    return app.building.name and app.building.location and app.bldgHeight and app.bldgWidth and app.bldgLenght



def handleClickCalculateScreen(app, mouseX, mouseY):
    pass

def handleClickDetailScreen(app, mouseX, mouseY):
    pass


def main():
    runApp(width=1000, height=1000)
main()
