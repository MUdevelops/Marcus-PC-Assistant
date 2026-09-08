"""
commands/files_apps.py
File & app control: open files/folders/apps by name, and manage
windows (close/minimize/maximize/restore/switch).

Windows-specific notes:
- Launching apps uses `os.startfile`, which is the same mechanism as
  double-clicking in Explorer — no admin rights needed.
- KNOWN_APPS below is a name -> launch-target map. Add your own paths
  for apps that aren't on PATH (e.g. Steam, Discord install elsewhere
  per machine) by editing this dict.
- Closing a window sends WM_CLOSE (same as clicking the X) so apps get
  a chance to prompt "save changes?" — Marcus does NOT auto-dismiss
  that prompt, by design, so you never silently lose work.
"""

import os
import subprocess

from logger_setup import get_logger
from utils import window_utils

log = get_logger(__name__)

# Map of spoken app names -> either a bare executable (must be on PATH)
# or a full path. Extend this as needed for your machine.
KNOWN_APPS = {
    "chrome": "chrome",
    "google chrome": "chrome",
    "vs code": "code",
    "visual studio code": "code",
    "vscode": "code",
    "notepad": "notepad.exe",
    "notepad plus plus": "notepad++.exe",
    "word": "winword.exe",
    "excel": "excel.exe",
    "powerpoint": "powerpnt.exe",
    "calculator": "calc.exe",
    "paint": "mspaint.exe",
    "explorer": "explorer.exe",
    "file explorer": "explorer.exe",
    "task manager": "taskmgr.exe",
    "spotify": "spotify.exe",
    "discord": "discord.exe",
    "camera": "microsoft.windows.camera:",
    "settings": "ms-settings:",
}

# Common shortcuts spoken commands might reference. Add your own.
KNOWN_PATHS = {
    "downloads": os.path.join(os.path.expanduser("~"), "Downloads"),
    "documents": os.path.join(os.path.expanduser("~"), "Documents"),
    "desktop": os.path.join(os.path.expanduser("~"), "Desktop"),
    "pictures": os.path.join(os.path.expanduser("~"), "Pictures"),
    # Example — point this at your actual resume file/folder:
    "resume": os.path.join(os.path.expanduser("~"), "Documents", "Resume.pdf"),
}


def open_app(app_name: str) -> str:
    """Launches an installed application by spoken name. Returns a
    response string to speak back."""
    key = app_name.lower().strip()
    target = KNOWN_APPS.get(key)

    if not target:
        log.warning("open_app: %r not found in KNOWN_APPS", app_name)
        return (
            f"I don't have {app_name} mapped to a launch command yet. "
            f"You can add it to KNOWN_APPS in commands/files_apps.py."
        )

    try:
        if target.endswith(":"):
            # UWP app protocol (e.g. ms-settings:, camera:)
            os.startfile(target)
        else:
            os.startfile(target)
        log.info("Launched app: %s -> %s", app_name, target)
        return f"Opening {app_name}."
    except FileNotFoundError:
        log.error("open_app: executable not found on PATH: %s", target)
        return (
            f"I couldn't find {app_name} on this system's PATH. "
            f"Try adding its full .exe path to KNOWN_APPS."
        )
    except Exception:
        log.exception("open_app: unexpected failure launching %s", app_name)
        return f"Something went wrong trying to open {app_name}."


def open_file_or_folder(name: str) -> str:
    """Opens a known shortcut (KNOWN_PATHS) or a literal path spoken
    aloud. Voice recognition won't produce perfect file paths, so this
    is realistically most useful for a handful of named shortcuts —
    extend KNOWN_PATHS with your own frequently used files/folders."""
    key = name.lower().strip()
    path = KNOWN_PATHS.get(key, name)

    if not os.path.exists(path):
        log.warning("open_file_or_folder: path does not exist: %s", path)
        return (
            f"I couldn't find {name}. If this is a file or folder you "
            f"open often, add it to KNOWN_PATHS in commands/files_apps.py "
            f"so I recognize it by name."
        )

    try:
        os.startfile(path)
        log.info("Opened file/folder: %s -> %s", name, path)
        return f"Opening {name}."
    except Exception:
        log.exception("open_file_or_folder: failed to open %s", path)
        return f"I found {name} but couldn't open it."


def close_active_window() -> str:
    hwnd, title = window_utils.get_active_window()
    if not hwnd or not title:
        return "I couldn't tell what window is currently active."
    window_utils.close_window(hwnd)
    log.info("Closed active window: %s", title)
    return f"Closing {title}."


def close_named_window(name: str) -> str:
    match = window_utils.find_window_by_partial_title(name)
    if not match:
        return f"I couldn't find a window matching {name}."
    hwnd, title = match
    window_utils.close_window(hwnd)
    log.info("Closed window: %s", title)
    return f"Closing {title}."


def minimize_active_window() -> str:
    hwnd, title = window_utils.get_active_window()
    if not hwnd:
        return "I couldn't tell what window is currently active."
    window_utils.minimize_window(hwnd)
    return f"Minimized {title}."


def maximize_active_window() -> str:
    hwnd, title = window_utils.get_active_window()
    if not hwnd:
        return "I couldn't tell what window is currently active."
    window_utils.maximize_window(hwnd)
    return f"Maximized {title}."


def restore_active_window() -> str:
    hwnd, title = window_utils.get_active_window()
    if not hwnd:
        return "I couldn't tell what window is currently active."
    window_utils.restore_window(hwnd)
    return f"Restored {title}."


def switch_to_window(name: str) -> str:
    match = window_utils.find_window_by_partial_title(name)
    if not match:
        return f"I couldn't find a window matching {name}."
    hwnd, title = match
    window_utils.activate_window(hwnd)
    log.info("Switched to window: %s", title)
    return f"Switching to {title}."
