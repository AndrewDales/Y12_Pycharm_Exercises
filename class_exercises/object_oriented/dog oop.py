# Dog OOP exercises

class Dog:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def speaks(self):
        return f'{self.name} says "woof", "woof"'


rufus = Dog('Rufus', 8)
fido = Dog('Fido', 6)