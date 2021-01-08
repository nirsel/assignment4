import sqlite3

class Vaccines:
    def __init__(self, conn):
        self.conn=conn

    def insert(self, vaccine):
        self.conn.execute('INSERT into Vaccines VALUES(vaccine.id, vaccine.date, vaccine.supplier, vaccine.quantity)')


class Suppliers:
    def __init__(self, conn):
        self.conn = conn

    def insert(self, supplier):
        self.conn.execute('INSERT into Suppliers VALUES(supplier.id, supplier.name, supplier.logistic)')


class Logistics:
    def __init__(self, conn):
        self.conn = conn

    def insert(self, logistic):
        self.conn.execute('INSERT into Logistics VALUES(logistic.id, logistic.name, logistic.count_sent, logistic.count_received)')

class Clinics:
    def __init__(self, conn):
        self.conn = conn

    def insert(self, clinic):
        self.conn.execute('INSERT into Clinics VALUES(clinic.id, clinic.location, clinic.demand, clinic.logistic)')