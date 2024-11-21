# unit conversion, area calculation, data validation/formatting, buttons etc.
from cmu_graphics import *
from screens import *

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
                    self.buttonHeight , border = 'white', fill = 'white', opacity = 40)
            drawLabel(self.text[i], (i+0.5)*self.buttonStep, self.top + self.buttonHeight/2,
                        font = 'monospace', fill='white', bold = True, size = 16)

class Gallery:
    def __init__(self):
        pass
    
    def draw(self):
        # rect
        # image
        # self.name below
        pass

class Project:
    def __init__(self,name,lenght,width):
        self.name = name
        self.length = lenght
        self.width = width
    
    def addWindow(self):
        pass
    
    def addDoor(self):
        pass

    def toggleView(self):
        pass
    