from cmu_graphics import *


def drawIntroScreen(app, canvas):
    canvas.create_text(app.width/2, 50, text='ISOMETRISM', font='Courier 20')

    for button in app.hScreenButtons:
        button.draw(app,canvas,button.fillColor, button.lineColor)

    #keyboard shortcuts 
    f = 'Courier 15 bold'
    w = app.width/5
    canvas.create_text(w,250, text='r', font=f)
    canvas.create_text(w,300, text='t', font=f)
    canvas.create_text(w,350, text='v', font=f)
    canvas.create_text(w,400, text='c', font=f)
    canvas.create_text(w,450, text='f g', font=f)
    canvas.create_text(w,500, text='h', font=f)

    #button functionality
    f2 = 'Courier 12'
    w2 = app.width/4
    canvas.create_text(w2, 100, font=f2, anchor=W,
        text='start a room. click 3x to set floor & walls.')
    canvas.create_text(w2, 140, font=f2, anchor=W,
        text='drag & drop furniture into your room.')
    canvas.create_text(w2,160, font=f2, anchor=W,
        text='click inside furniture to rotate furniture.')
    canvas.create_text(w2,200, font=f2, anchor=W,
        text='clear room and all furniture.')
    canvas.create_text(w2,250, font=f2, anchor=W,
        text='toggle clockwise room rotation.')
    canvas.create_text(w2,300, font=f2, anchor=W,
        text='toggle counterclockwise room rotation.')
    canvas.create_text(w2,350, font=f2, anchor=W,
        text='toggle between edit mode and perspective viewing mode.')
    canvas.create_text(w2,390, font=f2, anchor=W,
        text='toggle camera visibility in edit and view mode.')
    canvas.create_text(w2,410, font=f2, anchor=W,
        text='wasdxz keys move camera in edit and view mode.')
    canvas.create_text(w2,450, font=f2, anchor=W,
        text='rotate camera view window in edit and view mode.')
    canvas.create_text(w2,500, font=f2, anchor=W,
        text='toggle help screen.')

    app.helpButton.draw(app, canvas, app.helpButton.fillColor, 
                                    app.helpButton.lineColor)

def drawTitleScreen(app, canvas):
    #rotating room and furniture
    for obj in app.titleObjs:
        obj.draw(app,canvas,'black')

    ox,oy = app.titleButton.origin
    canvas.create_text(ox,oy, text=app.titleText, font='Courier 80', 
                                                    fill=app.textColor)

    ox,oy = app.subtitleButton.origin
    canvas.create_text(ox,oy, text=app.subtitleText, font='Courier 30', 
                                                    fill=app.textColor)

def drawViewScreen(app, canvas): 
    if app.showCamera: #pink tinted view window
        canvas.create_rectangle(0,0,app.width, app.height, fill='pink')
    
    if isinstance(app.CORW, Cube):
        for furniture in app.furniture:
            furniture.drawImageCoords(app, canvas, color='black')

        for cube in [app.COFloor, app.CORW, app.COLW]:
            cube.drawImageCoords(app, canvas, color='black')

    for button in app.viewButtons:
        button.draw(app, canvas, button.fillColor, button.lineColor)

def drawEditScreen(app, canvas):
    if app.showCamera:
        #image face (view window)
        x0,y0 = app.cameraImageCoords[0]
        x1,y1 = app.cameraImageCoords[1]
        x2,y2 = app.cameraImageCoords[2]
        x3,y3 = app.cameraImageCoords[3]
        canvas.create_polygon(x0,y0,x1,y1,x2,y2,x3,y3, fill='pink')

        camCoord = vecs2Graph(app, [app.cameraOrigin])[0]
        x,y = camCoord
        r = 3
        canvas.create_oval(x-r, y-r, x+r, y+r, fill = 'red', width=0)

    ox, oy = app.origin

    #draw walls (static, set by mousePressed)
    if (app.drawCubeFloor and app.cubeFloorVecs.shape[0]==8 
                           and isinstance(app.CORW, Cube)):
        app.CORW.draw(app, canvas, 'black')
        app.COLW.draw(app, canvas, 'black')

    #draw walls (moving, set by mouseMoved)
    elif (app.drawCubeFloor and app.cubeFloorVecs.shape[0]==8 
    and app.cubeWallHeight==None and isinstance(app.tempCORW, Cube)):
        app.tempCORW.draw(app, canvas, 'red')
        app.tempCOLW.draw(app, canvas, 'red')

    #draw floor (static, set by mousePressed)
    if app.drawCubeFloor and app.cubeFloorVecs.shape[0]==8:
        app.COFloor.draw(app, canvas, 'black')

    #cube floor (moving, set by mouseMoved)
    if (app.drawCubeFloor and app.cubeFloorVecs.shape[0]==2 
    and isinstance(app.tempCOFloor, Cube)):
        app.tempCOFloor.draw(app, canvas, 'red')

    #draw furniture
    if app.newFurniture!=None:
        app.newFurniture.draw(app, canvas, 'red')
    for furniture in app.furniture:
        furniture.draw(app, canvas, 'black')

    #buttons
    for button in app.editButtons+[app.helpButton]:
        button.draw(app, canvas, button.fillColor, button.lineColor)