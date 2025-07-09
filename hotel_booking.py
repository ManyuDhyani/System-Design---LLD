from enum import Enum
from datetime import datetime
from typing import List

# ---------- ENUMS (Defined constants for clarity) ----------

# Room status: either available or booked
class RoomStatus(Enum):
    EMPTY = 1
    BOOKED = 2

# Room types: single, double, triple
class RoomType(Enum):
    SINGLE = 1
    DOUBLE = 2
    TRIPLE = 3

# Payment status for a booking
class PaymentStatus(Enum):
    PAID = 1
    UNPAID = 2

# Hotel facilities
class Facility(Enum):
    WIFI = 1
    BREAKFAST = 2
    POOL = 3


# ---------- CORE ENTITIES ----------

# User class represents a customer
class User:
    def __init__(self, user_id, name, email):
        self.user_id = user_id
        self.name = name
        self.email = email
    
# Address of the hotel
class Address:
    def __init__(self, city, state, pin):
        self.city = city
        self.state = state
        self.pin = pin

# Room class represents an individual room in a hotel
class Room:
    def __init__(self, room_id, room_type: RoomType):
        self.room_id = room_id
        self.room_type = room_type
        self.status = RoomStatus.EMPTY

# Hotel class holds list of rooms, address, and facilities
class Hotel:
    def __init__(self, hotel_id, name, address: Address, rooms: List[Room], facilities: List[Facility]):
        self.hotel_id = hotel_id
        self.name = name
        self.address = address
        self.rooms = rooms
        self.facilities = facilities

    # Return list of rooms that are currently empty
    def available_rooms(self):
        return [room for room in self.rooms if room.status == RoomStatus.EMPTY]
    
# Booking class represents a user's booking of rooms in a hotel
class Booking:
    def __init__(self, booking_id, user:User, hotel:Hotel, rooms: List[Room], amount: int):
        self.booking_id = booking_id
        self.user = user
        self.hotel = hotel
        self.rooms = rooms
        self.amount = amount
        self.payment_status = PaymentStatus.UNPAID  # Initially unpaid
        self.booking_time = datetime.now()
    
    # Method to mark payment as done and mark rooms as booked
    def confirm_payment(self):
        self.payment_status = PaymentStatus.PAID
        for room in self.rooms:
            room.status = RoomStatus.BOOKED


# Creating a user
user = User(1, "Alice", "alice@email.com")

# Hotel address
addr = Address("Delhi", "DL", "110001")

# Hotel has 2 rooms: one SINGLE and one DOUBLE
rooms = [Room(101, RoomType.SINGLE), Room(102, RoomType.DOUBLE)]

# Hotel with name, address, rooms, and facilities
hotel = Hotel(1, "Taj Palace", addr, rooms, [Facility.WIFI, Facility.BREAKFAST])

# Search for available rooms
available = hotel.available_rooms()  # returns both rooms initially

# Book the first available room for user Alice
booking = Booking(1, user, hotel, available, amount=5000)

# Confirm payment and finalize the booking
booking.confirm_payment()

# Print booking confirmation
room_ids = ", ".join(str(room.room_id) for room in booking.rooms)
print(f"User {booking.user.name} booked room(s) {room_ids} at {booking.hotel.name}")

