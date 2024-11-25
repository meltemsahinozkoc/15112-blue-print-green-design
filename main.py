# init + transition bw screens
from cmu_graphics import *
from components import *
from web_scraping import *
from screens import *
from utils import *

########################################################
################### INITIALIZE APP #####################
########################################################

def onAppStart(app):
    initializeHomeScreen(app)
    app.gallery = Gallery()

    app.textSizeHead = 24
    app.textSize = 16

    reset(app)

    app.currentComponent = None
    app.thermalData = fetchFilteredThermalData()
    app.materialRValueDict = dict()
    for dictionary in app.thermalData:
        app.materialRValueDict[dictionary['Material']] = float(dictionary['Conductivity (W/m·K)'])
    print(app.materialRValueDict)

def reset(app):
    initilaizeBuilding(app)
    # mouse position
    app.cx = None 
    app.cy = None
    # app.hx = None
    # app.hy = None
    # app.mouseOverButton = False

def initilaizeBuilding(app):
    stdWallHeight = 6.5
    app.building = Building(200,200,stdWallHeight) # default building
    
    app.windows = []
    app.walls = []
    app.doors = []
    app.floors = []
    app.roofs = []

    app.addWindow = False
    app.addDoor = False

def initializeHomeScreen(app):
    app.screen= 'home'
    app.fill = 'mediumblue'
    app.font = 'monospace'
    app.instruction = ('''WHAT
BLUE PRINT GREEN DESIGN aims to integrate design and basic sustainability
evaluation in a user-friendly, visually compelling interface.  
It is an interactive app for anyone who wants to create and visualize
simple building plans in 2D and calculate their heat loss.

HOW
The app allows users to design layouts by defining dimensions and location,
adding walls, windows, doors, floors, and roofs. The “Detail” and “Calculate”
stages allow users to either directly input component U-values (thermal transmittance value)
or enter material layers and thicknesses for each building component.

The app uses web-scraping to fetch thermal conductivity for heat loss calculations.
After the heat loss calculations, the “3. Calculate” screen will break down the building’s
heat loss, detect the least efficient components, and give prioritized
retrofit suggestions.''')


########################################################
####################### DRAWING ########################
########################################################

def redrawAll(app):
    drawBg(app)
    if app.screen == 'home':
        draw0HomeScreen(app)
        app.gallery.draw()
    elif app.screen == 'draw':
        draw1DrawScreen(app)
        if app.building != None:
            app.building.drawBuilding()
            app.building.drawMeasureLines()
        if len(app.windows) > 0:
            drawWindows(app)
        if len(app.doors) > 0:
            drawDoors(app)
    elif app.screen == 'detail':
        draw2DetailScreen(app)
    elif app.screen == 'calculate':
        draw3CalculateScreen(app)
    elif app.screen == 'detailWalls':
        drawDetailWallsScreen(app)
    elif app.screen == 'detailWindows':
        drawDetailWindowsScreen(app)
    elif app.screen == 'detailDoors':
        drawDetailDoorsScreen(app)
    elif app.screen == 'detailFloor':
        drawDetailFloorsScreen(app)
    elif app.screen == 'detailRoof':
        drawDetailRoofsScreen(app)
    
def drawWindows(app):
    for window in app.windows:
        if window.type != None:
            window.draw()
                
def drawDoors(app):
    for door in app.doors:
        if door.type != None:
            door.draw()

########################################################
################# MOUSE AND KEY EVENTS #################
########################################################

def onKeyPress(app, key):
    if key == '0':
        app.screen = 'home'
    elif key == '1':
        app.screen = 'draw'
    elif key == '2':
        app.screen = 'detail'
    elif key == '3':
        app.screen = 'calculate'

    if app.screen == 'detail':
        if key == 'w':
            app.screen = 'detailWalls'
        elif key == 'g':
            app.screen = 'detailWindows'
        elif key == 'd':
            app.screen = 'detailDoors'
        elif key == 'f':
            app.screen = 'detailFloor'
        elif key == 'r':
            app.screen = 'detailRoof'

