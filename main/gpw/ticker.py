import requests
from bs4 import BeautifulSoup
from helper import helper
from helper import url
from db import db

def getStockTicker():
    response = requests.get(url.GPW_STOCK_NAMES_URL)
    soup = BeautifulSoup(response.text, 'html.parser')

    companyNamesRecord = map(lambda aElement: aElement.text, soup.find_all("a", {"class" : "s_tt"}))
    companyShortToNameMap = map(helper.splitShortAndName, companyNamesRecord)

    return list(map(lambda pair : pair[0], companyShortToNameMap))

def getStockFullName():
    response = requests.get(url.GPW_STOCK_NAMES_URL)
    soup = BeautifulSoup(response.text, 'html.parser')

    companyNamesRecord = map(lambda aElement: aElement.text, soup.find_all("a", {"class" : "s_tt"}))
    companyShortToNameMap = map(helper.splitShortAndName, companyNamesRecord)

    return list(map(lambda pair : pair[1] if len(pair) > 1 else "", companyShortToNameMap))

def writeNamesToDb(BASE_DIR):
    response = requests.get(url.GPW_STOCK_NAMES_URL)
    soup = BeautifulSoup(response.text, 'html.parser')

    companyNamesRecord = map(lambda aElement: aElement.text, soup.find_all("a", {"class" : "s_tt"}))
    companyShortToNameList = list(map(helper.splitShortAndName, companyNamesRecord))

    db.writeAllToTable(db.STOCK, companyShortToNameList, BASE_DIR)

def getNames(BASE_DIR):
    result = db.getAllFromTable(BASE_DIR, db.STOCK)
    return list(map(lambda a : a[1], result))

def getTicker(BASE_DIR):
    result = db.getAllFromTable(BASE_DIR, db.STOCK)
    return list(map(lambda a : a[0], result))