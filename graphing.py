import cacheAndStockClass as css
import portfolioBuilder as pb
import portfolioAnalysis as pa
import math
from cmu_graphics import *

def onAppStart(app):
    app.background = 'white'

def drawLineGraph(app, portfolio):
    data = portfolio.weightedDF['portfolio weighted price']
    
    if len(data) == 0:
        drawLabel("No data to display", 200, 200, size=20)  
        return
    
    graphX, graphY = 50, 50
    width, height = 400, 300
    maxPrice = max(data)
    minPrice = min(data)
    
    drawLine(graphX, graphY + height, graphX + width, graphY + height)  # X-axis
    drawLine(graphX, graphY, graphX, graphY + height)  # Y-axis
    
    # Plot Y-axis labels
    numYLabels = 5  
    for i in range(numYLabels + 1):
        yLabel = minPrice + i * (maxPrice - minPrice) / numYLabels
        yPos = graphY + height - (yLabel - minPrice) / (maxPrice - minPrice) * height
        drawLabel(f'{yLabel:.2f}', graphX - 25, yPos, size=10)  

    # Plot X-axis labels
    numXLabels = 5  
    for i in range(numXLabels + 1):
        xLabel = i * (len(data) - 1) / numXLabels
        xPos = graphX + xLabel * width / (len(data) - 1)
        drawLabel(f'{int(xLabel)}', xPos, graphY + height + 15, size=10)  
    
    # Plot points and lines
    prevX = graphX
    prevY = graphY + height - (data.iloc[0] - minPrice) / (maxPrice - minPrice) * height
    
    for i in range(1, len(data)):
        x = graphX + (i / len(data)) * width
        y = graphY + height - (data.iloc[i] - minPrice) / (maxPrice - minPrice) * height
        
        # Convert values to float to prevent error since weird float.64 thing
        drawLine(float(prevX), float(prevY), float(x), float(y))
        prevX, prevY = x, y

def drawPieChart(app, sectors):
    if not sectors:
        drawLabel('no sectors', 200, 200)
        return
    else:
        sectorCounts = {}
        for sector in sectors:
            if sector in sectorCounts:
                sectorCounts[sector] +=1
            else:
                sectorCounts[sector] =1
        totalSectors = sum(sectorCounts.values())
        centerX, centerY = 200, 200
        radius = 100
        startAngle = 0
        colors = ['red', 'blue', 'green', 'yellow', 'purple', 
        'orange', 'cyan', 'pink', 'brown', 'turqoise', 'olive']
        for i, (sector, count) in enumerate(sectorCounts.items()):
            sliceAngle = 360 * (count / totalSectors)
            color = colors[i % len(colors)]
            endAngle = startAngle + sliceAngle
            for angle in range(int(startAngle), int(endAngle)):
                rad = math.radians(angle)
                x = centerX + radius * math.cos(rad)
                y = centerY - radius * math.sin(rad)
            
                drawPolygon(centerX, centerY, x, y, 
                        centerX + radius * math.cos(math.radians(angle + 1)), 
                        centerY - radius * math.sin(math.radians(angle + 1)), 
                        fill=color)
        
            midAngle = startAngle + sliceAngle / 2
            labelX = centerX + radius * 0.5 * math.cos(math.radians(midAngle))
            labelY = centerY - radius * 0.5 * math.sin(math.radians(midAngle))
            drawLabel(sector, labelX, labelY, size=10, fill="black")
        
            startAngle = endAngle

def drawBarChart(app, portfolio):
    stockData = portfolio.stockData
    if not stockData:
        drawLabel('no data', 200, 200)
        return
    stockNames = list(stockData.keys())
    numShares = [data['num_shares'] for data in stockData.values()]
    graphX, graphY = 50,50
    width, height = 400, 300
    barWidth = width / len(stockNames)
    maxShares = max(numShares)

    #draw axises
    drawLine(graphX, graphY + height, graphX + width, graphY + height)
    drawLine(graphX, graphY, graphX, graphY + height)

    colors = ['red', 'blue', 'green', 'yellow', 'purple', 
        'orange', 'cyan', 'pink', 'brown', 'turqoise', 'olive']
    for i, shares in enumerate(numShares):
        barHeight = (shares / maxShares) * height
        x = graphX + i * barWidth
        y = graphY + height - barHeight
        drawRect(x, y, barWidth * .8, barHeight, fill = colors[i % len(colors)])
        drawLabel(stockNames[i],  x + barWidth * .4, graphY + height + 15, size = 10, align = 'center' )
    
    numYLabels = 5
    for i in range(numYLabels+1):
        labelShares = int(maxShares * i / numYLabels)
        yPos = graphY + height - (labelShares / maxShares) * height
        drawLabel(f'{labelShares}', graphX - 10, yPos, size = 10, align = 'right')


def redrawAll(app):
    tickers = css.getTickers()
    port = pb.buildPortfolio(tickers, 1, 1, 1, 1, ['TECHNOLOGY'], 10_000)
    AP = pa.Portfolio(port)
    sectors = ['Tech', 'Finance', 'Healthcare', 'Energy','Tech', 'Tech', 'Energy']
    
    #drawPieChart(sectors)
    #drawLineGraph(AP)
    
    #drawBarChart(AP)

def main():
    runApp()

main()
