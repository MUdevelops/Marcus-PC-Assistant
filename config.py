"""
config.py
Central configuration for Marcus. Keep all tunable values here so
nothing is hardcoded deep inside listener/speaker/command modules.
"""

import os

# ---- Identity ----
ASSISTANT_NAME = "Marcus"
WAKE_WORD = "hey marcus"          # lowercase, matched against lowercase transcript
WAKE_WORD_ALIASES = ["hey marcus", "hey markus", "a marcus"]  # common mis-hearings
REQUIRE_WAKE_WORD = False          # allow supported commands such as "volume up" directly

# ---- Paths ----
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
LOG_DIR = os.path.join(BASE_DIR, "logs")
LOG_FILE = os.path.join(LOG_DIR, "marcus.log")
SCREENSHOT_DIR = os.path.join(os.path.expanduser("~"), "Pictures", "Marcus_Screenshots")

# ---- Speech recognition (online / Google) ----
# Values tuned for a typical desktop mic in a normal room. If Marcus
# mishears often, raise ENERGY_THRESHOLD; if it doesn't hear you at
# all, lower it.
ENERGY_THRESHOLD = 250          # ambient noise cutoff for "is someone speaking"
PAUSE_THRESHOLD = 0.65          # seconds of silence that end a phrase
NON_SPEAKING_DURATION = 0.35    # silence needed before speech is considered finished
AMBIENT_CALIBRATION_SECONDS = 2  # longer calibration improves noisy-room detection
WAKE_WORD_TIMEOUT = None        # seconds to wait for wake word (None = wait forever)
WAKE_WORD_PHRASE_LIMIT = 3      # max seconds for the wake-word utterance itself
COMMAND_TIMEOUT = 6             # seconds to wait for the command after wake word fires
COMMAND_PHRASE_LIMIT = 10       # max seconds for the command utterance itself

# ---- Text-to-speech (pyttsx3) ----
TTS_RATE = 178                  # words per minute-ish; 150-200 is natural
TTS_VOLUME = 1.0                # 0.0 - 1.0
TTS_VOICE_INDEX = None          # None = system default; set to 0/1/etc after we list voices

# ---- Confirmation ----
CONFIRMATION_TIMEOUT = 8        # seconds to wait for yes/no before auto-cancelling
DESTRUCTIVE_PHRASES_YES = {"yes", "yeah", "confirm", "do it", "go ahead", "yes marcus"}
DESTRUCTIVE_PHRASES_NO = {"no", "cancel", "stop", "nevermind", "never mind", "abort"}

os.makedirs(LOG_DIR, exist_ok=True)
