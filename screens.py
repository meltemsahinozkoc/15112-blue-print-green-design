from cmu_graphics import *
from building_components import *
from utils import *

def drawBg(app):
    drawRect(0,0,app.width, app.height, fill = app.fill)

def draw0HomeScreen(app):    
    buttons = Button(app.height/2, 3, app.width/3, 50,['1."DRAW"', '2."DETAIL"', '3. "CALCULATE"'])
    buttons.draw()
    
    drawLabel('BLUE PRINT GREEN DESIGN', app.width/2, app.height/11, size=app.textSizeHead, fill=app.secondFill, bold=True, font=app.font)
    
    margin = 100
    for i in range(len(app.instruction.splitlines())):
        lines = app.instruction.splitlines()
        margin = 20
        drawLabel(lines[i], app.width/2, app.height/7 + margin*i, size=app.textSize, fill=app.secondFill, bold=True, font=app.font)

    drawLabel('Press (1, 2, 3) or click on buttons to navigate.', app.width/2, app.height/2+75, size=app.textSize, fill=app.secondFill, font=app.font, italic=True)
    drawLabel('GALLERY', app.width/2, app.height/1.6, size=app.textSizeHead, fill=app.secondFill, bold=True, font=app.font)
    buttonReset = Button((app.height/1.6)+20, 1, app.width/1, 30, ['RESET GALLERY'])
    buttonReset.draw()

def draw1DrawScreen(app):
    buttonsTop = Button(0, 5, app.width/5, 50,['1.PROJECT NAME', '2.LOCATION', '3. HDD', '4.HEIGHT', '5.DIMENSIONS'])
    buttonsTop2 = Button(50, 3, app.width/3, 50,['+ADD WINDOW', '+ADD DOOR', '+ADD ROOM'])
    buttonsBottom2 = Button(app.height-100, 5, app.width/5, 50,['UNDO WINDOW', 'UNDO DOOR', 'UNDO ROOM', '← BACK', 'FORWARD →'])
    buttonsBottom = Button(app.height-50, 3, app.width/3, 50,['RESET', 'SAVE & CLOSE', '⌂ HOME'])
    buttonsTop.draw()
    buttonsTop2.draw()
    buttonsBottom.draw()
    buttonsBottom2.draw()

    drawLabel(f'PROJECT NAME: {app.building.name}', 25, 125, size=app.textSize, fill=app.secondFill, bold=True, font=app.font, align='left')
    drawLabel(f'LOCATION: {app.building.location}', 25, 150, size=app.textSize, fill=app.secondFill, bold=True, font=app.font, align='left')
    drawLabel(f'HEATING DEGREE DAYS: {app.heatingDegreeDays65F}', 25, 175, size=app.textSize, fill=app.secondFill, bold=True, font=app.font, align='left')
    drawLabel(f'ANNUAL HEAT LOSS: {app.building.annualHeatLoss} kWh/year', 25, 200, size=app.textSize, fill=app.secondFill, bold=True, font=app.font, align='left')

    drawLabel('+ TIP 1: Start with the Project Name and follow the numbers!', 25, app.height-175, size=app.textSize, fill=app.secondFill, font=app.font, align='left', bold = True)
    drawLabel('+ TIP 2: Press S to recalculate the annual heat loss!', 25, app.height-150, size=app.textSize, fill=app.secondFill, font=app.font, align='left', bold = True)
    drawLabel(app.building, 25, app.height-125, size=app.textSize, fill=app.secondFill, font=app.font, align='left')
    drawLabel(f'Current screen: {app.screen}', app.width-25, app.height-125, size=app.textSize, fill=app.secondFill, font=app.font, align='right')


    if app.building.annualHeatLoss != 'Unknown':
        if app.building.annualHeatLoss > 15000:
            app.building.thermalColor = gradient('red','orange', start = 'left-bottom')
        elif app.building.annualHeatLoss > 10000:
            app.building.thermalColor = gradient('orange','yellow', start = 'left-bottom')
        elif app.building.annualHeatLoss > 5000:
            app.building.thermalColor = gradient('yellow','green', start = 'left-bottom')
        else:
            app.building.thermalColor = 'gray'

