# wall, window, door, roof, floor etc. + helpers to calculate area, heat loss etc.
from cmu_graphics import *
from utils import *

class Building:
    def __init__(self, length, width, height):
        self.length = length
        self.width = width
        self.height = height

        self.name = f'Project {(len(app.gallery.items)) + 1}'
        self.location = 'Unknown Location'
        self.annualHeatLoss = 'Unknown'

    def drawBuilding(self):
        drawRect(app.width/2, app.height/2, self.width, self.length, fill = None, border = 'white', borderWidth = 15, align = 'center')

    def drawToPlace(self, center):
        cx, cy = center
        drawRect(cx, cy, self.width, self.length, fill = None, border = 'white', borderWidth = 3, align = 'center')

    def createScaledBuildingIcon(self):
        scaleFactor = 0.3
        scaledLenght = self.length * scaleFactor
        scaledWidth = self.width * scaleFactor
        scaledHeight = self.height * scaleFactor
        return Building(scaledLenght, scaledWidth, scaledHeight)
    
    def drawMeasureLines(self):
        paddingDist = 30
        textDist = 40
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
    
    def save(self):
        app.gallery.items.append(app.building)
        app.showMessage(f'{app.building.name} at {app.building.location} with dimensions ' + 
                        f'{app.building.length}x{app.building.width}x{app.building.height} cm is saved to gallery!')
        print(app.gallery.items)
        
class BuildingComponent:
    def __init__(self, length, height, uValue): 
        self.length = length
        self.height = height
        self.uValue = uValue
        self.rValue = self.calculateRValue()

    def calculateArea(self):
        return self.length * self.width

    def calculateRValue(self):
        return None if self.uValue is None else 1 / self.uValue

    def setMaterial(self, material):
        self.uValue = float(material['Conductivity (BTU·ft/h·°F'])
        self.rValue = self.calculateRValue()
    
class Wall(BuildingComponent):
    def __init__(self, length, height, width, uValue):
        super().__init__(length, height, uValue)
        self.width = width

    def calculateArea(self):
        return ((self.length * self.height) + (self.width * self.height)) * 2

class Window(BuildingComponent):
    def __init__(self, length, height, uValue, cx, cy):
        super().__init__(length, height, uValue)
        self.type = None
        self.cx = cx
        self.cy = cy
    
    def draw(self):
        if self.type == 'vertical':
            drawRect(self.cx, self.cy, 30, self.length, fill = app.fill, align = 'center')
            drawLine(self.cx-2.5, self.cy - self.length/2, self.cx-2.5, self.cy + self.length/2, fill = 'white', lineWidth = 1)
            drawLine(self.cx, self.cy - self.length/2, self.cx, self.cy + self.length/2, fill = 'white', lineWidth = 1)
            drawLine(self.cx+2.5, self.cy - self.length/2, self.cx+2.5, self.cy + self.length/2, fill = 'white', lineWidth = 1)
        elif self.type == 'horizontal':
            drawRect(self.cx, self.cy, self.length, 30, fill = app.fill, align = 'center')
            drawLine(self.cx - self.length/2, self.cy-2.5, self.cx + self.length/2, self.cy-2.5, fill = 'white', lineWidth = 1)
            drawLine(self.cx - self.length/2, self.cy, self.cx + self.length/2, self.cy, fill = 'white', lineWidth = 1)
            drawLine(self.cx - self.length/2, self.cy+2.5, self.cx + self.length/2, self.cy+2.5, fill = 'white', lineWidth = 1)

class Door(BuildingComponent):
    def __init__(self, length, height, uValue, cx, cy):
        super().__init__(length, height, uValue)
        self.type = None
        self.cx = cx
        self.cy = cy

    def draw(self):
        if self.type == 'vertical':
            drawRect(self.cx, self.cy, 30, self.length, fill = app.fill, align = 'center')
            drawLine(self.cx, self.cy - self.length/2, self.cx - self.length/2, self.cy - self.length/2 + self.length/2, fill = 'white', lineWidth = 1)
        elif self.type == 'horizontal':
            drawRect(self.cx, self.cy, self.length, 30, fill = app.fill, align = 'center')
            drawLine(self.cx - self.length/2, self.cy, self.cx - self.length/2 + self.length/2,self.cy - self.length/2, fill = 'white', lineWidth = 1)

class Floor(BuildingComponent):
    pass

class Roof(BuildingComponent):
    pass

