import os 
import time
import requests
import pandas as pd

CacheDirectory = './cache'
os.makedirs(CacheDirectory, exist_ok=True)

def isCacheValid(symbol, cacheType = 'data'):
    cacheFile = os.path.join(CacheDirectory, f"{symbol}_{cacheType}.txt")
    if not os.path.exists(cacheFile):
        return False
    cacheAge = time.time() - os.path.getmtime(cacheFile)
    return cacheAge < 24 * 60 * 60  * 30 # Valid for 30 days

def loadFromCache(symbol, cacheType = 'data'):
    cacheFile = os.path.join(CacheDirectory, f"{symbol}_{cacheType}.txt")
    with open(cacheFile, "r") as f:
        return f.read()

def saveToCache(symbol, data, cacheType = 'data'):
    cacheFile = os.path.join(CacheDirectory, f"{symbol}_{cacheType}.txt")
    with open(cacheFile, "w") as f:
        f.write(data)

class Stock:
    def __init__(self, symbol):
        self.symbol = symbol
        self.api = f'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={self.symbol}&apikey=XSHJZ94EQQVGGCTM'
        self.overviewApi = f'https://www.alphavantage.co/query?function=OVERVIEW&symbol={self.symbol}&apikey=XSHJZ94EQQVGGCTM'
        self.priceData = self.getData()
        self.metrics = {}
        if self.priceData:
            self.df = pd.DataFrame.from_dict(self.priceData, orient = 'index')
            self.df.index = pd.to_datetime(self.df.index)
            self.df = self.df.astype(float)
            self.calculateMetrics()
            self.addOverviewStats()   

    def __repr__(self):
        return f'{self.df}'

    def calculateMetrics(self):
        self.calcAvgPrice()
        self.mostRecentPrice()
        self.calcVolatility()
        self.calculateGrowth()

    def calculateGrowth(self):
        dates = [(date - self.df.index[0]).days for date in self.df.index]
        prices = self.df['4. close'].values

    # Ensure enough data points
        if len(dates) < 2 or len(prices) < 2:
            self.metrics['Growth Rate'] = 0
            return

        meanX = sum(dates) / len(dates)
        meanY = sum(prices) / len(prices)

        numerator = sum((date - meanX) * (price - meanY) for date, price in zip(dates, prices))
        denominator = sum((date - meanX) ** 2 for date in dates)

        if denominator == 0:
            self.metrics['Growth Rate'] = 0
        else:
            growthRate = numerator / denominator
            self.metrics['Growth Rate'] = growthRate

   

    def calcAvgPrice(self):
        average = (self.df['1. open'].mean() + self.df['4. close'].mean() + self.df['2. high'].mean() / 3)
        self.metrics['Average Price'] = average

    def mostRecentPrice(self):
        self.metrics['Recent Price'] = self.df['4. close'].iloc[-1]      
    
    def calcVolatility(self):
        dailyReturns = self.df['4. close'].pct_change()
        volatility = dailyReturns.std()
        self.metrics['Volatility'] = volatility
        self.metrics['Standard Deviation'] = self.df['4. close'].std()
    
    def addOverviewStats(self):
        overviewData = self.getOverviewData()
        if overviewData:
            self.metrics['Sector'] = overviewData.get('Sector', 'N/A')
            self.metrics['Dividend Yield'] = overviewData.get('DividendYield', 'N/A')
    
    def getOverviewData(self):
        if isCacheValid(self.symbol, cacheType = 'overview'):
            rawData = loadFromCache(self.symbol, cacheType = 'overview')
            if rawData:
                try:
                    data = requests.Response()
                    data._content = rawData.encode('utf-8')
                    data.encoding = 'utf-8'
                    return data.json()
                except requests.exceptions.JSONDecodeError:
                    return
            else:
                response = requests.get(self.overviewApi)
                if repsonse.status_code == 200:
                    try:
                        data = response.json()
                        saveToCache(self.symbol, response.text, cacheType = 'overview')
                        return data
                    except requests.exceptions.JSONDecodeError:
                        return
                else:
                    return 
    
    def getData(self):
        if isCacheValid(self.symbol):
            rawData = loadFromCache(self.symbol)
            if rawData:  # Check if cached data is not None
                try:
                    data = requests.Response()  # Create a mock Response object
                    data._content = rawData.encode('utf-8')
                    data.encoding = 'utf-8'
                    return data.json().get('Time Series (Daily)', {})  #Get time series data
                except ValueError: #Catches if theres a JSON decoding error
                    print("Cached data is corrupted or invalid JSON.")
                    return {}
        else:
            response = requests.get(self.api)
            if response.status_code == 200:
                try:
                    data = response.json().get('Time Series (Daily)', {})
                    if data:
                        saveToCache(self.symbol, response.text)
                    return data
                except ValueError:
                    print("API response is invalid JSON.")
                    return {}
            else:
                print("API request failed.")
                return {}
#Use webscarping to get a list of stock tickers from the NYSE
def getTickers():
    url = "https://stockanalysis.com/list/nyse-stocks/"
    response = requests.get(url)
    tickers = []
    if response.status_code != 200:
        print(f"Failed to fetch the page, status code: {response.status_code}")
        return []
    html_content = response.text
    df_list = pd.read_html(html_content)  
    df = df_list[0] 
    df.columns = df.columns.str.strip()
    for symbol in df['Symbol']:
        tickers.append(symbol)
    return tickers 


