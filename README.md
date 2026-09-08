<div align="center">

<img src="https://capsule-render.vercel.app/api?type=waving&color=0:0F2027,50:00A8FF,100:00C8FF&height=220&section=header&text=MARCUS&fontSize=80&fontColor=ffffff&fontAlignY=38&desc=PC%20Assistant%20%E2%80%94%20Think%20%E2%80%A2%20Assist%20%E2%80%A2%20Execute&descAlignY=58&descSize=20&animation=fadeIn" width="100%"/>

<a href="https://github.com/MUdevelops/Marcus-PC-Assistant">
  <img src="https://readme-typing-svg.demolab.com?font=Fira+Code&weight=600&size=26&duration=2600&pause=900&color=00C8FF&center=true&vCenter=true&width=750&lines=Hey+Marcus%2C+open+chrome...;Hey+Marcus%2C+set+a+timer+for+10+minutes...;Hey+Marcus%2C+take+a+screenshot...;Hey+Marcus%2C+what%27s+my+battery%3F;A+futuristic+Jarvis-style+Windows+voice+assistant." alt="Typing SVG" />
</a>

<br/>

<p>
  <img src="https://img.shields.io/badge/Python-3.11.9-00A8FF?style=for-the-badge&logo=python&logoColor=white&labelColor=0F2027" alt="Python 3.11.9">
  <img src="https://img.shields.io/badge/Platform-Windows-0078D4?style=for-the-badge&logo=windows&logoColor=white&labelColor=0F2027" alt="Windows">
  <img src="https://img.shields.io/badge/UI-CustomTkinter-00C8FF?style=for-the-badge&labelColor=0F2027" alt="CustomTkinter">
  <img src="https://img.shields.io/badge/License-MIT-00A8FF?style=for-the-badge&labelColor=0F2027" alt="MIT License">
</p>

<p>
  <img src="https://img.shields.io/github/stars/MUdevelops/Marcus-PC-Assistant?style=for-the-badge&color=00C8FF&labelColor=0F2027&logo=github" alt="Stars">
  <img src="https://img.shields.io/github/forks/MUdevelops/Marcus-PC-Assistant?style=for-the-badge&color=00A8FF&labelColor=0F2027&logo=github" alt="Forks">
  <img src="https://img.shields.io/github/last-commit/MUdevelops/Marcus-PC-Assistant?style=for-the-badge&color=00C8FF&labelColor=0F2027&logo=git" alt="Last Commit">
  <img src="https://img.shields.io/github/issues/MUdevelops/Marcus-PC-Assistant?style=for-the-badge&color=00A8FF&labelColor=0F2027" alt="Issues">
</p>

<p>
  <a href="#-introduction"><b>Introduction</b></a> •
  <a href="#-features"><b>Features</b></a> •
  <a href="#-how-marcus-works"><b>Architecture</b></a> •
  <a href="#-screenshots"><b>Screenshots</b></a> •
  <a href="#-installation"><b>Installation</b></a> •
  <a href="#-commands"><b>Commands</b></a> •
  <a href="#-roadmap"><b>Roadmap</b></a>
</p>

<img src="Screenshots/marcus-readme-animated.gif" alt="Marcus animated interface" width="100%">

</div>

<img src="https://capsule-render.vercel.app/api?type=rect&color=0:00A8FF,100:0F2027&height=3&width=100%" width="100%"/>

## 🤖 Introduction

> **Marcus** is a Windows desktop voice assistant built around a simple idea:
> **your computer should understand what you say and help you get things done.**

Marcus listens for voice commands, interprets them with a keyword/regex intent parser, executes the requested Windows action, and responds through offline text-to-speech — wrapped in a futuristic **neon-blue / black** desktop interface.

The project combines a striking visual identity with practical PC automation — from opening applications and controlling volume to taking screenshots, searching the web, managing timers, and performing protected system actions.

<div align="center">

### ✨ Design Language

| Element | Marcus Style |
|:---|:---|
| 🎨 **Visual theme** | Deep black / navy + electric cyan-blue |
| 🧠 **Personality** | Futuristic, direct, helpful |
| ⚡ **Interaction** | Voice-first, with optional manual UI input |
| 🖥️ **Interface** | CustomTkinter desktop UI |
| 🔊 **Voice input** | Google Web Speech API |
| 🗣️ **Voice output** | `pyttsx3` + Windows SAPI5 |
| 🛡️ **Safety** | Confirmation before destructive actions |
| 📝 **Diagnostics** | Rotating command/outcome logs |

</div>

