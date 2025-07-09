"""
2 players place ships on their own board.

Players take turns firing at (row, col) on opponent's board.

If all cells of a ship are hit, that ship is sunk.

First player to sink all opponent's ships wins.
"""

#Each board has many cells.
#Contain a ship or be empty.
#Be hit or untouched.
class Cell:
    def __init__(self):
        self.ship = None # Will point to a Ship object if a ship is placed here
        self.is_hit = False # Tracks if the cell has been attacked
    
    #shoot(): Marks the cell as hit. Returns True if a ship was there.
    def shoot(self):
        self.is_hit = True
        if self.ship:
            return True
        else:
            return False 


# Ship: Stores the coordinates of a ship and tracks if it’s sunk.
#register_hit(coord): Adds a hit coordinate.
#is_sunk(): Returns True if all parts are hit.
class Ship:
    def __init__(self, size, coordinates):
        self.size = size # Number of cells the ship takes (e.g., 2)
        self.coordinates = coordinates # List of positions [(r1,c1), (r2,c2)]
        self.hits = set() # Set of coordinates that have been hit
    
    def is_sunk(self):
        return len(self.hits) == self.size
    
    def register_hit(self, coordinate):
        if coordinate in self.coordinates:
            self.hits.add(coordinate)

# square board
#Each player has their own board to:
#   -Place ships
#   -Receive attacks
class Board:
    def __init__(self, size):
        self.size = size
        self.grid = [[Cell() for _ in range(size)] for _ in range(size)]
        self.ships = [] # List of all ships placed on this board
    
    # Use place_ship() to put ships on the board
    def place_ship(self, ship):
        for r,c in ship.coordinates:
            self.grid[r][c].ship = ship # Place ship reference in each cell
        self.ships.append(ship)

    # When attacked, call receive_attack(row, col) and check if a ship was hit.
    def receive_attack(self, row, col):
        cell = self.grid[row][col]
        hit = cell.shoot()
        if hit:
            cell.ship.register_hit((row, col))
        return hit
    
    # all_ships_sunk() returns True when the game is over for this board.
    def all_ship_sunk(self):
        return all(ship.is_sunk() for ship in self.ships)
    
# Represents a single player, with their own board.
# The Game class will use Player objects to:
#   -Take turns
#   -Access the opponent’s board to attack
class Player:
    def __init__(self, name, board_size):
        self.name = name
        self.board = Board(board_size)

# Game
# Game alternates turns using self.current
# Each turn, a player picks coordinates to attack
# It prints hit/miss and checks if the game is over
class Game:
    def __init__(self, player1, player2):
        self.players = [player1, player2] # not using here but use to extend funtionality like more players or display status
        self.attacker = player1
        self.defender = player2

    def play_turn(self, row, col):
        print(f"{self.attacker.name} attacks ({row}, {col})")

        # Attacker fires at defender's board
        hit = self.defender.board.receive_attack(row, col)
        print("Hit!" if hit else "Miss!")

        # Check if defender has lost all ships
        if self.defender.board.all_ship_sunk():
            print(f"{self.attacker.name} wins!")
            return True  # Game over

        # Switch attacker and defender
        self.attacker, self.defender = self.defender, self.attacker
        return False

p1 = Player("Alice", 5)
p2 = Player("Bob", 5)

# Each player places one ship
p1.board.place_ship(Ship(2, [(0, 0), (0, 1)]))
p2.board.place_ship(Ship(2, [(1, 1), (1, 2)]))


# Simulate
game = Game(p1, p2)
# Turn 1: Alice attacks (1,1) — hits Bob's ship
game.play_turn(1, 1)  # Hit!

# Turn 2: Bob attacks (0,0) — hits Alice's ship
game.play_turn(0, 0)  # Hit!

# Turn 3: Alice attacks (1,2) — hits Bob's ship again (both parts hit → ship sunk → Alice wins!)
game.play_turn(1, 2)  # Hit + Win


"""
1. game.play_turn(1, 1)
    ↓
2. defender = players[1 - current] → Bob
    ↓
3. defender.board.receive_attack(1, 1)
    ↓
4. cell = board.grid[1][1]
    ↓
5. hit = cell.shoot()
       → sets cell.is_hit = True
       → returns True if cell.ship is not None
    ↓
6. if hit: 
       → cell.ship.register_hit((1, 1))
       → adds (1, 1) to ship.hits set
    ↓
7. defender.board.all_ships_sunk()
       → checks if all ships in board.ships are sunk
       → calls ship.is_sunk() on each
    ↓
8. if sunk: declare attacker wins
    ↓
9. else: switch turn


"""

"""
Game
└── play_turn(row, col)
    ├── players → [Player("Alice"), Player("Bob")]
    ├── defender = players[1 - current]
    └── defender.board.receive_attack(row, col)
           ├── grid[row][col] → Cell
           ├── cell.shoot()
           │     └── is_hit = True
           │     └── returns True if ship is not None
           ├── if hit:
           │     └── cell.ship.register_hit(coord)
           │           └── adds coord to ship.hits
           └── all_ships_sunk()
                 └── for each ship: ship.is_sunk()

"""