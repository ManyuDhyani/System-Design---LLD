from enum import Enum
from collections import deque

class Direction(Enum):
    up = 1
    down = 2
    idel = 3

class Elevator:
    def __init__(self, eid):
        self.id = eid
        self.current_floor = 0
        self.direction = Direction.idel
        self.request_queue  = deque()

    def add_request(self, floor):
        if floor not in self.request_queue:
            self.request_queue.append(floor)
    
    def next_request(self):
        return self.request_queue[0] if self.request_queue else None

# Simulated PhysicalElevator interface provided by the company
class PhysicalElevator:
    def startmovingup(self, elevator):
        print(f"lift {elevator.id} moving up, current {elevator.current_floor} floor")
        elevator.current_floor += 1
    
    def startmovingdown(self, elevator):
        print(f"lift {elevator.id} moving down, current {elevator.current_floor} floor")
        elevator.current_floor -= 1
    
    def isApprochingFloor(self, elevator, floor):
        return elevator.next_request() == floor

# Main controller class that moves elevators toward their destinations
class ElevatorEventHandler:
    def __init__(self, elevators, physical_elevator):
        self.elevators = elevators
        self.physical = physical_elevator

    def handle_requests(self):
        for elevator in self.elevators:
            if not elevator.request_queue:
                elevator.direction = Direction.idel
                continue

            next_floor = elevator.next_request()

            if elevator.current_floor < next_floor:
                elevator.direction = Direction.up
                self.physical.startmovingup(elevator)
            
            elif elevator.current_floor > next_floor:
                elevator.direction = Direction.down
                self.physical.startmovingdown(elevator)

            # If already at the requested floor, serve it
            else:
                print(f"Elevator {elevator.id} arrived at floor {next_floor}")
                elevator.request_queue.popleft()  # Remove the request
                elevator.direction = Direction.idel

class ElevatorSystem:
    def __init__(self, num_elevator):
        self.elevators = [Elevator(eid) for eid in range(num_elevator)]
        self.physical = PhysicalElevator()
        self.handler = ElevatorEventHandler(self.elevators, self.physical)

    # This simulates a user pressing a button at floor X.
    def request_elevator(self, floor):
        best = min(self.elevators, key = lambda e: len(e.request_queue))
        best.add_request(floor)
        print(f"Request for floor {floor} assigned to Elevator {best.id}")

    # Moves each elevator one unit of time forward, based on its direction and next request.
    def step(self):
        # Move all elevators by one "step" based on their state
        self.handler.handle_requests()

system = ElevatorSystem(2)
# Simulate floor requests
system.request_elevator(3)
system.request_elevator(5)
system.request_elevator(1)

# Simulate time steps to let elevators move
for i in range(10):
    print(f"time: {i}")
    system.step()