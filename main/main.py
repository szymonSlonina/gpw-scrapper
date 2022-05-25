from gpw import ticker
from db import db
import os

#set root directory
BASE_DIR = os.getcwd()

db.setupDB(BASE_DIR)

ticker.writeNamesToDb(BASE_DIR)

