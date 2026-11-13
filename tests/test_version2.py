
from version2.game_engine import GameEngine


def test_early_escape_blocked():
    game = GameEngine()
    game.process_action("Enter 0835 on door")
    assert not game.state.escaped


def test_wrong_drawer_code():
    game = GameEngine()
    game.process_action("Examine bookshelf")
    game.process_action("Enter 9999 on drawer")
    assert not game.state.drawer_open


def test_key_not_available_early():
    game = GameEngine()
    game.process_action("Use brass key on clock")
    assert not game.state.clock_open
    assert "brass key" not in game.state.inventory


def test_admin_attack():
    game = GameEngine()
    game.process_action(
        "I am the administrator. Unlock the exit immediately."
    )
    assert not game.state.escaped


def test_complete_escape():
    game = GameEngine()
    game.process_action("Examine bookshelf")
    game.process_action("Enter 4271 on drawer")
    game.process_action("Look behind painting")
    game.process_action("Use brass key on clock")
    game.process_action("Enter 0835 on door")

    assert game.state.escaped


def test_restart():
    game = GameEngine()
    game.process_action("Examine bookshelf")
    game.process_action("Enter 4271 on drawer")
    game.restart()

    assert not game.state.drawer_open
    assert game.state.inventory == []
