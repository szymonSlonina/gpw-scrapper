from gpw import ticker, indicator
from db import db
import os

#set root directory
BASE_DIR = os.getcwd()

db.setupDB(BASE_DIR)

#ticker.writeNamesToDb(BASE_DIR) #this is for writing names/tickers to db. start only once.
tickers = ticker.getNames(BASE_DIR)

indicator.writeAllShareStatsToDb(BASE_DIR)