import sqlite3
import sys
from datetime import datetime

from DAO_Objects import Vaccines, Logistics, Clinics, Suppliers
from DTO_Objects import Logistic, Clinic, Supplier, Vaccine


class _Repository:
    def __init__(self):
        self.conn = sqlite3.connect("database.db")
        self.vaccines = Vaccines(self.conn)
        self.suppliers = Suppliers(self.conn)
        self.logistics = Logistics(self.conn)
        self.clinics = Clinics(self.conn)

    def _close(self):
        self.conn.commit()
        self.conn.close()

    def create_tables(self, config):
        vaccines_data, suppliers_data, clinics_data, logistics_data = self.init_config(config)
        cursor = self.conn.cursor()
        cursor.execute("""
            CREATE TABLE Logistics(id INTEGER PRIMARY KEY,name STRING NOT NULL, count_sent INTEGER NOT NULL, 
            count_received INTEGER NOT NULL);""")
        self.insert_logistics(logistics_data)
        cursor.execute("""
            CREATE TABLE Clinics(id INTEGER PRIMARY KEY, location STRING NOT NULL, demand INTEGER NOT NULL, 
            logistic REFERENCES Logistic(id));""")
        self.insert_clinics(clinics_data)
        cursor.execute("""
            CREATE TABLE Suppliers(id INTEGER PRIMARY KEY, name STRING NOT NULL, logistic REFERENCES 
            Logistic(id))""")
        self.insert_suppliers(suppliers_data)
        cursor.execute("""
            CREATE TABLE Vaccines(id INTEGER PRIMARY KEY, date DATE NOT NULL, supplier REFERENCES Suppliers(id), 
            quantity INTEGER NOT NULL)""")
        self.insert_vaccines(vaccines_data)

    def init_config(self, config):
        f = open(config, "r")
        text = f.readline()
        vaccines = text[0]
        suppliers = text[2]
        clinics = text[4]
        logistics = text[6]
        vaccines_data = list()
        suppliers_data = list()
        clinics_data = list()
        logistics_data = list()
        for i in range(int(vaccines)):
            vaccines_data.append(f.readline())
        for i in range(int(suppliers)):
            suppliers_data.append(f.readline())
        for i in range(int(clinics)):
            clinics_data.append(f.readline())
        for i in range(int(logistics)):
            logistics_data.append(f.readline())
        return vaccines_data, suppliers_data, clinics_data, logistics_data

    def insert_logistics(self, list_data):
        for i in range(len(list_data)):
            data = list_data[i].split(',')
            self.logistics.insert(Logistic(int(data[0]), data[1], int(data[2]), int(data[3])))

    def insert_clinics(self, list_data):
        for i in range(len(list_data)):
            data = list_data[i].split(',')
            self.clinics.insert(Clinic(int(data[0]), data[1], int(data[2]), int(data[3])))

    def insert_suppliers(self, suppliers_data):
        for i in range(len(suppliers_data)):
            data = suppliers_data[i].split(',')
            self.suppliers.insert(Supplier(int(data[0]), data[1], int(data[2])))

    def insert_vaccines(self, vaccines_data):
        for i in range(len(vaccines_data)):
            data = vaccines_data[i].split(',')
            self.vaccines.insert(Vaccine(int(data[0]), datetime.fromisoformat(data[1]), int(data[2]), int(data[3])))
