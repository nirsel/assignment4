import sqlite3
from datetime import datetime
import atexit
import sys
from DAO_Objects import _Vaccines, _Logistics, _Clinics, _Suppliers
from DTO_Objects import Logistic, Clinic, Supplier, Vaccine


# constructor to the repository
class Repository:
    def __init__(self):
        self.conn = sqlite3.connect("database.db")
        self.vaccines = _Vaccines(self.conn)
        self.suppliers = _Suppliers(self.conn)
        self.logistics = _Logistics(self.conn)
        self.clinics = _Clinics(self.conn)
        self.output = list()

    # method close - commits and closes the repository
    def close(self):
        self.conn.commit()
        self.conn.close()

    # method create_tables creates and insert initial values
    def create_tables(self, config):
        vaccines_data, suppliers_data, clinics_data, logistics_data = self.init_config(config)
        cursor = self.conn.cursor()
        # creates table Logistics
        cursor.execute("""
            CREATE TABLE Logistics(id INTEGER PRIMARY KEY,
            name STRING NOT NULL,
            count_sent INTEGER NOT NULL, 
            count_received INTEGER NOT NULL);""")
        # insert initial values
        self.insert_logistics(logistics_data)
        # creates table Clinics
        cursor.execute("""
            CREATE TABLE Clinics(id INTEGER PRIMARY KEY,
            location STRING NOT NULL, 
            demand INTEGER NOT NULL, 
            logistic INTEGER,
            FOREIGN KEY(logistic) REFERENCES Logistics(id));""")
        # insert initial values
        self.insert_clinics(clinics_data)
        # creates table Suppliers
        cursor.execute("""
            CREATE TABLE Suppliers(id INTEGER PRIMARY KEY, 
            name STRING NOT NULL,
            logistic INTEGER, 
            FOREIGN KEY (logistic) REFERENCES 
            Logistics(id))""")
        # insert initial values
        self.insert_suppliers(suppliers_data)
        # creates table Vaccines
        cursor.execute("""
            CREATE TABLE Vaccines(id INTEGER PRIMARY KEY, 
            date DATE NOT NULL,
            supplier INTEGER, 
            quantity INTEGER NOT NULL,
            FOREIGN KEY (supplier) REFERENCES Suppliers(id))""")
        # insert initial values
        self.insert_vaccines(vaccines_data)

    # method init_config opens the file and reads the txt
    def init_config(self, config):
        f = open(config, "r")
        text = f.readline()
        text = text.split(',')
        vaccines = text[0]
        suppliers = text[1]
        clinics = text[2]
        logistics = text[3]
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
        f.close()
        return vaccines_data, suppliers_data, clinics_data, logistics_data

    # method insert_logistics splits the data into an array
    def insert_logistics(self, list_data):
        for i in range(len(list_data)):
            data = list_data[i].split(',')
            self.logistics.insert(Logistic(int(data[0]), data[1], int(data[2]), int(data[3])))

    # method insert_clinics splits the data into an array
    def insert_clinics(self, list_data):
        for i in range(len(list_data)):
            data = list_data[i].split(',')
            self.clinics.insert(Clinic(int(data[0]), data[1], int(data[2]), int(data[3])))

    # method insert_suppliers splits the data into an array
    def insert_suppliers(self, suppliers_data):
        for i in range(len(suppliers_data)):
            data = suppliers_data[i].split(',')
            self.suppliers.insert(Supplier(int(data[0]), data[1], int(data[2])))

    # method insert_vaccines splits the data into an array
    def insert_vaccines(self, vaccines_data):
        for i in range(len(vaccines_data)):
            data = vaccines_data[i].split(',')
            self.vaccines.insert(Vaccine(int(data[0]), data[1], int(data[2]), int(data[3])))

    # method execute_orders divides the 2 types of orders (send and receive shipment)
    def execute_orders(self, orders_path, output_path):
        orders = open(orders_path, "r")
        text_list = orders.readlines()
        for line in text_list:
            line = line.split(',')
            if len(line) == 2:
                self.send_shipment(line)
            else:
                self.receive_shipment(line)
            self.update_output(output_path)
        f = open(output_path, "w")
        for line in self.output:
            f.write(line)
        f.close()

    # method send_shipment updates the demand, remove the amount shipped and updates the amount sent
    def send_shipment(self, order):
        amount = int(order[1])
        location = order[0]
        self.clinics.update_demand(location, amount)
        self.vaccines.remove_amount(amount)
        self.logistics.update_sent(location, amount)

    # method receive_shipment adds an order according to the name amount and date received
    def receive_shipment(self, order):
        name = order[0]
        amount = int(order[1])
        date = order[2]
        self.vaccines.add_order(name, amount, date)
        self.logistics.receive(name, amount)

    # method update_output fetches the relevant fields to return to the user
    def update_output(self, path):
        inventory = self.vaccines.inventory
        demand = self.clinics.demand
        receive = self.logistics.count_received
        sent = self.logistics.count_sent
        line = (str(inventory) + ',' + str(demand) + ',' + str(receive) + ',' + str(sent) + '\n')
        self.output.append(line)


repo = Repository()
atexit.register(repo.close)
