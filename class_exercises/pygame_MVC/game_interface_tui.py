from class_exercises.pygame_mvc.game_controller import Game


class TextInterface:
    """ Create a text-based interface for the turn-based game."""
    def __init__(self):
        self.game = Game()
        self.game.set_up()
        self.player = self.game.characters[0]
        self.game_area = []
        self.running = True

    def _create_area(self):
        """ Create a list of lists where each [row][col] in self.game_area is given the first letter of the
        background or character in that grid location. If there is no background or character in
        a grid location, use the default '.'"""
        self.game_area = [['.'] * self.game.dimensions[1]
                          for _ in range(self.game.dimensions[0])]
        for obj in self.game.backgrounds + self.game.characters:
            row, col = obj.pos
            self.game_area[row][col] = obj.name[0]

    def _draw_area(self):
        """ Loop through each row, join the characters in that row and print it out
        'W' in the grid is replaced by '\u2593' (a gray square), borders of the grid are
        shown using the unicode box-drawing characters (https://jrgraphix.net/r/Unicode/2500-257F)"""
        self._create_area()
        print("\u2554" + "\u2550" * self.game.dimensions[0] + "\u2557")
        for row in self.game_area:
            row_string = "\u2551" + "".join(row) + "\u2551"
            row_string = row_string.replace('W', '\u2593')
            print(row_string)
        print("\u255A" + "\u2550" * self.game.dimensions[0] + "\u255D")

    def _handle_input(self):
        """Ask the user to input a direction and use game.move_character to move in that direction.
        Set self.running to false if the user enters Q."""
        direction = input('Enter N,E,W or S to move (Q to Quit): ')
        if direction.upper() in "NEWS":
            self.game.move_character(self.player, direction)
        else:
            self.running = False


    def main_loop(self):
        """Keep drawing the area and asking for player moves while self.running is True."""
        print("Welcome to the Maze Game")
        while self.running:
            self._draw_area()
            self._handle_input()

if __name__ == "__main__":
    tui = TextInterface()
    tui.main_loop()