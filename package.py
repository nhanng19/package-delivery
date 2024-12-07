from datetime import timedelta

class Package:
    
    def __init__(self, package_id, address, city, state, zip_code, deadline, weight, status):
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
        address_to_use = self.original_address
        
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
        return (
            f"{self.package_id:<5}{self.address:<40}{self.city:<20}{self.state:<5}"
            f"{self.zip_code:<10}{self.deadline:<10}{self.weight:<10}{self.status:<20}"
            f"{self.delivery_time if self.delivery_time else 'N/A':<20}"
        )
