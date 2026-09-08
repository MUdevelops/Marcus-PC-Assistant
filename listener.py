"""
listener.py
Microphone input + speech-to-text, using speech_recognition with the
Google Web Speech API (free tier, no API key required, but needs
internet).

Two public entry points:
  - wait_for_wake_word()   blocks until "hey marcus" (or an alias) is heard
  - listen_for_command()   captures one utterance and returns the text

Kept deliberately dumb: this module's only job is "microphone in,
text out." It doesn't know anything about intents or commands.
"""

import speech_recognition as sr

from config import (
    ENERGY_THRESHOLD,
    PAUSE_THRESHOLD,
    WAKE_WORD_ALIASES,
    WAKE_WORD_TIMEOUT,
    WAKE_WORD_PHRASE_LIMIT,
    COMMAND_TIMEOUT,
    COMMAND_PHRASE_LIMIT,
    REQUIRE_WAKE_WORD,
    NON_SPEAKING_DURATION,
    AMBIENT_CALIBRATION_SECONDS,
)
from logger_setup import get_logger

log = get_logger(__name__)


class Listener:
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.recognizer.energy_threshold = ENERGY_THRESHOLD
        self.recognizer.pause_threshold = PAUSE_THRESHOLD
        # Let the recognizer auto-adjust for background noise over time
        # instead of only once at startup — makes it more forgiving if
        # you move rooms or a fan kicks on.
        self.recognizer.dynamic_energy_threshold = True
        self.recognizer.dynamic_energy_adjustment_damping = 0.10
        self.recognizer.dynamic_energy_adjustment_ratio = 1.5
        self.recognizer.non_speaking_duration = NON_SPEAKING_DURATION

        self.microphone = sr.Microphone()
        self.last_transcript = None
        self.last_wake_detected = False

        # One-time ambient noise calibration so the very first listen
        # isn't wildly miscalibrated.
        with self.microphone as source:
            log.info("Calibrating for ambient noise (stay quiet for a moment)...")
            self.recognizer.adjust_for_ambient_noise(
                source, duration=AMBIENT_CALIBRATION_SECONDS
            )
        log.info("Calibration done. Energy threshold set to %.1f", self.recognizer.energy_threshold)

    def _listen_once(self, timeout, phrase_time_limit):
        """Capture raw audio from the mic. Returns an AudioData object
        or None if nothing was heard before timeout."""
        with self.microphone as source:
            try:
                audio = self.recognizer.listen(
                    source,
                    timeout=timeout,
                    phrase_time_limit=phrase_time_limit,
                )
                return audio
            except sr.WaitTimeoutError:
                return None

    def _transcribe(self, audio):
        """Send audio to Google's free Web Speech API. Returns lowercase
        text, or None if it couldn't understand / no internet."""
        if audio is None:
            return None
        try:
            text = self.recognizer.recognize_google(audio, language="en-US")
            log.info("Heard: %r", text)
            self.last_transcript = text.lower().strip()
            return self.last_transcript
        except sr.UnknownValueError:
            log.debug("Audio was unintelligible.")
            return None
        except sr.RequestError as e:
            log.error("Google Speech API request failed (check internet): %s", e)
            return None

    def wait_for_wake_word(self) -> str | None:
        """Blocks (listening in short bursts) until the wake word is
        heard. Returns any command spoken after it in the same utterance.
        This loops forever by design — call it at the top of main.py's
        while loop."""
        while True:
            self.last_wake_detected = False
            audio = self._listen_once(
                timeout=WAKE_WORD_TIMEOUT, phrase_time_limit=WAKE_WORD_PHRASE_LIMIT
            )
            text = self._transcribe(audio)
            if text and any(alias in text for alias in WAKE_WORD_ALIASES):
                log.info("Wake word detected in: %r", text)
                for alias in sorted(WAKE_WORD_ALIASES, key=len, reverse=True):
                    wake_index = text.find(alias)
                    if wake_index >= 0:
                        self.last_wake_detected = True
                        return text[wake_index + len(alias):].strip(" ,.!?") or None
                return None
            if text and not REQUIRE_WAKE_WORD:
                log.info("Direct command mode accepted: %r", text)
                return text
            # else: loop again silently — this is normal, not an error.

    def listen_for_command(self) -> str | None:
        """Captures one command utterance after the wake word fired.
        Returns lowercase text, or None if nothing usable was heard."""
        audio = self._listen_once(
            timeout=COMMAND_TIMEOUT, phrase_time_limit=COMMAND_PHRASE_LIMIT
        )
        return self._transcribe(audio)


if __name__ == "__main__":
    # Quick manual test — see the test instructions after this file.
    listener = Listener()
    print("Say 'Hey Marcus' followed by anything...")
    listener.wait_for_wake_word()
    print("Wake word heard! Now say a command...")
    command = listener.listen_for_command()
    print(f"You said: {command!r}")
