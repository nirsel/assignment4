import sqlite3

from DTO_Objects import Vaccine


class _Vaccines:
    def __init__(self, conn):
        self.conn = conn
        self.inventory=0
        self.last_id=0

    def insert(self, vaccine):
        self.conn.execute("""
        INSERT INTO Vaccines (id, date, supplier, quantity) VALUES(?, ?, ?, ?)
        """, [vaccine.id, vaccine.date, vaccine.supplier, vaccine.quantity])
        self.inventory=self.inventory+vaccine.quantity
        self.last_id=vaccine.id

    def remove_amount(self, amount):
        self.inventory = self.inventory - amount
        while amount>0:
            cursor=self.conn.cursor()
            cursor.execute("""
            SELECT id, quantity
            FROM Vaccines""")
            (id, quantity) = cursor.fetchone()
            if quantity<=amount:
                amount=amount-quantity
                self.delete_entry(id)
            else:
                cursor.execute("""
                UPDATE Vaccines
                SET quantity=(?)
                WHERE id=(?)""", [quantity-amount, id])
                amount=0

    def delete_entry(self, id):
        cursor=self.conn.cursor()
        cursor.execute("""
        DELETE FROM Vaccines
        WHERE id=(?)""", [id])

    def add_order(self, name, amount, date):
        cursor=self.conn.cursor()
        cursor.execute("""
        SELECT id
        FROM Suppliers
        WHERE name=(?)""", [name])
        supplier_id=cursor.fetchone()[0]
        self.insert(Vaccine(self.last_id+1, date, supplier_id, amount))



class _Suppliers:
    def __init__(self, conn):
        self.conn = conn

    def insert(self, supplier):
        self.conn.execute("""
        INSERT INTO Suppliers (id, name, logistic) VALUES(?, ?, ?)
        """, [supplier.id, supplier.name, supplier.logistic])


class _Logistics:
    def __init__(self, conn):
        self.conn = conn
        self.count_sent=0
        self.count_received=0

    def insert(self, logistic):
        self.conn.execute(""" 
        INSERT INTO Logistics (id, name, count_sent, count_received) VALUES(?, ?, ?, ?)
        """, [logistic.id, logistic.name, logistic.count_sent, logistic.count_received])

    def update_sent(self, location, amount):
        cursor=self.conn.cursor()
        cursor.execute("""
        SELECT logistic
        FROM Clinics
        WHERE location=(?)""", [location])
        logistic = cursor.fetchone()[0]
        cursor.execute("""
        SELECT count_sent
        FROM Logistics
        WHERE id=(?)""", [logistic])
        count=cursor.fetchone()[0]
        cursor.execute("""
        UPDATE Logistics
        SET count_sent=(?)
        WHERE id = (?)""", [count+amount, logistic])
        self.count_sent=self.count_sent+amount

    def receive(self, name, amount):
        cursor=self.conn.cursor()
        cursor.execute("""
        SELECT logistic
        FROM Suppliers
        WHERE name=(?)""", [name])
        logistic=cursor.fetchone()[0]
        cursor.execute("""
                SELECT count_received
                FROM Logistics
                WHERE id=(?)""", [logistic])
        count = cursor.fetchone()[0]
        cursor.execute("""
        UPDATE Logistics
        SET count_received=(?)
        WHERE id=(?)""", [count+amount, logistic])
        self.count_received=self.count_received+amount


class _Clinics:
    def __init__(self, conn):
        self.conn = conn
        self.demand=0

    def insert(self, clinic):
        self.conn.execute("""
        INSERT INTO Clinics (id, location, demand, logistic) VALUES(?, ?, ?, ?)
        """, [clinic.id, clinic.location, clinic.demand, clinic.logistic])
        self.demand = self.demand+clinic.demand

    def update_demand(self, location, amount):
        cursor=self.conn.cursor()
        cursor.execute("""
        SELECT demand
        FROM Clinics
        WHERE location=(?)""",[location])
        curr_demand = cursor.fetchone()[0]
        self.conn.execute("""
        UPDATE Clinics
        SET demand=(?)
        WHERE location=(?)""",[curr_demand-amount, location])
        self.demand=self.demand-amount