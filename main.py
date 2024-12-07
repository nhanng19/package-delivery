import csv
import msvcrt
import time
import sys

from datetime import timedelta
from HashMap import HashMap
from Package import Package
from DeliveryTruck import DeliveryTruck

with open("data/distance.csv") as dist, open("data/address.csv") as addy:
    distance_csv = list(csv.reader(dist))
    address_csv = list(csv.reader(addy))

with open("data/package.csv") as pkg:
    package_hash_map = HashMap()
    for package in (Package(int(row[0]), row[1], row[2], row[3], row[4], row[5], row[6], "at the hub")
                    for row in csv.reader(pkg)):
        package_hash_map.set(package.package_id, package)
        
trucks = []
with open("data/truck.csv") as file:
    reader = csv.reader(file)
    next(reader)
    for row in reader:
        package_ids = list(map(int, row[1].split(','))) 
        departure_time_str = row[-1]
        hours, minutes = map(int, departure_time_str.split(':'))
        departure_time = timedelta(hours=hours, minutes=minutes)
        truck = DeliveryTruck(package_ids, departure_time)
        trucks.append(truck)


def get_distance(first_address, second_address):
    distance = distance_csv[first_address][second_address] or distance_csv[second_address][first_address]
    return float(distance)
    
def get_address_index(address):
    for row in address_csv:
        if address in row[2]:
            return int(row[0])
    return None

def simulate_delivery(truck):
    not_delivered = []
    
    for package_id in truck.packages:
        not_delivered.append(package_hash_map.get(package_id))

    truck.packages.clear()

    while not_delivered:
        next_package = None
        next_address = float('inf')

        for package in not_delivered:
            distance = get_distance(get_address_index(truck.address), get_address_index(package.address))
    
            if distance <= next_address:
                next_address = distance
                next_package = package
        
        next_address = get_distance(get_address_index(truck.address), get_address_index(next_package.address))

        truck.packages.append(next_package.package_id)
        not_delivered.remove(next_package)
        truck.mileage += next_address
        truck.address = next_package.address
        truck.time += timedelta(hours=next_address / truck.speed)

        next_package.delivery_time = truck.time
        next_package.departure_time = truck.depart_time
    
class Main:
    def __init__(self):
        print("WGUPS Routing Program")
        input("Press Enter to start the delivery process...")
        self.load_animation()
        self.start_delivery()
        self.show_menu()

    def load_animation(self):
        print("\nDelivering packages...")
        truck_frames = [
            "[🚚........]",
            "[..🚚......]",
            "[....🚚....]",
            "[......🚚..]",
            "[........🚚]"
        ]
        num_repeats = 3
        for _ in range(num_repeats):
            for frame in truck_frames:
                sys.stdout.write(f"\r{frame}")
                sys.stdout.flush()
                time.sleep(0.4)
        print("\nPackages delivered!\n")

    def start_delivery(self):
        for i, truck in enumerate(trucks):    
            if i == 2:
                trucks[2].depart_time = min(trucks[0].time, trucks[1].time)
            simulate_delivery(truck)

    def show_menu(self):
        print("Press '1' to view package details")
        print("Press '2' to view total mileage")
        print("Press '3' to exit the program")

        while True:
            choice = msvcrt.getch().decode("utf-8")
            if choice == "1":
                self.view_package_details()
                break
            elif choice == "2":
                self.view_total_mileage()
                break
            elif choice == "3":
                self.exit_program("Goodbye!")
                break

    def view_package_details(self):
        try:
            time_input = input("\nAt what time do you want to view the delivery status? (HH:MM) ")
            hr, min = time_input.split(":")
            convert_time = timedelta(hours=int(hr), minutes=int(min))
            print("\nPress '1' to view a single package or '2' for all packages: ")
            while True:
                choice = msvcrt.getch().decode("utf-8")
                if choice == "1":
                    self.view_single_package(convert_time)
                    break
                elif choice == "2":
                    self.view_all_packages(convert_time)
                    break
                else:
                    print("Invalid option; please try again.")
                    self.view_package_details()

        except ValueError:
            print("Invalid time format; please try again.")
            self.view_package_details()

    def print_header(self):
            print(
                f"{'Truck':<7}{'ID':<5}{'Address':<40}{'City':<20}{'State':<5}"
                f"{'Zip':<10}{'Deadline':<10}{'Weight':<10}{'Status':<20}"
            )
            print("-" * 150)

    def view_single_package(self, convert_time):
        try:
            single_input = input("Please provide a package ID: ")
            package_id = int(single_input)
            package = package_hash_map.get(package_id)
            if package:
                self.print_header()
                for i, truck in enumerate(trucks, start=1):
                    if package_id in truck.packages:
                        print(f"{i:<7}{package.update_status(convert_time)}")
            else:
                print("Package not found; please try again.")
                self.view_single_package(convert_time)
        except ValueError:
            print("Invalid package ID; please try again.")
            self.view_single_package(convert_time)

    def view_all_packages(self, convert_time):
        try:
            self.print_header()
            for package_id in range(1, 41):
                package = package_hash_map.get(package_id)
                if package:
                    for i, truck in enumerate(trucks, start=1):
                        if package_id in truck.packages:
                            print(f"{i:<7}{package.update_status(convert_time)}")
                            break
        except ValueError:
            self.exit_program("An error occurred; exiting the program.")

    def view_total_mileage(self):
        total_mileage = sum(truck.mileage for truck in trucks)
        for i, truck in enumerate(trucks, start=1):
            print(f'Truck {i} traveled {truck.mileage:.2f} miles.')
        print(f'\nThe total distance traveled by all trucks is {total_mileage:.2f} miles.\n')

    def exit_program(self, message):
        print(message)
        exit()

if __name__ == "__main__":
    Main()