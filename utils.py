# Some helper functions and auxilary implementations, such as unit conversion,
# data validation/formatting, Buttons, Gallery etc

from cmu_graphics import *

########################################################
#################### DATA VALIDATION ###################
########################################################

def isValidDimension(app, dimension):
    if not dimension.isdigit() or dimension == None or int(dimension) < 100 or int(dimension) > 500:
        app.showMessage('Invalid dimension. Please enter a value between 100-500.')
        return False
    return True

def isValidHeight(app, dimension):
    if not dimension.isdigit() or dimension == None or int(dimension) < 6 or int(dimension) > 35:
        app.showMessage('Invalid dimension. Please enter a value between 0-10!')
        return False
    return True

def hasAllParametersSet(app):
    if isValidDimension(app.building.length) and isValidDimension(app.building.width):
        return app.building.name and app.building.location and app.buidling.height
    return False

def castCmToMeter(app, dimension):
    return dimension * 100

########################################################
################ HEAT LOSS CALCULATIONS ################
########################################################

def calculateHeatLossCoefficient(app):
    """
    Calculates components' heat loss coefficient using total area and U-Value(Transmissiont coefficient).

    Parameters:
    - total area (float): The area of the building component in m².
    - total u-value (float): The U-value(1/R-value) of the component in W/m²K.

    Returns:
    - float: Heat loss coefficient in W/K.
    """
    totalArea = 0
    totalRValue = 0

    for wall in app.walls:
        totalArea += wall.calculateArea()
    for window in app.windows:
        totalArea += window.calculateArea()
        totalRValue += window.calculateRValue()
    for door in app.doors:
        totalArea += door.calculateArea()
        totalRValue += door.calculateRValue()
    for floor in app.floors:
        totalArea += floor.calculateArea()
        totalRValue += floor.calculateRValue()
    for roof in app.roofs:
        totalArea += roof.calculateArea()
        totalRValue += roof.calculateRValue()
    
    totalUValue = 1/totalRValue
    return totalArea * totalUValue

def calculateInfiltrationHeatLoss(app):
    ACH = 1.0
    heatCapacityAir = 0.018 # BTU/hr*ft^3*F
    volume = app.building.length * app.building.width * app.building.height
    return ACH * heatCapacityAir * volume


def calculateAnnualHeatLoss(app,walls, windows, doors, floors, roofs):
    heatLossCoefficient = calculateHeatLossCoefficient(app,walls)
    return heatLossCoefficient * 24 * app.heatingDegreeDays65F # BTU * 10^6 = MMBTU

def calculateTotalHeatLoss(app,walls, windows, doors, floors, roofs):
    return calculateAnnualHeatLoss(app,walls) + calculateInfiltrationHeatLoss(app)


########################################################
##################### UI COMPONENTS ####################
########################################################

class Button:
    def __init__(self, top, buttonNum, buttonStep, buttonHeight, text):
        self.buttonNum = buttonNum
        self.buttonStep = buttonStep
        self.buttonHeight = buttonHeight
        self.text = text
        self.top = top

    def draw(self):
        for i in range(self.buttonNum):
            drawRect(i*self.buttonStep,self.top, self.buttonStep,
                    self.buttonHeight , border = 'white', borderWidth = 1, fill = 'white', opacity = 40)
            drawLabel(self.text[i], (i+0.5)*self.buttonStep, self.top + self.buttonHeight/2,
                        font = 'monospace', fill='white', bold = True, size = 16)
        
    def mouseOver(self,i):
        if app.cx != None and app.cy != None:
            if (app.cx > i*self.buttonStep and app.cx < (i+1)*self.buttonStep and
                        app.cy > self.top and app.cy < self.top + self.buttonHeight):
                app.mouseOverButton = True
                return True
        return False

class Icon:
    def __init__(self, r, origin, name=None, lineColor='white', lineWidth=1):
        self.r = r
        self.origin = origin
        self.name = name
        self.lineColor = lineColor
        self.lineWidth = lineWidth
    
    def draw(self, app):
        lineColor, fillColor = 'white'
        cx, cy = self.origin
        r = self.r
        if self.name == 'Forward Arrow':
            drawLabel(cx,cy-r, text='→', fill=lineColor, 
                                        font=app.font)
            drawLabel(cx,cy+r, text='F', fill=lineColor, 
                                        font=app.font)
        elif self.name == 'Backward Arrow':
            drawLabel(cx,cy-r, text='←', fill=lineColor, 
                                        font=app.font)
            drawLabel(cx,cy+r, text='B', fill=lineColor, 
                                        font=app.font)
        
        elif self.name == 'Help':
            drawLabel(cx,cy, text='?', fill=lineColor, 
                                        font=app.font)
            drawCircle(cx,cy,r, fill=fillColor, border=lineColor, borderWidth=self.lineWidth)
        elif self.name == 'Save':
            pass


class Gallery:
    def __init__(self):
        self.items = []
        self.padding = 50
        self.width = 200
        self.length = 200
        self.top = 700
    
    def updateProjectCount(self):
        self.projectCount = len(self.items) # num
        self.galleryStep = (app.width - self.padding*2) / self.projectCount if self.projectCount > 0 else 0 # step

    def draw(self):
        self.updateProjectCount()
        for i in range(self.projectCount):
            drawRect(i*(self.galleryStep) + self.padding, self.top, self.width, self.length, fill = None, border = 'white', borderWidth = 1)
            
            currBuilding = self.items[i]
            newBuilding = currBuilding.createScaledBuildingIcon()

            center = (i*self.galleryStep + self.padding + self.width/2, self.top + self.length/2)
            newBuilding.drawToPlace(center)
            
            cx, cy = center
            drawLabel(currBuilding.name, cx, cy+120, fill = 'white', bold = True, size = 16)
            drawLabel(currBuilding.location, cx, cy+140, fill = 'white', size = 12)
            drawLabel(f'{currBuilding.annualHeatLoss} MMBTU', cx, cy+155, fill = 'white', size = 12)
    
    def mouseOver(self,i):
        self.updateProjectCount()
        if app.cx != None and app.cy != None:
            return (app.cx > i*self.galleryStep and app.cx < (i+1)*self.galleryStep and
                        app.cy > self.top and app.cy < self.top + self.length)
    

def navigateBack(app):
    if len(app.pageHistory) > 1:
        app.pageHistory.pop()
        app.screen = app.pageHistory[-1]

def navigateForward(app):
    pass