def draw2DetailScreen(app):
    buttonsMiddle = Button(app.height/2, 5, app.width/5, 50,['1. WALLS (W)', '2. WINDOWS (G)', '3. DOORS (D)', '4. FLOOR (F)', '5. ROOF (R)'])
    buttonsBottom = Button(app.height-50, 4, app.width/4, 50,['RESET', '⌂ HOME', '← BACK', 'FORWARD →'])
    buttonsMiddle.draw()
    buttonsBottom.draw()
    
    drawLabel('Press (W, G, D, F, R) or click on buttons to navigate.', app.width/2, app.height/2 + 100, size=app.textSize, fill=app.secondFill, font=app.font, italic=True)
    drawLabel(f'Current screen: {app.screen}', app.width-25, app.height-75, size=app.textSize, fill=app.secondFill, font=app.font, align='right')
    

def drawDetailWallsScreen(app):
    drawLabel('WALLS (W)', app.width/2, app.height/10, size=app.textSizeHead, fill=app.secondFill, bold=True, font=app.font)

    buttonsTop = Button(0, 4, app.width/4, 50,['← BACK', 'RESET', 'UNDO WALL', 'FORWARD →'])
    buttonsTop.draw()

    drawLabel('Enter U-value if you know it.', app.width/2, app.height/8, size=app.textSize, fill=app.secondFill, bold=True, font=app.font)
    drawLabel('OR select layers from the BLUE PRINT GREEN DESIGN database if you do not.', app.width/2, app.height/7 + 20, size=app.textSize, fill=app.secondFill, bold=True, font=app.font)
    drawLabel('The app will do the work for you!', app.width/2, app.height/7 + 40, size=app.textSize, fill=app.secondFill, bold=True, font=app.font)

    buttonsMiddle = Button(app.height/2, 2, app.width/2, 50,['ENTER U-VALUE', 'OR ENTER LAYERS'])
    buttonsMiddle.draw()

    app.dropdownMenu.draw()
    
    drawLabel(f'Wall layers: {app.building.wallsLayers}', 25, app.height-100, size=app.textSizeSmall, fill=app.secondFill, font=app.font, align='left', bold = True)
    drawLabel(f'Wall layers R-Values: {app.building.wallsRValue}', 25, app.height-75, size=app.textSizeSmall, fill=app.secondFill, font=app.font, align='left', bold = True)
    if isinstance(app.building.wallsRValue, list):
        drawLabel(f'Wall Total R-Value: {pythonRound(sum(app.building.wallsRValue), 2)}', 25, app.height-50, size=app.textSizeSmall, fill=app.secondFill, font=app.font, align='left', bold = True)
    else:
        drawLabel(f'Wall Total R-Value: {app.building.wallsRValue}', 25, app.height-50, size=app.textSizeSmall, fill=app.secondFill, font=app.font, align='left', bold = True)


