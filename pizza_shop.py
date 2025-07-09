import enum

class PizzaBase(enum.Enum):
    Regular = 1
    ThinCrust = 2
    StuffedCrust = 3
class PizzaSize(enum.Enum):
    Small = 1
    Medium = 2
    Large = 3
class Topping(enum.Enum):
    Mushroom = 2
    Onion = 1
    Cheese = 2
class DrinkType(enum.Enum):
    SODA = 2
    WATER = 0

class Pizza:
    def __init__(self, base: PizzaBase, size: PizzaSize, toppings: list[Topping]):
        self.base = base
        self.size =  size
        self.toppings = toppings
        
    def get_price(self):
        base_price = self.base.value
        size_price = self.size.value
        topping_price = sum(topping.value for topping in self.toppings)
        return base_price + size_price + topping_price

class Drink:
    def __init__(self, type_):
        self.type_ = type_
    
    def get_price(self):
        return self.type_.value
        
class Order:
    def __init__(self):
        self.items = []
        self.deals = []
    
    def add_item(self, item):
        self.items.append(item)
    
    def add_deal(self, deal):
        self.deals.append(deal)
        
    def calculate_total(self):
        total = sum(item.get_price() for item in self.items)
        discount = sum(deal.apply(self.items) for deal in self.deals)
        return total - discount

class Deal:
    def __init__(self, description, function):
        self.description = description
        self.function = function
    def apply(self, items):
        return self.function(items)
        
def buy_one_get_one_free(items):
    pizzas = [item for item in items if isinstance(item, Pizza)]
    if len(pizzas) < 2:
        return 0
    cheapest = min(pizza.get_price() for pizza in pizzas)
    return cheapest
    
# Create an order
order = Order()

# Add items to the order
order.add_item(Pizza(PizzaBase.Regular, PizzaSize.Medium, [Topping.Mushroom, Topping.Cheese]))
order.add_item(Pizza(PizzaBase.ThinCrust, PizzaSize.Large, [Topping.Onion]))
order.add_item(Drink(DrinkType.SODA))
order.add_deal(Deal("Buy one get one free", buy_one_get_one_free))
        
        
# Calculate total price
print(f"Total Order Price: ${order.calculate_total():.2f}")