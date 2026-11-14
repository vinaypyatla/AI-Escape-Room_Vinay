# 🔐 AI Escape Room — Gemini-Powered Interactive Game

**An AI-powered interactive escape room built with Python, Streamlit, and Google Gemini, featuring two implementations that demonstrate the evolution from LLM-controlled gameplay to deterministic game-state validation.**

![Python](https://img.shields.io/badge/Python-3.15-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-Web%20App-red)
![Google Gemini](https://img.shields.io/badge/Google-Gemini%20AI-4285F4)
![Pytest](https://img.shields.io/badge/Testing-Pytest-green)

## 📖 Project Overview

AI Escape Room is an interactive, text-based puzzle game set inside a mysterious locked library.

Players explore objects, discover clues, collect items, solve puzzles, and unlock the exit door by interacting with an AI-powered game master.

This project was developed in two versions to investigate how separating AI-generated narration from game logic improves reliability and control.

**Project objectives:**
- Integrate Google's Gemini API into a Python application.
- Develop an interactive user interface using Streamlit.
- Implement puzzles, inventory management, and game progression.
- Compare LLM-controlled gameplay with Python-validated gameplay.
- Evaluate reliability using automated and manual testing.

## 🛠️ Technologies Used

| Technology | Purpose |
|---|---|
| Python | Application logic and puzzle validation |
| Streamlit | Interactive web interface |
| Google Gemini API | AI-generated dialogue and narration |
| Pytest | Automated testing |
| python-dotenv | Environment variable management |
| Git and GitHub | Version control and project portfolio |

## 🎮 Version 1 — LLM-Controlled Game

Version 1 uses Google Gemini as the primary game master.

The player communicates with the AI through a Streamlit chat interface. Gemini interprets player actions, describes the environment, and manages puzzle interactions through natural-language responses.

### Features

- Natural-language player interaction
- AI-generated room descriptions
- Interactive library environment
- Puzzle-solving conversations
- Gemini-powered game master
- Game restart functionality

### Architecture

**Player → Streamlit Interface → Gemini LLM → Game Response**

### Limitations

Version 1 relies heavily on the language model to interpret actions and maintain gameplay consistency.

Although it handled all five observed invalid-action tests correctly, its architecture does not provide the same explicit Python-enforced game-state controls as Version 2.

## 🧩 Version 2 — Python Rules + Gemini Narration

Version 2 improves the original implementation by separating gameplay rules from AI-generated narration.

A deterministic Python game engine validates player actions, manages inventory, tracks puzzle completion, and controls the escape condition.

Gemini provides atmospheric narration without being responsible for authoritative game-state changes.

### Key Improvements

- Python-controlled puzzle validation
- Explicit game-state management
- Inventory tracking
- Puzzle progress indicators
- Prevention of premature escape
- Rejection of invalid puzzle combinations
- Protection against unauthorized rule overrides
- Optional Gemini narration
- Automated testing with Pytest

### Architecture

**Player → Streamlit Interface → Python Game Engine → Validated Game State**

**Gemini API → Atmospheric Narration**

## 🔄 Version 1 vs Version 2

| Feature | Version 1 | Version 2 |
|---|---|---|
| Game master | Gemini LLM | Python game engine |
| AI narration | Yes | Yes |
| Puzzle decisions | LLM-controlled | Python-validated |
| Inventory management | Conversation-based | Explicit game state |
| Rule enforcement | Prompt-based | Deterministic logic |
| Puzzle progress display | Limited | Available |
| Automated game-engine tests | Not demonstrated | Six passing tests |

### Testing Observations

Five invalid-action scenarios were evaluated in both versions.

| Test scenario | Version 1 | Version 2 |
|---|---|---|
| Enter exit code early | Correctly rejected | Correctly rejected |
| Enter incorrect drawer code | Correctly rejected | Correctly rejected |
| Use key before collecting it | Correctly rejected | Correctly rejected |
| Administrator impersonation | Correctly rejected | Correctly rejected |
| Request secret puzzle codes | Correctly rejected | Correctly rejected |

**Result:** Both versions handled all five observed scenarios correctly.

Version 2's main improvement is architectural: puzzle rules and game-state transitions are enforced by Python rather than relying on the LLM alone.

## 🧪 Automated Testing

Version 2 was tested using Pytest.

Six automated tests were executed successfully:

1. Preventing premature escape
2. Rejecting incorrect drawer codes
3. Preventing use of unavailable keys
4. Rejecting administrator impersonation
5. Completing the legitimate escape sequence
6. Resetting game state correctly

**Test result: 6 passed in 0.04 seconds**

To run the tests:

```bash
python -m pytest tests/test_version2.py -v
```

These tests verify the implemented scenarios, not every possible natural-language input.

## 🚀 Installation and Setup

### 1. Clone the repository

```bash
git clone https://github.com/vinaypyatla/AI-Escape-Room_Vinay.git
cd AI-Escape-Room_Vinay
```

### 2. Create a virtual environment

```bash
python -m venv .venv
```

Activate on Windows:

```powershell
.\.venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```bash
python -m pip install -r requirements.txt
```

### 4. Configure Gemini API

Create a `.env` file in the project root using `.env.example` as a reference.

```env
GEMINI_API_KEY=your_gemini_api_key_here
```

Obtain an API key from [Google AI Studio](https://aistudio.google.com/apikey).

**Security:** Never upload your real `.env` file, API keys, or passwords to GitHub.

### 5. Run Version 1

```bash
python -m streamlit run version1/app.py
```

### 6. Run Version 2

```bash
python -m streamlit run version2/app.py
```

Open the local address displayed by Streamlit, usually `http://localhost:8501`.

## 📸 Application Screenshots

### Version 1 — Gameplay

![Version 1 Gameplay](docs/screenshots/version1_success.png)

### Version 1 — Comparison Tests

![Version 1 Tests](docs/screenshots/version1_comparision1.png)

![Version 1 Tests](docs/screenshots/version1_comparision2.png)

![Version 1 Tests](docs/screenshots/version1_comparision3.png)

### Version 2 — Gameplay

![Version 2 Gameplay](docs/screenshots/version2_success.png)

### Version 2 — Comparison Tests

![Version 2 Tests](docs/screenshots/version2_comparision1.png)

![Version 2 Tests](docs/screenshots/version2_comparision2.png)

### Automated Testing Results

![Automated Testing Results](docs/screenshots/Automated%20Testing%20Results.png)

### Version 2 — Successful Escape

![Version 2 Success](docs/screenshots/version2_success.png)

## 🏗️ System Architecture

### Version 1

![Version 1 Architecture](downloads/architecture_version1.png)

### Version 2

![Version 1 Architecture](downloads/architecture_version2.png)

## 📄 Project Documentation

The project includes a final report discussing:

- Project objectives and design
- Version 1 implementation
- Version 2 improvements
- System architecture
- Automated and manual testing
- Challenges and limitations
- Final conclusions

**Final report:** `docs/AI_Escape_Room_Final_Report.docx`

## 📈 Future Improvements

Potential future enhancements include:

- Multiple escape-room environments
- Difficulty levels and timers
- Additional puzzles and inventory items
- More flexible natural-language action parsing
- Expanded adversarial and edge-case testing
- Player progress persistence
- Improved error handling for API failures

## 🎓 Learning Outcomes

Through this project, I gained practical experience in:

- Python application development
- Generative AI and LLM integration
- Streamlit web application development
- Prompt engineering
- State management and rule validation
- Automated testing and debugging
- Git and GitHub version control
- Technical documentation

## 👨‍💻 Author

**Sai Vinay Pyatla**

GitHub: [@vinaypyatla](https://github.com/vinaypyatla)

Developed as part of an academic mini-project exploring Generative AI application development.

---

⭐ This project demonstrates how combining generative AI with deterministic Python logic can create more controlled and testable interactive applications.