def drawDetailWindowsScreen(app):
    buttonsTop = Button(0, 4, app.width/4, 50,['← BACK', 'RESET', 'UNDO WINDOW', 'FORWARD →'])
    buttonsTop.draw()

    drawLabel('WINDOWS (G)', app.width/2, app.height/10, size=app.textSizeHead, fill=app.secondFill, bold=True, font=app.font)

    drawLabel('Enter U-value if you know it.', app.width/2, app.height/8, size=app.textSize, fill=app.secondFill, bold=True, font=app.font)
    drawLabel('OR select layers from the BLUE PRINT GREEN DESIGN database if you do not.', app.width/2, app.height/7 + 20, size=app.textSize, fill=app.secondFill, bold=True, font=app.font)
    drawLabel('The app will do the work for you!', app.width/2, app.height/7 + 40, size=app.textSize, fill=app.secondFill, bold=True, font=app.font)

    buttonsMiddle = Button(app.height/2, 2, app.width/2, 50,['ENTER U-VALUE', 'OR ENTER LAYERS'])
    buttonsMiddle.draw()

    app.dropdownMenu.draw()

       
    drawLabel(f'Window layers: {app.building.windowsLayers}', 25, app.height-100, size=app.textSizeSmall, fill=app.secondFill, font=app.font, align='left', bold = True)
    drawLabel(f'Window layers R-Values: {app.building.windowsRValue}', 25, app.height-75, size=app.textSizeSmall, fill=app.secondFill, font=app.font, align='left', bold = True)
    if isinstance(app.building.windowsRValue, list):
        drawLabel(f'Window Total R-Value: {pythonRound(sum(app.building.windowsRValue), 2)}', 25, app.height-50, size=app.textSizeSmall, fill=app.secondFill, font=app.font, align='left', bold = True)
    else:
        drawLabel(f'Window Total R-Value: {app.building.windowsRValue}', 25, app.height-50, size=app.textSizeSmall, fill=app.secondFill, font=app.font, align='left', bold = True)

def drawDetailDoorsScreen(app):
    buttonsTop = Button(0, 4, app.width/4, 50,['← BACK', 'RESET', 'UNDO DOOR', 'FORWARD →'])
    buttonsTop.draw()

    drawLabel('DOORS (D)', app.width/2, app.height/10, size=app.textSizeHead, fill=app.secondFill, bold=True, font=app.font)

    drawLabel('Enter U-value if you know it.', app.width/2, app.height/8, size=app.textSize, fill=app.secondFill, bold=True, font=app.font)
    drawLabel('OR select layers from the BLUE PRINT GREEN DESIGN database if you do not.', app.width/2, app.height/7 + 20, size=app.textSize, fill=app.secondFill, bold=True, font=app.font)
    drawLabel('The app will do the work for you!', app.width/2, app.height/7 + 40, size=app.textSize, fill=app.secondFill, bold=True, font=app.font)

    buttonsMiddle = Button(app.height/2, 2, app.width/2, 50,['ENTER U-VALUE', 'OR ENTER LAYERS'])
    buttonsMiddle.draw()

    app.dropdownMenu.draw()

    drawLabel(f'Door layers: {app.building.doorsLayers}', 25, app.height-100, size=app.textSizeSmall, fill=app.secondFill, font=app.font, align='left', bold = True)
    drawLabel(f'Door layers R-Values: {app.building.doorsRValue}', 25, app.height-75, size=app.textSizeSmall, fill=app.secondFill, font=app.font, align='left', bold = True)
    if isinstance(app.building.doorsRValue, list):    
        drawLabel(f'Door Total R-Value: {pythonRound(sum(app.building.doorsRValue), 2)}', 25, app.height-50, size=app.textSizeSmall, fill=app.secondFill, font=app.font, align='left', bold = True)
    else:
        drawLabel(f'Door Total R-Value: {app.building.doorsRValue}', 25, app.height-50, size=app.textSizeSmall, fill=app.secondFill, font=app.font, align='left', bold = True)

    
