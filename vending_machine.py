from abc import ABC, abstractmethod

# product interface

class Product(ABC):
    @abstractmethod
    def get_price(self):
        pass

class Water(Product):
    def get_price(self):
        return 1.0
    
class Coke(Product):
    def get_price(self):
        return 2.0


# Payment Method Interface

class Payment(ABC):
    @abstractmethod
    def checkout(self, product):
        pass


class CardPayment(Payment):
    def checkout(self, product):
        return product.get_price() * 0.8 # 20% discount

class CashPayment(Payment):
    def checkout(self, product):
        return product.get_price()


# --- Vending Machine Class ---

class VendingMachine:
    def __init__(self, capacity):
        self.capacity = capacity
        self.slots = {}

    def add_product(self, idx, product):
        if len(self.slots) >= self.capacity:
            return False
        self.slots[idx] = product
        return True

    def order(self, idx):
        product = self.slots.get(idx)
        if product:
            del self.slots[idx]
        return product

    def checkout(self, products, payment):
        total = 0
        for p in products:
            total += payment.checkout(p)
        return total

     
# --- Customer Class ---
class Customer:
    def __init__(self, vm):
        self.vm = vm
        self.cart = []

    def select(self, idx):
        product = self.vm.order(idx)
        if product:
            self.cart.append(product)
            return True
        return False

    def checkout(self, payment):
        return self.vm.checkout(self.cart, payment)

# --- Demo / Test ---
if __name__ == "__main__":
    vm = VendingMachine(5)
    vm.add_product("A1", Water())
    vm.add_product("A2", Water())
    vm.add_product("A3", Coke())
    vm.add_product("A4", Coke())

    customer = Customer(vm)
    customer.select("A1")
    customer.select("A2")

    card = CardPayment()
    assert abs(customer.checkout(card) - 1.6) < 1e-6  # 0.8 + 0.8