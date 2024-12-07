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
        
        # Change the address for package 9 when it's 10:20AM
        if self.package_id == 9 and current_time >= timedelta(hours=10, minutes=20):
            address_to_use = "410 S State St"

        # Determine the status based on delivery and departure times
        if self.delivery_time and self.delivery_time < current_time:
            status = f"Delivered at {self.delivery_time}."
        elif self.departure_time and self.departure_time <= current_time:
            status = f"En Route as of {current_time}."
        else:
            status = f"At The Hub as of {current_time}."

        # Return a table row-like string
        return (
            f"{self.package_id:<5} | {address_to_use:<25} | {self.city:<15} | {self.state:<5} | "
            f"{self.zip_code:<10} | {self.deadline:<15} | {self.weight:<5} | {status:<20}"
        )

    def __str__(self):
        return (
            f"{self.package_id:<5} | {self.address:<25} | {self.city:<15} | {self.state:<5} | "
            f"{self.zip_code:<10} | {self.deadline:<15} | {self.weight:<5} | {self.status:<20} | "
            f"{self.delivery_time if self.delivery_time else 'N/A':<20}"
        )
