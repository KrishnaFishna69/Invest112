import cacheAndStockClass as css
import portfolioBuilder as pb
import portfolioAnalysis as pa
import math
from cmu_graphics import *

def onAppStart(app):
    app.width, app.height = 1200, 700
    app.onInputScreen = False
    app.onBarScreen = False
    app.onPieScreen = False
    app.onLineScreen = False
    app.onStatsScreen = False
    app.showReset = False
    app.showGraphOptions = False
    app.pageOptions = ['Bar Chart', 'Pie Chart', 'Line Chart', 'Stats', 'Reset']

def redrawAll(app):
    #side Panel drawing
    sidePanelWidth = 300
    drawRect(0, 0, sidePanelWidth, app.height, fill = 'lightSteelBlue')

    #header drawing
    headerHeight = 100
    headCenterX, headCenterY = app.width // 2, headerHeight // 2
    drawRect(0, 0, app.width, headerHeight, fill = 'midnightBlue')
    drawLabel('Invest 112', headCenterX, headCenterY, size = 64, fill = 'white', bold = True)

    if app.onInputScreen == True:
        drawInputScreen(app)
    else:
        drawOptionBoxes(app)
        if app.onBarScreen:
            drawBarScreen(app)
        if app.onLineScreen:
            drawLineScreen(app)
        if app.onPieScreen:
            drawPieScreen(app)
        if app.onStatsScreen:
            drawStatsScreen(app):
        if app.showReset:
            showReset(app)
        
        
           
def drawOptionBoxes(app):
    subheadHeight = 50
    subheadY = 100
    drawRect(0, subheadY, app.width, subheadHeight, fill = 'lavender')

    optionBoxSize = 25
    boxSpacing = 100
    numOptions = len(app.pageOptions)

    totalContentWidth = (numOptions * optionBoxSize) + ((numOptions - 1 ) * boxSpacing)
    startX = (app.width - totalContentWidth) // 2

    boxYCenter = subheadY + subheadHeight // 2
    for i, option in enumerate(app.pageOptions):
        boxX = startX + i * (optionBoxSize + boxSpacing)
        color = determineBoxColor(app, option)
        drawRect(boxX, (boxYCenter - optionBoxSize // 2), optionBoxSize, optionBoxSize,
                fill = color , border = 'black')
        labelX = boxX + optionBoxSize + 15
        drawLabel(option, labelX, boxYCenter, align = 'left', bold = True)

def determineBoxColor(app, option):
    if option == 'Bar Chart' and app.onBarScreen:
        return 'blue'
    elif option == 'Pie Chart' and app.onPieScreen:
        return 'blue'
    elif option == 'Line Chart' and app.onLineScreen:
        return 'blue'
    elif option == 'Stats' and app.onStatsScreen:
        return 'blue'
    elif option == 'Reset' and app.showReset:
        return 'blue'
    else:
        return 'white'
    

def drawInputScreen(app):
    pass

def drawBarScreen(app):
    pass

def drawLineScreen(app):
    pass

def drawPieScreen(app):
    pass
    
def drawStatsScreen(app):
    pass
       
def showReset(app):
    pass
    
def onMousePress(app, mouseX, mouseY):
    #same parameters as before for the optoin boxes
    subheadHeight = 50
    subheadY = 100
    optionBoxSize = 25
    boxSpacing = 100
    numOptions = len(app.pageOptions)

    totalContentWidth = (numOptions * optionBoxSize) + ((numOptions - 1) * boxSpacing)
    startX = (app.width - totalContentWidth) // 2
    boxYCenter = subheadY + subheadHeight // 2

    for i, option in enumerate(app.pageOptions):
        boxX = startX + i * (optionBoxSize + boxSpacing)
        boxY = boxYCenter - optionBoxSize // 2

        # If mouse is within the box
        if boxX <= mouseX <= boxX + optionBoxSize and boxY <= mouseY <= boxY + optionBoxSize:
            app.onBarScreen = False
            app.onPieScreen = False
            app.onLineScreen = False
            app.onStatsScreen = False
            app.showReset = False

            if option == 'Bar Chart':
                app.onBarScreen = True
            elif option == 'Pie Chart':
                app.onPieScreen = True
            elif option == 'Line Chart':
                app.onLineScreen = True
            elif option == 'Stats':
                app.onStatsScreen = True
            elif option == 'Reset':
                app.showReset = True



def main():
    runApp()

main()


