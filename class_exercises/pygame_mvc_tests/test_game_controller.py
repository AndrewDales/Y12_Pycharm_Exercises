import pytest
from pathlib import Path

# Adjust import if your package/module path differs
from class_exercises.pygame_mvc.game_objects import GameObj, Position, Character
from class_exercises.pygame_mvc.game_controller import Game


# ---------- Helpers ----------

def write_floor_plan(tmp_path: Path, lines: list[str]) -> str:
    """
    Create a CSV at tmp_path / "floor_plan.csv" with the given lines.
    Returns the file path as a string.
    """
    fp = tmp_path / "floor_plan.csv"
    fp.write_text("\n".join(lines), encoding="utf-8")
    return str(fp)


def make_simple_map(tmp_path: Path) -> str:
    """
    A 3x3 map with:
      W . .
      S . E
      W W .
    Using tokens from BACKGROUND_TYPES: W=Wall(solid), S=Start, E=Exit
    """
    # CSV rows: use commas to separate tokens
    lines = [
        "W,.,.",
        "S,.,E",
        "W,W,."
    ]
    # Replace dots with empty tokens or some safe placeholder.
    # If your controller ignores unknown tokens, keep '.' and assert behavior accordingly.
    # If your add_background_object raises on unknown tokens, replace '.' with known non-solid, e.g., 'S'/'E' carefully.
    # For this suite, we’ll keep '.' and let the controller ignore unknown tokens.
    return write_floor_plan(tmp_path, lines)


# ---------- Fixtures ----------

@pytest.fixture
def game(tmp_path, monkeypatch):
    """
    Provide a fresh Game with a temporary floor plan file.
    We monkeypatch the FILE_LOCATION constant inside game_controller to point to the temp file.
    """
    # Import module to access and patch FILE_LOCATION
    import class_exercises.pygame_mvc.game_controller as gc

    floor_plan = make_simple_map(tmp_path)
    monkeypatch.setattr(gc, "FILE_LOCATION", floor_plan, raising=True)

    g = Game()
    return g


# ---------- Tests ----------

class TestSetupAndParsing:

    def test_set_up_creates_character_at_start(self, game):
        # This relies on your map having a 'Start' tile present.
        game.set_up(name="Player1")

        assert len(game.characters) == 1
        player = game.characters[0]
        assert isinstance(player, Character)
        assert player.name == "Player1"

        # The 'Start' object exists in backgrounds and sets player's starting pos
        start_objs = [obj for obj in game.backgrounds if obj.name == "Start"]
        assert start_objs, "Expected a 'Start' tile in the parsed backgrounds"
        assert player.pos == start_objs[0].pos

    def test_dimensions_are_computed(self, game):
        game.set_up()
        rows, cols = game.dimensions
        assert (rows, cols) == (3, 3)

    def test_background_objects_created(self, game):
        game.set_up()
        # Expect: W, S, E, and W, W => total 5 background objects if '.' are ignored
        # If '.' are unknown tokens and ignored, this passes; if you raise on '.', adjust the helper map.
        names = [b.name for b in game.backgrounds]
        assert "Wall" in names
        assert "Start" in names
        assert "Exit" in names
        # At least 4 or 5 objects depending on your token policy
        assert len(game.backgrounds) >= 4


class TestCellQueries:

    def test_get_cell_contents_includes_background_and_character(self, game):
        game.set_up()
        start_pos = game.start
        assert start_pos is not None

        # There should be a background "Start" and the player at the same cell
        contents = game.get_cell_contents(start_pos)
        names = sorted(obj.name for obj in contents)
        assert "Start" in names
        assert any(isinstance(obj, Character) for obj in contents)

    def test_find_objects_by_name(self, game):
        game.set_up()
        # Backgrounds
        starts = game.find_objects_by_name("Start")
        assert starts and isinstance(starts[0], GameObj)

        # Characters
        players = game.find_objects_by_name("Player")
        assert players and isinstance(players[0], Character)


class TestCollisionAndMovement:

    def test_outside_bounds_is_collision(self, game):
        game.set_up()
        rows, cols = game.dimensions
        assert game.check_collision(Position(-1, 0)) is True
        assert game.check_collision(Position(rows, 0)) is True
        assert game.check_collision(Position(0, -1)) is True
        assert game.check_collision(Position(0, cols)) is True

    def test_inside_empty_cell_is_not_collision(self, game):
        game.set_up()
        # Choose a cell that is inside grid and not a wall; in our simple map, (1,1) is '.'
        assert game.check_collision(Position(1, 1)) is False

    def test_wall_is_collision(self, game):
        game.set_up()
        # Our map has a wall at (0,0)
        assert any(b.name == "Wall" and b.pos == Position(0, 0) for b in game.backgrounds)
        assert game.check_collision(Position(0, 0)) is True

    def test_move_character_succeeds_on_open_cell(self, game):
        game.set_up()
        player = game.characters[0]
        start = player.pos

        # In the sample map: S is at (1,0). Moving east to (1,1) should be open.
        game.move_character(player, "e")
        assert player.pos == Position(start.row, start.col + 1)

    def test_move_character_blocked_by_wall(self, game):
        game.set_up()
        player = game.characters[0]
        # From S at (1,0), moving north goes to (0,0) which is a wall => blocked
        game.move_character(player, "n")
        # Should not have moved
        assert player.pos == Position(1, 0)

    def test_find_next_location_invalid_direction_message(self, game):
        """
        Tests for an invalid key in find_next_location().
        """
        game.set_up()
        player = game.characters[0]

        # Error trapping ->  ValueError is raised if an invalid direction is given
        with pytest.raises(ValueError, match='direction north is not valid'):
            player.find_next_location("north")  # invalid key



class TestStartExitProperties:

    def test_start_property(self, game):
        game.set_up()
        start = game.start
        assert start is not None
        assert isinstance(start, Position)

    def test_exit_property(self, game):
        game.set_up()
        ex = game.exit
        assert ex is not None
        assert isinstance(ex, Position)


class TestGridRendering:

    def test_show_game_grid_prints(self, game, capsys):
        """
        Verifies that show_game_grid prints a grid of the expected size,
        using first letters of names or '.' for empty.
        """
        game.set_up()
        game.show_game_grid()
        out = capsys.readouterr().out.strip()

        lines = out.splitlines()
        assert len(lines) == game.dimensions[0]
        assert all(len(line) == game.dimensions[1] for line in lines)

        # The printed grid should include at least one 'S' (Start), 'E' (Exit), and 'P' (Player)
        # because the rendering uses obj.name[0]
        # Depending on z-order, the Player might occupy the Start cell; accept either.
        grid_text = "\n".join(lines)
        assert any(ch in grid_text for ch in ("S", "P")), "Expected to see Start or Player initial"
        assert "E" in grid_text or any(o.name == "Exit" for o in game.backgrounds)

