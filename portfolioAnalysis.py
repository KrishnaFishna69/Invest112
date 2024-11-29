import cacheAndStockClass as css
import portfolioBuilder as pb
import pandas as pd

class Portfolio:

    def __init__(self, allocatedPortfolio):
        self.allocatedPortfolio = allocatedPortfolio
        self.stockData = {}
        self.totalValue = 0
        self.totalDividendYield = 0
        self.totalVolatility = 0
        self.totalGrowth = 0
        self.stockCount = len(allocatedPortfolio)
        self.sectors = []
        self.aggregateMetrics()
        self.weightedDF = self.getWeightedDF()

    def aggregateMetrics(self):
        for symbol, data in self.allocatedPortfolio.items():
            stock = css.Stock(symbol)
            dividendYield = stock.metrics.get('Dividend Yield', 0)
            volatility = stock.metrics.get('Volatility', 0)
            growthRate = stock.metrics.get('Growth Rate', 0)
            sector = stock.metrics['Sector']
            print(stock.symbol)
            print(growthRate)
            
            self.stockData[symbol] = {
                'price_per_share': data['price per share'],
                'num_shares': data['number of shares'],
                'allocated_equity': data['allocated equity'],
                'dividend_yield': dividendYield,
                'volatility': volatility,
                'growth_rate': growthRate}
            

            self.totalValue += data['allocated equity']
            self.totalDividendYield += dividendYield * data['allocated equity']
            self.totalVolatility += volatility * data['allocated equity']
            self.totalGrowth += growthRate * data['allocated equity']
            self.sectors.append(sector)

    def getTotalValue(self):
        return self.totalValue

    def getAverageDividendYield(self):
        return self.totalDividendYield / self.totalValue
    
    def getAverageVolatility(self):
        return self.totalVolatility / self.totalValue
    
    def getAverageGrowth(self):
        return self.totalGrowth / self.totalValue
    
    def getWeightedDF(self):
        portfolioDF = pd.DataFrame()
        for symbol, data in self.allocatedPortfolio.items():
            stock = css.Stock(symbol)
            stockDF = stock.df[['4. close']]
            stockDF = stockDF.rename(columns={'4. close': 'price'})
            stockWeight = data['allocated equity'] / self.totalValue
            print(stockWeight)
            stockDF['weighted price'] = stockDF['price'] * stockWeight
            if portfolioDF.empty:
                portfolioDF = stockDF[['weighted price']]
            else:
                stockDF = stockDF.rename(columns= {'weighted price': f'weighted price {symbol}'})
                portfolioDF = (portfolioDF.merge(stockDF[[f'weighted price {symbol}']], left_index = True, 
                right_index = True, how = 'outer'))

        portfolioDF['portfolio weighted price'] = portfolioDF.sum(axis =1)
        return portfolioDF

    def __repr__(self):
        return (f"Portfolio Value: {self.getTotalValue():.2f}\n"
                f"Average Dividend Yield: {self.getAverageDividendYield():.4f}\n"
                f"Average Volatility: {self.getAverageVolatility():.4f}\n"
                f"Average Growth Rate: {self.getAverageGrowth():.4f}"
                f'{self.totalDividendYield}')

tickers = css.getTickers()
port = pb.buildPortfolio(tickers, 1, 1, 1, 1, ['TECHNOLOGY'], 10_000)
AP = Portfolio(port)
print(AP)
print(AP.weightedDF)


