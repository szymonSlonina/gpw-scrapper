import os
import sqlite3


STOCK = "STOCK"
STOCK_INDICATORS = "STOCK_INDICATORS"


def setupDB(BASE_DIR):
    dbExists = False
    if os.path.exists(os.sep.join([BASE_DIR, "db", "example.db"])):
        dbExists = True
    con = sqlite3.connect(os.sep.join([BASE_DIR, "db", "example.db"]))
    if not dbExists:
        setup()
    con.close()


def setup():
    con.execute('''CREATE TABLE stock (
                    ticker TEXT NOT NULL,
                    name TEXT,
                    newest_data_string TEXT
                    )
                    ''')

    con.execute('''CREATE TABLE stock_indicators (
                    ticker TEXT NOT NULL,
                    data_string TEXT,
                    year INTEGER,
                    quarter TEXT,
                    share_price REAL,
                    share_count INTEGER,
                    bv_per_share REAL,
                    sales_per_share REAL,
                    eps REAL,
                    pbv REAL,
                    cape REAL,
                    roe REAL,
                    fscore INTEGER
                    )                
                    ''')  


def writeAllToTable(dbName, tickerNameList, BASE_DIR):
    con = sqlite3.connect(os.sep.join([BASE_DIR, "db", "example.db"]))
    con.executemany("insert into " + dbName + " values (?, ?, '')", tickerNameList)
    con.close()
    print(dbName)
    print(tickerNameList)