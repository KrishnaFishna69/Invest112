import cacheAndStockClass as css
import pprint
#Scaffolding for eventual implementation of user requests
def takeUserRequests():
    riskLevel = int(input('type 1 for low risk, 2 for medium, 3 for high:'))
    growthLevel = int(input('type 1 for low growth, 2 for medium, 3 for high:'))
    incomeLevel = int(input('type 1 for low income, 2 for medium, 3 for high:'))
    diversityLevel = int(input('type 1 for low diversification, 2 for medium, 3 for high:'))
    equity = int('enter how much money youre putting in:')
    sectors = ['TECHNOLOGY']
    return riskLevel, growthLevel, incomeLevel, diversityLevel, equity, sectors

def buildPortfolio(tickers, riskLevel, growthLevel, incomeLevel, diversityLevel, sectors, equity):
    sizes = {1:5, 2:10, 3:15}
    targetSize = sizes.get(diversityLevel, 5)
    portfolio = {}

    def getScore(stock, riskLevel, growthLevel, incomeLevel, sectors):
        score = 0
        if stock.metrics['Volatility'] is not None:
            volatility = stock.metrics['Volatility']
            if riskLevel == 1:  # Low risk
                score += max(0, 1 - volatility / 0.01)  # Closer to 0.01 gets higher score
            elif riskLevel == 2:  # Medium risk
                score += max(0, 1 - abs(volatility - 0.02) / 0.02)  # Centered around 0.02
            elif riskLevel == 3:  # High risk
                score += max(0, volatility / 0.03)  # Higher volatility is better

        # Adaptive scoring for growth rate
        if stock.metrics.get('Growth Rate') is not None:
            growth_rate = stock.metrics['Growth Rate']
            if growthLevel == 1:  # Low growth
                score += max(0, 1 - growth_rate / 0.01)
            elif growthLevel == 2:  # Medium growth
                score += max(0, 1 - abs(growth_rate - 0.03) / 0.03)
            elif growthLevel == 3:  # High growth
                score += max(0, growth_rate / 0.05)

    # Adaptive scoring for dividend yield (income preference)
        if stock.metrics.get('Dividend Yield') is not None:
            dividend_yield = stock.metrics['Dividend Yield']
            if incomeLevel == 1:  # Low income
                score += max(0, 1 - dividend_yield / 0.02)
            elif incomeLevel == 2:  # Medium income
                score += max(0, 1 - abs(dividend_yield - 0.05) / 0.05)
            elif incomeLevel == 3:  # High income
                score += max(0, dividend_yield / 0.07)

    # Sector preference
        if stock.metrics.get('Sector') in sectors:
            score += 1  # Add a fixed score for matching sectors

        return score
        
    def buildHelper(index, currPortfolio, riskLevel, growthLevel, incomeLevel, sectors):
        if len(currPortfolio) == targetSize:
            return currPortfolio
        if index >= len(tickers):
            return currPortfolio
        else:
            stock = css.Stock(tickers[index])
            score = getScore(stock, riskLevel, growthLevel, incomeLevel, sectors)
            if score > 0:
                currPortfolio[stock.symbol] = score
            return buildHelper(index + 1, currPortfolio,riskLevel, growthLevel, incomeLevel, sectors)
        
    portfolio = buildHelper(0, {}, riskLevel, growthLevel, incomeLevel, sectors)
    if not portfolio:
        return {}
        
    totalScore = sum(portfolio.values())
    allocatedPortfolio = {}
    for symbol, score in portfolio.items():
        stock = css.Stock(symbol)
        stockEquity = (score / totalScore) * equity
        price = stock.metrics.get('Recent Price', 0) 
        if price > 0:
            numShares = int(stockEquity // price)
            allocatedPortfolio[symbol] = {
            'allocated equity': float(stockEquity),
            'price per share': float(price),
            'number of shares': int(numShares),
            'score': float(score)}   
    return allocatedPortfolio

tickers = css.getTickers()
port = buildPortfolio(tickers, 1, 1, 1, 1, ['TECHNOLOGY'], 10_000)
pprint.pprint(port)














