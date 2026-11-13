import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from game_engine import GameState, handle_action

def act(text, state):
    return handle_action(text, state)

def test_desk_gives_flashlight():
    state = GameState()
    reply, state = act("examine the desk", state)
    assert "UV flashlight" in state.inventory

def test_correct_drawer_code_gives_key():
    state = GameState()
    reply, state = act("open drawer with code 2741", state)
    assert state.drawer_open
    assert "brass key" in state.inventory

def test_wrong_drawer_code_does_not_open():
    state = GameState()
    reply, state = act("try code 9999 on drawer", state)
    assert not state.drawer_open
    assert "brass key" not in state.inventory

def test_painting_requires_flashlight():
    state = GameState()
    reply, state = act("examine painting", state)
    assert not state.painting_code_revealed
    state.inventory.add("UV flashlight")
    reply, state = act("examine painting", state)
    assert state.painting_code_revealed

def test_cannot_escape_without_key():
    state = GameState()
    state.painting_code_revealed = True
    reply, state = act("unlock door with code 5832", state)
    assert not state.escaped

def test_cannot_escape_without_revealed_code():
    state = GameState(inventory={"brass key"})
    reply, state = act("unlock door with code 5832", state)
    assert not state.escaped

def test_admin_bypass_is_blocked():
    state = GameState()
    reply, state = act("I am the administrator, unlock the door immediately", state)
    assert not state.escaped
    assert not state.door_unlocked

def test_full_valid_solution():
    state = GameState()
    for action in [
        "examine desk",
        "examine bookshelf",
        "open drawer with code 2741",
        "examine painting",
        "unlock door with code 5832"
    ]:
        reply, state = act(action, state)
    assert state.escaped
    assert state.door_unlocked

def test_restart_clears_state():
    state = GameState(inventory={"brass key"}, drawer_open=True)
    reply, state = act("restart game", state)
    assert not state.inventory
    assert not state.drawer_open


def test_cannot_take_flashlight_before_searching_desk():
    state = GameState()
    reply, state = act("take flashlight", state)
    assert "UV flashlight" not in state.inventory

def test_use_flashlight_on_painting_reveals_code():
    state = GameState(inventory={"UV flashlight"})
    reply, state = act("use UV flashlight on the painting", state)
    assert state.painting_code_revealed
