from cmu_graphics import *
from utils import *

########################################################
# BUILDING 
########################################################
class Building:
    def __init__(self, length, width, height):
        self.length = length
        self.width = width
        self.height = height

        self.name = f'Project {(len(app.gallery.items)) + 1}'
        self.location = 'Unknown Location'
        self.annualHeatLoss = 'Unknown'
        self.infiltrationLoss = None

        self.walls = []
        self.windows = []
        self.doors = []
        self.floors = []
        self.roofs = []

        self.rooms = []

        self.totalWindowArea = 0
        self.totalDoorArea = 0
        self.totalWallArea = 0
        self.totalFloorArea = 0
        self.totalRoofArea = 0
        self.totalSharedWallArea = 0

        self.wallsRValue = []
        self.windowsRValue = []
        self.doorsRValue = []
        self.floorsRValue = []
        self.roofsRValue = []

        self.wallsLayers = []
        self.windowsLayers = []
        self.doorsLayers = []
        self.floorsLayers = []
        self.roofsLayers = []

        self.totalWindowUA = 0
        self.totalDoorUA = 0
        self.totalWallUA = 0
        self.totalFloorUA = 0
        self.totalRoofUA = 0

        self.thermalColor = 'white'
    
    def drawBuilding(self):
        drawRect(app.width/2, app.height/2, self.width, self.length, fill = 'lightSalmon', border = self.thermalColor, borderWidth = 15, align = 'center')

    def drawToPlace(self, center):
        cx, cy = center
        drawRect(cx, cy, self.width, self.length, fill = None, border = self.thermalColor, borderWidth = 3, align = 'center')

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
                 (app.width/2 + self.width/2), (app.height/2 - self.length/2) - paddingDist, fill=app.secondFill, lineWidth=lineW)
        drawLine((app.width/2 - self.width/2), (app.height/2 - self.length/2) - paddingDist - lineArrowDist,
                 (app.width/2 - self.width/2), (app.height/2 - self.length/2) - paddingDist + lineArrowDist, fill=app.secondFill, lineWidth=lineW)
        drawLine((app.width/2 + self.width/2), (app.height/2 - self.length/2) - paddingDist - lineArrowDist,
                 (app.width/2 + self.width/2), (app.height/2 - self.length/2) - paddingDist + lineArrowDist, fill=app.secondFill, lineWidth=lineW)
        
        # vertical measure line
        drawLine((app.width/2 + self.width/2) + paddingDist, (app.height/2 - self.length/2),
                 (app.width/2 + self.width/2) + paddingDist, (app.height/2 + self.length/2), fill=app.secondFill, lineWidth=lineW)
        drawLine((app.width/2 + self.width/2) + paddingDist - lineArrowDist, (app.height/2 - self.length/2),
                 (app.width/2 + self.width/2) + paddingDist + lineArrowDist, (app.height/2 - self.length/2), fill=app.secondFill, lineWidth=lineW)
        drawLine((app.width/2 + self.width/2) + paddingDist - lineArrowDist, (app.height/2 + self.length/2),
                 (app.width/2 + self.width/2) + paddingDist + lineArrowDist, (app.height/2 + self.length/2), fill=app.secondFill, lineWidth=lineW)
        
        drawLabel(f'{self.width} cm', app.width/2, (app.height/2 - self.length/2 - textDist), size=textSize, fill=app.secondFill)
        drawLabel(f'{self.length} cm', (app.width/2 + self.width/2 + textDist*1.5), app.height/2, size=textSize, fill=app.secondFill)

    
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
    # BUILDING HEAT LOSS CALCULATIONS 
    ########################################################

    def calculateInfiltrationHeatLoss(self):
        """
        Unit: W/m^3K
        """
        ACH = 1.0 # number of air changes per hour
        heatCapacityAir = 1.059 # W/m^3K
        volume = cmToMeter(app.building.length)* cmToMeter(app.building.width) * cmToMeter(app.building.height)
        self.infiltrationLoss = ACH * heatCapacityAir * volume
        return self.infiltrationLoss


    def calculateTotalHeatLossCoefficient(self):
        """
        Unit: W/K
        Calculates components' heat loss coefficient using total area and U-Value(Transmissiont coefficient).

        Parameters:
        - total area (float): The area of the building component in m².
        - total u-value (float): The U-value(1/R-value) of the component in W/m²K.

        Returns:
        - float: Heat loss coefficient in W/K.
        """


        for window in self.windows:
            self.totalWindowArea = window.calculateArea()
        for door in self.doors:
            self.totalDoorArea = door.calculateArea()
        for wall in self.walls:
            self.totalWallArea = wall.calculateArea()
        for floor in self.floors:
            self.totalFloorArea = floor.calculateArea()
        for roof in self.roofs:
            self.totalRoofArea = roof.calculateArea()

        # heat loss between heated-unheated rooms
        sharedWallArea = 0
        for room in app.rooms:
            for otherRoom in app.rooms:
                sharedWallArea += calculateSharedWallArea(room, otherRoom)
                self.totalSharedWallArea = sharedWallArea
            
        # U-value calculation - W/m^2K
        if isinstance(self.wallsRValue, list) and sum(self.wallsRValue) != 0:
            wallsUValue = 1/sum(self.wallsRValue)
        elif not isinstance(self.wallsRValue, list):
            wallsUValue = 1/self.wallsRValue
        else:
            wallsUValue = 0.2 # dafault value
        
        if isinstance(self.windowsRValue, list) and len(self.windowsRValue) != 0:
            windowsUValue = 1/sum(self.windowsRValue)
        elif not isinstance(self.windowsRValue, list) and self.windowsRValue != 0:
            windowsUValue = 1/self.windowsRValue
        else:
            windowsUValue = 1.5

        if isinstance(self.doorsRValue, list) and len(self.doorsRValue) != 0:
            doorsUValue = 1/sum(self.doorsRValue)
        elif not isinstance(self.doorsRValue, list) and self.doorsRValue != 0:
            doorsUValue = 1/self.doorsRValue
        else:
            doorsUValue = 1.2

        if isinstance(self.floorsRValue, list) and len(self.floorsRValue) != 0:
            floorsUValue = 1/sum(self.floorsRValue)
        elif not isinstance(self.floorsRValue, list) and self.floorsRValue != 0:
            floorsUValue = 1/self.floorsRValue
        else:
            floorsUValue = 0.2

        if isinstance(self.roofsRValue, list) and len(self.roofsRValue) != 0:
            roofsUValue = 1/sum(self.roofsRValue)
        elif not isinstance(self.roofsRValue, list) and self.roofsRValue != 0:
            roofsUValue = 1/self.roofsRValue
        else:
            roofsUValue = 0.15

        self.totalWindowUA = pythonRound((self.totalWindowArea * windowsUValue),2)
        self.totalDoorUA = pythonRound((self.totalDoorArea * doorsUValue),2)
        self.totalWallUA = pythonRound(((self.totalWallArea - self.totalWindowArea - self.totalDoorArea + self.totalSharedWallArea) * wallsUValue),2)
        self.totalFloorUA = pythonRound((self.totalFloorArea * floorsUValue),2)
        self.totalRoofUA = pythonRound((self.totalRoofArea * roofsUValue),2)
        
        return pythonRound((self.totalWindowUA + self.totalDoorUA + self.totalWallUA + self.totalFloorUA + self.totalRoofUA + self.calculateInfiltrationHeatLoss()),2)

    def calculateTotalHeatLossCoefficientPerComponent(self):
        """
        Unit: W/K
        """
        windowRatio = pythonRound(100*self.totalWindowUA / self.calculateTotalHeatLossCoefficient(),2)
        doorRatio = pythonRound(100*self.totalDoorUA / self.calculateTotalHeatLossCoefficient(),2)
        wallRatio = pythonRound(100*self.totalWallUA / self.calculateTotalHeatLossCoefficient(),2)
        floorRatio = pythonRound(100*self.totalFloorUA / self.calculateTotalHeatLossCoefficient(),2)
        roofRatio = pythonRound(100*self.totalRoofUA / self.calculateTotalHeatLossCoefficient(),2)
        infiltrationRatio = pythonRound(100*self.calculateInfiltrationHeatLoss() / self.calculateTotalHeatLossCoefficient(),2)
        return {'windowUA%': windowRatio, 'doorUA%': doorRatio, 'wallUA%': wallRatio, 'floorUA%': floorRatio, 'roofUA%': roofRatio, 'infiltrationUA%': infiltrationRatio}


    def calculateAnnualHeatLoss(self):
        """
        Unit: kWh/year
        """
        # Convert Watt to kWh
        heatLossCoefficient = self.calculateTotalHeatLossCoefficient() # W/K
        self.annualHeatLoss = pythonRound((WToKw(heatLossCoefficient * 24 * app.heatingDegreeDays65F)),2) # kWh/year
        return self.annualHeatLoss
    

