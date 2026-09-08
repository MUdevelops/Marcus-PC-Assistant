"""
ui/app.py
Main application window. Visually modeled on the provided splash art:
dark navy background, glowing blue accents, left sidebar nav, a large
"MARCUS / Your PC Assistant" header, a chat-style transcript panel, and
a "Ready to Assist" mic status pill.

This window is optional — Marcus's voice engine (main.py) runs fine
without it. Launch with `python main.py --ui` to see this alongside
voice control. The UI polls a thread-safe queue that main.py's voice
loop pushes events into (status changes, recognized text, responses)
so Tkinter itself never touches the microphone or speech engine
directly — avoids the classic "GUI freezes while blocking on mic
input" problem.

To use your own logo/mascot image (e.g. the splash art you attached),
drop a PNG into ui/assets/ and see the commented-out example in
_build_header() below for how to load it with Pillow/CTkImage.
"""

import os
import queue
import threading
import tkinter as tk

import customtkinter as ctk
from PIL import Image, ImageTk

from ui import theme
from ui.components.sidebar import Sidebar
from ui.components.chat_bubble import ChatBubblePanel
from ui.components.mic_button import MicButton
from ui.components.tools_panel import ToolsPanel
from ui.components.apps_panel import AppsPanel
from ui.components.settings_panel import SettingsPanel
from config import ASSISTANT_NAME
from logger_setup import get_logger
from intent_parser import handle_command
from speaker import speak, speaker

log = get_logger(__name__)

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")


def _main_menu_asset_path():
    root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    for filename in ("Main Menu.jpg", "Main Menu.jpeg", "Main Menu.png"):
        path = os.path.join(root, filename)
        if os.path.exists(path):
            return path
    raise FileNotFoundError("Main Menu image was not found.")


