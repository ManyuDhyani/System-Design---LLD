"""
Design a basic Parking Lot system with the following:

Park / Unpark vehicles

fixed number of spots

Spot types: Compact, Large

Vehicle types: Bike, Car, Truck
"""

from enum import Enum

# Define types of vehicles
class VehicleType(Enum):
    BIKE = 1
    CAR = 2
    TRUCK = 3

# Define types of parking spots
class SpotType(Enum):
    COMPACT = 1
    LARGE = 2

# Vehicle class with license plate and type
class Vehicle:
    def __init__(self, plate, v_type):
        self.plate = plate          # e.g. "DL01AB1234"
        self.type = v_type          # e.g. VehicleType.BIKE

# ParkingSpot class to represent a physical parking slot
class ParkingSpot:
    def __init__(self, spot_id, spot_type):
        self.id = spot_id           # e.g. "C1", "L1"
        self.type = spot_type       # SpotType.COMPACT or LARGE
        self.free = True            # True if available
        self.vehicle = None         # Store parked vehicle

    # Check if the vehicle can park in this spot
    def can_park(self, vehicle):
        if self.type == SpotType.COMPACT and vehicle.type == VehicleType.BIKE:
            return True  # Only bikes can park in compact
        if self.type == SpotType.LARGE:
            return True  # Any vehicle can use large spot
        return False

# ParkingLot class manages all spots and operations
class ParkingLot:
    def __init__(self):
        # Initialize the parking lot with 1 compact and 1 large spot
        self.spots = [
            ParkingSpot("C1", SpotType.COMPACT),
            ParkingSpot("L1", SpotType.LARGE)
        ]

    # Try to park the vehicle in an available spot
    def park(self, vehicle):
        for spot in self.spots:
            if spot.free and spot.can_park(vehicle):
                # Assign vehicle to the spot
                spot.free = False
                spot.vehicle = vehicle
                print(f"Parked {vehicle.plate} at spot {spot.id}")
                return
        print("No spot available")

    # Unpark vehicle based on license plate
    def unpark(self, plate):
        for spot in self.spots:
            if not spot.free and spot.vehicle.plate == plate:
                # Free the spot and remove the vehicle
                spot.free = True
                spot.vehicle = None
                print(f"Unparked {plate} from spot {spot.id}")
                return
        print("Vehicle not found")


# Create parking lot
lot = ParkingLot()

# Create vehicles
bike = Vehicle("B123", VehicleType.BIKE)
car = Vehicle("C456", VehicleType.CAR)

# Try parking them
lot.park(bike)     # Should go to Compact spot
lot.park(car)      # Should go to Large spot

# Unpark the bike
lot.unpark("B123")
