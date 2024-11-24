# wall, window, door, roof, floor etc. + helpers to calculate area, heat loss etc.
from cmu_graphics import *
from utils import *

class Building:
    def __init__(self, length, width, height):
        self.length = length
        self.width = width
        self.height = height

        self.name = f'Project {(app.projectCount) + 1}'
        self.location = 'Unknown Location'

    def drawBuilding(self):
        drawRect(app.width/2, app.height/2, self.width, self.length, fill = None, border = 'white', borderWidth = 15, align = 'center')

    def drawMeasureLines(self):
        paddingDist = 15
        textDist = 25
        textSize = 12
        lineW = 1
        lineArrowDist = 5
        
        # horizontal measure line
        drawLine((app.width/2 - self.width/2), (app.height/2 - self.length/2) - paddingDist,
                 (app.width/2 + self.width/2), (app.height/2 - self.length/2) - paddingDist, fill='white', lineWidth=lineW)
        drawLine((app.width/2 - self.width/2), (app.height/2 - self.length/2) - paddingDist - lineArrowDist,
                 (app.width/2 - self.width/2), (app.height/2 - self.length/2) - paddingDist + lineArrowDist, fill='white', lineWidth=lineW)
        drawLine((app.width/2 + self.width/2), (app.height/2 - self.length/2) - paddingDist - lineArrowDist,
                 (app.width/2 + self.width/2), (app.height/2 - self.length/2) - paddingDist + lineArrowDist, fill='white', lineWidth=lineW)
        
        # vertical measure line
        drawLine((app.width/2 + self.width/2) + paddingDist, (app.height/2 - self.length/2),
                 (app.width/2 + self.width/2) + paddingDist, (app.height/2 + self.length/2), fill='white', lineWidth=lineW)
        drawLine((app.width/2 + self.width/2) + paddingDist - lineArrowDist, (app.height/2 - self.length/2),
                 (app.width/2 + self.width/2) + paddingDist + lineArrowDist, (app.height/2 - self.length/2), fill='white', lineWidth=lineW)
        drawLine((app.width/2 + self.width/2) + paddingDist - lineArrowDist, (app.height/2 + self.length/2),
                 (app.width/2 + self.width/2) + paddingDist + lineArrowDist, (app.height/2 + self.length/2), fill='white', lineWidth=lineW)
        
        drawLabel(f'{self.width} cm', app.width/2, (app.height/2 - self.length/2 - textDist), size=textSize, fill='white')
        drawLabel(f'{self.length} cm', (app.width/2 + self.width/2 + textDist*1.5), app.height/2, size=textSize, fill='white')

    
    def __repr__(self):
        return f'{self.name} at {self.location} with dimensions {self.length}x{self.width}x{self.height}cm'
    

class BuildingComponent:
    def __init__(self, length, height, uValue): 
        self.length = length
        self.height = height
        self.uValue = uValue

    def calculateArea(self):
        return self.length * self.width

    def calculateRValue(self):
        return 1 / self.uValue
    

class Wall(BuildingComponent):
    def __init__(self, length, height, width, uValue):
        super().__init__(length, height, uValue)
        self.width = width

    def calculateArea(self):
        return ((self.length * self.height) + (self.width * self.height)) * 2

class Window(BuildingComponent):
    def draw(self):
        print(self.length)
        drawRect(app.cx, app.cy, 30, self.length, fill = app.fill, align = 'center')
        drawLine(app.cx, app.cy - self.length/2, app.cx, app.cy + self.length/2, fill = 'white', lineWidth = 1)

class Door(BuildingComponent):
    def draw(self):
        print(self.length)
        drawRect(app.cx, app.cy, 30, self.length, fill = app.fill, align = 'center')
        drawLine(app.cx, app.cy - self.length/2, app.cx - self.length/2, app.cy - self.length/2 + self.length/2, fill = 'white', lineWidth = 1) # draw 45 degree line

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
    volume = app.building.length * app.building.width * app.building.height
    return ACH * heatCapacityAir * volume


def calculateAnnualHeatLoss(app,walls, windows, doors, floors, roofs):
    heatLossCoefficient = calculateHeatLossCoefficient(app,walls)
    return heatLossCoefficient * 24 * app.heatingDegreeDays65F # BTU * 10^6 = MMBTU

def calculateTotalHeatLoss(app,walls, windows, doors, floors, roofs):
    return calculateAnnualHeatLoss(app,walls) + calculateInfiltrationHeatLoss(app)

