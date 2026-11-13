
import re
from dataclasses import dataclass, field


@dataclass
class GameState:
    inventory: list = field(default_factory=list)
    discovered: set = field(default_factory=set)
    drawer_open: bool = False
    painting_checked: bool = False
    clock_open: bool = False
    escaped: bool = False


class GameEngine:
    OBJECTS = (
        "bookshelf", "desk", "drawer",
        "painting", "clock", "door"
    )

    def __init__(self):
        self.state = GameState()

    def restart(self):
        self.state = GameState()

    def process_action(self, action):
        s = self.state
        text = action.lower().strip()
        codes = re.findall(r"\b\d{4}\b", text)

        # Reject prompt injection and requests to override rules.
        forbidden = (
            "ignore previous instructions",
            "ignore all instructions",
            "administrator",
            "system prompt",
            "reveal all codes",
            "reveal all secrets",
            "bypass the rules",
            "pretend i already",
        )
        if any(phrase in text for phrase in forbidden):
            return "The game rules cannot be overridden."

        if s.escaped:
            return "You have already escaped! Restart to play again."

        if not text:
            return "Describe what you want to do."

        if any(word in text for word in ("look around", "room", "help")):
            return (
                "You are inside a locked library. "
                "You see a bookshelf, desk, locked drawer, "
                "painting, grandfather clock, and exit door."
            )

        if "bookshelf" in text or "books" in text:
            s.discovered.add("bookshelf")
            return (
                "Four unusual books have handwritten numbers: "
                "4, 2, 7, 1. They may form a combination."
            )

        if "desk" in text and "drawer" not in text:
            return "The wooden desk contains a locked drawer."

        if "drawer" in text:
            if s.drawer_open:
                return (
                    "The drawer is already open. "
                    "Inside is a note: 'Look behind the painting.'"
                )

            if "4271" in codes:
                if "bookshelf" not in s.discovered:
                    return (
                        "You haven't discovered the drawer "
                        "combination yet."
                    )
                s.drawer_open = True
                return (
                    "The drawer clicks open! A note inside reads: "
                    "'Look behind the painting.'"
                )

            if codes:
                return "Incorrect drawer code. The drawer stays locked."

            return "The drawer is locked with a four-digit combination."

        if "painting" in text:
            if not s.drawer_open:
                return (
                    "You examine the painting but find nothing "
                    "useful yet. Perhaps another clue will help."
                )

            s.painting_checked = True
            if "brass key" not in s.inventory:
                s.inventory.append("brass key")
                return (
                    "You move the painting and collect a brass key!"
                )

            return "You have already collected the brass key."

        if "clock" in text or "brass key" in text:
            if "brass key" not in s.inventory:
                return (
                    "The clock has a locked compartment. "
                    "You need to find its key."
                )

            if not any(
                word in text for word in
                ("use", "unlock", "open", "key")
            ):
                return "The clock has a keyhole. Try using your key."

            s.clock_open = True
            return (
                "The brass key opens the clock compartment. "
                "A note inside reveals the final code: 0835."
            )

        if "door" in text or "exit" in text:
            if "0835" in codes:
                if not (
                    s.drawer_open
                    and s.painting_checked
                    and s.clock_open
                    and "brass key" in s.inventory
                ):
                    return (
                        "The exit remains locked. "
                        "You must complete the puzzles first."
                    )

                s.escaped = True
                return (
                    "ESCAPED! The keypad turns green, "
                    "the door opens, and you leave the library. "
                    "Congratulations!"
                )

            if codes:
                return "Incorrect exit code. The door remains locked."

            return "The exit door requires a four-digit code."

        if "inventory" in text:
            return (
                "Inventory: " + ", ".join(s.inventory)
                if s.inventory else "Your inventory is empty."
            )

        return (
            "That action is not available. "
            "Try examining one of the objects in the library."
        )
