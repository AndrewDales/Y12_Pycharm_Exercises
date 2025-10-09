class Item:
    # Constructor
    def __init__(self, name, description, price, stock: int = 100):
        self.name = name
        self.description = description
        self.price = price
        self.stock = stock


class ShoppingBasket:
    # Constructor
    def __init__(self):
        self.items = {}  # A dictionary of all the items in the shopping basket: {item:quantity}
        self.checkout = False

    # A method to add an item to the shopping basket
    def addItem(self, item, quantity=1):
        if quantity > 0 and item.stock >= quantity:
            # Check if the item is already in the shopping basket
            if item in self.items:
                self.items[item] += quantity
            else:
                self.items[item] = quantity
            item.stock -= quantity
        if item.stock < quantity:
            print("Error, not enough stock")
        else:
            print("Invalid operation - Quantity must be a positive number!")

    # A method to remove an item from the shopping basket (or reduce its quantity)
    def removeItem(self, item, quantity=0):
        if quantity <= 0:
            # Remove the item
            self.items.pop(item, None)
        else:
            if item in self.items:
                if quantity < self.items[item]:
                    # Reduce the required quantity for this item
                    self.items[item] -= quantity
                    item.stock += quantity
                else:
                    # Remove the item
                    self.items.pop(item, None)

    # A method to update the quantity of an item from the shopping basket
    def updateItem(self, item, quantity):
        if quantity > 0:
            self.items[item] = quantity
            item.stock -= quantity
        else:
            self.removeItem(item)

    # A method to view/list the content of the basket.
    def view(self):
        totalCost = 0
        print("---------------------")
        for item in self.items:
            quantity = self.items[item]
            cost = quantity * item.price
            print(" + " + item.name + " - " + str(quantity) + " x £" + '{0:.2f}'.format(
                item.price) + " = £" + '{0:.2f}'.format(cost))
            totalCost += cost
        print("---------------------")
        print(" = £" + '{0:.2f}'.format(totalCost))
        print("---------------------")

        # A method to calculate the total cost of the basket.

    def getTotalCost(self):
        totalCost = 0
        for item in self.items:
            quantity = self.items[item]
            cost = quantity * item.price
            totalCost += cost
        return totalCost

    def reset(self):
        for item in self.items:
            item.stock += self.items[item]
            self.item.pop(item, None)