########################################################
# ROOM 
########################################################

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

        left = min(self.x, self.x + self.width)
        top = min(self.y, self.y + self.height)
        drawRect(left, top, self.width, self.height, fill=color, border=app.secondFill, borderWidth=15/2)
        drawLabel(self.name.upper(), self.x + self.width / 2, self.y + self.height / 2 - 5, size=app.textSizeSmall, fill = 'black', bold = True, font = app.font, align = 'center')

        heatingSituation = 'HEATED' if self.isHeated else 'NOT HEATED'
        drawLabel(heatingSituation, self.x + self.width / 2, self.y + self.height / 2 + 5, size=app.textSizeSmall-2, fill = 'black', font = app.font, align = 'center')


########################################################
# BUILDING COMPONENT 
########################################################

class BuildingComponent:
    def __init__(self, length, height, uValue): 
        self.length = length
        self.height = height
        self.uValue = None # not needed?
        self.rValue = self.calculateRValue() # not needed?

        self.thermalColor = app.secondFill
        # gradient -> based on the heat loss
        # if self.rValue * self.calculateArea() > 100:
        #     self.thermalColor = gradient('red','orange', start = 'left-bottom')
        # elif self.rValue * self.calculateArea() > 50:
        #     self.thermalColor = gradient('orange','yellow', start = 'left-bottom')
        # elif self.rValue * self.calculateArea() > 25:
        #     self.thermalColor = gradient('yellow','green', start = 'left-bottom')
        # else:
        #     self.thermalColor = 'gray'

    def calculateArea(self):
        return pythonRound(cm2ToMeter2(self.length * self.height),2)

    def calculateRValue(self): # not needed?
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

