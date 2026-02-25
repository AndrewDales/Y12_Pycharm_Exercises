import pygame
from game_controller import Game

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


class CharacterSprite(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.surf = pygame.Surface((SQUARE_SIZE, SQUARE_SIZE))
        # self.surf.fill((255, 0, 0))
        pygame.draw.circle(self.surf,
                           (255, 0, 0),
                           (SQUARE_SIZE // 2, SQUARE_SIZE // 2),
                           SQUARE_SIZE // 3,
                           )


class GameGUI:
    key_moves = {K_UP: 'N',
                 K_DOWN: 'S',
                 K_RIGHT: 'E',
                 K_LEFT: 'W',
                 }

    def __init__(self):
        pygame.init()

        self.game = Game()
        self.game.set_up()
        self.player = self.game.characters[0]
        for character in self.game.characters:
            character.sprite = CharacterSprite()

        self.screen = pygame.display.set_mode([self.game.dimensions[1] * SQUARE_SIZE,
                                               self.game.dimensions[0] * SQUARE_SIZE])
        self.running = True
        self.move_direction = None

    @staticmethod
    def _convert_position(grid_position):
        return (SQUARE_SIZE * grid_position[1] + SQUARE_SIZE // 2,
                SQUARE_SIZE * grid_position[0] + SQUARE_SIZE // 2)

    def main_loop(self):
        while self.running:
            self._handle_input()
            self._process_game_logic()
            self._draw()
        pygame.quit()

    def _handle_input(self):
        """ Checks key presses and adjusts GameGUI attributes depending on the presses """
        self.move_direction = None
        for event in pygame.event.get():
            # Quit conditions
            if (event.type == QUIT or
                    event.type == KEYDOWN and event.key == K_ESCAPE):
                self.running = False

            if event.type == KEYDOWN and event.key in self.key_moves:
                self.move_direction = self.key_moves[event.key]

    def _process_game_logic(self):
        """ Implements character moves and checks for collisions """
        if self.move_direction:
            collision_character = self.game.move_character(self.player, self.move_direction)
            if collision_character:
                print(f"{self.player} meets {collision_character}")

    def _draw(self):
        self.screen.fill((0, 0, 0))
        for character in self.game.characters:
            coord_pos = self._convert_position(character.pos)
            char_rect = character.sprite.surf.get_rect(center=coord_pos)
            self.screen.blit(character.sprite.surf, char_rect)
        pygame.display.flip()


if __name__ == "__main__":
    game = GameGUI()
    game.main_loop()