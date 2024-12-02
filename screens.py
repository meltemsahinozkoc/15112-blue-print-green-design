# all screens here. draw funcs.
from cmu_graphics import *
from building_components import *
from utils import *

def drawBg(app):
    drawRect(0,0,app.width, app.height, fill = app.fill)

def draw0HomeScreen(app):    
    buttons = Button(app.height/2, 3, app.width/3, 50,['1."DRAW"', '2."DETAIL"', '3. "CALCULATE"'])
    buttons.draw()
    
    drawLabel('BLUE PRINT GREEN DESIGN', app.width/2, app.height/11, size=app.textSizeHead, fill='white', bold=True, font=app.font)
    
    margin = 100
    for i in range(len(app.instruction.splitlines())):
        lines = app.instruction.splitlines()
        margin = 20
        drawLabel(lines[i], app.width/2, app.height/7 + margin*i, size=app.textSize, fill='white', bold=True, font=app.font)

    drawLabel('Press (1, 2, 3) or click on buttons to navigate.', app.width/2, app.height/2+75, size=app.textSize, fill='white', font=app.font, italic=True)
    drawLabel('GALLERY', app.width/2, app.height/1.6, size=app.textSizeHead, fill='white', bold=True, font=app.font)
    buttonReset = Button((app.height/1.6)+20, 1, app.width/1, 30, ['RESET GALLERY'])
    buttonReset.draw()

def draw1DrawScreen(app):
    buttonsTop = Button(0, 5, app.width/5, 50,['1.PROJECT NAME', '2.LOCATION', '3. HDD', '4.HEIGHT', '5.DIMENSIONS'])
    buttonsTop2 = Button(50, 3, app.width/3, 50,['+ADD WINDOW', '+ADD DOOR', '+ADD ROOM'])
    buttonsBottom2 = Button(app.height-100, 5, app.width/5, 50,['UNDO WINDOW', 'UNDO DOOR', 'UNDO ROOM', '← BACK', 'FORWARD →'])
    buttonsBottom = Button(app.height-50, 3, app.width/3, 50,['RESET', 'TOGGLE VIEW', '⌂ HOME'])
    buttonsTop.draw()
    buttonsTop2.draw()
    buttonsBottom.draw()
    buttonsBottom2.draw()

    drawLabel(f'PROJECT NAME: {app.building.name}', 25, 125, size=app.textSize, fill='white', bold=True, font=app.font, align='left')
    drawLabel(f'LOCATION: {app.building.location}', 25, 150, size=app.textSize, fill='white', bold=True, font=app.font, align='left')
    drawLabel(app.building, 25, app.height-125, size=app.textSize, fill='white', font=app.font, align='left')
    drawLabel(f'Current screen: {app.screen}', app.width-25, app.height-125, size=app.textSize, fill='white', font=app.font, align='right')


def draw2DetailScreen(app):
    buttonsMiddle = Button(app.height/2, 5, app.width/5, 50,['1. WALLS (W)', '2. WINDOWS (G)', '3. DOORS (D)', '4. FLOOR (F)', '5. ROOF (R)'])
    buttonsBottom = Button(app.height-50, 4, app.width/4, 50,['RESET', '⌂ HOME', '← BACK', 'FORWARD →'])
    buttonsMiddle.draw()
    buttonsBottom.draw()
    
    drawLabel('Press (W, G, D, F, R) or click on buttons to navigate.', app.width/2, app.height/2 + 100, size=app.textSize, fill='white', font=app.font, italic=True)
    drawLabel(f'Current screen: {app.screen}', app.width-25, app.height-75, size=app.textSize, fill='white', font=app.font, align='right')
    

def drawDetailWallsScreen(app):
    drawLabel('WALLS (W)', app.width/2, app.height/10, size=app.textSizeHead, fill='white', bold=True, font=app.font)

    buttonsTop = Button(0, 2, app.width/2, 50,['← BACK', 'FORWARD →'])
    buttonsTop.draw()

    drawLabel('Enter U-value if you know it.', app.width/2, app.height/8, size=app.textSize, fill='white', bold=True, font=app.font)
    drawLabel('OR select layers from the BLUE PRINT GREEN DESIGN database if you do not.', app.width/2, app.height/7 + 20, size=app.textSize, fill='white', bold=True, font=app.font)
    drawLabel('The app will do the work for you!', app.width/2, app.height/7 + 40, size=app.textSize, fill='white', bold=True, font=app.font)

    buttonsMiddle = Button(app.height/2, 2, app.width/2, 50,['ENTER U-VALUE', 'OR ENTER LAYERS'])
    buttonsMiddle.draw()

    app.dropdownMenu.draw()

def drawDetailWindowsScreen(app):
    buttonsTop = Button(0, 2, app.width/2, 50,['← BACK', 'FORWARD →'])
    buttonsTop.draw()

    drawLabel('WINDOWS (G)', app.width/2, app.height/10, size=app.textSizeHead, fill='white', bold=True, font=app.font)

    drawLabel('Enter U-value if you know it.', app.width/2, app.height/8, size=app.textSize, fill='white', bold=True, font=app.font)
    drawLabel('OR select layers from the BLUE PRINT GREEN DESIGN database if you do not.', app.width/2, app.height/7 + 20, size=app.textSize, fill='white', bold=True, font=app.font)
    drawLabel('The app will do the work for you!', app.width/2, app.height/7 + 40, size=app.textSize, fill='white', bold=True, font=app.font)

    buttonsMiddle = Button(app.height/2, 2, app.width/2, 50,['ENTER U-VALUE', 'OR ENTER LAYERS'])
    buttonsMiddle.draw()

    app.dropdownMenu.draw()

