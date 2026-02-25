# pygame_MVC/game_objects

class GameObj:
    def __init__(self, name, pos=None):
        self._observers = []
        self._name = name
        self._pos = pos

    def __str__(self):
        return f'GameObj(name={self.name}, pos={self.pos})'

    # Set name and pos as properties which, if changed, will allow the _observers, which will be sprites
    # referencing the GameObj to be updated.
    @property
    def name(self):
        return self._name

    # Code is run when the .name property of GameObj is changed
    @name.setter
    def name(self, value):
        self._name = value

    @property
    def pos(self):
        return self._pos

    # Code is run when the .setter property of GameObj is changed
    @pos.setter
    def pos(self, value):
        self._pos = value


class Character(GameObj):
    _directions = {"n": (-1,0), "e": (0, 1), "s": (1, 0), "w": (0, -1)}

    def __str__(self):
        return f'Character(name={self.name}, pos={self.pos})'

    def find_next_location(self, move_dir):
        move_vec = self._directions[move_dir.lower()]
        # Add the move_vec to the current position
        new_pos = tuple(sum(coords) for coords in zip(self.pos, move_vec))
        return new_pos

    def move(self, move_dir: str):
        self.pos = self.find_next_location(move_dir)

if __name__ == "__main__":
    character = Character('Andrew', (0, 0))