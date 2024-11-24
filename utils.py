# unit conversion, area calculation, data validation/formatting, buttons etc.
from cmu_graphics import *

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
                    self.buttonHeight , border = 'white', borderWidth=1, fill = 'white', opacity = 40)
            drawLabel(self.text[i], (i+0.5)*self.buttonStep, self.top + self.buttonHeight/2,
                        font = 'monospace', fill='white', bold = True, size = 16)
            
    def mouseOver(self, mouseX, mouseY):
        for i in range(self.buttonNum):
            if mouseX > i*self.buttonStep and mouseX < (i+1)*self.buttonStep:
                if mouseY > self.top and mouseY < self.top + self.buttonHeight:
                    return True
        return False
        

class Icon:
    def __init__(self, r, origin, name = None, lineColor='black', lineWidth=2):
        self.r = r
        self.origin = origin
        self.name = name
        self.lineColor = lineColor
        self.lineWidth = lineWidth
    
    def draw(self, app, lineColor, fillColor):
        cx, cy = self.origin
        r = self.r
        if self.name == 'Forward Arrow':
            drawLabel(cx,cy-r, text='→', fill=lineColor, 
                                        font=Button.font)
            drawLabel(cx,cy+r, text='F', fill=lineColor, 
                                        font=Button.font)
        elif self.name == 'Backward Arrow':
            drawLabel(cx,cy-r, text='←', fill=lineColor, 
                                        font=Button.font)
            drawLabel(cx,cy+r, text='B', fill=lineColor, 
                                        font=Button.font)
        
        elif self.name == 'Help':
            drawLabel(cx,cy, text='?', fill=lineColor, 
                                        font=Button.font)
        

class Gallery:
    def __init__(self):
        pass
    
    def draw(self):
        # rect
        # image
        # self.name below
        pass

    def save(self):
        app.buildingGallery.append(app.building)
        app.building = None

class Project:
    def __init__(self,name,length,width):
        self.name = name
        self.length = length
        self.width = width
    
    def addWindow(self):
        pass
    
    def addDoor(self):
        pass

    def toggleView(self):
        pass
    
def isValidDimension(app, dimension):
    if not dimension.isdigit() or dimension == None or int(dimension) < 100 or int(dimension) > 600:
        app.showMessage('Invalid dimension. Please enter a value between 100-600.')
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

