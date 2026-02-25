# pygame_MVC/game_controller
from game_objects import GameObj, Character

FILE_LOCATION = 'assets/floor_plan.csv'

class Game:
    def __init__(self):
        self.characters = []
        self.backgrounds = []
        self.start = None
        self.end = None
        self.dimensions = (0, 0)

    def set_up(self, name='Player'):
        self.set_background_from_file(FILE_LOCATION)
        self.characters.append(Character(name, pos=self.start))

    def add_background(self, b_type, pos):
        if b_type == "W":
            wall = GameObj('Wall', pos)
            self.backgrounds.append(wall)
        elif b_type == "S":
            self.start = pos
            self.backgrounds.append(GameObj('Start', pos))
        elif b_type == 'E':
            self.end = pos
            self.backgrounds.append(GameObj('End', pos))

    def set_background_from_file(self, file_location):
        with open(file_location, 'r') as f:
            for row, line in enumerate(f):
                for col, b_type in enumerate(line.strip().split(',')):
                    self.add_background(b_type, pos=(row, col))
        self.dimensions = (row + 1, col + 1)

    def get_background(self, pos):
        backgrounds = [obj for obj in self.backgrounds if obj.pos == pos]
        if backgrounds:
            background = backgrounds[0].name
        else:
            background = None
        return background

    def check_collision(self, pos):
        return (self.get_background(pos) == "Wall" or
                not (0 <= pos[0] < self.dimensions[0]) or
                not (0 <= pos[0] < self.dimensions[0]))

    def move_character(self, character, direction):
        new_pos = character.find_next_location(direction)
        if not self.check_collision(new_pos):
            character.pos = new_pos


    def show_game_grid(self):
        game_str = ""
        for row in range(game.dimensions[0]):
            for col in range(game.dimensions[1]):
                obj = [obj for obj in self.characters + self.backgrounds if obj.pos == (row, col)]
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