<img src="https://capsule-render.vercel.app/api?type=rect&color=0:00A8FF,100:0F2027&height=3&width=100%" width="100%"/>

## 🚀 Features

<table>
<tr>
<td width="50%" valign="top">

### 🎙️ Voice Control
- Wake word support: **"Hey Marcus"**
- Speech-to-text via Google Web Speech API
- Offline text-to-speech via `pyttsx3`
- Direct command recognition (wake word optional)

### 🖥️ Windows Control
- Open apps, files, and folders
- Close / minimize / maximize / restore windows
- Switch between applications
- Volume control, mute / unmute
- Display brightness control
- Screenshots & webcam toggle
- Lock screen
- Sleep / restart / shutdown *(with confirmation)*
- Battery, Wi-Fi & disk space checks

</td>
<td width="50%" valign="top">

### 🌐 Web & Media
- Open websites
- Google search
- YouTube search

### ⏱️ Productivity
- Current date & time
- Named & unnamed timers
- Cancel / list active timers

### 🎨 Futuristic UI
- Responsive splash screen
- Neon-blue visual system
- Animated listening indicator
- Chat / transcript component
- Home • Apps • Tools • Settings navigation

### 🛡️ Safety First
Destructive actions — **close, sleep, restart, shutdown** — always require confirmation before executing.

</td>
</tr>
</table>

<img src="https://capsule-render.vercel.app/api?type=rect&color=0:00A8FF,100:0F2027&height=3&width=100%" width="100%"/>

## 🧩 How Marcus Works

<div align="center">

```mermaid
flowchart TD
    A["🎙️ Microphone"] --> B["Speech Recognition<br/>Google Web API"]
    B --> C["Intent Parser<br/>Keyword / Regex"]
    C --> D["Command Handler<br/>Files • System • Web • Productivity"]
    D --> E["Windows / Web<br/>Action Executed"]
    E --> F["🔊 Marcus TTS Response"]

    style A fill:#0F2027,stroke:#00C8FF,stroke-width:2px,color:#00C8FF
    style B fill:#0F2027,stroke:#00A8FF,stroke-width:2px,color:#00A8FF
    style C fill:#0F2027,stroke:#00C8FF,stroke-width:2px,color:#00C8FF
    style D fill:#0F2027,stroke:#00A8FF,stroke-width:2px,color:#00A8FF
    style E fill:#0F2027,stroke:#00C8FF,stroke-width:2px,color:#00C8FF
    style F fill:#0F2027,stroke:#00A8FF,stroke-width:2px,color:#00A8FF
```

</div>

<img src="https://capsule-render.vercel.app/api?type=rect&color=0:00A8FF,100:0F2027&height=3&width=100%" width="100%"/>

## 🛠️ Technology Stack

<div align="center">

<p>
  <img src="https://img.shields.io/badge/Python-3776AB?style=flat-square&logo=python&logoColor=white" alt="Python"/>
  <img src="https://img.shields.io/badge/CustomTkinter-00C8FF?style=flat-square" alt="CustomTkinter"/>
  <img src="https://img.shields.io/badge/SpeechRecognition-00A8FF?style=flat-square" alt="SpeechRecognition"/>
  <img src="https://img.shields.io/badge/pyttsx3-0F2027?style=flat-square" alt="pyttsx3"/>
  <img src="https://img.shields.io/badge/PyAudio-00C8FF?style=flat-square" alt="PyAudio"/>
  <img src="https://img.shields.io/badge/Pillow-00A8FF?style=flat-square&logo=python&logoColor=white" alt="Pillow"/>
  <img src="https://img.shields.io/badge/pycaw%20%2F%20comtypes-0F2027?style=flat-square" alt="pycaw"/>
  <img src="https://img.shields.io/badge/psutil-00C8FF?style=flat-square" alt="psutil"/>
  <img src="https://img.shields.io/badge/pyautogui-00A8FF?style=flat-square" alt="pyautogui"/>
  <img src="https://img.shields.io/badge/pywin32-0F2027?style=flat-square&logo=windows&logoColor=white" alt="pywin32"/>
  <img src="https://img.shields.io/badge/python--dotenv-00C8FF?style=flat-square" alt="dotenv"/>
</p>

</div>

| Layer | Technology |
|:---|:---|
| Language | **Python 3.11.9** |
| Speech Recognition | `SpeechRecognition` |
| Microphone | `PyAudio` |
| Text-to-Speech | `pyttsx3` |
| Desktop UI | `CustomTkinter` |
| Image Processing | `Pillow` |
| Windows Audio | `pycaw` / `comtypes` |
| Brightness | `screen-brightness-control` |
| System Information | `psutil` |
| Automation | `pyautogui` |
| Windows Integration | `pywin32` |
| Configuration | `python-dotenv` |

