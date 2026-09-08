"""
speaker.py
Offline text-to-speech output using pyttsx3 (wraps Windows SAPI5,
so no internet or API key needed).

Design note: pyttsx3's engine.runAndWait() does NOT play well if you
call it from multiple threads or re-init the engine repeatedly, so we
build ONE engine at import time and reuse it via a module-level
Speaker instance. Call speak() from anywhere in the app.
"""

import pyttsx3
import threading

try:
    from comtypes import CLSCTX_ALL
    from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
    from ctypes import POINTER, cast
except ImportError:
    CLSCTX_ALL = None
    AudioUtilities = None
    IAudioEndpointVolume = None
    POINTER = None
    cast = None

from config import TTS_RATE, TTS_VOLUME, TTS_VOICE_INDEX
from logger_setup import get_logger

log = get_logger(__name__)


def _safe_volume(value: float) -> float:
    """Keep SAPI volume in its supported range to avoid clipping."""
    return max(0.0, min(1.0, float(value)))


class Speaker:
    def __init__(self):
        self._lock = threading.RLock()
        self.engine = pyttsx3.init()
        self.engine.setProperty("rate", TTS_RATE)
        self.volume = _safe_volume(TTS_VOLUME)
        self.engine.setProperty("volume", self.volume)

        if TTS_VOICE_INDEX is not None:
            voices = self.engine.getProperty("voices")
            try:
                self.engine.setProperty("voice", voices[TTS_VOICE_INDEX].id)
            except IndexError:
                log.warning(
                    "TTS_VOICE_INDEX %s out of range (only %d voices found); "
                    "using default voice.",
                    TTS_VOICE_INDEX,
                    len(voices),
                )

    @staticmethod
    def _ensure_audible_output():
        """Raise very low Windows output volume without exceeding 85%."""
        if AudioUtilities is None:
            return
        try:
            devices = AudioUtilities.GetSpeakers()
            interface = devices.Activate(
                IAudioEndpointVolume._iid_, CLSCTX_ALL, None
            )
            volume = cast(interface, POINTER(IAudioEndpointVolume))
            if volume.GetMasterVolumeLevelScalar() < 0.85:
                volume.SetMasterVolumeLevelScalar(0.85, None)
        except Exception:
            log.debug("Unable to adjust Windows output volume.", exc_info=True)

    def list_voices(self):
        """Utility: print available system voices with their index,
        so you can pick one for TTS_VOICE_INDEX in config.py."""
        voices = self.engine.getProperty("voices")
        for i, v in enumerate(voices):
            print(f"[{i}] {v.name}  ({v.id})")
        return voices

    def set_volume(self, value: float):
        """Set Marcus's text-to-speech volume for future responses."""
        with self._lock:
            self.volume = _safe_volume(value)
            self.engine.setProperty("volume", self.volume)
            log.info("TTS volume set to %.0f%%", self.volume * 100)

    def speak(self, text: str):
        """Speak text aloud and log it. Blocking call by design —
        Marcus shouldn't listen for a new command while mid-sentence."""
        if not text:
            return
        log.info("SPEAK: %s", text)
        try:
            with self._lock:
                # Re-apply the configured level for every response. This keeps
                # output consistent if another SAPI client changes the engine.
                self.engine.setProperty("volume", self.volume)
                self.engine.say(text)
                self.engine.runAndWait()
        except Exception:
            log.exception("TTS failed to speak text: %r", text)


# Single shared instance the rest of the app imports.
speaker = Speaker()


def speak(text: str):
    """Module-level convenience function: from speaker import speak"""
    speaker.speak(text)


if __name__ == "__main__":
    # Quick manual test — see the test instructions after this file.
    print("Available voices on this system:")
    speaker.list_voices()
    speak("Hello, I am Marcus, your P C assistant. Text to speech is working.")
