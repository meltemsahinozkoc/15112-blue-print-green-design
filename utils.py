from cmu_graphics import *

def isValidDimension(app, dimension):
    if not dimension.isdigit() or dimension == None or int(dimension) < 500 or int(dimension) > 6000:
        app.showMessage('Invalid dimension. Please enter a value between 500-6000cm.')
        return False
    return True

def isValidHeight(app, dimension):
    if not dimension.isdigit() or dimension == None or int(dimension) < 150 or int(dimension) > 1000:
        app.showMessage('Invalid dimension. Please enter a value between 150-1000cm!')
        return False
    return True

def hasAllParametersSet(app):
    if isValidDimension(app.building.length) and isValidDimension(app.building.width):
        return app.building.name and app.building.location and app.buidling.height
    return False


def calculateSharedWallArea(room1, room2):
    """
    Calculate the shared wall area between two rooms.
    Only calculates if one room is heated and the other is not.

    Parameters:
    - room1, room2: Room objects to calculate shared wall area

    Returns:
    - float: Shared wall area between UNHEATED rooms in square meters

    Unit: m^2
    """
    if room1.isHeated == room2.isHeated:
        return 0

    xOverlap = max(0, min(room1.x + room1.width, room2.x + room2.width) - max(room1.x, room2.x))
    yOverlap = max(0, min(room1.y + room1.height, room2.y + room2.height) - max(room1.y, room2.y))
    
    if xOverlap > 0 and yOverlap < 15/2:
        return cm2ToMeter2(xOverlap * app.building.height)
    elif yOverlap > 0 and xOverlap < 15/2:
        return cm2ToMeter2(yOverlap * app.building.height)
    else:
        return 0

def cmToMeter(cm):
    return cm/100

def cm2ToMeter2(cm2):
    return cm2/10000

def WToKw(W):
    return W/1000
########################################################
# UI COMPONENTS 
########################################################

class Button:
    def __init__(self, top, buttonNum, buttonStep, buttonHeight, text):
        self.buttonNum = buttonNum
        self.buttonStep = buttonStep
        self.buttonHeight = buttonHeight
        self.text = text
        self.top = top
        self.isHovered = [False]*buttonNum

    def draw(self):
        for i in range(self.buttonNum):
            fill = 'gray' if self.isHovered[i] else app.secondFill
            drawRect(i * self.buttonStep, self.top, self.buttonStep,
                     self.buttonHeight, border=app.secondFill, borderWidth=1,
                     fill=fill, opacity=40)
            drawLabel(self.text[i], (i + 0.5) * self.buttonStep, self.top + self.buttonHeight / 2,
                      font='monospace', fill=app.secondFill, bold=True, size=16)
        
    def mouseOver(self, i):
        if app.hx is not None and app.hy is not None:
            if (i * self.buttonStep < app.hx < (i + 1) * self.buttonStep and
                    self.top < app.hy < self.top + self.buttonHeight):
                self.isHovered[i] = True
                return True
            self.isHovered[i] = False
        return False

    def handleHover(self):
        for i in range(self.buttonNum):
            self.mouseOver(i) 

class Gallery:
    def __init__(self):
        self.items = []
        self.padding = 50
        self.width = 200
        self.length = 200
        self.top = 750
    
    def updateProjectCount(self):
        self.projectCount = len(self.items) # num
        self.galleryStep = (app.width - self.padding*2) / self.projectCount if self.projectCount > 0 else 0 # step

    def draw(self):
        self.updateProjectCount()
        for i in range(self.projectCount):
            drawRect(i*(self.galleryStep) + self.padding, self.top, self.width, self.length, fill = None, border = app.secondFill, borderWidth = 1)
            
            currBuilding = self.items[i]
            newBuilding = currBuilding.createScaledBuildingIcon()

            center = (i*self.galleryStep + self.padding + self.width/2, self.top + self.length/2)
            newBuilding.drawToPlace(center)
            
            cx, cy = center
            drawLabel(currBuilding.name, cx, cy+120, fill = app.secondFill, bold = True, size = 16)
            drawLabel(currBuilding.location, cx, cy+140, fill = app.secondFill, size = 12)
            drawLabel(f'{currBuilding.annualHeatLoss} kWh/year', cx, cy+155, fill = app.secondFill, size = 12)
    
    def mouseOver(self,i):
        self.updateProjectCount()
        if app.cx != None and app.cy != None:
            return (app.cx > i*self.galleryStep and app.cx < (i+1)*self.galleryStep and
                        app.cy > self.top and app.cy < self.top + self.length)
    

def navigateBack(app):
    if len(app.pageHistory) > 1:
        app.pageHistory.pop()
        app.screen = app.pageHistory[-1]

