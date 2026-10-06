# 🤖 JARVIS AI Voice Assistant

A Python-based personal voice assistant that allows users to interact with their laptop using voice commands.

---

## 📛 **Badges**

![Python](https://img.shields.io/badge/Python-3.8%2B-blue.svg)
![Tkinter](https://img.shields.io/badge/GUI-Tkinter%20HUD-cyan)
![Platform](https://img.shields.io/badge/Platform-Windows-0078D6)
![Status](https://img.shields.io/badge/Status-Active-brightgreen)
![License](https://img.shields.io/badge/License-MIT-green)
![Stars](https://img.shields.io/github/stars/ishantSingh3142/AI-ASSISTANT-?style=social)

---

## 📌 Description

JARVIS AI Voice Assistant is a Python-based desktop voice assistant designed to perform common tasks using simple voice commands.

The project combines Speech Recognition, Text-to-Speech, Web Automation, Wikipedia API, YouTube search, Google search, laptop brightness control, volume control, and a Tkinter-based graphical interface into one simple application.

The goal of this project is to demonstrate how Python can be used to build an interactive voice-controlled desktop assistant.

### ✨ Features & Capabilities (v3.8)

1. 🎙️ **Voice Command Recognition & Ingestion**: High-accuracy speech capture via Google Speech Recognition with ambient noise adaptation and acoustic sonar ping feedback.
2. 🗣️ **Complete Text-to-Speech Narration**: Native Windows SAPI COM engine reads all generated results in full with sentence chunking and natural symbol expansion.
3. 🎭 **Voice-Over Personality Switcher**: Switch dynamically between J.A.R.V.I.S (David - Tactical Male) and F.R.I.D.A.Y (Zira - Neural Female) or any installed system voices.
4. 🔊 **Procedural Cybernetic Audio SFX Suite**: 7 built-in 44.1kHz sci-fi audio effects (Boot Chord, Transmit Chirp, Sonar Ping, Data Downlink, Voice Switch, Hardware Ack, Cyber Alert) running asynchronously.
5. 🎛️ **Voice & Audio Lab Modal**: Interactive dialog with selectable voice cards, live audition buttons, tempo sliders, and a soundboard.
6. 🌤️ **Meteorological Satellite Telemetry**: Real-time atmospheric reports via wttr.in with India as default location.
7. 📰 **Live Global News RSS Dispatches**: Top breaking headlines across World, Technology, Business, and Sports.
8. 🎬 **Smart YouTube Direct Autoplay**: Automated background video ID discovery and browser dispatch with direct autoplay.
9. ⏰ **12-Hour Chronometer & Telemetry**: Full date and time formatted in standard 12-hour AM/PM notation.
10. 💡 **Workstation Hardware Automation**: Instant display brightness modulation and system master volume control.
11. 🖥️ **Holographic 3-Panel HUD**: Animated Arc Reactor, audio waveform, live terminal feed, and matrix data rain.
12. 📑 **Formal IEEE 830 Specification**: Full engineering documentation available in [`SRS.md`](SRS.md).

<details> <summary><strong>🛠️ Setup Guide — Programming Software & IDE</strong></summary>
1. Install Python

This project is written in Python, so Python must be installed on your computer.

Download Python from the official website:

```python
https://www.python.org/downloads/
```

During installation on Windows, make sure to check:

☑ Add Python to PATH

After installation, open Command Prompt or Terminal and verify:

```python
python --version
```

You should see something similar to:

```python
Python 3.x.x
```

If python does not work, try:

```python
py --version
```

1. Choose an IDE / Code Editor

You can use any Python-compatible IDE or editor.

Recommended options:

- Visual Studio Code

Download:

```python
https://code.visualstudio.com/
```

Install the Python extension from Microsoft after installing VS Code.

> PyCharm

Download:

```python
https://www.jetbrains.com/pycharm/
```

PyCharm is another good option for Python development.

IDLE

Python also comes with IDLE, which can be used for basic development without installing another IDE.

For beginners, VS Code is recommended.

</details>
<details> <summary><strong>📦 Prerequisites — Required Python Packages</strong></summary>
## Required Libraries

Before running the project, install the following Python packages:

### Package Purpose

SpeechRecognition Converts voice into text
PyAudio Provides microphone access
pyttsx3 Converts text into speech
requests Communicates with the Wikipedia API
screen-brightness-control Controls laptop brightness

The project also uses Python's built-in libraries such as:

tkinter
webbrowser
ctypes
urllib
re

These do not normally require separate installation.

Install Required Packages

Open Command Prompt / PowerShell / Terminal.

Run:

```python
pip install SpeechRecognition pyttsx3 requests screen-brightness-control PyAudio
```

If pip is not recognized, try:

```python
python -m pip install SpeechRecognition pyttsx3 requests screen-brightness-control PyAudio
```

On Windows, you can also try:

```python
py -m pip install SpeechRecognition pyttsx3 requests screen-brightness-control PyAudio
```

Install Packages One by One

If you prefer installing them separately:

```python
pip install SpeechRecognition

pip install pyttsx3

pip install requests

pip install screen-brightness-control

pip install PyAudio
```

Verify Installation

You can verify the installed packages with:

```python
pip list
```

Look for:

SpeechRecognition
PyAudio
pyttsx3
requests
screen-brightness-control

You can also test individual imports:

python -c "import speech_recognition"

python -c "import pyttsx3"

python -c "import requests"

python -c "import screen_brightness_control"

If the command returns without an error, the package is installed correctly.

PyAudio Installation Issue

On some Windows systems, PyAudio may show an installation error.

Try:

```python
python -m pip install --upgrade pip
```

Then:

```python
pip install PyAudio
```

If it still fails, check the Python version and architecture installed on your computer.

</details>
<details> <summary><strong>📥 How to Download and Run the Project</strong></summary>
## Step 1 — Clone the Repository

Open Terminal / Command Prompt and run:

```bash
git clone https://github.com/ishantSingh3142/AI-ASSISTANT-.git
```

Move into the project folder:

```bash
cd AI-ASSISTANT-
```

Step 2 — Install Dependencies

Run:

```python
pip install SpeechRecognition pyttsx3 requests screen-brightness-control PyAudio
```

Step 3 — Open the Project

Open the folder in VS Code, PyCharm, or another Python IDE.

The main Python file should look similar to:

```text
jarvis-ai-voice-assistant/
│
├── jarvis.py
├── images/
│   └── jarvis-ui.png
└── README.md
```

Step 4 — Run the Assistant

Run:

```python
python jarvis.py
```

If you use Windows and python does not work:

py jarvis.py

The JARVIS AI graphical interface should appear.

Step 5 — Allow Microphone Access

When you click:

🎙️ Tap to Speak

allow your computer to use the microphone if Windows asks for permission.

</details>
<details> <summary><strong>1️⃣ What Is This Project About?</strong></summary>

### JARVIS AI Voice Assistant is a desktop application created using Python

  It allows users to perform different tasks through voice commands instead of manually typing or navigating through applications.

  The project demonstrates how multiple Python technologies can be combined to create a practical voice-controlled application.

The assistant currently supports:

-Voice recognition
-Text-to-speech
-Web searching
-Wikipedia information
-YouTube searching
-Brightness control
-Volume control
-GUI interaction
</details>
<details> <summary><strong>2️⃣ Why Was This Project Designed?</strong></summary>

> This project was designed to explore how Python, voice recognition, automation, and APIs can work together to create a personal desktop assistant.

The main objectives are:

Learn practical Python development
Understand speech recognition
Work with APIs
Practice GUI development with Tkinter
Explore desktop automation
Create a real-world Python project
Build a foundation for a more advanced AI assistant

Rather than being only a simple command-line program, the project provides a graphical interface and voice-based interaction.

</details>
<details> <summary><strong>3️⃣ Who Can Use This?</strong></summary>

This project can be useful for:

🧑‍💻 Python beginners
🎓 Students learning programming
🛠️ Developers experimenting with automation
🤖 AI and voice-assistant enthusiasts
📚 Anyone interested in learning Python projects
💡 Developers who want a starting point for building their own assistant

The project can also be modified and extended according to individual requirements.

</details>
<details> <summary><strong>4️⃣ How to Use JARVIS</strong></summary>

After starting the application:

Step 1

Click:

🎙️ Tap to Speak

Step 2

Wait for JARVIS to say:

How can I help you?

Step 3

Speak a command.

Example Commands
🌐 Websites
Open Google

Open YouTube

Open Wikipedia

🔎 Google Search
Search Google Python programming

Google search artificial intelligence

▶️ YouTube
Play Arijit Singh on YouTube

Play Python tutorial on YouTube

Search YouTube cricket highlights

📖 Wikipedia
Wikipedia Albert Einstein

Wikipedia Mahatma Gandhi

Wikipedia Artificial Intelligence

JARVIS retrieves the Wikipedia summary and reads it aloud.

💡 Brightness
Increase brightness

Decrease brightness

Set brightness 50

🔊 Volume
Volume up

Volume down

Mute volume

</details>
<details> <summary><strong>5️⃣ Future Improvements</strong></summary>

This project is designed as a foundation that can be expanded with many additional features.

Planned / Possible Improvements

🗣️ Wake Word Detection

"Hey JARVIS" or "Jarvis" to activate the assistant without clicking the button.

🎵 Direct YouTube Playback

Automatically identify and play the requested video instead of only opening search results.

🌦️ Weather Information

Ask JARVIS about current weather and forecasts.

🕐 Time and Date

Voice commands for current time and date.

📂 Application Control

Open and close applications using voice commands.

💻 System Control

Shutdown, restart, sleep, and lock the computer through voice commands.

📁 File Management

Open, search, create, rename, and manage files using voice commands.

📧 Email Automation

Compose and send emails using voice commands.

💬 Messaging

Integration with messaging platforms.

🤖 AI Chat Capability

Integrate an AI model to make JARVIS capable of answering general questions conversationally.

🧠 Context Awareness

Allow JARVIS to understand follow-up commands and maintain conversation context.

🎨 Advanced GUI

Add animations, waveform visualization, themes, system monitoring, and a more futuristic JARVIS-style interface.

🔐 User Authentication

Add voice or PIN-based authentication for sensitive system commands.

🌍 Multilingual Support

Add Hindi and other language support for voice commands and responses.

The long-term goal is to evolve this project from a basic voice assistant into a more capable AI-powered personal desktop assistant.

</details>
---

## 📸 Project Preview

<p align="center">
  <img src="banner.jpg" alt="Jarvis Banner" width="100%">
</p>

---

## 📬 Connect With Me

- **GitHub**: [@ishantSingh3142](https://github.com/ishantSingh3142)
- **Repository**: [ishantSingh3142/AI-ASSISTANT-](https://github.com/ishantSingh3142/AI-ASSISTANT-)

---

## 🙏 Thank You

Thank you for visiting the **JARVIS AI Voice Assistant** project!

If you find this project useful or interesting:

- ⭐ **Star** the repository
- 🍴 **Fork** the repository
- 🐛 **Report issues**
- 💡 **Suggest improvements**

Contributions and suggestions are always welcome.

<p align="center">
  <strong>🤖 JARVIS AI — Your Voice, Your Assistant.</strong>
</p>
