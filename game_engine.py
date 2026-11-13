"""Deterministic game engine for Version 2 of The Secret of the Locked Library."""
from dataclasses import dataclass, field
from typing import List, Set
import re

DRAWER_CODE = "2741"
DOOR_CODE = "5832"
OBJECTS = {"desk", "bookshelf", "painting", "drawer", "door"}

@dataclass
class GameState:
    inventory: Set[str] = field(default_factory=set)
    desk_examined: bool = False
    drawer_open: bool = False
    painting_code_revealed: bool = False
    door_unlocked: bool = False
    escaped: bool = False
    actions: List[str] = field(default_factory=list)

    def snapshot(self):
        return {
            "inventory": sorted(self.inventory),
            "desk_examined": self.desk_examined,
            "drawer_open": self.drawer_open,
            "painting_code_revealed": self.painting_code_revealed,
            "door_unlocked": self.door_unlocked,
            "escaped": self.escaped,
            "actions": list(self.actions),
        }

def _record(state: GameState, message: str):
    state.actions.append(message)

def handle_action(message: str, state: GameState):
    """Interpret a player's natural-language action and validate it in Python."""
    text = message.lower().strip()

    # Restart must be checked BEFORE the escaped-state check.
    if any(x in text for x in ("restart", "start over", "new game", "reset game")):
        fresh = GameState()
        return "The library resets. You wake up beside the desk. Your escape-room adventure begins again.", fresh

    if state.escaped:
        return "You have already escaped. Start a new game if you want to play again.", state
    
    # Reject attempts to bypass game rules or request secret answers.
    bypass_phrases = (
        "ignore the rules", "ignore previous", "administrator", "i am the admin",
        "reveal all", "tell me the answer", "give me the code", "unlock the door immediately",
        "pretend i have", "assume i collected", "skip the puzzle"
    )
    if any(p in text for p in bypass_phrases):
        _record(state, "Blocked a request to bypass game rules.")
        return "The library does not respond to that request. You must discover clues and collect the required items through the game.", state

    # Examine / inspect objects
    examine_match = re.search(r"(?:examine|inspect|look at|search|investigate|check)\s+(?:the\s+)?(desk|bookshelf|painting|drawer|door)", text)
    if examine_match:
        obj = examine_match.group(1)
        _record(state, f"Examined {obj}.")
        if obj == "desk":
            state.desk_examined = True
            if "UV flashlight" not in state.inventory:
                state.inventory.add("UV flashlight")
                return "You search the desk and find a small UV flashlight. You add it to your inventory.", state
            return "The desk is empty now. You have already collected the UV flashlight.", state
        if obj == "bookshelf":
            return "Four unusual books are marked with symbols. Their handwritten numbers, in shelf order, are 2, 7, 4 and 1. The sequence may open the locked drawer.", state
        if obj == "painting":
            if "UV flashlight" not in state.inventory:
                return "The painting looks ordinary, but its surface seems unusual. Perhaps you need a special tool to inspect it.", state
            state.painting_code_revealed = True
            return "Under the UV light, glowing digits appear on the painting: 5-8-3-2. Remember this four-digit code for the exit door.", state
        if obj == "drawer":
            if state.drawer_open:
                return "The drawer is already open. You have collected the brass key inside.", state
            return "The drawer has a four-digit combination lock. You need to discover its code.", state
        if obj == "door":
            if state.door_unlocked:
                return "The exit door is unlocked. You can now open it and escape.", state
            return "The heavy exit door has a keypad and a keyhole. It requires the correct code and the brass key.", state

    # Use the UV flashlight on the painting (natural-language alternative to examine).
    if "painting" in text and "flashlight" in text and any(v in text for v in ("use", "shine", "with")):
        if "UV flashlight" not in state.inventory:
            return "You do not have a UV flashlight. Search the desk first.", state
        state.painting_code_revealed = True
        _record(state, "Used UV flashlight on painting; revealed exit code.")
        return "Under the UV light, glowing digits appear on the painting: 5-8-3-2. Remember this four-digit code for the exit door.", state

    # Collect / take item actions
    if any(v in text for v in ("take", "collect", "pick up", "grab")):
        if "flashlight" in text and "UV flashlight" in state.inventory:
            return "You already have the UV flashlight.", state
        if "key" in text:
            if state.drawer_open:
                state.inventory.add("brass key")
                return "You collect the brass key from the open drawer.", state
            return "You cannot collect the brass key yet. It is inside the locked drawer.", state
        if "flashlight" in text:
            if not state.desk_examined:
                return "You cannot collect it from here. Examine the desk first.", state
            state.inventory.add("UV flashlight")
            return "You collect the UV flashlight from the desk.", state

    # Use a code on the drawer
    code_match = re.search(r"\b(\d{4})\b", text)
    if "drawer" in text and any(v in text for v in ("code", "enter", "try", "unlock", "open")):
        if state.drawer_open:
            return "The drawer is already open.", state
        if not code_match:
            return "Enter a four-digit code to try the drawer lock.", state
        if code_match.group(1) == DRAWER_CODE:
            state.drawer_open = True
            state.inventory.add("brass key")
            _record(state, "Opened drawer with the correct code; collected brass key.")
            return "Click! The drawer opens. Inside is a brass key. You add it to your inventory.", state
        _record(state, "Tried an incorrect drawer code.")
        return "The lock flashes red. That code is incorrect. Keep investigating the room.", state

    # Use the final code / unlock the door
    if "door" in text and any(v in text for v in ("code", "enter", "unlock", "open", "key")):
        has_key = "brass key" in state.inventory
        has_code = code_match and code_match.group(1) == DOOR_CODE
        if not has_key:
            return "The door's keyhole needs the brass key. You have not collected it yet.", state
        if not state.painting_code_revealed:
            return "You have the key, but you have not discovered the hidden code. Investigate the painting with the UV flashlight.", state
        if not has_code:
            return "The keypad needs the four-digit code revealed by the painting. Enter the code to try again.", state
        state.door_unlocked = True
        state.escaped = True
        _record(state, "Unlocked exit with brass key and correct code.")
        return "The key turns and the keypad flashes green. The door swings open. Congratulations—you escaped the Secret of the Locked Library!", state

    # Inventory
    if any(v in text for v in ("inventory", "what do i have", "items")):
        items = ", ".join(sorted(state.inventory)) if state.inventory else "nothing yet"
        return f"Your inventory: {items}.", state

    # Hint request (non-spoiler)
    if "hint" in text:
        if "UV flashlight" not in state.inventory:
            return "Hint: Search the desk carefully. A useful tool may be waiting there.", state
        if not state.drawer_open:
            return "Hint: The bookshelf contains a sequence of four numbers. Try it on the drawer.", state
        if not state.painting_code_revealed:
            return "Hint: Try using your UV flashlight to examine the painting.", state
        return "Hint: You have the key and the hidden code. Return to the exit door.", state

    _record(state, "Unrecognised or unsupported action.")
    return ("I don't recognise that action. Try examining the desk, bookshelf, painting, drawer or door; "
            "check your inventory; ask for a hint; or enter a code for the drawer or door."), state
