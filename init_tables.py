import sqlite3
from datetime import datetime

def insert_logistics_clinics(cursor, list_data):
    for i in range(len(list_data)):
        data=list_data[i].split(',')
        cursor.execute('INSERT into Logistics VALUES(int(data[0]),data[1],int(data[2]),int(data[3]))')

def insert_suppliers(cursor, suppliers_data):
    for i in range(len(suppliers_data)):
        data=suppliers_data[i].split(',')
        cursor.execute('INSERT into Logistics VALUES(int(data[0]),data[1],int(data[2]))')

def insert_vaccines(cursor, vaccines_data):
    for i in range(len(vaccines_data)):
        data=vaccines_data[i].split(',')
        cursor.execute('INSERT into Logistics VALUES(int(data[0]),datetime.fromisoformat(data[1]),int(data[2]),int(data[3]))')