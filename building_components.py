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

        self.totalWindowArea = 0
        self.totalDoorArea = 0
        self.totalWallArea = 0
        self.totalFloorArea = 0
        self.totalRoofArea = 0
        self.totalSharedWallArea = 0

        self.totalWindowUA = 0
        self.totalDoorUA = 0
        self.totalWallUA = 0
        self.totalFloorUA = 0
        self.totalRoofUA = 0

    def drawBuilding(self):
        drawRect(app.width/2, app.height/2, self.width, self.length, fill = None, border = 'white', borderWidth = 15, align = 'center')

    def drawToPlace(self, center):
        cx, cy = center
        drawRect(cx, cy, self.width, self.length, fill = None, border = 'white', borderWidth = 3, align = 'center')

    def createScaledBuildingIcon(self):
        scaleFactor = 0.3
        scaledLength = self.length * scaleFactor
        scaledWidth = self.width * scaleFactor
        scaledHeight = self.height * scaleFactor
        return Building(scaledLength, scaledWidth, scaledHeight)
    
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
        return f'{self.name} in {self.location} with dimensions {self.length}x{self.width}x{self.height}cm'
    
    def save(self):
        if app.building in app.gallery.items:
                app.showMessage(f'{self.name} is already saved in gallery!')
        else:
            app.gallery.items.append(app.building)
            app.showMessage(f'{app.building.name} at {app.building.location} with dimensions ' + 
                            f'{app.building.length}x{app.building.width}x{app.building.height} cm is saved to gallery!')
    
    ########################################################
    ################ HEAT LOSS CALCULATIONS ################
    ########################################################

    def calculateInfiltrationHeatLoss(self):
        ACH = 1.0 # number of air changes per hour
        heatCapacityAir = 0.018 # BTU/hr*ft^3*F
        volume = app.building.length * app.building.width * app.building.height
        return ACH * heatCapacityAir * volume

    def calculateTotalHeatLossCoefficient(self):
        """
        Calculates components' heat loss coefficient using total area and U-Value(Transmissiont coefficient).

        Parameters:
        - total area (float): The area of the building component in m².
        - total u-value (float): The U-value(1/R-value) of the component in W/m²K.

        Returns:
        - float: Heat loss coefficient in W/K.
        """

        for window in app.windows:
            self.totalWindowArea += window.calculateArea()

        for door in app.doors:
            self.totalDoorArea += door.calculateArea()

        for wall in app.walls:
            self.totalWallArea += wall.calculateArea()

        for floor in app.floors:
            self.totalFloorArea += floor.calculateArea()

        for roof in app.roofs:
            self.totalRoofArea += roof.calculateArea()

        # heat loss between heated-unheated rooms
        for room in app.rooms:
            if room.isHeated:
                for otherRoom in app.rooms:
                    if not otherRoom.isHeated:
                        self.sharedWallArea = calculateSharedWallArea(room, otherRoom)
                        totalSharedWallArea += self.sharedWallArea


        self.totalWindowUA += self.totalWindowArea * 1/window.calculateRValue()
        self.totalDoorUA += self.totalDoorArea * 1/door.calculateRValue()
        self.totalWallUA += (self.totalWallArea - self.totalWindowArea - self.totalDoorArea + totalSharedWallArea) * 1/wall.calculateRValue()
        self.totalFloorUA += self.totalFloorArea * 1/floor.calculateRValue()
        self.totalRoofUA += self.totalRoofArea * 1/roof.calculateRValue()
        
        return self.totalWindowUA + self.totalDoorUA + self.totalWallUA + self.totalFloorUA + self.totalRoofUA + self.calculateInfiltrationHeatLoss()

    def calculateTotalHeatLossCoefficientPerComponent(self):
        windowRatio = self.totalWindowUA / self.calculateTotalHeatLossCoefficient()
        doorRatio = self.totalDoorUA / self.calculateTotalHeatLossCoefficient()
        wallRatio = self.totalWallUA / self.calculateTotalHeatLossCoefficient()
        floorRatio = self.totalFloorUA / self.calculateTotalHeatLossCoefficient()
        roofRatio = self.totalRoofUA / self.calculateTotalHeatLossCoefficient()
        return {'windowUA': windowRatio, 'doorUA': doorRatio, 'wallUA': wallRatio, 'floorUA': floorRatio, 'roofUA': roofRatio}


    def calculateAnnualHeatLoss(self):
        heatLossCoefficient = self.calculateTotalHeatLossCoefficient()
        return heatLossCoefficient * 24 * app.heatingDegreeDays65F # BTU * 10^6 = MMBTU


class Room:
    def __init__(self, x, y, width, height, name, isHeated):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.name = name
        self.isHeated = isHeated

    def draw(self):
        color = 'lightSalmon' if self.isHeated else 'lightGray'
        print(color) # DELETE
        drawRect(self.x, self.y, self.width, self.height, fill=color, border='white', borderWidth=15)
        drawLabel(self.name.upper(), self.x + self.width / 2, self.y + self.height / 2 - 5, size=app.textSizeSmall, fill = 'black', bold = True, font = app.font, align = 'center')

        heatingSituation = 'HEATED' if self.isHeated else 'NOT HEATED'
        drawLabel(heatingSituation, self.x + self.width / 2, self.y + self.height / 2 + 5, size=app.textSizeSmall-2, fill = 'black', font = app.font, align = 'center')


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
    def __init__(self, length, height, width, uValue, cx, cy):
        super().__init__(length, height, uValue)
        self.width = width
        self.cx = cx
        self.cy = cy

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
            drawRect(self.cx, self.cy, 20, self.length, fill = app.fill, align = 'center')
            drawLine(self.cx-2.5, self.cy - self.length/2, self.cx-2.5, self.cy + self.length/2, fill = 'white', lineWidth = 1)
            drawLine(self.cx, self.cy - self.length/2, self.cx, self.cy + self.length/2, fill = 'white', lineWidth = 1)
            drawLine(self.cx+2.5, self.cy - self.length/2, self.cx+2.5, self.cy + self.length/2, fill = 'white', lineWidth = 1)
        elif self.type == 'horizontal':
            drawRect(self.cx, self.cy, self.length, 20, fill = app.fill, align = 'center')
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
            drawRect(self.cx, self.cy, 20, self.length, fill = app.fill, align = 'center')
            drawLine(self.cx, self.cy - self.length/2, self.cx - self.length/2, self.cy - self.length/2 + self.length/2, fill = 'white', lineWidth = 1)
        elif self.type == 'horizontal':
            drawRect(self.cx, self.cy, self.length, 20, fill = app.fill, align = 'center')
            drawLine(self.cx - self.length/2, self.cy, self.cx - self.length/2 + self.length/2,self.cy - self.length/2, fill = 'white', lineWidth = 1)

class Floor(BuildingComponent):
    pass

class Roof(BuildingComponent):
    pass