def drawDetailDoorsScreen(app):
    buttonsTop = Button(0, 2, app.width/2, 50,['← BACK', 'FORWARD →'])
    buttonsTop.draw()

    drawLabel('DOORS (D)', app.width/2, app.height/10, size=app.textSizeHead, fill='white', bold=True, font=app.font)

    drawLabel('Enter U-value if you know it.', app.width/2, app.height/8, size=app.textSize, fill='white', bold=True, font=app.font)
    drawLabel('OR select layers from the BLUE PRINT GREEN DESIGN database if you do not.', app.width/2, app.height/7 + 20, size=app.textSize, fill='white', bold=True, font=app.font)
    drawLabel('The app will do the work for you!', app.width/2, app.height/7 + 40, size=app.textSize, fill='white', bold=True, font=app.font)

    buttonsMiddle = Button(app.height/2, 2, app.width/2, 50,['ENTER U-VALUE', 'OR ENTER LAYERS'])
    buttonsMiddle.draw()

    app.dropdownMenu.draw()


def drawDetailFloorsScreen(app):
    buttonsTop = Button(0, 2, app.width/2, 50,['← BACK', 'FORWARD →'])
    buttonsTop.draw()
    
    drawLabel('FLOORS (F)', app.width/2, app.height/10, size=app.textSizeHead, fill='white', bold=True, font=app.font)

    drawLabel('Enter U-value if you know it.', app.width/2, app.height/8, size=app.textSize, fill='white', bold=True, font=app.font)
    drawLabel('OR select layers from the BLUE PRINT GREEN DESIGN database if you do not.', app.width/2, app.height/7 + 20, size=app.textSize, fill='white', bold=True, font=app.font)
    drawLabel('The app will do the work for you!', app.width/2, app.height/7 + 40, size=app.textSize, fill='white', bold=True, font=app.font)

    buttonsMiddle = Button(app.height/2, 2, app.width/2, 50,['ENTER U-VALUE', 'OR ENTER LAYERS'])
    buttonsMiddle.draw()

    app.dropdownMenu.draw()


def drawDetailRoofsScreen(app):
    buttonsTop = Button(0, 2, app.width/2, 50,['← BACK', 'FORWARD →'])
    buttonsTop.draw()

    drawLabel('ROOFS (R)', app.width/2, app.height/10, size=app.textSizeHead, fill='white', bold=True, font=app.font)

    drawLabel('Enter U-value if you know it.', app.width/2, app.height/8, size=app.textSize, fill='white', bold=True, font=app.font)
    drawLabel('OR select layers from the BLUE PRINT GREEN DESIGN database if you do not.', app.width/2, app.height/7 + 20, size=app.textSize, fill='white', bold=True, font=app.font)
    drawLabel('The app will do the work for you!', app.width/2, app.height/7 + 40, size=app.textSize, fill='white', bold=True, font=app.font)

    buttonsMiddle = Button(app.height/2, 2, app.width/2, 50,['ENTER U-VALUE', 'OR ENTER LAYERS'])
    buttonsMiddle.draw()

    app.dropdownMenu.draw()


def draw3CalculateScreen(app):
    rowWidth = 200
    rowHeight = 50
    colWidth = 750
    colHeight = 600
    tableLeft = 100
    tableTop = 200


    drawLabel('TRANSMISSION LOSSES', app.width/2, app.height/8, size=app.textSizeHead, fill='white', bold=True, font=app.font)
    buttonsBottom = Button(app.height-50, 4, app.width/4, 50,['RESET', '⌂ HOME', '← BACK', 'SAVE & CLOSE'])
    drawLabel('RETROFIT SUGGESTIONS', app.width/2, app.height-350, size=app.textSizeHead, fill='white', bold=True, font=app.font)
    buttonsBottom.draw()

    drawLabel(f'Current screen: {app.screen}', app.width-25, app.height-75, size=app.textSize, fill='white', font=app.font, align='right')

    # left col
    componentNamesCol = TableCol(['COMPONENTS', 'WALLS', 'WINDOWS', 'DOORS', 'FLOOR', 'ROOF'], tableLeft, tableTop, colWidth, colHeight, rowWidth, rowHeight)
    componentNamesCol.draw()

    # middle col
    lossesCol = TableCol(['TOTAL HEAT LOSS', app.building.totalWallUA, app.building.totalWindowUA, app.building.totalDoorUA, app.building.totalFloorUA, app.building.totalRoofUA], tableLeft+200, tableTop, colWidth, colHeight, rowWidth, rowHeight)
    lossesCol.draw()

    # right col
    if (app.building.wallsRValue != [] and app.building.windowsRValue != [] and app.building.doorsRValue != [] and
        app.building.floorsRValue != [] and app.building.roofsRValue != []):
        ratioDict = app.building.calculateTotalHeatLossCoefficientPerComponent()
        wallRatio = pythonRound(ratioDict['wallUA%'], 2)
        windowRatio = pythonRound(ratioDict['windowUA%'], 2)
        doorRatio = pythonRound(ratioDict['doorUA%'], 2)
        floorRatio = pythonRound(ratioDict['floorUA%'], 2)
        roofRatio = pythonRound(ratioDict['roofUA%'], 2)
        ratioCol = TableCol(['RATIO', wallRatio, windowRatio, doorRatio, floorRatio, roofRatio], tableLeft+200*2, tableTop, colWidth, colHeight, rowWidth, rowHeight)
        ratioCol.draw()
    else:
        app.showMessage('Make sure you have entered U-values for all components to get the full table.')
