import pytest
from class_exercises.pygame_mvc.game_objects import GameObj, Character, Position

class TestGameObj:

    def test_initialisation(self):
        obj = GameObj("tree", Position(2, 3), solid=True)

        assert obj.name == "tree"
        assert obj.pos == Position(2, 3)
        assert obj.is_solid is True

    def test_name_setter(self):
        obj = GameObj("rock", Position(0, 0))
        obj.name = "boulder"

        assert obj.name == "boulder"

    def test_pos_setter(self):
        obj = GameObj("item", Position(0, 0))
        obj.pos = Position(5, 6)

        assert obj.pos == Position(5, 6)


class TestCharacter:

    def test_inherits_gameobj(self):
        c = Character("player", Position(1, 1))
        assert isinstance(c, GameObj)

    def test_find_next_location_north(self):
        c = Character("player", Position(5, 5))
        new_pos = c.find_next_location("n")

        assert new_pos == Position(4, 5)

    def test_find_next_location_east(self):
        c = Character("player", Position(5, 5))
        new_pos = c.find_next_location("e")

        assert new_pos == Position(5, 6)

    def test_move_updates_position(self):
        c = Character("player", Position(0, 0))
        c.move("s")   # south = +1 row

        assert c.pos == Position(1, 0)

    def test_invalid_direction_raises_error(self):
        c = Character("player", Position(0, 0))

        with pytest.raises(ValueError, match='direction north is not valid'):
            c.find_next_location("north")  # invalid key in your current implementation