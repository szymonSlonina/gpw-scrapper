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
    statNamesMarketIndicators = ["Quote", "ShareAmount", "WK",
        "P", "Z"]
    statNamesProfitability = ["ROE"]
    statNamesRating = ["Piotroski F-Score"]
    fullPath = url.MARKET_VALUE_INDICATOR_PREFIX + tick
    response = requests.get(fullPath)
    
    soup = BeautifulSoup(response.text, 'html.parser')
    stats = getStatsByName(soup, statNamesMarketIndicators)

def getStatsByName(soup, statNames):
    quarters = soup.select("table.report-table > tr:first-child > th.h")
    quarters = list(map(lambda q : q.contents[0].strip(), quarters))
    
    stats = {}
    for statName in statNames:
        stat = soup.select("table.report-table tr[data-field=\"" + statName + "\"] td.h > span.value")
        stat = list(map(lambda s : s.string, stat))
        stats[statName] = dict(zip(quarters, stat))
        print(statName, len(stat))
        print(stat)
        print("\n")


class Stats:
    def __init__(self, ticker, stats):
        self.ticker = ticker
        self.stats = stats
