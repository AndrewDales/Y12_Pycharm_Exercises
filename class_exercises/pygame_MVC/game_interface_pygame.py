import pygame
from class_exercises.pygame_mvc.game_controller import Game
from class_exercises.pygame_mvc.game_objects import Position

from pygame.locals import (
    K_LEFT,
    K_RIGHT,
    K_UP,
    K_DOWN,
    K_ESCAPE,
    KEYDOWN,
    QUIT,
)

SQUARE_SIZE = 50

BACKGROUND_COLORS = {'Wall': 'gray30',
                     'Start': 'gold',
                     'Exit': 'dodgerblue',
                     'Floor': 'white'
                     }
PLAYER_COLOR = 'firebrick'

class GameGUI:
    key_moves = {K_UP: 'n',
                 K_DOWN: 's',
                 K_RIGHT: 'e',
                 K_LEFT: 'w',
                 }

    def __init__(self):
        pygame.init()
        pygame.display.set_caption('Pygame MVC')

        # Set clock so that FPS can be limited
        self.clock = pygame.time.Clock()

        self.game = Game()
        self.game.set_up()
        self.player = self.game.characters[0]
        self.move_direction: str | None = None

        self.screen = pygame.display.set_mode([self.game.dimensions[1] * SQUARE_SIZE,
                                               self.game.dimensions[0] * SQUARE_SIZE])
        self.running = True

        self.player_image = pygame.image.load('assets/player.png').convert_alpha()
        self.player_rect = self.player_image.get_rect()

    @staticmethod
    def _convert_position(pos: Position, center: bool = False) -> tuple[int, int]:
        gx, gy = (SQUARE_SIZE * pos.col, SQUARE_SIZE * pos.row)
        if center:
            gx += SQUARE_SIZE // 2
            gy += SQUARE_SIZE // 2
        return gx, gy

    def main_loop(self):
        while self.running:
            self._handle_input()
            self._process_game_logic()
            self._draw()
            self.clock.tick(60) # cap to 60 FPS
        pygame.quit()

    def _handle_input(self):
        """ Checks key presses and adjusts GameGUI attributes depending on the presses """
        self.move_direction = None
        for event in pygame.event.get():
            # Quit conditions
            if (event.type == QUIT or
                    event.type == KEYDOWN and event.key == K_ESCAPE):
                self.running = False

            # Checks for movement keys
            if event.type == KEYDOWN and event.key in self.key_moves:
                self.move_direction = self.key_moves[event.key]

    def _process_game_logic(self):
        """ Implements character moves and checks if player has reached the exit """
        if self.move_direction:
            self.game.move_character(self.player, self.move_direction)
        if self.game.at_exit(self.player):
            self.running = False

    def _draw(self):
        self._draw_background()
        self._draw_characters()
        pygame.display.flip()

    def _draw_background(self):
        self.screen.fill(BACKGROUND_COLORS['Floor'])
        for bg in self.game.backgrounds:
            grid_x, grid_y = self._convert_position(bg.pos)
            color = BACKGROUND_COLORS[bg.name]
            pygame.draw.rect(self.screen, color, (grid_x, grid_y, SQUARE_SIZE, SQUARE_SIZE))

    def _draw_characters(self):
        for character in self.game.characters:
            coord_pos = self._convert_position(character.pos, True)
            # pygame.draw.circle(self.screen, PLAYER_COLOR, coord_pos, 20)

            self.player_rect.center = coord_pos
            self.screen.blit(self.player_image, self.player_rect)



if __name__ == "__main__":
    game = GameGUI()
    game.main_loop()