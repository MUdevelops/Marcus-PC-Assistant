"""
intent_parser.py
Maps recognized speech text to the right command function. Intentionally
simple keyword/regex matching, not ML — this is easy to extend, easy to
debug, and easy for you to read. Patterns are checked in order, first
match wins, so put more specific patterns above more general ones.

Every entry point is `handle_command(text, listener) -> str`, called
from main.py with the raw lowercase transcript. `listener` is passed
through so destructive actions can route through
utils/confirmation.py's confirm_action() without opening a second mic
stream.
"""

import re

from commands import files_apps, system, media_web, productivity
from utils.confirmation import confirm_action
from logger_setup import get_logger

log = get_logger(__name__)


def _extract_number(text: str, default=None):
    match = re.search(r"(\d+(?:\.\d+)?)", text)
    return float(match.group(1)) if match else default


def _normalize_command(text: str) -> str:
    """Remove conversational filler while preserving the user's intent."""
    normalized = re.sub(r"[^a-z0-9.\s]", " ", text.lower())
    normalized = re.sub(
        r"^(?:please|could you|can you|would you|will you|marcus|hey marcus)\s+",
        "",
        normalized,
    )
    normalized = re.sub(r"\s+", " ", normalized).strip()
    return normalized


# ---------------------------------------------------------------------
# Individual handlers — each takes the regex match + listener, returns
# a response string to speak.
# ---------------------------------------------------------------------

def _h_open(match, listener):
    target = match.group(1).strip()
    # Try known app names first; fall back to file/folder lookup.
    if target in files_apps.KNOWN_APPS:
        return files_apps.open_app(target)
    if target in files_apps.KNOWN_PATHS:
        return files_apps.open_file_or_folder(target)
    # Unknown name: guess app first (covers "open chrome" style phrasing
    # for apps not yet in KNOWN_APPS but present on PATH), then file.
    app_result = files_apps.open_app(target)
    if "don't have" not in app_result and "couldn't find" not in app_result:
        return app_result
    return files_apps.open_file_or_folder(target)


def _h_close_active(match, listener):
    if confirm_action(
        "That window might have unsaved work. Close it anyway?", listener
    ):
        return files_apps.close_active_window()
    return "Okay, leaving it open."


def _h_close_named(match, listener):
    name = match.group(1).strip()
    if confirm_action(f"Close {name}? It might have unsaved work.", listener):
        return files_apps.close_named_window(name)
    return "Okay, leaving it open."


def _h_minimize(match, listener):
    return files_apps.minimize_active_window()


def _h_maximize(match, listener):
    return files_apps.maximize_active_window()


def _h_restore(match, listener):
    return files_apps.restore_active_window()


def _h_switch(match, listener):
    return files_apps.switch_to_window(match.group(1).strip())


def _h_brightness_set(match, listener):
    return system.set_brightness(int(_extract_number(match.group(0), 50)))


def _h_brightness_up(match, listener):
    return system.adjust_brightness(+10)


def _h_brightness_down(match, listener):
    return system.adjust_brightness(-10)


def _h_volume_set(match, listener):
    return system.set_volume(int(_extract_number(match.group(0), 50)))


def _h_volume_up(match, listener):
    return system.adjust_volume(+10)


def _h_volume_down(match, listener):
    return system.adjust_volume(-10)


def _h_mute(match, listener):
    return system.mute_volume()


def _h_unmute(match, listener):
    return system.unmute_volume()


def _h_screenshot(match, listener):
    return system.take_screenshot()


def _h_webcam_open(match, listener):
    return system.open_webcam()


def _h_webcam_close(match, listener):
    return system.close_webcam()


def _h_lock(match, listener):
    return system.lock_screen()


def _h_sleep(match, listener):
    if confirm_action("Put the system to sleep now?", listener):
        return system.sleep_system()
    return "Okay, staying awake."


def _h_shutdown(match, listener):
    if confirm_action("Are you sure you want to shut down the system?", listener):
        return system.shutdown_system()
    return "Okay, cancelling shutdown."


def _h_restart(match, listener):
    if confirm_action("Are you sure you want to restart the system?", listener):
        return system.restart_system()
    return "Okay, cancelling restart."


def _h_battery(match, listener):
    return system.get_battery_status()


def _h_wifi(match, listener):
    return system.get_wifi_status()


def _h_disk(match, listener):
    return system.get_disk_space()


def _h_website(match, listener):
    return media_web.open_website(match.group(1).strip())


def _h_search_google(match, listener):
    return media_web.search_google(match.group(1).strip())


def _h_search_youtube(match, listener):
    return media_web.search_youtube(match.group(1).strip())


