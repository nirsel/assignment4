
# class Vaccine represents a singe vaccine and its relevant data
class Vaccine:
    def __init__(self, id, date, supplier, quantity):
        self.id=id
        self.date=date
        self.supplier=supplier
        self.quantity=quantity

# class Clinic represents a singe clinic and its relevant data
class Clinic:
    def __init__(self, id, location, demand, logistic):
        self.id=id
        self.location=location
        self.demand=demand
        self.logistic=logistic


# class Supplier represents a singe supplier and its relevant data
class Supplier:
    def __init__(self, id, name, logistic):
        self.id=id
        self.name=name
        self.logistic=logistic


# class Logistic represents a singe logistic and its relevant data
class Logistic:
    def __init__(self, id, name, count_sent, count_received):
        self.id=id
        self.name=name
        self.count_sent=count_sent
        self.count_received=count_received
