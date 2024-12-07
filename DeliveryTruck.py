class DeliveryTruck:
    def __init__(self, packages=None, depart_time=None, capacity=16, speed=18, mileage=0.0, address="4001 South 700 East"):
        """
        """
        self.capacity = capacity
        self.speed = speed
        self.load = 0
        self.packages = packages if packages is not None else []
        self.mileage = mileage
        self.address = address
        self.depart_time = depart_time
        self.time = depart_time

    def __str__(self):
        return f"Capacity: {self.capacity}, Speed: {self.speed} mph, Load: {self.load}, Mileage: {self.mileage} miles, Address: {self.address}, Departure Time: {self.depart_time}, Current Time: {self.time}"

