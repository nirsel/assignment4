import sys
import sqlite3
from sqlite3 import Error

import repository
rep=repository.Repository()
rep.create_tables(sys.argv[1])