def drawDetailFloorsScreen(app):
    buttonsTop = Button(0, 4, app.width/4, 50,['← BACK', 'RESET', 'UNDO FLOOR', 'FORWARD →'])
    buttonsTop.draw()
    
    drawLabel('FLOORS (F)', app.width/2, app.height/10, size=app.textSizeHead, fill=app.secondFill, bold=True, font=app.font)

    drawLabel('Enter U-value if you know it.', app.width/2, app.height/8, size=app.textSize, fill=app.secondFill, bold=True, font=app.font)
    drawLabel('OR select layers from the BLUE PRINT GREEN DESIGN database if you do not.', app.width/2, app.height/7 + 20, size=app.textSize, fill=app.secondFill, bold=True, font=app.font)
    drawLabel('The app will do the work for you!', app.width/2, app.height/7 + 40, size=app.textSize, fill=app.secondFill, bold=True, font=app.font)

    buttonsMiddle = Button(app.height/2, 2, app.width/2, 50,['ENTER U-VALUE', 'OR ENTER LAYERS'])
    buttonsMiddle.draw()

    app.dropdownMenu.draw()

    drawLabel(f'Floor layers: {app.building.floorsLayers}', 25, app.height-100, size=app.textSizeSmall, fill=app.secondFill, font=app.font, align='left', bold = True)
    drawLabel(f'Floor layers R-Values: {app.building.floorsRValue}', 25, app.height-75, size=app.textSizeSmall, fill=app.secondFill, font=app.font, align='left', bold = True)
    if isinstance(app.building.floorsRValue, list): 
        drawLabel(f'Floor Total R-Value: {pythonRound(sum(app.building.floorsRValue), 2)}', 25, app.height-50, size=app.textSizeSmall, fill=app.secondFill, font=app.font, align='left', bold = True)
    else:
        drawLabel(f'Floor Total R-Value: {app.building.floorsRValue}', 25, app.height-50, size=app.textSizeSmall, fill=app.secondFill, font=app.font, align='left', bold = True)


def drawDetailRoofsScreen(app):
    buttonsTop = Button(0, 4, app.width/4, 50,['← BACK', 'RESET', 'UNDO ROOF', 'FORWARD →'])
    buttonsTop.draw()

    drawLabel('ROOFS (R)', app.width/2, app.height/10, size=app.textSizeHead, fill=app.secondFill, bold=True, font=app.font)

    drawLabel('Enter U-value if you know it.', app.width/2, app.height/8, size=app.textSize, fill=app.secondFill, bold=True, font=app.font)
    drawLabel('OR select layers from the BLUE PRINT GREEN DESIGN database if you do not.', app.width/2, app.height/7 + 20, size=app.textSize, fill=app.secondFill, bold=True, font=app.font)
    drawLabel('The app will do the work for you!', app.width/2, app.height/7 + 40, size=app.textSize, fill=app.secondFill, bold=True, font=app.font)

    buttonsMiddle = Button(app.height/2, 2, app.width/2, 50,['ENTER U-VALUE', 'OR ENTER LAYERS'])
    buttonsMiddle.draw()

    app.dropdownMenu.draw()
    
    drawLabel(f'Roof layers: {app.building.roofsLayers}', 25, app.height-100, size=app.textSizeSmall, fill=app.secondFill, font=app.font, align='left', bold = True)
    drawLabel(f'Roof layers R-Values: {app.building.roofsRValue}', 25, app.height-75, size=app.textSizeSmall, fill=app.secondFill, font=app.font, align='left', bold = True)
    if isinstance(app.building.roofsRValue, list): 
        drawLabel(f'Roof Total R-Value: {pythonRound(sum(app.building.roofsRValue), 2)}', 25, app.height-50, size=app.textSizeSmall, fill=app.secondFill, font=app.font, align='left', bold = True)
    else:
        drawLabel(f'Roof Total R-Value: {app.building.roofsRValue}', 25, app.height-50, size=app.textSizeSmall, fill=app.secondFill, font=app.font, align='left', bold = True)