All dependencies are pinned in [`requirements.txt`](requirements.txt).

<img src="https://capsule-render.vercel.app/api?type=rect&color=0:00A8FF,100:0F2027&height=3&width=100%" width="100%"/>

## 📸 Screenshots

<div align="center">

<table>
<tr>
<td align="center" width="50%">
<b>🌌 Main Interface</b><br/><br/>
<img src="Screenshots/Main%20Interface.png" width="100%">
<br/><sub>Marcus's primary desktop interface — the central command environment.</sub>
</td>
<td align="center" width="50%">
<b>🗣️ Manual Command</b><br/><br/>
<img src="Screenshots/Manual%20Command.png" width="100%">
<br/><sub>Manual command input when voice interaction isn't convenient.</sub>
</td>
</tr>
<tr>
<td align="center" width="50%">
<b>🎙️ Ready to Assist</b><br/><br/>
<img src="Screenshots/Ready%20to%20Assist.png" width="100%">
<br/><sub>Visual state showing Marcus is ready for your next command.</sub>
</td>
<td align="center" width="50%">
<b>⚙️ Settings</b><br/><br/>
<img src="Screenshots/Setting.png" width="100%">
<br/><sub>Configure Marcus from the dedicated settings interface.</sub>
</td>
</tr>
<tr>
<td align="center" width="50%">
<b>🧰 Tools</b><br/><br/>
<img src="Screenshots/Tools.png" width="100%">
<br/><sub>Tools and utility controls available from the Marcus interface.</sub>
</td>
<td align="center" width="50%">
<b>🚀 Splash Screen</b><br/><br/>
<img src="Screenshots/Splash%20Screen.png" width="100%">
<br/><sub>A responsive futuristic splash experience on launch.</sub>
</td>
</tr>
</table>

<b>🧠 Marcus Info</b><br/><br/>
<img src="Screenshots/Marcus%20Info%20Readme.file.png" width="70%">
<br/><sub>The Marcus visual identity and introduction artwork that inspired this README's presentation.</sub>

</div>

<img src="https://capsule-render.vercel.app/api?type=rect&color=0:00A8FF,100:0F2027&height=3&width=100%" width="100%"/>

## 💬 Commands

<details open>
<summary><b>📁 Files & Applications</b></summary>

```text
Hey Marcus, open chrome
open notepad
open downloads
close notepad
close the active window
minimize
maximize
restore the window
switch to chrome
```
</details>

<details>
<summary><b>🖥️ System</b></summary>

```text
brightness up
brightness down
set brightness to 70

volume up
volume down
mute
unmute
set volume to 40

take a screenshot
open the camera
close the camera
lock the screen

go to sleep
shut down
restart

what's my battery
check wifi
disk space
```
</details>

<details>
<summary><b>🌐 Web</b></summary>

```text
go to github.com
open the website reddit
search google for python tutorials
search youtube for lofi beats
```
</details>

<details>
<summary><b>⏱️ Productivity</b></summary>

```text
what time is it

set a timer for 10 minutes
set a timer for 5 minutes for pasta

cancel the pasta timer
list timers
```
</details>

<img src="https://capsule-render.vercel.app/api?type=rect&color=0:00A8FF,100:0F2027&height=3&width=100%" width="100%"/>

## 📦 Installation

<table>
<tr><td>

**1. Clone the repository**
```bash
git clone https://github.com/MUdevelops/Marcus-PC-Assistant.git
cd Marcus-PC-Assistant
```

**2. Create a virtual environment**
```bash
python -m venv venv
venv\Scripts\activate
```

**3. Install PyAudio**

On Windows, PyAudio may fail to build from source — install it through `pipwin` first:
```bash
pip install pipwin
pipwin install pyaudio
```

**4. Install the remaining dependencies**
```bash
pip install -r requirements.txt
```

**5. Launch Marcus**
```bash
python main.py
```

**Optional modes**
```bash
python main.py --ui
python main.py --console
```

</td></tr>
</table>

### ⚙️ Configuration

Wake-word-only operation can be enabled in `config.py`:

```python
REQUIRE_WAKE_WORD = True
```

When enabled, Marcus requires **"Hey Marcus"** before processing a command.

<img src="https://capsule-render.vercel.app/api?type=rect&color=0:00A8FF,100:0F2027&height=3&width=100%" width="100%"/>

