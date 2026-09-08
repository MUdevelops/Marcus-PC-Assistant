"""
utils/window_utils.py
Thin wrapper around pywin32 for finding, activating, and manipulating
windows by title. Kept separate from commands/files_apps.py so the
Win32-specific plumbing doesn't clutter the command logic.

Windows-specific note: some operations (e.g. activating a window that
belongs to a process running as Administrator) will silently fail if
Marcus itself is NOT running elevated. If "switch to X" stops working
only for one specific app, that's almost always why — run Marcus as
admin, or run that app as a normal user.
"""

import win32gui
import win32con
import win32process
import psutil

from logger_setup import get_logger

log = get_logger(__name__)


def _enum_windows():
    """Yields (hwnd, title) for every visible top-level window with a
    non-empty title."""
    results = []

    def _callback(hwnd, _):
        if win32gui.IsWindowVisible(hwnd):
            title = win32gui.GetWindowText(hwnd)
            if title.strip():
                results.append((hwnd, title))
        return True

    win32gui.EnumWindows(_callback, None)
    return results


def find_window_by_partial_title(partial_title: str):
    """Case-insensitive substring match against all visible window
    titles. Returns (hwnd, full_title) for the first match, or None."""
    partial_title = partial_title.lower().strip()
    for hwnd, title in _enum_windows():
        if partial_title in title.lower():
            return hwnd, title
    return None


def get_active_window():
    """Returns (hwnd, title) for the currently focused window."""
    hwnd = win32gui.GetForegroundWindow()
    title = win32gui.GetWindowText(hwnd)
    return hwnd, title


def activate_window(hwnd) -> bool:
    """Brings a window to the foreground and restores it if minimized."""
    try:
        if win32gui.IsIconic(hwnd):
            win32gui.ShowWindow(hwnd, win32con.SW_RESTORE)
        win32gui.SetForegroundWindow(hwnd)
        return True
    except Exception:
        log.exception("Failed to activate window handle %s", hwnd)
        return False


def minimize_window(hwnd) -> bool:
    try:
        win32gui.ShowWindow(hwnd, win32con.SW_MINIMIZE)
        return True
    except Exception:
        log.exception("Failed to minimize window handle %s", hwnd)
        return False


def maximize_window(hwnd) -> bool:
    try:
        win32gui.ShowWindow(hwnd, win32con.SW_MAXIMIZE)
        return True
    except Exception:
        log.exception("Failed to maximize window handle %s", hwnd)
        return False


def restore_window(hwnd) -> bool:
    try:
        win32gui.ShowWindow(hwnd, win32con.SW_RESTORE)
        return True
    except Exception:
        log.exception("Failed to restore window handle %s", hwnd)
        return False


def close_window(hwnd) -> bool:
    """Sends a polite WM_CLOSE (same as clicking the X) rather than
    force-killing the process, so apps get a chance to prompt for
    unsaved work."""
    try:
        win32gui.PostMessage(hwnd, win32con.WM_CLOSE, 0, 0)
        return True
    except Exception:
        log.exception("Failed to close window handle %s", hwnd)
        return False


def get_pid_for_window(hwnd) -> int | None:
    try:
        _, pid = win32process.GetWindowThreadProcessId(hwnd)
        return pid
    except Exception:
        return None


def kill_process_by_name(process_name: str) -> bool:
    """Force-kills all processes matching process_name (e.g. 'notepad.exe').
    Used only as a fallback when a polite WM_CLOSE doesn't work, or for
    background apps with no visible window (e.g. camera preview)."""
    process_name = process_name.lower()
    killed = False
    for proc in psutil.process_iter(["pid", "name"]):
        try:
            if proc.info["name"] and proc.info["name"].lower() == process_name:
                proc.kill()
                killed = True
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue
    return killed


def list_open_window_titles() -> list[str]:
    return [title for _, title in _enum_windows()]
