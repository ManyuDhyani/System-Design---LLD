import heapq

class Locker:
    def __init__(self, locker_id, size):
        self.locker_id = locker_id
        self.size = size
        self.occupied = False  # Initially unoccupied
        self.bag_id = None

    def __lt__(self, other):
        return self.locker_id < other.locker_id  # Min-heap based on locker_id
 
class LockerSystem:
    def __init__(self):
        self.lockers = {
            'Small': [],
            'Medium': [],
            'Large': []
        }
        self.occupied_lockers = {}  # Dictionary to track occupied lockers

    def add_locker(self, locker):
        heapq.heappush(self.lockers[locker.size], locker)

    def find_empty_locker(self, bag_size):
        # Return the smallest available locker for the bag size
        for size in ['Small', 'Medium', 'Large']:
            if size >= bag_size:
                while self.lockers[size] and self.lockers[size][0].occupied:
                    heapq.heappop(self.lockers[size])  # Remove occupied lockers
                if self.lockers[size]:
                    return self.lockers[size][0].locker_id
        return None

    def store_bag(self, bag):
        for size in ['Small', 'Medium', 'Large']:
            if size >= bag.size:
                while self.lockers[size] and self.lockers[size][0].occupied:
                    heapq.heappop(self.lockers[size])  # Remove occupied lockers
                if self.lockers[size]:
                    locker = heapq.heappop(self.lockers[size])  # Get the locker
                    locker.occupied = True
                    locker.bag_id = bag.bag_id
                    self.occupied_lockers[locker.locker_id] = locker  # Track occupied locker
                    return locker.locker_id
        return "No locker available"

    def free_locker(self, locker_id):
        # Free an occupied locker and return it to the available heap
        if locker_id in self.occupied_lockers:
            locker = self.occupied_lockers.pop(locker_id)  # Retrieve and remove from occupied lockers
            locker.occupied = False
            locker.bag_id = None
            heapq.heappush(self.lockers[locker.size], locker)  # Return to available heap
            return True
        return False


locker_system = LockerSystem()

# Add lockers
locker_system.add_locker(Locker(1, 'Small'))
locker_system.add_locker(Locker(2, 'Medium'))
locker_system.add_locker(Locker(3, 'Large'))

# Store bags
print(locker_system.store_bag(Locker(4, 'Small')))  # Assigns locker 1
print(locker_system.store_bag(Locker(5, 'Medium')))  # Assigns locker 2

# Find empty locker
print(locker_system.find_empty_locker('Small'))  # None, as locker 1 is occupied

# Free locker
locker_system.free_locker(1)  # Frees locker 1

# Find empty locker again
print(locker_system.find_empty_locker('Small'))  # Locker 1 is now available