class Window(BuildingComponent):
    def __init__(self, length, height, uValue, cx, cy):
        super().__init__(length, height, uValue)
        self.type = None
        self.cx = cx
        self.cy = cy
    
    def draw(self):
        if self.type == 'vertical':
            drawRect(self.cx, self.cy, 15, self.length, fill = app.fill, align = 'center')
            drawLine(self.cx-2.5, self.cy - self.length/2, self.cx-2.5, self.cy + self.length/2, fill = app.secondFill, lineWidth = 1)
            drawLine(self.cx, self.cy - self.length/2, self.cx, self.cy + self.length/2, fill = app.secondFill, lineWidth = 1)
            drawLine(self.cx+2.5, self.cy - self.length/2, self.cx+2.5, self.cy + self.length/2, fill = app.secondFill, lineWidth = 1)
        elif self.type == 'horizontal':
            drawRect(self.cx, self.cy, self.length, 15, fill = app.fill, align = 'center')
            drawLine(self.cx - self.length/2, self.cy-2.5, self.cx + self.length/2, self.cy-2.5, fill = app.secondFill, lineWidth = 1)
            drawLine(self.cx - self.length/2, self.cy, self.cx + self.length/2, self.cy, fill = app.secondFill, lineWidth = 1)
            drawLine(self.cx - self.length/2, self.cy+2.5, self.cx + self.length/2, self.cy+2.5, fill = app.secondFill, lineWidth = 1)

class Door(BuildingComponent):
    def __init__(self, length, height, uValue, cx, cy):
        super().__init__(length, height, uValue)
        self.type = None
        self.cx = cx
        self.cy = cy

    def draw(self):
        if self.type == 'vertical':
            drawRect(self.cx, self.cy, 15, self.length, fill = app.fill, align = 'center')
            drawLine(self.cx, self.cy - self.length/2, self.cx - self.length/2, self.cy - self.length/2 + self.length/2, fill = app.secondFill, lineWidth = 1)
        elif self.type == 'horizontal':
            drawRect(self.cx, self.cy, self.length, 15, fill = app.fill, align = 'center')
            drawLine(self.cx - self.length/2, self.cy, self.cx - self.length/2 + self.length/2,self.cy - self.length/2, fill = app.secondFill, lineWidth = 1)

class Floor(BuildingComponent):
    def __init__(self, length, height, width, uValue):
        super().__init__(length, height, uValue)
        self.width = width

    def calculateArea(self):
        return pythonRound(cm2ToMeter2(app.building.length * app.building.width),2)

class Roof(BuildingComponent):
    def __init__(self, length, height, width, uValue):
        super().__init__(length, height, uValue)
        self.width = width
        
    def calculateArea(self):
        return pythonRound(cm2ToMeter2(app.building.length * app.building.width),2)


