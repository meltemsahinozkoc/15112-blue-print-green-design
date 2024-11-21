# wall, window, door, roof, floor etc. + helpers to calculate area, heat loss etc.
from cmu_graphics import *

class Building:
    def __init__(self, location, lenght, width):
        self.bldgLenght = 0
        self.bldgWidth = 0
        self.bldgLenght = lenght
        self.location = location

        self.cx = lenght/2
        self.cy = width/2

    def drawRoom(self):
        left = self.cy - (self.bldgWidth/2)
        top = self.cx - (self.bldgLenght/2)
        drawRect(left, top, self.bldgWidth, self.bldgLenght, fill = 'gray', border = 'black')
    
    def drawMeasureLines(app):
        drawLine(0, app.roomHeight/2, app.bldgWidth, app.roomHeight/2, fill='black')
        drawLine(app.bldgWidth/2, 0, app.bldgWidth/2, app.roomHeight, fill='black')
        drawLabel(f'{app.bldgWidth} ft', app.bldgWidth/2, app.roomHeight, size=12, fill='black')
        drawLabel(f'{app.roomHeight} ft', app.bldgWidth, app.roomHeight/2, size=12, fill='black')
        drawLabel('0', 0, app.roomHeight/2, size=12, fill='black')
        drawLabel('0', app.bldgWidth/2, 0, size=12, fill='black')
    

class BuildingComponent:
    def __init__(self, length, width, uValue): 
        self.length = length
        self.width = width
        self.uValue = uValue

    def calculateArea(self):
        return self.length * self.width

    def calculateRValue(self):
        return 1 / self.uValue


class Wall(BuildingComponent):
    def __init__(self, length, width, height, uValue):
        super().__init__(length, width, uValue)
        self.height = height

    def calculateArea(self):
        return ((self.length * self.height) + (self.width * self.height)) * 2

class Window(BuildingComponent):
    pass

class Door(BuildingComponent):
    pass

class Floor(BuildingComponent):
    pass

class Roof(BuildingComponent):
    pass


def calculateHeatLossCoefficient(app):
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
    volume = app.bldgLenght * app.bldgWidth * app.roomHeight
    return ACH * heatCapacityAir * volume


def calculateAnnualHeatLoss(app,walls, windows, doors, floors, roofs):
    heatLossCoefficient = calculateHeatLossCoefficient(app,walls)
    return heatLossCoefficient * 24 * app.heatingDegreeDays65F # BTU * 10^6 = MMBTU

def calculateTotalHeatLoss(app,walls, windows, doors, floors, roofs):
    return calculateAnnualHeatLoss(app,walls) + calculateInfiltrationHeatLoss(app)

