from datetime import timedelta

class Package:
    """
    Implementation of a package with properties
    """
    def __init__(self, package_id, address, city, state, zip_code, deadline, weight, status):
        """
        Initializes an instance of a Package.
        Args:
            package_id (int)
            address (str)
            city (str)
            state (str)
            zip_code (str)
            deadline (str)
            weight (str)
            status (str)
        Returns:
            None
        """
        self.package_id = package_id
        self.original_address = address 
        self.address = address
        self.city = city
        self.state = state
        self.zip_code = zip_code
        self.deadline = deadline
        self.weight = weight
        self.status = status
        self.departure_time = None
        self.delivery_time = None

    def update_status(self, current_time):
        """
        Updates the delivery status of the package based on the current time.
        Args:
            current_time (datetime.timedelta)

        Returns:
            A formatted string in columns containing package details and the updated status.
        """
        address_to_use = self.original_address
        
        # Special case for package ID 9 with address change after a specific time
        if self.package_id == 9 and current_time >= timedelta(hours=10, minutes=20):
            address_to_use = "410 S State St"

        if self.delivery_time and self.delivery_time < current_time:
            status = f"Delivered: {self.delivery_time}"
        elif self.departure_time and self.departure_time <= current_time:
            status = f"En Route: {current_time}"
        else:
            status = f"At the hub: {current_time}"

        return (
            f"{self.package_id:<5}{address_to_use:<40}{self.city:<20}{self.state:<5}"
            f"{self.zip_code:<10}{self.deadline:<10}{self.weight:<10}{status:<20}"
        )

    def __str__(self):
        """
        Dunder representation of a package instance.
        Returns:
            A formatted string with package details, including delivery time.
        """
        return (
            f"{self.package_id:<5}{self.address:<40}{self.city:<20}{self.state:<5}"
            f"{self.zip_code:<10}{self.deadline:<10}{self.weight:<10}{self.status:<20}"
            f"{self.delivery_time if self.delivery_time else 'N/A':<20}"
        )
