import sqlite3

class Vaccines:
    def __init__(self, conn):
        self.conn=conn

    def insert(self, vaccine):
        self.conn.execute("""
        INSERT INTO Vaccines (id, date, supplier, quantity) VALUES(?, ?, ?, ?)
        """,[vaccine.id, vaccine.date, vaccine.supplier, vaccine.quantity])


class Suppliers:
    def __init__(self, conn):
        self.conn = conn

    def insert(self, supplier):
        self.conn.execute("""
        INSERT INTO Suppliers (id, name, logistic) VALUES(?, ?, ?)
        """,[supplier.id, supplier.name, supplier.logistic])


class Logistics:
    def __init__(self, conn):
        self.conn = conn

    def insert(self, logistic):
        self.conn.execute(""" 
        INSERT INTO Logistics (id, name, count_sent, count_received) VALUES(?, ?, ?, ?)
        """,[logistic.id, logistic.name, logistic.count_sent, logistic.count_received])

class Clinics:
    def __init__(self, conn):
        self.conn = conn

    def insert(self, clinic):
        self.conn.execute("""
        INSERT INTO Clinics (id, location, demand, supplier) VALUES(?, ?, ?, ?)
        """,[clinic.id, clinic.location, clinic.demand, clinic.logistic])