class dropdownMenu:
    def __init__(self, items, x, y, width, height, buttonWidth, buttonHeight):
        self.items = items
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.buttonWidth = buttonWidth
        self.buttonHeight = buttonHeight

        self.currStartIdx = 0
        self.elementsPerPage = 6

        self.isHovered = [False]*len(self.items)

    def draw(self):
        currPageItems = self.items[self.currStartIdx:self.currStartIdx+self.elementsPerPage]
        for i in range(len(currPageItems)):
            fill = 'gray' if self.isHovered[i] else app.secondFill
            item = currPageItems[i]
            drawRect(self.x, self.y + i*self.buttonHeight, self.buttonWidth, self.buttonHeight, fill=fill, border=app.secondFill, borderWidth=1, opacity = 20)
            drawLabel(item['Material'], self.x + self.buttonWidth/2, self.y + i*self.buttonHeight + self.buttonHeight/2, fill=app.secondFill, size=app.textSizeSmall, font=app.font, align='center', bold = True)
        
        # navi buttons
        buttonSize = self.buttonHeight
        drawRect(self.x + self.width, self.y, buttonSize, buttonSize, fill=app.secondFill, border=app.secondFill, borderWidth=1, opacity = 20)
        drawLabel('↑', self.x + self.width + buttonSize/2, self.y + buttonSize/2, fill=app.secondFill, size=app.textSizeHead, align='center', bold = True)
        drawRect(self.x + self.width, self.y + buttonSize, buttonSize, buttonSize, fill=app.secondFill, border=app.secondFill, borderWidth=1, opacity = 20)
        drawLabel('↓', self.x + self.width + buttonSize/2, self.y + buttonSize + buttonSize/2, fill=app.secondFill, size=app.textSizeHead, align='center', bold = True)

    
    def handleClick(self, mouseX, mouseY):
        if mouseX > self.x + self.width and mouseX < self.x + self.width + self.buttonWidth:
            if mouseY > self.y and mouseY < self.y + self.buttonHeight:
                if self.currStartIdx > 0:
                    self.currStartIdx -= 1
            elif mouseY > self.y + self.buttonHeight and mouseY < self.y + self.buttonHeight*2:
                if self.currStartIdx < len(self.items) - self.elementsPerPage:
                    self.currStartIdx += 1

        if mouseX > self.x and mouseX < self.x + self.buttonWidth:
            currPageItems = self.items[self.currStartIdx:self.currStartIdx+self.elementsPerPage]
            for i in range(len(currPageItems)):
                if mouseY > self.y + i*self.buttonHeight and mouseY < self.y + (i+1)*self.buttonHeight:
                    itemRValue = pythonRound(1/(float(currPageItems[i]['Conductivity (W/m·K)'])), 2)
                    if app.screen == 'detailWalls':
                        if isinstance(app.building.wallsRValue, list):
                            app.building.wallsLayers.append(currPageItems[i]['Material'])
                            app.building.wallsRValue.append(itemRValue) # append the selected item conductivity
                    elif app.screen == 'detailWindows':
                        if isinstance(app.building.windowsRValue, list):
                            app.building.windowsLayers.append(currPageItems[i]['Material'])
                            app.building.windowsRValue.append(itemRValue)
                    elif app.screen == 'detailDoors':
                        if isinstance(app.building.doorsRValue, list):
                            app.building.doorsLayers.append(currPageItems[i]['Material'])
                            app.building.doorsRValue.append(itemRValue)
                    elif app.screen == 'detailFloor':
                        if isinstance(app.building.floorsRValue, list):
                            app.building.floorsLayers.append(currPageItems[i]['Material'])
                            app.building.floorsRValue.append(itemRValue)
                    elif app.screen == 'detailRoof':
                        if isinstance(app.building.roofsRValue, list):
                            app.building.roofsLayers.append(currPageItems[i]['Material'])
                            app.building.roofsRValue.append(itemRValue)

    def handleHover(self):
        currPageItems = self.items[self.currStartIdx:self.currStartIdx+self.elementsPerPage]
        for i in range(len(currPageItems)):
            if (self.x <= app.hx <= self.x + self.buttonWidth and
                    self.y + i * self.buttonHeight <= app.hy <= self.y + (i + 1) * self.buttonHeight):
                self.isHovered[i] = True
            else:
                self.isHovered[i] = False
                
class TableCol:
    def __init__(self, items, x, y, width, height, rowWidth, rowHeight):
        self.items = items
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.rowWidth = rowWidth
        self.rowHeight = rowHeight

        self.currStartIdx = 0
        self.elementsPerPage = 8

    def draw(self):
        for i in range(len(self.items)):
            item = self.items[i]
            drawRect(self.x, self.y + i*self.rowHeight, self.rowWidth, self.rowHeight, fill=None, border=app.secondFill, borderWidth=1)
            drawLabel(item, self.x + self.rowWidth/2, self.y + i*self.rowHeight + self.rowHeight/2, fill=app.secondFill, size=app.textSize, font=app.font, align='center', bold = True)