def draw3CalculateScreen(app):
    app.building.calculateInfiltrationHeatLoss()
    app.building.calculateTotalHeatLossCoefficient()
    app.building.calculateTotalHeatLossCoefficientPerComponent()
    app.building.calculateAnnualHeatLoss()

    drawLabel('TRANSMISSION LOSSES', app.width/2, app.height/8, size=app.textSizeHead, fill=app.secondFill, bold=True, font=app.font)
    
    rowWidth = 200
    rowHeight = 50
    colWidth = 750
    colHeight = 600
    tableLeft = app.width/2 - 3*rowWidth/2
    tableTop = 200
    # left col
    componentNamesCol = TableCol(['COMPONENTS', 'WALLS', 'WINDOWS', 'DOORS', 'FLOOR', 'ROOF', 'INFILTRATION'], tableLeft, tableTop, colWidth, colHeight, rowWidth, rowHeight)
    componentNamesCol.draw()

    # middle col
    lossesCol = TableCol(['TOTAL HEAT LOSS', app.building.totalWallUA, app.building.totalWindowUA, app.building.totalDoorUA, app.building.totalFloorUA, app.building.totalRoofUA, app.building.infiltrationLoss], tableLeft+200, tableTop, colWidth, colHeight, rowWidth, rowHeight)
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
        infiltrationRatio = pythonRound(ratioDict['infiltrationUA%'], 2)
        ratioCol = TableCol(['RATIO', f'{wallRatio}%', f'{windowRatio}%', f'{doorRatio}%', f'{floorRatio}%', f'{roofRatio}%', f'{infiltrationRatio}%'], tableLeft+200*2, tableTop, colWidth, colHeight, rowWidth, rowHeight)
        ratioCol.draw()

        drawLabel('ENERGY REPORT', app.width/2, app.height-350, size=app.textSizeHead, fill=app.secondFill, bold=True, font=app.font)
        ratioList = sorted([wallRatio, windowRatio, doorRatio, floorRatio, roofRatio, infiltrationRatio], reverse=True)
        ratioDict = {wallRatio: 'WALLS', windowRatio: 'WINDOWS', doorRatio: 'DOORS', floorRatio: 'FLOOR', roofRatio: 'ROOF', infiltrationRatio: 'INFILTRATION'}
        biggestLossRatio = ratioList[0]
        secondBiggestLossRatio = ratioList[1]
        biggestLossName = ratioDict[ratioList[0]]
        secondBiggestLossName = ratioDict[ratioList[1]]
        drawLabel(f'- You can save the most energy by improving {biggestLossName} ({biggestLossRatio}%) and {secondBiggestLossName} ({secondBiggestLossRatio}%)', app.width/2, app.height-300, size=app.textSize, fill=app.secondFill, font=app.font, bold=True)

        suggestionDict = {'INFILTRATION': 'For infiltration, consider sealing leaks and insulating.', 'WALLS': 'For walls, consider adding insulation.',
                          'WINDOWS': 'For windows, consider adding storm windows or upgrading to triple glazing with argon.',
                          'DOORS': 'For doors, consider adding weatherstripping.', 'FLOOR': 'For floors, consider buying carpet or adding insulation.',
                          'ROOF': 'For roofs, consider adding insulation.'}
        
        drawLabel(suggestionDict[biggestLossName], app.width/2, app.height-275, size=app.textSize, fill=app.secondFill, font=app.font, italic=True)
        drawLabel(suggestionDict[secondBiggestLossName], app.width/2, app.height-250, size=app.textSize, fill=app.secondFill, font=app.font, italic=True)

        if app.building.annualHeatLoss != None:
            if app.building.annualHeatLoss > 15000:
                isExcellent = 'EXCELLENT'
            elif app.building.annualHeatLoss > 10000:
                isExcellent = 'GOOD'
            elif app.building.annualHeatLoss > 5000:
                isExcellent = 'MODERATE'
            else:
                isExcellent = 'POOR'
        
        drawLabel(f'- ANNUAL HEAT LOSS: {isExcellent} with {app.building.annualHeatLoss} kWh/year', app.width/2, app.height-200, size=app.textSize, fill=app.secondFill, bold=True, font=app.font)

        drawLabel('[PRESS 1 TO SEE THE THERMAL VISUALIZATION]', app.width/2, app.height-100, size=app.textSize, fill=app.secondFill, font=app.font, italic=True, bold = True)

    else:
        if app.pageHistory != [] and app.pageHistory[-1] != app.screen:
            if app.pageHistory[-1] != app.screen:
                app.showMessage('Make sure you have entered U-values for all components to get the full table.')


    drawLabel(f'Current screen: {app.screen}', app.width-25, app.height-75, size=app.textSize, fill=app.secondFill, font=app.font, align='right')
    buttonsBottom = Button(app.height-50, 4, app.width/4, 50,['RESET', '⌂ HOME', '← BACK', 'SAVE & CLOSE'])
    buttonsBottom.draw()
