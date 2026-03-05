# pygame_MVC/game_controller
from pathlib import Path
import csv
from collections import namedtuple
from typing import Optional

from .game_objects import GameObj, Character, Position

# Resolve assets path relative to this file
ASSETS_DIR = Path(__file__).resolve().parent / "assets"
FILE_LOCATION = ASSETS_DIR / "floor_plan.csv"

Background = namedtuple('Background', ('type', 'solid'), defaults=[True])

BACKGROUND_TYPES = {'W': Background('Wall', True),
                    'S': Background('Start', False),
                    'E': Background('Exit', False),
                    }

class Game:
    def __init__(self):
        self.characters: list[Character] = []
        self.backgrounds: list[GameObj] = []
        self.dimensions: tuple[int, int] = (0, 0)
        self._start: Optional[Position] = None
        self._exit: Optional[Position] = None

    def set_up(self, name:str='Player'):
        self.set_background_from_file(str(FILE_LOCATION))
        self.characters.append(Character(name, self.start))

    def add_background_object(self, b_type:str, pos:Position):
        if b_type in BACKGROUND_TYPES:
            background = BACKGROUND_TYPES[b_type]
            self.backgrounds.append(GameObj(background.type, pos=pos, solid=background.solid))

    def set_background_from_file(self, file_location:str):
        with open(file_location, 'r') as f:
            reader = csv.reader(open(file_location))
            for row, line in enumerate(reader):
                for col, b_type in enumerate(line):
                    self.add_background_object(b_type, pos=Position(row, col))
        self.dimensions = (row + 1, col + 1)

        # Cache start/exit if present
        start = self.find_objects_by_name('Start')
        ex = self.find_objects_by_name('Exit')
        self._start = start[0].pos if start else None
        self._exit = ex[0].pos if ex else None

    def get_cell_contents(self, pos:Position) -> list[GameObj]:
        contents = [obj for obj in (self.backgrounds + self.characters) if obj.pos == pos]
        return contents

    def check_collision(self, pos:Position) -> bool:
        outside_grid = not (0 <= pos.row < self.dimensions[0] and 0 <= pos.col < self.dimensions[1])
        cell_contents = self.get_cell_contents(pos)
        return outside_grid or any(cell.is_solid for cell in cell_contents)

    def move_character(self, character:Character, direction:str) -> bool:
        mv = False
        new_pos = character.find_next_location(direction)
        if not self.check_collision(new_pos):
            character.pos = new_pos
            mv = True
        return mv

    def find_objects_by_name(self, name:str) -> list[GameObj]:
        return [obj for obj in self.backgrounds + self.characters if obj.name == name]

    def at_exit(self, char: Character) -> bool:
        return char.pos == self.exit

    @property
    def start(self) -> Optional[Position]:
        return self._start

    @property
    def exit(self) -> Position:
        return self._exit

    def show_game_grid(self):
        game_str = ""
        for row in range(self.dimensions[0]):
            for col in range(self.dimensions[1]):
                pos = Position(row, col)
                obj = [obj for obj in self.characters + self.backgrounds if obj.pos == pos]
                if obj:
                    game_str += obj[0].name[0]
                else:
                    game_str += '.'
            game_str += '\n'
        print(game_str)

if __name__ == "__main__":
    game = Game()
    game.set_up()
    player = game.characters[0]



