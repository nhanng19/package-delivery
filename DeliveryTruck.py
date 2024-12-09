class DeliveryTruck:
    """
    Implementation of a delivery truck object with properties
    """
    def __init__(self, packages=None, depart_time=None, capacity=16, speed=18, mileage=0.0, address="4001 South 700 East"):
        """
        Initializes a delivery truck instance
        Args:
            packages (list[int])
            depart_time (datetime.timedelta)
            capacity (int)
            speed (float)
            mileage (float)
            address (str)
        Returns:
            None
        """
        self.capacity = capacity
        self.speed = speed
        self.load = 0
        self.packages = packages if packages is not None else []
        self.mileage = mileage
        self.address = address
        self.depart_time = depart_time
        self.time = depart_time