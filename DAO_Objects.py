import sqlite3

from DTO_Objects import Vaccine


# class _Vaccines represents the table vaccines
class _Vaccines:
    def __init__(self, conn):
        self.conn = conn
        self.inventory = 0
        self.last_id = 0

    #  method insert to insert a new row to the table with the relevant info: id, date, supplier, quantity
    def insert(self, vaccine):
        self.conn.execute("""
        INSERT INTO Vaccines (id, date, supplier, quantity) VALUES(?, ?, ?, ?)
        """, [vaccine.id, vaccine.date, vaccine.supplier, vaccine.quantity])
        self.inventory = self.inventory + vaccine.quantity
        self.last_id = vaccine.id

    # method remove_amount removes the amount from the inventory, while making sure older vaccines will be shipped
    # prior to newer ones
    def remove_amount(self, amount):
        self.inventory = self.inventory - amount
        while amount > 0:
            cursor = self.conn.cursor()
            cursor.execute("""
            SELECT id, quantity
            FROM Vaccines""")
            (id, quantity) = cursor.fetchone()  # fetch only the first row
            if quantity <= amount:
                amount = amount - quantity
                self.delete_entry(id)  # delete this row from the table since quantity<=amount
            else:
                cursor.execute("""
                UPDATE Vaccines
                SET quantity=(?)
                WHERE id=(?)""", [quantity - amount, id])  # reduce quantity to the amount (quantity - amount)
                amount = 0

    #  method delete_entry deletes the row from the table
    def delete_entry(self, id):
        cursor = self.conn.cursor()
        cursor.execute("""
        DELETE FROM Vaccines
        WHERE id=(?)""", [id])

    #  method add_order adds a new row to the table according to supplier's name.
    def add_order(self, name, amount, date):
        cursor = self.conn.cursor()
        cursor.execute("""
        SELECT id
        FROM Suppliers
        WHERE name=(?)""", [name])
        supplier_id = cursor.fetchone()[0]
        self.insert(Vaccine(self.last_id + 1, date, supplier_id, amount))


# class _Suppliers represents the table suppliers
class _Suppliers:
    def __init__(self, conn):
        self.conn = conn

    #  method insert to insert a new row to the table with the relevant info: id, name, logistic
    def insert(self, supplier):
        self.conn.execute("""
        INSERT INTO Suppliers (id, name, logistic) VALUES(?, ?, ?)
        """, [supplier.id, supplier.name, supplier.logistic])


# class _Logistics represents the table Logistics
class _Logistics:
    def __init__(self, conn):
        self.conn = conn
        self.count_sent = 0
        self.count_received = 0

    #  method insert to insert a new row to the table with the relevant info: id, name, count_sent, count_received
    def insert(self, logistic):
        self.conn.execute(""" 
        INSERT INTO Logistics (id, name, count_sent, count_received) VALUES(?, ?, ?, ?)
        """, [logistic.id, logistic.name, logistic.count_sent, logistic.count_received])

    #  method update_sent updates the amount sent from a location.
    def update_sent(self, location, amount):
        cursor = self.conn.cursor()
        cursor.execute("""
        SELECT logistic
        FROM Clinics
        WHERE location=(?)""", [location])
        logistic = cursor.fetchone()[0]
        # fetch the count_sent in the DB associated to a specific id.
        cursor.execute("""
        SELECT count_sent  
        FROM Logistics
        WHERE id=(?)""", [logistic])
        count = cursor.fetchone()[0]
        # update count_sent to the new value (count + amount)
        cursor.execute("""
        UPDATE Logistics
        SET count_sent=(?)
        WHERE id = (?)""", [count + amount, logistic])
        self.count_sent = self.count_sent + amount

    # method receive updates the amount received
    def receive(self, name, amount):
        cursor = self.conn.cursor()
        # fetch the right supplier
        cursor.execute("""
        SELECT logistic
        FROM Suppliers
        WHERE name=(?)""", [name])
        logistic = cursor.fetchone()[0]
        # fetch the value of count_received in the DS
        cursor.execute("""
                SELECT count_received
                FROM Logistics
                WHERE id=(?)""", [logistic])
        count = cursor.fetchone()[0]
        # updates the amount received to the right supplier.
        cursor.execute("""
        UPDATE Logistics
        SET count_received=(?)
        WHERE id=(?)""", [count + amount, logistic])
        self.count_received = self.count_received + amount


# class _Clinics represents the table clinics
class _Clinics:
    def __init__(self, conn):
        self.conn = conn
        self.demand = 0

    #  method insert to insert a new row to the table with the relevant info: id, location, demand, logistic
    def insert(self, clinic):
        self.conn.execute("""
        INSERT INTO Clinics (id, location, demand, logistic) VALUES(?, ?, ?, ?)
        """, [clinic.id, clinic.location, clinic.demand, clinic.logistic])
        self.demand = self.demand + clinic.demand

    # method update_demand updates the demand in a specific location to the current demand - the amount
    def update_demand(self, location, amount):
        cursor = self.conn.cursor()
        # fetch the right location
        cursor.execute("""
        SELECT demand
        FROM Clinics
        WHERE location=(?)""", [location])
        curr_demand = cursor.fetchone()[0]
        # update demand to the new value (curr_demand - amount)
        self.conn.execute("""
        UPDATE Clinics
        SET demand=(?)
        WHERE location=(?)""", [curr_demand - amount, location])
        self.demand = self.demand - amount