def _h_datetime(match, listener):
    return productivity.get_current_datetime()


def _h_set_timer(match, listener):
    minutes = _extract_number(match.group(1), None)
    if minutes is None:
        return "How many minutes should the timer be for?"
    # Named group "label" only exists in the "... for <label>" phrasing,
    # e.g. "set a timer for 5 minutes for pasta" -> label="pasta".
    label = (match.group("label") or "").strip()
    return productivity.set_timer(minutes, label)


def _h_cancel_timer(match, listener):
    label = match.group(1).strip() if match.lastindex else ""
    return productivity.cancel_timer(label)


def _h_list_timers(match, listener):
    return productivity.list_active_timers()


# ---------------------------------------------------------------------
# Ordered pattern table. First match wins — specific patterns first.
# ---------------------------------------------------------------------

_PATTERNS = [
    # Timers / productivity (before generic "set ... to" patterns)
    (re.compile(r"cancel (?:the )?(.+?) timer"), _h_cancel_timer),
    (re.compile(r"list (?:active )?timers"), _h_list_timers),
    (re.compile(r"set (?:a )?timer for (\d+(?:\.\d+)?)\s*minutes?(?:\s+for\s+(?P<label>.+))?"), _h_set_timer),
    (re.compile(r"what(?:'s| is) the (?:time|date)"), _h_datetime),
    (re.compile(r"what time is it"), _h_datetime),

    # Web / search
    (re.compile(r"search (?:google|the web) for (.+)"), _h_search_google),
    (re.compile(r"google (.+)"), _h_search_google),
    (re.compile(r"search youtube for (.+)"), _h_search_youtube),
    (re.compile(r"open (?:the )?website (.+)"), _h_website),
    (re.compile(r"go to (.+\.\w{2,})"), _h_website),

    # System info
    (re.compile(r"battery"), _h_battery),
    (re.compile(r"wi[- ]?fi"), _h_wifi),
    (re.compile(r"disk space"), _h_disk),

    # Screenshot / webcam
    (re.compile(r"take a screenshot"), _h_screenshot),
    (re.compile(r"open (?:the )?(?:webcam|camera)"), _h_webcam_open),
    (re.compile(r"close (?:the )?(?:webcam|camera)"), _h_webcam_close),

    # Power state (destructive — confirmation happens inside handler)
    (re.compile(r"lock (?:the )?screen"), _h_lock),
    (re.compile(r"(?:go to )?sleep"), _h_sleep),
    (re.compile(r"shut ?down"), _h_shutdown),
    (re.compile(r"restart"), _h_restart),

    # Brightness
    (re.compile(r"brightness (?:to )?(\d+)"), _h_brightness_set),
    (re.compile(r"set brightness to (\d+)"), _h_brightness_set),
    (re.compile(r"brightness up|increase (?:the )?brightness|brighten|turn (?:the )?brightness up"), _h_brightness_up),
    (re.compile(r"brightness down|decrease (?:the )?brightness|dim|turn (?:the )?brightness down"), _h_brightness_down),

    # Volume
    (re.compile(r"volume (?:to )?(\d+)"), _h_volume_set),
    (re.compile(r"set volume to (\d+)"), _h_volume_set),
    (re.compile(r"volume up|increase (?:the )?volume|louder|turn (?:the )?volume up"), _h_volume_up),
    (re.compile(r"volume down|decrease (?:the )?volume|quieter|turn (?:the )?volume down"), _h_volume_down),
    (re.compile(r"mute"), _h_mute),
    (re.compile(r"unmute"), _h_unmute),

    # Window management
    (re.compile(r"minimize"), _h_minimize),
    (re.compile(r"maximize"), _h_maximize),
    (re.compile(r"restore (?:the )?window"), _h_restore),
    (re.compile(r"switch to (.+)"), _h_switch),
    (re.compile(r"close (?:the )?(?:active|this|current) window"), _h_close_active),
    (re.compile(r"close (.+)"), _h_close_named),

    # Open (apps/files/folders) — kept near the end since it's broad
    (re.compile(r"(?:open|launch|start) (.+)"), _h_open),
]


def handle_command(text: str, listener) -> str:
    """Main entry point. Returns the response string to speak."""
    if not text:
        return "I didn't catch that."

    text = _normalize_command(text)
    log.info("Parsing command: %r", text)

    for pattern, handler in _PATTERNS:
        match = pattern.search(text)
        if match:
            try:
                response = handler(match, listener)
                log.info("Command handled -> %s", response)
                return response
            except Exception:
                log.exception("Handler failed for text: %r", text)
                return "Something went wrong while I was doing that."

    log.info("No pattern matched for: %r", text)
    return "I heard you say that, but I don't know that command yet."
