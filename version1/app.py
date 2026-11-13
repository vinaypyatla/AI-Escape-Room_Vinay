
import os
import streamlit as st
from dotenv import load_dotenv
from google import genai

load_dotenv()

st.set_page_config(
    page_title="AI Escape Room - Version 1",
    page_icon="🔐"
)

st.title("🔐 AI Escape Room — Version 1")
st.write("Explore the locked library and solve puzzles to escape.")

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
model = os.getenv("GEMINI_MODEL", "gemini-3.5-flash-lite")

GAME_RULES = """
You are the Game Master of an interactive escape room.

SCENARIO:
The player wakes up inside a locked library.

OBJECTS:
1. Bookshelf
2. Wooden desk
3. Locked drawer
4. Painting
5. Grandfather clock
6. Exit door

PUZZLES:
- Examining the bookshelf reveals four numbers: 4, 2, 7, 1.
- The drawer opens using code 4271.
- The drawer contains a note suggesting something is hidden
  behind the painting.
- Behind the painting is a brass key.
- The brass key unlocks the grandfather clock.
- The clock reveals the final door code: 0835.
- The player must solve all puzzles before escaping.

RULES:
- Describe the room and respond to natural-language actions.
- Remember collected items and previously completed puzzles.
- Do not reveal puzzle solutions before the player discovers them.
- Do not invent new objects or change established clues.
- Only declare victory after the required puzzles are completed.
- Keep responses engaging, concise, and atmospheric.
"""

if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": (
                "You wake up in a mysterious locked library. "
                "A bookshelf, desk, painting, clock, and exit door "
                "surround you. What would you like to examine?"
            )
        }
    ]

with st.sidebar:
    st.header("Game Controls")
    st.write("Version 1: LLM-controlled game")

    if st.button("Restart Game"):
        st.session_state.clear()
        st.rerun()

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

user_input = st.chat_input("What would you like to do?")

if user_input:
    st.session_state.messages.append({
        "role": "user",
        "content": user_input
    })

    with st.chat_message("user"):
        st.write(user_input)

    conversation = [
        {
            "role": "user" if msg["role"] == "user" else "model",
            "parts": [{"text": msg["content"]}]
        }
        for msg in st.session_state.messages
    ]

    try:
        response = client.models.generate_content(
            model=model,
            contents=conversation,
            config={
                "system_instruction": GAME_RULES,
                "temperature": 0.4
            }
        )

        answer = response.text or "The room falls silent."

    except Exception as error:
        answer = (
            "The AI Game Master is temporarily unavailable. "
            "Please try again."
        )
        st.error(f"API request failed: {type(error).__name__}")

    st.session_state.messages.append({
        "role": "assistant",
        "content": answer
    })

    with st.chat_message("assistant"):
        st.write(answer)
