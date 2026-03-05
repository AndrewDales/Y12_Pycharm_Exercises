# pygame_MVC/game_objects
from collections import namedtuple
from typing import Optional

Position = namedtuple('Position', ('row', 'col'), defaults=[0, 0])

class GameObj:
    def __init__(self, name: str, pos: Optional[Position] = None, solid: bool =True):
        self._name = name
        self._pos = pos
        self._solid = solid

    def __repr__(self) -> str:
        return f'GameObj(name={self.name}, {self.pos})'

    # Set name and pos as properties which, if changed, will allow the _observers, which will be sprites
    # referencing the GameObj to be updated.
    @property
    def name(self) -> str:
        return self._name

    # Code is run when the .name property of GameObj is changed
    @name.setter
    def name(self, value: str) :
        self._name = value

    @property
    def pos(self) -> Optional[Position]:
        return self._pos

    # Code is run when the .pos property of GameObj is changed
    @pos.setter
    def pos(self, value: Position):
        self._pos = value

    @property
    def is_solid(self) -> bool:
        return self._solid


class Character(GameObj):
    _directions = {"n": Position(-1,0), "e": Position(0, 1), "s": Position(1, 0), "w": Position(0, -1)}

    def __repr__(self) -> str:
        return f'Character(name={self.name}, {self.pos})'

    def find_next_location(self, move_dir: str) -> Position:
        try:
            move_vec = self._directions[move_dir.lower()]
        except KeyError:
            raise ValueError(f'direction {move_dir} is not valid')

        # Add the move_vec to the current position
        new_pos = Position(self.pos.row + move_vec.row, self.pos.col + move_vec.col)
        return new_pos

    def move(self, move_dir: str):
        self.pos = self.find_next_location(move_dir)

if __name__ == "__main__":
    player = Character('Andrew', Position(0, 0))