from game_controller import Game


class TextInterface:
    """ Create a text-based interface for the turn-based game."""
    def __init__(self):
        self.game = Game()
        self.game.set_up()
        self.player = self.game.characters[0]
        self.game_area = []
        self.running = True

    def _create_area(self):
        self.game_area = [['.'] * self.game.dimensions[1]
                          for _ in range(self.game.dimensions[0])]
        for obj in self.game.backgrounds + self.game.characters:
            pos = obj.pos
            self.game_area[pos[0]][pos[1]] = obj.name[0]

    def _draw_area(self):
        self._create_area()
        print(f"\u2554{'\u2550' * self.game.dimensions[0]}\u2557")
        for row in self.game_area:
            row_string = f"\u2551{"".join(row)}\u2551"
            row_string = row_string.replace('W', '\u2593')
            print(row_string)
        print(f"\u255A{'\u2550' * self.game.dimensions[1]}\u255D")

    def _handle_input(self):
        direction = input('Enter N,E,W or S to move (Q to Quit): ')
        if direction.upper() in "NEWS":
            self.game.move_character(self.player, direction)
        else:
            self.running = False


    def main_loop(self):
        print("Welcome to Andrew's Game")
        while self.running:
            self._draw_area()
            self._handle_input()


if __name__ == "__main__":
    tui = TextInterface()
    tui.main_loop()