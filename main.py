import sys
import sqlite3
from sqlite3 import Error
from repository import repo

repo.create_tables(sys.argv[1])


