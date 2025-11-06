import random


def dice_sum(num_dice: int = 1, num_sides: int = 6):
    """returns the sum of num_dice dice, each with num_sides sides"""
    return sum(random.randint(1, num_sides) for _ in range(num_dice))


class Character:
    """ A Fighting Fantasy Character Object"""
    def __init__(self, name, skill=0, stamina=0):
        self.name = name.title()
        self.skill = skill
        self.stamina = stamina
        self.roll = None
        self.score = None

    def __repr__(self):
        return f"Character('{self.name}', skill={self.skill}, stamina={self.stamina})"

    def __str__(self):
        return self.name.title()

    def find_score(self):
        self.roll = dice_sum(num_dice=2)
        self.score = self.roll + self.skill

    def take_hit(self, damage=2):
        self.stamina -= damage

    def fight_round(self, other):
        self.find_score()
        other.find_score()
        if self.score > other.score:
            result = 'won'
            other.take_hit()
        elif self.score < other.score:
            result = 'lost'
            self.take_hit()
        else:
            result = 'draw'
            self.take_hit(1)
            other.take_hit(1)
        return result

    def return_character_status(self):
        return f"{self.name} has skill {self.skill} and stamina {self.stamina}"

    def return_roll_status(self):
        return f"{self.name} rolled {self.roll} for a total score of {self.score}"

    @property
    def is_dead(self):
        # character.is_dead will now return True or False
        return self.stamina <= 0

    @is_dead.setter
    def is_dead(self, dead: bool):
        # character can be made dead or alive by setting is_dead to True or False
        if dead:
            self.stamina = 0
        else:
            self.stamina = max(self.stamina, 1)


class PlayerCharacter(Character):
    def __init__(self, name, skill=0, stamina=0, luck=0):
        super().__init__(name, skill, stamina)
        self.luck = luck

    def test_luck(self):
        dice_roll = dice_sum(num_dice=2)
        if dice_roll <= self.luck:
            lucky = True
        else:
            lucky = False
        self.roll = dice_roll
        self.luck -= 1
        return lucky

    @classmethod
    def generate_player_character(cls, name):
        # Roll for skill stamina and luck and pass them to the cls constructor, returning the created instance
        skill = 6 + dice_sum(1)
        stamina = 12 + dice_sum(2)
        luck = 6 + dice_sum(1)
        return cls(name, skill, stamina, luck)

    def __repr__(self):
        return (f"PlayerCharacter('{self.name}', "
                f"skill={self.skill}, "
                f"stamina={self.stamina}, "
                f"luck={self.luck})")


class Game:
    """ Game class - controls the Fighting Fantasy game class """
    @classmethod
    def load_creatures(cls):
        creatures = [Character("Dragon", 10, 22),
                     Character("Orc", 7, 10),
                     Character("Skeleton", 5, 8),
                     Character("Giant Rat", 6, 6),
                     ]
        return creatures

    def __init__(self):
        self.opponent = None
        self.player = None
        self.round_result = None
        self.creatures = self.load_creatures()

    def choose_opponent(self):
        self.opponent = random.choice(self.creatures)
        self.creatures.remove(self.opponent)

    def set_player(self, player_character):
        self.player = player_character

    def resolve_fight_round(self):
        self.round_result = self.player.fight_round(self.opponent)

    def return_characters_status(self):
        msg = (self.player.return_character_status() + "\n" +
               self.opponent.return_character_status())
        return msg

    def return_round_result(self):
        msg = (self.player.return_roll_status() + "\n" +
               self.opponent.return_roll_status() + "\n")
        if self.round_result == "won":
            msg += 'Player won this round\n'
        elif self.round_result == "lost":
            msg += 'Player lost this round\n'
        else:
            msg += 'This round was a draw\n'
        return msg

    @property
    def game_over(self):
        return not self.player or self.player.is_dead


class GameCLI:
    def __init__(self):
        self.game = Game()
        self.run_game()

    def run_game(self):
        """Welcomes the player to Fighting Fantasy - asks for a player_name
            calls self.game methods to set the player"""
        print('Welcome to Fighting Fantasy Battle')
        player_name = input("Enter the name for your character: ")
        self.game.set_player(PlayerCharacter.generate_player_character(player_name))
        print(f'Welcome {player_name}')
        print(self.game.player.return_character_status())
        self.fight_opponent()

    def fight_opponent(self):
        """Chooses an opponent and displays their stats"""
        self.game.choose_opponent()
        print(f'You will be fighting {self.game.opponent}')
        print(self.game.opponent.return_character_status() + '\n')
        self.fight_battle()

    def fight_battle(self):
        """Continues to fight rounds until the player chooses to quit or either player or opponent are dead."""
        continue_battle = True
        while continue_battle:
            print(self.game.return_characters_status())
            print()
            action = input("Would you like to fight a round (y/n)? ").strip().lower()
            if action == 'n':
                print("You flee in terror!")
                continue_battle = False
            else:
                self.game.resolve_fight_round()
                print(self.game.return_round_result())
                if self.game.player.is_dead:
                    print('You died')
                    continue_battle = False
                if self.game.opponent.is_dead:
                    print(f"You defeated the {self.game.opponent.name}")
                    continue_battle = False


if __name__ == "__main__":
    GameCLI()
