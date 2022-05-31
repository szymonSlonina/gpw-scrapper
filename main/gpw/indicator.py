from gpw import ticker
import requests
from bs4 import BeautifulSoup
from db import db
from helper import url

def writeAllShareStatsToDb(BASE_DIR):
    tickers = ticker.getTicker(BASE_DIR)
    for tick in tickers:
        stats = getShareStats(tick)
        db.writeShareStats(stats, BASE_DIR)        
        break

def getShareStats(tick):
    stats = {}

    #getMarketStatsByName(stats, tick)
    #getProfitabilityStatsByName(stats, tick)
    #getRatingStatsByName(stats, tick)
    getDividendsStatsByName(stats, tick)
    print(stats)

def getMarketStatsByName(stats, tick):
    statNamesMarketIndicators = ["Quote", "ShareAmount", "WK",
        "P", "Z"]
    fullPath = url.MARKET_VALUE_INDICATOR_PREFIX + tick
    response = requests.get(fullPath)
    soup = BeautifulSoup(response.text, 'html.parser')
    quarters = soup.select("table.report-table > tr:first-child > th.h")
    quarters = list(map(lambda q : q.contents[0].strip(), quarters))
    
    for statName in statNamesMarketIndicators:
        stat = soup.select("table.report-table tr[data-field=\"" + statName + "\"] td.h > span.value")
        stat = list(map(lambda s : s.string, stat))
        stats[statName] = dict(zip(quarters, stat))

def getProfitabilityStatsByName(stats, tick):
    statNamesProfitability = ["ROE"]
    fullPath = url.PROFITABILITY_VALUE_INDICATOR_PREFIX + tick
    response = requests.get(fullPath)
    soup = BeautifulSoup(response.text, 'html.parser')
    quarters = soup.select("table.report-table > tr:first-child > th.h")
    quarters = list(map(lambda q : q.contents[0].strip(), quarters))
    
    for statName in statNamesProfitability:
        stat = soup.select("table.report-table tr[data-field=\"" + statName + "\"] td.h > span.value")
        stat = list(map(lambda s : s.string, stat))
        stats[statName] = dict(zip(quarters, stat))

def getRatingStatsByName(stats, tick):
    statNamesRating = ["Piotroski F-Score"]
    fullPath = url.RATING_INDICATOR_PREFIX + tick
    response = requests.get(fullPath)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    for statName in statNamesRating:
        stat = soup.select("table.rating-table tr:last-child td:last-child")
        stat = list(map(lambda s : s.string, stat[1]))
        stats[statName] = stat[0]

def getDividendsStatsByName(stats, tick):
    fullPath = url.DIVIDEND_HISTORY_RATING_VAR_URL.format(ticker = tick)
    response = requests.get(fullPath)
    soup = BeautifulSoup(response.text, 'html.parser')
    divRows = soup.select("table.instrument-dividends tr")
    divDict = {}
    for row in divRows[1:]:
        if "-" not in row.contents[2].string:
            divDict[row.contents[0].string.strip()] = row.contents[2].string.strip()
    
    stats["Dividend Yields"] = divDict

class Stats:
    def __init__(self, ticker, stats):
        self.ticker = ticker
        self.stats = stats
