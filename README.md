# Marcus — PC Assistant

A Jarvis-style Windows voice assistant. Wake word: **"Hey Marcus"**.
Speech recognition: Google Web Speech API (free, needs internet).
Text-to-speech: pyttsx3 (offline, uses Windows SAPI5 voices).

## Project layout

```
marcus/
├── main.py                # main listen → parse → execute → respond loop
├── config.py               # paths, wake word, thresholds, feature flags
├── listener.py              # mic input + speech-to-text
├── speaker.py                # pyttsx3 TTS wrapper
├── intent_parser.py        # keyword/regex → command function mapping
├── logger_setup.py           # rotating file logger for commands/outcomes
│
├── commands/
│   ├── files_apps.py         # open file/folder, launch app, close/min/max/switch window
│   ├── system.py            # brightness, volume, screenshot, webcam, lock/sleep/shutdown/restart, battery/wifi/disk
│   ├── media_web.py           # browser open, Google/YouTube search
│   └── productivity.py      # date/time, reminders/timers
│
├── ui/
│   ├── app.py                # main UI window (CustomTkinter)
│   ├── theme.py               # colors, fonts, glow styling from the splash art
│   ├── assets/                # logo, mascot, icons
│   └── components/
│       ├── sidebar.py         # Home / Apps / Tools / Settings nav
│       ├── chat_bubble.py      # transcript panel
│       └── mic_button.py      # animated listening indicator
│
├── utils/
│   ├── confirmation.py       # spoken/typed confirm-before-destructive-action helper
│   └── window_utils.py       # pywin32 helpers for active window/title lookup
│
├── logs/
│   └── marcus.log
├── requirements.txt
└── README.md
```

## Setup (Windows, Python 3.11.9)

```powershell
cd marcus
python -m venv venv
venv\Scripts\activate

# pyaudio often fails to build from source on Windows — install via pipwin first:
pip install pipwin
pipwin install pyaudio

# then everything else:
pip install -r requirements.txt
```

If `pipwin install pyaudio` fails, download the matching `.whl` from
https://www.lfd.uci.edu/~gohlke/pythonlibs/#pyaudio (match your Python
version, 64-bit) and `pip install path\to\that.whl`.

## Running it

```powershell
# Voice + visual UI with responsive splash and Main Menu artwork:
python main.py

# The --ui form remains supported as an explicit alias:
python main.py --ui

# Voice-only console mode:
python main.py --console
```

Say a supported command directly, such as **"volume up"**, or say
**"Hey Marcus"** followed by a command. See the command list below for
what's supported out of the box. Set `REQUIRE_WAKE_WORD = True` in
`config.py` if you want wake-word-only operation.

## Windows-specific notes (read this before running)

- **No admin rights needed** for: opening apps/files, volume, brightness,
  screenshots, webcam, lock screen, shutdown/restart/sleep (these use
  the standard `shutdown.exe`, which works for the current user), web
  search, timers.
- **Admin rights may be needed** only if you're trying to switch to /
  close a window belonging to an app that is *itself* running elevated
  (e.g. an admin Command Prompt). If "switch to X" silently fails only
  for one app, that's almost always why.
- **Brightness control** only works on displays that expose brightness
  via WMI or DDC/CI. Most laptop screens work; some external monitors
  don't respond — you'll get a spoken error rather than a crash.
- **Volume control (pycaw)** uses Windows' COM-based Core Audio API.
  COM needs per-thread init; the shipped code only calls volume
  functions from threads that already have COM available by default,
  so you shouldn't hit this — but if you extend it into a new
  background thread later and get a COM error, add
  `comtypes.CoInitialize()` at the top of that thread's function.
- **Closing windows is "polite"**: Marcus sends the same WM_CLOSE
  signal as clicking the X button, so apps with unsaved work will show
  their own "Save changes?" dialog — Marcus does not auto-dismiss it.
  Combined with the required confirmation step, this means you get two
  layers of protection against losing work.

## Command reference (what you can say)

**Files & apps**
- "Hey Marcus, open chrome" / "open notepad" / "open downloads"
- "close notepad" / "close the active window" *(asks to confirm)*
- "minimize" / "maximize" / "restore the window"
- "switch to chrome"

**System**
- "brightness up" / "brightness down" / "set brightness to 70"
- "volume up" / "volume down" / "mute" / "unmute" / "set volume to 40"
- "take a screenshot"
- "open the camera" / "close the camera"
- "lock the screen"
- "go to sleep" / "shut down" / "restart" *(all ask to confirm)*
- "what's my battery" / "check wifi" / "disk space"

**Web**
- "go to github.com" / "open the website reddit"
- "search google for python tutorials"
- "search youtube for lofi beats"

**Productivity**
- "what time is it"
- "set a timer for 10 minutes" / "set a timer for 5 minutes for pasta"
- "cancel the pasta timer" / "list timers"

## Extending it

- New app names: add to `KNOWN_APPS` in `commands/files_apps.py`.
- New file/folder shortcuts: add to `KNOWN_PATHS` in the same file.
- New voice phrasing: add a regex + handler to `_PATTERNS` in
  `intent_parser.py` — patterns are checked top-to-bottom, first match
  wins, so keep specific patterns above general ones.
- New UI sections (Apps/Tools/Settings panels): `ui/app.py`'s
  `_on_nav_select()` is the hook point — currently all sidebar items
  show the same Home view.

## Testing individual pieces

```powershell
python speaker.py      # lists system TTS voices, speaks a test line
python listener.py     # tests wake word + one command capture
python ui/app.py        # UI-only preview with no mic needed
python main.py          # full thing: voice engine + UI together
```

The UI loads `Main Menu.jpg` as its responsive background, with PNG/JPEG
fallback support. Startup uses
`Splash.png` when present and falls back to the included `Splash Screen.png`.
Both images are contained proportionally so they are never stretched or
distorted when the window is resized.

Every recognized command and its outcome is logged to `logs/marcus.log`
— check there first if something doesn't behave as expected.
