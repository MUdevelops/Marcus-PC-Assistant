"""
utils/confirmation.py
Gatekeeper for anything destructive (shutdown, restart, force-closing
an app, deleting a file). Speaks a warning, then accepts either a
spoken yes/no (via the shared Listener) or typed yes/no from the
console — whichever comes back first is used, so Marcus stays usable
even if you're in a loud room or want to confirm quietly.
"""

import threading
import queue

from config import (
    CONFIRMATION_TIMEOUT,
    DESTRUCTIVE_PHRASES_YES,
    DESTRUCTIVE_PHRASES_NO,
)
from speaker import speak
from logger_setup import get_logger

log = get_logger(__name__)


def _typed_input_worker(result_queue: queue.Queue):
    try:
        text = input("Type 'yes' or 'no' to confirm: ").strip().lower()
        result_queue.put(("typed", text))
    except Exception:
        pass


def confirm_action(prompt: str, listener) -> bool:
    """
    Speaks `prompt` (should end in a yes/no question), then waits up to
    CONFIRMATION_TIMEOUT seconds for either a spoken or typed answer.

    `listener` is the shared Listener instance from listener.py — passed
    in rather than imported/instantiated here so we never open two
    competing microphone streams.

    Returns True only on an explicit, recognized "yes". Anything else
    (no, silence, timeout, unrecognized speech) returns False — a
    destructive action should never proceed on ambiguity.
    """
    speak(prompt)
    log.info("CONFIRMATION requested: %s", prompt)

    result_queue: queue.Queue = queue.Queue()

    # Typed input runs in a background thread so it doesn't block the
    # voice path; whichever answers first wins.
    typed_thread = threading.Thread(
        target=_typed_input_worker, args=(result_queue,), daemon=True
    )
    typed_thread.start()

    # Try the spoken path with a bounded wait.
    def _voice_worker():
        try:
            text = listener.listen_for_command()
            if text:
                result_queue.put(("voice", text))
        except Exception:
            log.exception("Voice confirmation capture failed.")

    voice_thread = threading.Thread(target=_voice_worker, daemon=True)
    voice_thread.start()

    try:
        source, text = result_queue.get(timeout=CONFIRMATION_TIMEOUT)
    except queue.Empty:
        log.info("Confirmation timed out — treating as NO.")
        speak("I didn't get a response, so I'm cancelling that.")
        return False

    text = text.lower().strip()
    if any(phrase in text for phrase in DESTRUCTIVE_PHRASES_YES):
        log.info("Confirmation ANSWER=%s (%s) -> CONFIRMED", text, source)
        return True
    if any(phrase in text for phrase in DESTRUCTIVE_PHRASES_NO):
        log.info("Confirmation ANSWER=%s (%s) -> CANCELLED", text, source)
        speak("Okay, cancelled.")
        return False

    log.info("Confirmation ANSWER=%s (%s) -> UNRECOGNIZED, treating as NO", text, source)
    speak("I didn't understand that, so I'm cancelling that for safety.")
    return False
