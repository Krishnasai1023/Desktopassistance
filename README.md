# 🖥️ Desktop Assistance System

A Python-based intelligent voice-controlled desktop assistant capable of executing user commands through natural speech. The assistant uses speech recognition and text-to-speech synthesis, and is enhanced with context-aware synonym handling to ensure flexible and seamless user interactions.

## 🚀 Features

- **Real-Time Voice Control**  
  Understands and executes spoken commands using Google's speech recognition.

- **Synonym-Aware Commands**  
  Maintains context across interactions and recognizes alternate phrases (e.g., "look up" = "search", "launch" = "open").

- **Multifunction Automation**  
  Supports tasks like:
  - Wikipedia search
  - Opening websites (e.g., YouTube, Google)
  - Launching system applications (e.g., Notepad)
  - Telling the current time

- **Modular Design**  
  Each command is encapsulated in separate functions, making the codebase maintainable and extensible.

## 🛠️ Tools & Libraries

- `Python 3`
- `speech_recognition` – for voice input
- `pyttsx3` – for text-to-speech output
- `wikipedia` – for fetching content summaries
- `webbrowser` – for opening websites
- `datetime` – for time queries
- `os` – for system-level operations

## 🧠 How Synonym Recognition Works

The assistant uses a synonym mapping dictionary to match user commands more flexibly. For example:
- `"search"`, `"look up"`, and `"find"` trigger Wikipedia lookup
- `"open"`, `"launch"`, and `"start"` open websites or apps

Additionally, the assistant keeps track of the **last used command type** and can infer the intended action even when the exact keyword is not repeated.

## 🔧 Setup Instructions

1. **Clone the repository**

```bash
git clone https://github.com/Krishnasai1023/Desktopassistance.git
cd Desktopassistance
Install dependencies

Make sure Python 3 is installed, then run:

bash
Copy
Edit
pip install -r requirements.txt
If requirements.txt is not available, manually install:

bash
Copy
Edit
pip install pyttsx3 speechrecognition wikipedia
Run the assistant

bash
Copy
Edit
python assistant.py
(Assuming your main file is named assistant.py — update if different)

🗣️ Example Commands
“Search Wikipedia for Python”

“Look up Django” (recognized as synonym of search)

“Open YouTube”

“Launch Google”

“What’s the time?”

📁 Project Structure
bash
Copy
Edit
Desktopassistance/
│
├── assistant.py           # Main logic and command handling
├── README.md              # Project documentation
└── requirements.txt       # Python dependencies
👨‍💻 Author
Gopi Krishna Sai
GitHub Profile

📄 License
This project is open-source and available under the MIT License.

yaml
Copy
Edit

---

### ✅ To Complete This:
- Ensure your main file is named `assistant.py`. If it’s different (e.g., `main.py`), adjust the README accordingly.
- Add a `requirements.txt` file using:

```bash
pip freeze > requirements.txt
