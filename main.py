"""
main.py
The main listen -> parse -> execute -> respond loop.
    voice_started = False

    def start_voice():
        nonlocal voice_started
        if voice_started:
            return
        voice_started = True
        threading.Thread(
            target=voice_loop, args=(ui_queue,), daemon=True
        ).start()

Run modes:
        app = MarcusApp(event_queue=ui_queue, on_start=start_voice)
Ctrl+C stops Marcus in either mode.
"""

import argparse
import queue
import threading

from listener import Listener
from speaker import speak
from intent_parser import handle_command
from config import ASSISTANT_NAME, WAKE_WORD
from logger_setup import get_logger

log = get_logger(__name__)


def voice_loop(ui_queue: "queue.Queue | None" = None):
    """Runs forever: wait for wake word -> capture command -> handle it
    -> speak the response. If ui_queue is provided, pushes status/text
    events so the UI thread can display them (see ui/app.py)."""

    def notify(event_type: str, payload: str):
        if ui_queue is not None:
            ui_queue.put((event_type, payload))

    listener = Listener()
    speak(f"{ASSISTANT_NAME} is online and ready.")
    log.info("%s started. Wake word: %r", ASSISTANT_NAME, WAKE_WORD)
    notify("status", "idle")

    while True:
        try:
            notify("status", "waiting_for_wake_word")
            inline_command = listener.wait_for_wake_word()

            if listener.last_transcript and listener.last_wake_detected:
                notify("detected", listener.last_transcript)

            notify("status", "listening")
            if inline_command:
                command_text = inline_command
            else:
                speak("Yes?")
                command_text = listener.listen_for_command()

            if not command_text:
                notify("status", "idle")
                speak("I didn't catch that.")
                log.info("No usable command captured after wake word.")
                continue

            notify("heard", command_text)
            notify("status", "thinking")

            response = handle_command(command_text, listener)

            notify("response", response)
            notify("status", "idle")
            speak(response)

        except KeyboardInterrupt:
            log.info("%s shutting down (KeyboardInterrupt).", ASSISTANT_NAME)
            speak("Goodbye.")
            break
        except Exception:
            log.exception("Unhandled error in main voice loop.")
            speak("Something went wrong, but I'm still here.")
            notify("status", "idle")
            # Deliberately do NOT re-raise — a single bad command should
            # never take down the whole assistant.
            continue


def run_console_only():
    voice_loop(ui_queue=None)


def run_with_ui():
    """Starts the voice loop in a background thread and the
    CustomTkinter UI on the main thread (Tkinter must own the main
    thread on most platforms)."""
    from ui.app import MarcusApp
    from ui.splash import SplashScreen

    ui_queue: queue.Queue = queue.Queue()
    voice_started = False

    def start_voice_assistant():
        nonlocal voice_started
        if voice_started:
            return
        voice_started = True
        threading.Thread(
            target=voice_loop,
            args=(ui_queue,),
            daemon=True,
            name="marcus-voice-loop",
        ).start()

    def launch_app():
        app = MarcusApp(event_queue=ui_queue, on_start=start_voice_assistant)
        app.mainloop()

    splash = SplashScreen(on_complete=launch_app)
    splash.mainloop()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=f"{ASSISTANT_NAME} — PC Assistant")
    parser.add_argument(
        "--ui",
        action="store_true",
        help="Launch with the visual UI (the default).",
    )
    parser.add_argument(
        "--console",
        action="store_true",
        help="Run voice control without the visual UI.",
    )
    args = parser.parse_args()

    if args.console:
        run_console_only()
    else:
        run_with_ui()
