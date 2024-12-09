# Student ID: 011180749

import csv # Read and parse CSV files
import msvcrt # capture keypresses from user's input
import time # Time-related functions, such as sleep
import sys # Used for output and flushing the console.

from datetime import timedelta # Useful for time calculations
from HashMap import HashMap # Custom implementation of a hash map
from Package import Package # Custom implementation of a package instance
from DeliveryTruck import DeliveryTruck # Custom implementation of a delivery truck instance

# Load prerequisite data in different structures before starting program
def load_data():
    with open("data/distance.csv") as file, open("data/address.csv") as file2:
        distance_csv = list(csv.reader(file)) # Store distance matrix
        address_csv = list(csv.reader(file2)) # Store address information
    
    with open("data/package.csv") as file:
        package_hash_map = HashMap()
        # Create Package instance for each row in the CSV file and add to the hash map
        for package in (Package(int(row[0]), row[1], row[2], row[3], row[4], row[5], row[6], "at the hub")
                        for row in csv.reader(file)):
            package_hash_map.set(package.package_id, package)
    
    # Hardcoded trucks with their required packages in CSV.
    trucks = []
    with open("data/truck.csv") as file:
        reader = csv.reader(file)
        next(reader)
        for row in reader:
            # Parse package IDs and departure time.
            package_ids = list(map(int, row[1].split(',')))
            hours, minutes = map(int, row[-1].split(':'))
            departure_time = timedelta(hours=hours, minutes=minutes)
            # Create and push each DeliveryTruck instance.
            truck = DeliveryTruck(package_ids, departure_time)
            trucks.append(truck)
    
    return distance_csv, address_csv, package_hash_map, trucks

# Store parsed information from csv files as global data structure variables.
distance_csv, address_csv, package_hash_map, trucks = load_data()

# Retrieve the distance between two addresses using the distance matrix.
def get_distance(first_address, second_address):
    return float(distance_csv[first_address][second_address] or distance_csv[second_address][first_address])

# Retrieve the index of a given address from the address CSV file. 
def get_index(address):
    for row in address_csv:
        if address in row[2]:
            return int(row[0])
    return None

# Simulate the delivery process for a given truck using the Nearest Neighbor Algorithm.
def simulate_delivery(truck):
    # Get packages that are not yet delivered.
    not_delivered = [package_hash_map.get(pid) for pid in truck.packages]
    truck.packages.clear()
    
    while not_delivered:
        # Find the closest package based on distance.
        next_package = min(
            not_delivered,
            key=lambda pkg: get_distance(get_index(truck.address), get_index(pkg.address))
        )
        # Calculate the distance to the next package's address.
        distance = get_distance(get_index(truck.address), get_index(next_package.address))
        
        # Update truck status and delivery details.
        truck.packages.append(next_package.package_id)
        not_delivered.remove(next_package)
        truck.mileage += distance
        truck.address = next_package.address
        truck.time += timedelta(hours=distance / truck.speed)
        next_package.delivery_time = truck.time
        next_package.departure_time = truck.depart_time

# Main workflow of the program.
class Main:
    def __init__(self):
        self.start()

    # Display a welcome message and prepare to start the program.
    def start(self):
        print("Welcome to The Western Governors University Parcel Service")
        input("Press Enter to start the delivery process...")
        self.load_animation()
        self.start_delivery()
        self.show_options()

    # Display a loading animation before starting delivery.
    def load_animation(self):
        print("\nDelivering packages...")
        frames = ["[🚚........]", "[..🚚......]", "[....🚚....]", "[......🚚..]", "[........🚚]"]
        for _ in range(3):
            for frame in frames:
                sys.stdout.write(f"\r{frame}")
                sys.stdout.flush()
                time.sleep(0.4)
        print("\nPackages delivered!\n")

    # Simulate delivery on all trucks, if it's the third truck, delay its departure until others finish.
    def start_delivery(self):
        for i, truck in enumerate(trucks):
            if i == 2:
                trucks[2].depart_time = min(trucks[0].time, trucks[1].time)
            simulate_delivery(truck)

    # Display the main options and handle user input.
    def show_options(self):
        print("Press '1' to view package status")
        print("Press '2' to view total mileage")
        print("Press '3' to exit")

        while True:
            option = msvcrt.getch().decode("utf-8")
            if option == "1":
                self.show_package_status()
            elif option == "2":
                self.show_total_mileage()
            elif option == "3":
                self.exit_program("Goodbye!")
            else:
                print("Invalid option; please try again.")
                self.show_options()

    # Display options to view the delivery status of any or all packages.
    def show_package_status(self):
        try:
            time_input = input("\nEnter time (HH:MM) to view package status: ")
            hr, min = map(int, time_input.split(":"))
            convert_time = timedelta(hours=hr, minutes=min)
            print("\nPress '1' for a single package or '2' for all packages: ")
            
            while True:
                option = msvcrt.getch().decode("utf-8")
                if option == "1":
                    self.show_single_package(convert_time)
                    break
                elif option == "2":
                    self.show_all_packages(convert_time)
                    break
                else:
                    print("Invalid input; please try again.")
        except ValueError:
            print("Invalid time format; please try again.")
            self.show_package_status()

    # Display a formatted header/column for package details.
    def print_header(self):
        print(f"{'Truck':<7}{'ID':<5}{'Address':<40}{'City':<20}{'State':<5}{'Zip':<10}{'Deadline':<10}{'Weight':<10}{'Status':<20}")
        print("-" * 150)

    # Display status of a single package.
    def show_single_package(self, convert_time):
        try:
            package_id = int(input("Enter package ID: "))
            package = package_hash_map.get(package_id)
            if package:
                self.print_header()
                for i, truck in enumerate(trucks, start=1):
                    if package_id in truck.packages:
                        print(f"{i:<7}{package.update_status(convert_time)}")
                        break
            else:
                print("Package not found; please try again.")
        except ValueError:
            print("Invalid package ID; please try again.")

    # Display status for every packages.
    def show_all_packages(self, convert_time):
        self.print_header()
        for pid in range(1, 41):
            package = package_hash_map.get(pid)
            if package:
                for i, truck in enumerate(trucks, start=1):
                    if pid in truck.packages:
                        print(f"{i:<7}{package.update_status(convert_time)}")
                        break
    
    # Display each truck's total mileage.
    def show_total_mileage(self):
        total_mileage = sum(truck.mileage for truck in trucks)
        for i, truck in enumerate(trucks, start=1):
            print(f"Truck {i} traveled {truck.mileage:.2f} miles.")
        print(f"Total distance traveled by all trucks: {total_mileage:.2f} miles.")

    # Exit the program.
    def exit_program(self, message):
        print(message)
        exit()

if __name__ == "__main__":
    Main()
