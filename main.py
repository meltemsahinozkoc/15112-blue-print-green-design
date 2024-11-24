# init + transition bw screens
from cmu_graphics import *
from components import *
from web_scraping import *
from screens import *
from utils import *

def onAppStart(app):
    initializeHomeScreen(app)
    app.buildingGallery = []
    app.projectCount = len(app.buildingGallery)
    reset(app)

def reset(app):
    initilaizeBuilding(app)
    # mouse
    app.cx = None 
    app.cy = None
    app.help = False

def initilaizeBuilding(app):
    stdWallHeight = 6.5
    app.building = Building(200,200,stdWallHeight) # bad!!!! - default values
    
    app.windows = []
    app.walls = []
    app.doors = []
    app.floors = []
    app.roofs = []

def initializeHomeScreen(app):
    app.screen= 'home'
    app.fill = 'mediumblue'
    app.font = 'monospace'
    app.instruction = ('''BLUE PRINT GREEN DESIGN ia an interactive app for anyone who wants to create and visualize simple building plans\n
    in 2D and calculate their heat loss. The app allows users to design layouts by defining dimensions and location,
    adding walls, windows, doors, floors, and roofs. The “Detail” and “Calculate” stages allow users to either directly
    input component U-values (thermal transmittance) or enter material layers and thicknesses for each building component.
    The app plans to use web-scraping to fetch thermal conductivity and heating degree day values for heat loss calculations.
    After the heat loss calculations, the “4. Calculate” screen will break down the building’s heat loss, detect the least
    efficient components, and give prioritized retrofit suggestions. This project aims to integrate design and basic sustainability\n
    evaluation in a user-friendly, visually compelling interface.''')

def redrawAll(app):
    drawBg(app)
    if app.screen == 'home':
        draw0HomeScreen(app)
    elif app.screen == 'draw':
        # drawRect(app.width/2,app.height/2,600, 600, fill = None, border = 'White', borderWidth = 15, align = 'center')
        draw1DrawScreen(app)
        if app.building != None:
            app.building.drawBuilding()
            app.building.drawMeasureLines()
        if len(app.windows) != 0:
            drawWindows(app)
        if len(app.doors) != 0:
            drawDoors(app)
        
        
    elif app.screen == 'detail':
        draw2DetailScreen(app)
    elif app.screen == 'calculate':
        draw3CalculateScreen(app)
    

def drawWindows(app):
    if (app.width/2 - app.building.length/2 < app.cx < app.width/2 + app.building.length/2
        and app.height/2 - app.building.width/2 < app.cy < app.height/2 + app.building.width/2):
        for window in app.windows:
            window.draw()

def drawDoors(app):
    if (app.width/2 - app.building.length/2 < app.cx < app.width/2 + app.building.length/2
        and app.height/2 - app.building.width/2 < app.cy < app.height/2 + app.building.width/2):
        for door in app.doors:
            door.draw()

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
            if mouseX > 0 and mouseX < app.width/3 :
                app.screen = 'draw'
            elif mouseX > app.width:
                app.screen = 'see'
            elif mouseX > 2*app.width/3:
                app.screen = 'detail_calculate'

def handleClickDrawScreen(app, mouseX, mouseY):   
    # top buttons 
    if mouseY > 0 and mouseY < 50:
        if mouseX > 0 and mouseX < app.width/4:
             app.building.name = app.getTextInput('Enter project name: ')

        elif mouseX > app.width/4 and mouseX < app.width/2:
            app.building.location = app.getTextInput('Enter location: ')
            
        elif mouseX > app.width/2 and mouseX < 3*app.width/4:
            inputHeight = app.getTextInput('Enter building height (Between 6-35): ')
            if isValidHeight(app, inputHeight):
                app.building.height = int(inputHeight)

        elif mouseX > 3*app.width/4 and mouseX < app.width:
            inputLength = app.getTextInput('Enter building length (Between 100-600): ')
            if isValidDimension(app, inputLength):
                app.building.length= int(inputLength)

            inputWidth = app.getTextInput('Enter building width (Between 100-600): ')
            if isValidDimension(app, inputWidth):
                app.building.width = int(inputWidth)

            stdWallWidth = 25
            stdWallUValue = 0.1
            w0 = Wall(app.building.length, app.building.height, stdWallWidth, stdWallUValue)
            w1 = Wall(app.building.width, app.building.height, stdWallWidth, stdWallUValue)
            w2 = Wall(app.building.length, app.building.height, stdWallWidth, stdWallUValue)
            w3 = Wall(app.building.width, app.building.height, stdWallWidth, stdWallUValue)
            app.walls = [w0,w1,w2,w3]

    # +add window/door buttons
    if mouseY > 50 and mouseY < 100:
        if mouseX > 0 and mouseX < app.width/2:
            stdWindowLenght = 40
            stdWindowHeight = 60
            stdWindowUValue = 5
            app.windows.append(Window(stdWindowLenght,stdWindowHeight,stdWindowUValue))

        elif mouseX > app.width/2 and mouseX < app.width:
            stdDoorLength = 60
            stdDoorHeight = 180
            stdDoorUValue = 1
            app.doors.append(Door(stdDoorLength,stdDoorHeight,stdDoorUValue))

    # bottom buttons
    if mouseY > app.height-50:
        if mouseX > 0 and mouseX < app.width/3:
            reset(app)
        elif mouseX > app.width/3 and mouseX < 2*app.width/3:
            app.building.toggleView()
        elif mouseX > 2*app.width/3:
            app.help = True
            app.screen = 'home' # or show message


def handleClickDetailScreen(app, mouseX, mouseY):
    pass

def handleClickCalculateScreen(app, mouseX, mouseY):
    pass


def main():
    runApp(width=1000, height=1000)
main()