## 🧱 Project Architecture

```text
Marcus-PC-Assistant/
│
├── commands/
│   ├── files_apps.py
│   ├── system.py
│   ├── media_web.py
│   └── productivity.py
│
├── ui/
│   ├── app.py
│   ├── theme.py
│   ├── assets/
│   └── components/
│       ├── sidebar.py
│       ├── chat_bubble.py
│       └── mic_button.py
│
├── utils/
│   ├── confirmation.py
│   └── window_utils.py
│
├── logs/
│   └── marcus.log
│
├── main.py
├── config.py
├── listener.py
├── speaker.py
├── intent_parser.py
├── logger_setup.py
├── requirements.txt
└── README.md
```

<img src="https://capsule-render.vercel.app/api?type=rect&color=0:00A8FF,100:0F2027&height=3&width=100%" width="100%"/>

## 🔧 Extending Marcus

| Task | Where |
|:---|:---|
| Add a known application | `commands/files_apps.py` → `KNOWN_APPS` |
| Add a file/folder shortcut | `commands/files_apps.py` → `KNOWN_PATHS` |
| Add a new voice phrase | `intent_parser.py` — add a new regex pattern + handler |
| Add new UI sections | `ui/app.py` → `_on_nav_select()` connects new **Apps / Tools / Settings** views |

> ⚠️ Patterns in `intent_parser.py` are checked **top-to-bottom**, and the first match wins — so more specific patterns should be listed before general ones.

<img src="https://capsule-render.vercel.app/api?type=rect&color=0:00A8FF,100:0F2027&height=3&width=100%" width="100%"/>

## 🧪 Testing Individual Components

```bash
python speaker.py
python listener.py
python ui/app.py
python main.py
```

These commands give focused ways to test the TTS engine, listener, UI, and complete application independently.

<img src="https://capsule-render.vercel.app/api?type=rect&color=0:00A8FF,100:0F2027&height=3&width=100%" width="100%"/>

## 📝 Logging & Troubleshooting

Marcus records recognized commands and their outcomes in `logs/marcus.log`. If a command doesn't behave as expected, check the log first.

**Windows notes**
- Most standard actions do not require administrator rights.
- Some interactions with elevated applications may require elevated privileges.
- Brightness support depends on the display exposing WMI or DDC/CI controls.
- External monitors may not support brightness adjustment.
- Windows Core Audio functions use COM through `pycaw`.

<img src="https://capsule-render.vercel.app/api?type=rect&color=0:00A8FF,100:0F2027&height=3&width=100%" width="100%"/>

## 🛡️ Responsible Automation

Marcus is designed to make everyday PC interaction faster **without removing user control**.

Destructive operations use confirmation handling, and closing an application sends a normal Windows close request rather than forcibly killing the process — so applications can still display their own **"Save changes?"** dialogs.

<img src="https://capsule-render.vercel.app/api?type=rect&color=0:00A8FF,100:0F2027&height=3&width=100%" width="100%"/>

## 🗺️ Roadmap

- [ ] More natural-language intent understanding
- [ ] More customizable commands
- [ ] Expanded Apps / Tools / Settings panels
- [ ] More visual assistant states
- [ ] Custom wake-word engine
- [ ] Offline speech recognition option
- [ ] Plugin-style command modules
- [ ] User-configurable themes
- [ ] More productivity integrations

<img src="https://capsule-render.vercel.app/api?type=rect&color=0:00A8FF,100:0F2027&height=3&width=100%" width="100%"/>

## 🤝 Contributing

Contributions are welcome! Feel free to open an issue or submit a pull request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

<img src="https://capsule-render.vercel.app/api?type=rect&color=0:00A8FF,100:0F2027&height=3&width=100%" width="100%"/>

## 📄 License

This project is licensed under the **MIT License** — see [`LICENSE`](LICENSE) for details.

<div align="center">

<img src="https://capsule-render.vercel.app/api?type=waving&color=0:00C8FF,50:00A8FF,100:0F2027&height=160&section=footer&text=Think%20%E2%86%92%20Assist%20%E2%86%92%20Execute&fontSize=24&fontColor=ffffff&animation=fadeIn" width="100%"/>

**Your digital partner. Always on your side.**

<a href="https://github.com/MUdevelops/Marcus-PC-Assistant">
  <img src="https://img.shields.io/badge/GitHub-Marcus--PC--Assistant-00A8FF?style=for-the-badge&logo=github&logoColor=white" alt="GitHub Repository">
</a>

**If Marcus helps you, consider giving the repository a ⭐**

</div>
