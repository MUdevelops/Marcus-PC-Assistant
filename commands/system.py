"""
commands/system.py
System-level controls: brightness, volume, screenshots, webcam,
power state (lock/sleep/shutdown/restart), and system info readback.

Windows-specific notes:
- Brightness control (screen_brightness_control) only works on laptops
  / monitors that expose brightness via WMI or DDC/CI — some external
  monitors won't respond; the function returns a spoken error rather
  than crashing if so.
- Volume control (pycaw) talks to the Windows Core Audio API via COM.
  COM requires per-thread initialization — if you call these functions
  from a background thread (e.g. inside the confirmation module's
  threads), you may need `comtypes.CoInitialize()` in that thread first.
  main.py's flow only calls these from the main thread, which is safe
  by default.
- shutdown/restart/sleep run as the CURRENT user and do NOT require
  admin rights for a normal `shutdown.exe` call. Locking the screen
  also doesn't require admin.
"""

import ctypes
import os
import subprocess
import psutil
import screen_brightness_control as sbc
import pyautogui
from datetime import datetime
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

from config import SCREENSHOT_DIR
from logger_setup import get_logger
from utils import window_utils

log = get_logger(__name__)

os.makedirs(SCREENSHOT_DIR, exist_ok=True)


# ---------------------------------------------------------------------
# Brightness
# ---------------------------------------------------------------------

def _get_brightness() -> int | None:
    try:
        return sbc.get_brightness()[0]
    except Exception:
        log.exception("Failed to read current brightness.")
        return None


def set_brightness(percent: int) -> str:
    percent = max(0, min(100, percent))
    try:
        sbc.set_brightness(percent)
        log.info("Brightness set to %d%%", percent)
        return f"Brightness set to {percent} percent."
    except Exception:
        log.exception("Failed to set brightness.")
        return "I couldn't change the brightness on this display."


def adjust_brightness(delta: int) -> str:
    current = _get_brightness()
    if current is None:
        return "I couldn't read the current brightness on this display."
    return set_brightness(current + delta)


# ---------------------------------------------------------------------
# Volume
# ---------------------------------------------------------------------

def _get_volume_interface():
    devices = AudioUtilities.GetSpeakers()
    interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
    return cast(interface, POINTER(IAudioEndpointVolume))


def set_volume(percent: int) -> str:
    percent = max(0, min(100, percent))
    try:
        volume = _get_volume_interface()
        volume.SetMasterVolumeLevelScalar(percent / 100.0, None)
        log.info("Volume set to %d%%", percent)
        return f"Volume set to {percent} percent."
    except Exception:
        log.exception("Failed to set volume.")
        return "I couldn't change the volume."


def adjust_volume(delta_percent: int) -> str:
    try:
        volume = _get_volume_interface()
        current = volume.GetMasterVolumeLevelScalar() * 100
        return set_volume(round(current + delta_percent))
    except Exception:
        log.exception("Failed to adjust volume.")
        return "I couldn't change the volume."


def mute_volume() -> str:
    try:
        volume = _get_volume_interface()
        volume.SetMute(1, None)
        log.info("Volume muted.")
        return "Muted."
    except Exception:
        log.exception("Failed to mute volume.")
        return "I couldn't mute the volume."


def unmute_volume() -> str:
    try:
        volume = _get_volume_interface()
        volume.SetMute(0, None)
        log.info("Volume unmuted.")
        return "Unmuted."
    except Exception:
        log.exception("Failed to unmute volume.")
        return "I couldn't unmute the volume."


# ---------------------------------------------------------------------
# Screenshot
# ---------------------------------------------------------------------

def take_screenshot() -> str:
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"screenshot_{timestamp}.png"
    filepath = os.path.join(SCREENSHOT_DIR, filename)
    try:
        image = pyautogui.screenshot()
        image.save(filepath)
        log.info("Screenshot saved: %s", filepath)
        return f"Screenshot saved as {filename}."
    except Exception:
        log.exception("Failed to take screenshot.")
        return "I couldn't take a screenshot."