def onMousemove(app, mouseX, mouseY):
    app.hx = mouseX
    app.hy = mouseY


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

    elif app.screen == 'detailWalls':
        app.currentComponent = app.walls
        handleClickDetailWallsScreen(app, mouseX, mouseY)
    elif app.screen == 'detailWindows':
        handleClickDetailWindowsScreen(app, mouseX, mouseY)
    elif app.screen == 'detailDoors':
        handleClickDetailDoorsScreen(app, mouseX, mouseY)
    elif app.screen == 'detailFloor':
        handleClickDetailFloorScreen(app, mouseX, mouseY)
    elif app.screen == 'detailRoof':
        handleClickDetailRoofScreen(app, mouseX, mouseY)

def handleClickHomeScreen(app, mouseX, mouseY):
    if mouseY > app.height/2 and mouseY < app.height/2 + 50:
            if mouseX > 0 and mouseX < app.width/3 :
                app.screen = 'draw'
            elif mouseX > app.width/3 and mouseX < 2*app.width/3:
                app.screen = 'detail'
            elif mouseX > 2*app.width/3:
                app.screen = 'calculate'

    if mouseY > 700 and mouseY < 800:
        for i in range(len(app.gallery.items)):
            if mouseX > 50 + i*app.gallery.galleryStep and mouseX < 50 + (i+1)*app.gallery.galleryStep:
                app.building = app.gallery.items[i]
                app.screen = 'draw'
    
    if mouseY > app.height/1.6 and mouseY < app.height/1.6 + 50:
            app.gallery.items = []


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
            inputLength = app.getTextInput('Enter building length (Between 100-500): ')
            if isValidDimension(app, inputLength):
                app.building.length= int(inputLength)

            inputWidth = app.getTextInput('Enter building width (Between 100-500): ')
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
            app.addWindow = True

        elif mouseX > app.width/2 and mouseX < app.width:
            app.addDoor = True
    
    if isMouseClickOnTheWall(app):
        if app.addWindow:
            stdWindowLenght = 40
            stdWindowHeight = 60
            stdWindowUValue = 5
            newWindow = Window(stdWindowLenght,stdWindowHeight,stdWindowUValue, mouseX, mouseY)
            app.windows.append(newWindow)
            newWindow.type = classifyComponentAllignment(app)
            app.addWindow = False

        elif app.addDoor:
            stdDoorLength = 60
            stdDoorHeight = 180
            stdDoorUValue = 1
            newDoor = Door(stdDoorLength,stdDoorHeight,stdDoorUValue, mouseX, mouseY)
            app.doors.append(newDoor)
            newDoor.type = classifyComponentAllignment(app)
            app.addDoor = False
            
    # bottom2 buttons:
    if mouseY > app.height-100:
        if mouseX > 0 and mouseX < app.width/4:
            if len(app.windows) > 0:
                app.windows.pop()
        elif mouseX > app.width/4 and mouseX < app.width/2:
            if len(app.doors) > 0:
                app.doors.pop()
        elif mouseX > app.width/2 and mouseX < 3*app.width/4:
            app.screen = 'home'
        elif mouseX > 3*app.width/4:
            app.screen = 'detail'
        

    # bottom buttons
    if mouseY > app.height-50:
        if mouseX > 0 and mouseX < app.width/3:
            reset(app)
        elif mouseX > app.width/3 and mouseX < 2*app.width/3:
            app.building.toggleView()
        elif mouseX > 2*app.width/3:
            app.showMessage(app.instruction) # or go to screen "home"?

def classifyComponentAllignment(app): # vertical, horizontal, None
    wallWidth = 15

    halfLength = app.building.length/2
    halfWidth = app.building.width/2

    innerLeft = app.width/2 - halfWidth + wallWidth
    innerRight = app.width/2 + halfWidth - wallWidth
    innerTop = app.height/2 - halfLength + wallWidth
    innerBottom = app.height/2 + halfLength - wallWidth

    if app.cx < innerLeft or app.cx > innerRight: # vertical or horizontal allignment
        return "vertical" 
    elif app.cy < innerTop or app.cy > innerBottom:
        return "horizontal" 
    return None