class MarcusApp(ctk.CTk):
    def __init__(self, event_queue: "queue.Queue | None" = None, on_start=None):
        super().__init__()

        self.event_queue = event_queue
        self._on_start_voice = on_start
        self._voice_started = False
        self._main_resize_job = None

        self.title(f"{ASSISTANT_NAME} — PC Assistant")
        self.geometry("1280x800")
        self.minsize(*theme.WINDOW_MIN_SIZE)
        self.configure(fg_color=theme.BG_SIDEBAR)

        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self._build_sidebar()
        self._build_main_panel()

        if self.event_queue is not None:
            self.after(150, self._poll_events)

    # ------------------------------------------------------------------
    def _build_sidebar(self):
        self.sidebar = Sidebar(self, on_select=self._on_nav_select)
        self.sidebar.grid(row=0, column=0, sticky="nswe")

    def _on_nav_select(self, section: str):
        log.info("Sidebar section selected: %s", section)
        if not hasattr(self, "tools_panel"):
            return
        if section == "Tools":
            self._show_tools()
        elif section == "Manual":
            self._show_apps()
        elif section == "Settings":
            self._show_settings()
        else:
            self._show_home()

    # ------------------------------------------------------------------
    def _build_main_panel(self):
        main = ctk.CTkFrame(
            self,
            fg_color="transparent",
            border_width=1,
            border_color=theme.BG_SIDEBAR,
            corner_radius=0,
        )
        main.grid(row=0, column=1, sticky="nswe", padx=24, pady=24)
        self._background_source = Image.open(
            _main_menu_asset_path()
        )
        self._background_label = tk.Label(
            main, bd=0, highlightthickness=0, bg=theme.BG_SIDEBAR
        )
        self._background_label.place(relx=0, rely=0, relwidth=1, relheight=1)
        main.bind("<Configure>", self._resize_background)

        self._build_header(main)

        # Chat / transcript panel
        self.chat_panel = ChatBubblePanel(main, height=230, width=470)
        self.chat_panel.place(
            relx=0.53,
            rely=0.43,
            relwidth=0.46,
            relheight=0.36,
        )

        self.tools_panel = ToolsPanel(
            main,
            on_command=self._run_tool_command,
        )
        self.tools_panel.place(relx=0.06, rely=0.06)
        self.tools_panel.place_forget()

        self.apps_panel = AppsPanel(main, on_command=self._run_tool_command)
        self.apps_panel.place_forget()

        self.settings_panel = SettingsPanel(
            main,
            volume=speaker.volume,
            on_volume_change=speaker.set_volume,
        )
        self.settings_panel.place_forget()

        self.start_button = ctk.CTkButton(
            main,
            text="START ASSISTANT",
            font=(theme.FONT_FAMILY, 14, "bold"),
            text_color="#FFFFFF",
            fg_color=theme.ACCENT_BLUE,
            hover_color=theme.ACCENT_BLUE_DIM,
            corner_radius=10,
            height=46,
            command=self._start_assistant,
        )
        self.start_button.place(
            relx=0.56,
            rely=0.84,
            relwidth=0.24,
            anchor="nw",
        )

        # Mic status pill, bottom-right — mirrors "Ready to Assist" box
        self.mic_button = MicButton(main)
        self.mic_button.place(relx=0.73, rely=0.84, relwidth=0.27, anchor="nw")
        self.mic_button.place_forget()

    def _start_assistant(self):
        if self._voice_started:
            return
        self._voice_started = True
        self.start_button.configure(
            text="ASSISTANT ACTIVE",
            fg_color=theme.ACCENT_BLUE_DIM,
            hover_color=theme.ACCENT_BLUE_DIM,
            state="disabled",
        )
        if self._on_start_voice is not None:
            self._on_start_voice()

    def _show_home(self):
        self.tools_panel.place_forget()
        self.apps_panel.place_forget()
        self.settings_panel.place_forget()
        self.chat_panel.place(
            relx=0.53,
            rely=0.43,
            relwidth=0.46,
            relheight=0.36,
        )
        self.start_button.place(relx=0.56, rely=0.84, relwidth=0.24, anchor="nw")
        if self._voice_started:
            self.mic_button.place(
                relx=0.73, rely=0.84, relwidth=0.27, anchor="nw"
            )

    def _show_tools(self):
        self.chat_panel.place_forget()
        self.apps_panel.place_forget()
        self.settings_panel.place_forget()
        self.start_button.place_forget()
        self.mic_button.place_forget()
        self.tools_panel.place(relx=0.06, rely=0.06, relwidth=0.88, relheight=0.86)

    def _show_apps(self):
        self.chat_panel.place_forget()
        self.tools_panel.place_forget()
        self.settings_panel.place_forget()
        self.start_button.place_forget()
        self.mic_button.place_forget()
        self.apps_panel.place(relx=0.06, rely=0.06, relwidth=0.88, relheight=0.86)

    def _show_settings(self):
        self.chat_panel.place_forget()
        self.tools_panel.place_forget()
        self.apps_panel.place_forget()
        self.start_button.place_forget()
        self.mic_button.place_forget()
        self.settings_panel.place(relx=0.06, rely=0.06, relwidth=0.88, relheight=0.86)

    def _run_tool_command(self, command: str):
        if command.endswith("for "):
            query = ctk.CTkInputDialog(
                text="What should Marcus search for?",
                title="Marcus Search",
            ).get_input()
            if not query:
                return
            command = command + query

        self.chat_panel.add_message(
            "user", command, label="COMMAND DETECTED"
        )
        threading.Thread(
            target=self._execute_tool_command,
            args=(command,),
            daemon=True,
            name="marcus-tool-command",
        ).start()

    def _execute_tool_command(self, command: str):
        try:
            response = handle_command(command, None)
            self.after(
                0,
                lambda: self.chat_panel.add_message(
                    "marcus", response, label="ACTION RESULT"
                ),
            )
            speak(response)
        except Exception:
            log.exception("Tool button command failed: %s", command)
            response = "I couldn't complete that tool action."
            self.after(0, lambda: self.chat_panel.add_message("marcus", response))

    def _build_header(self, parent):
        header = ctk.CTkFrame(parent, fg_color="transparent", height=1)
        header.grid(row=0, column=0, sticky="we")
        header.grid_propagate(False)

        # --- Logo mark ---
        # If you want to use the exact splash-art mascot image instead
        # of the text glyph below, drop a PNG at ui/assets/logo.png and
        # uncomment:
        #
        # from PIL import Image
        # logo_img = ctk.CTkImage(Image.open("ui/assets/logo.png"), size=(64, 64))
        # ctk.CTkLabel(header, image=logo_img, text="").pack(side="left", padx=(0, 16))

        # The supplied Main Menu image contains the brand and feature strip.

    # ------------------------------------------------------------------
    def _poll_events(self):
        """Drains the event queue pushed from main.py's voice_loop and
        updates the UI. Runs on Tkinter's own event loop via `after`,
        so this is safe cross-thread (the queue is the only thing
        shared between the voice thread and this Tk thread)."""
        try:
            while True:
                event_type, payload = self.event_queue.get_nowait()
                self._handle_event(event_type, payload)
        except queue.Empty:
            pass
        finally:
            self.after(150, self._poll_events)

    def _handle_event(self, event_type: str, payload: str):
        if event_type == "status":
            if payload in ("listening", "thinking"):
                self.mic_button.place(
                    relx=0.73, rely=0.84, relwidth=0.27, anchor="nw"
                )
            else:
                self.mic_button.place_forget()
            self.mic_button.set_status(payload)
        elif event_type == "heard":
            self.chat_panel.add_message(
                "user", payload, label="COMMAND DETECTED"
            )
        elif event_type == "response":
            self.chat_panel.add_message("marcus", payload, label="ACTION RESULT")
        elif event_type == "detected":
            self.chat_panel.add_message("detected", payload, label="WAKE WORD")

    def _resize_background(self, event):
        if self._main_resize_job is not None:
            self.after_cancel(self._main_resize_job)
        self._main_resize_job = self.after(
            80, lambda: self._render_background(event.width, event.height)
        )

    def _render_background(self, width, height):
        if (
            width < 2
            or height < 2
            or not self._background_label.winfo_exists()
        ):
            return
        source_ratio = self._background_source.width / self._background_source.height
        target_ratio = width / height
        if target_ratio > source_ratio:
            scaled_size = (width, round(width / source_ratio))
        else:
            scaled_size = (round(height * source_ratio), height)

        image = self._background_source.resize(scaled_size, Image.Resampling.LANCZOS)
        left = max(0, (image.width - width) // 2)
        top = max(0, round((image.height - height) * 0.38))
        canvas = image.crop((left, top, left + width, top + height))
        rendered = ImageTk.PhotoImage(canvas)
        self._background_label.configure(image=rendered)
        self._background_label.image = rendered

if __name__ == "__main__":
    # UI-only preview (no live mic/voice engine) — useful for iterating
    # on layout/theme without needing to say "Hey Marcus" each time.
    app = MarcusApp(event_queue=None)
    app.mainloop()