# ---------------------------------------------------------------------
# Webcam
# ---------------------------------------------------------------------

def open_webcam() -> str:
    try:
        os.startfile("microsoft.windows.camera:")
        log.info("Opened Windows Camera app.")
        return "Opening the camera."
    except Exception:
        log.exception("Failed to open camera app.")
        return "I couldn't open the camera app."


def close_webcam() -> str:
    killed = window_utils.kill_process_by_name("WindowsCamera.exe")
    if killed:
        log.info("Closed Windows Camera app.")
        return "Closing the camera."
    return "The camera doesn't appear to be open."


# ---------------------------------------------------------------------
# Power state — the functions below PERFORM the action immediately.
# Callers (intent_parser.py) are responsible for routing shutdown/
# restart/sleep through utils/confirmation.py FIRST. Locking is not
# destructive, so it's not gated.
# ---------------------------------------------------------------------

def lock_screen() -> str:
    try:
        ctypes.windll.user32.LockWorkStation()
        log.info("Screen locked.")
        return "Locking the screen."
    except Exception:
        log.exception("Failed to lock screen.")
        return "I couldn't lock the screen."


def sleep_system() -> str:
    try:
        subprocess.run(
            ["rundll32.exe", "powrprof.dll,SetSuspendState", "0", "1", "0"],
            check=False,
        )
        log.info("System sleep triggered.")
        return "Going to sleep now."
    except Exception:
        log.exception("Failed to trigger sleep.")
        return "I couldn't put the system to sleep."


def shutdown_system() -> str:
    try:
        subprocess.run(["shutdown", "/s", "/t", "0"], check=False)
        log.info("Shutdown triggered.")
        return "Shutting down now."
    except Exception:
        log.exception("Failed to trigger shutdown.")
        return "I couldn't shut down the system."


def restart_system() -> str:
    try:
        subprocess.run(["shutdown", "/r", "/t", "0"], check=False)
        log.info("Restart triggered.")
        return "Restarting now."
    except Exception:
        log.exception("Failed to trigger restart.")
        return "I couldn't restart the system."


# ---------------------------------------------------------------------
# System info readback
# ---------------------------------------------------------------------

def get_battery_status() -> str:
    battery = psutil.sensors_battery()
    if battery is None:
        return "This system doesn't report battery information — it may be a desktop."
    plugged = "and it's plugged in" if battery.power_plugged else "and it's not plugged in"
    return f"Battery is at {round(battery.percent)} percent, {plugged}."


def get_wifi_status() -> str:
    try:
        result = subprocess.run(
            ["netsh", "wlan", "show", "interfaces"],
            capture_output=True, text=True, timeout=5,
        )
        output = result.stdout
        if "State" not in output:
            return "I couldn't read Wi-Fi status on this system."
        connected = "connected" in output.lower() and "disconnected" not in output.lower()
        if connected:
            ssid_line = next((l for l in output.splitlines() if l.strip().startswith("SSID")), None)
            ssid = ssid_line.split(":", 1)[1].strip() if ssid_line and ":" in ssid_line else "an unknown network"
            return f"Wi-Fi is connected to {ssid}."
        return "Wi-Fi is not currently connected."
    except Exception:
        log.exception("Failed to read Wi-Fi status.")
        return "I couldn't check the Wi-Fi status."


def get_disk_space(drive: str = "C:\\") -> str:
    try:
        usage = psutil.disk_usage(drive)
        free_gb = usage.free / (1024 ** 3)
        total_gb = usage.total / (1024 ** 3)
        return (
            f"Drive {drive} has {free_gb:.1f} gigabytes free "
            f"out of {total_gb:.1f} gigabytes total."
        )
    except Exception:
        log.exception("Failed to read disk usage for %s", drive)
        return f"I couldn't read disk space for {drive}."
