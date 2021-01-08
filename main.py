import sys
import sqlite3
from sqlite3 import Error
import init_tables

def create_connection(db_file):
    conn= None
    try:
        conn=sqlite3.connect(db_file)
    except Error as e:
        print (e)
  #  finally:
      #  if conn:
         #   conn.close()
    return conn

db_con=create_connection("database.db")
def init_config():
    config = sys.argv[1]
    f = open(config,"r")
    text=f.readline()
    vaccines=text[0]
    suppliers=text[2]
    clinics=text[4]
    logistics=text[6]
    vaccines_data=list()
    suppliers_data=list()
    clinics_data=list()
    logistics_data=list()
    for i in range(int(vaccines)):
        vaccines_data.append(f.readline())
    for i in range(int(suppliers)):
        suppliers_data.append(f.readline())
    for i in range(int(clinics)):
        clinics_data.append(f.readline())
    for i in range(int(logistics)):
        logistics_data.append(f.readline())
    return vaccines_data, suppliers_data, clinics_data,  logistics_data

vaccines_data, suppliers_data, clinics_data,  logistics_data = init_config()



with db_con:
    cursor=db_con.cursor()
    cursor.execute('CREATE TABLE Logistics(id INTEGER PRIMARY KEY,name STRING NOT NULL, count_sent INTEGER NOT NULL, count_received INTEGER NOT NULL)')
    init_tables.insert_logistics_clinics(cursor,logistics_data)
    cursor.execute('CREATE TABLE Clinics(id INTEGER PRIMARY KEY, location STRING NOT NULL, demand INTEGER NOT NULL, logistic INTEGER REFERENCES Logistic(id))')
    init_tables.insert_logistics_clinics(cursor,clinics_data)
    cursor.execute('CREATE TABLE Suppliers(id INTEGER PRIMARY KEY, name STRING NOT NULL, logistic INTEGER REFERENCES Logistic(id))')
    init_tables.insert_suppliers(cursor,suppliers_data)
    cursor.execute('CREATE TABLE Vaccines(id INTEGER PRIMARY KEY, date DATE NOT NULL, supplier INTEGER REFERENCES Supplier(id), quantity INTEGER NOT NULL)')
    init_tables.insert_vaccines(cursor,vaccines_data)