def isMouseClickOnTheWall(app): # T/F
    wallWidth = 15

    halfLength = app.building.length/2
    halfWidth = app.building.width/2

    outerLeft = app.width/2 - halfWidth
    outerRight = app.width/2 + halfWidth
    outerTop = app.height/2 - halfLength
    outerBottom = app.height/2 + halfLength

    innerLeft = app.width/2 - halfWidth + wallWidth
    innerRight = app.width/2 + halfWidth - wallWidth
    innerTop = app.height/2 - halfLength + wallWidth
    innerBottom = app.height/2 + halfLength - wallWidth

    return ((outerLeft <= app.cx <= outerRight and outerTop <= app.cy <= outerBottom) and 
        not (innerLeft <= app.cx <= innerRight and innerTop <= app.cy <= innerBottom))


def handleClickDetailScreen(app, mouseX, mouseY):
    # middle component buttons
    if mouseY > app.height/2 and mouseY < app.height/2 + 50:
        if mouseX > 0 and mouseX < app.width/5:
            app.screen = 'detailWalls'
        elif mouseX > app.width/5 and mouseX < 2*app.width/5:
            app.screen = 'detailWindows'
        elif mouseX > 2*app.width/5 and mouseX < 3*app.width/5:
            app.screen = 'detailDoors'
        elif mouseX > 3*app.width/5 and mouseX < 4*app.width/5:
            app.screen = 'detailFloor'
        elif mouseX > 4*app.width/5 and mouseX < app.width:
            app.screen = 'detailRoof'
    
    # bottom2 buttons
    if mouseY > app.height-100:
        if mouseX > 0 and mouseX < app.width/2:
            app.screen = 'draw'
        elif mouseX > app.width/2:
            app.screen = 'calculate'

    # bottom buttons
    if mouseY > app.height-50:
        if mouseX > 0 and mouseX < app.width/3:
            reset(app)
        elif mouseX > app.width/3 and mouseX < 2*app.width/3:
            app.building.save()
            
        elif mouseX > 2*app.width/3:
            app.showMessage(app.instruction)
            
def handleClickDetailWallsScreen(app, mouseX, mouseY):
    # top buttons
    if mouseY > 0 and mouseY < 50:
        if mouseX > 0 and mouseX < app.width/2:
            app.screen = 'detail'
        elif mouseX > app.width/2:
            app.screen = 'detailWindows'

def handleClickDetailWindowsScreen(app, mouseX, mouseY):
    # top buttons
    if mouseY > 0 and mouseY < 50:
        if mouseX > 0 and mouseX < app.width/2:
            app.screen = 'detailWalls'
        elif mouseX > app.width/2:
            app.screen = 'detailDoors'

def handleClickDetailDoorsScreen(app, mouseX, mouseY):
    # top buttons
    if mouseY > 0 and mouseY < 50:
        if mouseX > 0 and mouseX < app.width/2:
            app.screen = 'detailWindows'
        elif mouseX > app.width/2:
            app.screen = 'detailFloor'

def handleClickDetailFloorScreen(app, mouseX, mouseY):
    # top buttons
    if mouseY > 0 and mouseY < 50:
        if mouseX > 0 and mouseX < app.width/2:
            app.screen = 'detailDoors'
        elif mouseX > app.width/2:
            app.screen = 'detailRoof'

def handleClickDetailRoofScreen(app, mouseX, mouseY):
    # top buttons
    if mouseY > 0 and mouseY < 50:
        if mouseX > 0 and mouseX < app.width/2:
            app.screen = 'detailFloor'
        elif mouseX > app.width/2:
            app.screen = 'detail'


def handleClickCalculateScreen(app, mouseX, mouseY):
    # bottom buttons
    if mouseY > app.height-50:
        if mouseX > 0 and mouseX < app.width/3:
            reset(app)
        elif mouseX > app.width/3 and mouseX < 2*app.width/3:
            app.building.save()
        elif mouseX > 2*app.width/3:
            app.showMessage(app.instruction)
    
    # bottom2 buttons
    if mouseY > app.height-100:
        if mouseX > 0 and mouseX < app.width/2:
            app.screen = 'detail'
        elif mouseX > app.width/2:
            app.gallery.items.append(app.building)
            reset(app)
            app.screen = 'home'


def main():
    runApp(width=1000, height=1000)
main()

