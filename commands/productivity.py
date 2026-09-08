"""
commands/productivity.py
Date/time readback and simple spoken-alert timers/reminders.

Timers run on background threading.Timer instances, so "set a timer
for 5 minutes" returns immediately (Marcus keeps listening for other
commands) and speaks an alert when it fires. This module keeps a
registry of active timers so they can be listed/cancelled later.
"""

import threading
from datetime import datetime

from speaker import speak
from logger_setup import get_logger

log = get_logger(__name__)

# label -> threading.Timer, so timers can be looked up/cancelled.
_active_timers: dict[str, threading.Timer] = {}
_timer_lock = threading.Lock()


def get_current_datetime() -> str:
    now = datetime.now()
    return now.strftime("It's %I:%M %p on %A, %B %d.")


def _fire_timer(label: str, duration_desc: str):
    speak(f"Time's up on your {duration_desc} timer{(' — ' + label) if label else ''}.")
    with _timer_lock:
        _active_timers.pop(label or duration_desc, None)


def set_timer(minutes: float, label: str = "") -> str:
    """Starts a timer for `minutes` minutes. `label` lets you set more
    than one concurrent timer (e.g. 'pasta' vs 'laundry')."""
    if minutes <= 0:
        return "I need a positive number of minutes for that timer."

    duration_desc = (
        f"{minutes:g} minute" if minutes == 1 else f"{minutes:g} minute"
    )
    key = label or duration_desc

    seconds = minutes * 60
    timer = threading.Timer(seconds, _fire_timer, args=(label, duration_desc))
    timer.daemon = True

    with _timer_lock:
        _active_timers[key] = timer
    timer.start()

    log.info("Timer started: %s (%.1f min)", key, minutes)
    label_phrase = f" for {label}" if label else ""
    return f"Timer set{label_phrase} for {duration_desc}."


def cancel_timer(label: str = "") -> str:
    with _timer_lock:
        timer = _active_timers.pop(label, None)
    if not timer:
        return f"I couldn't find an active timer{' called ' + label if label else ''}."
    timer.cancel()
    log.info("Timer cancelled: %s", label)
    return f"Cancelled the {label or ''} timer.".replace("  ", " ")


def list_active_timers() -> str:
    with _timer_lock:
        labels = list(_active_timers.keys())
    if not labels:
        return "You don't have any active timers."
    return "Active timers: " + ", ".join(labels) + "."
