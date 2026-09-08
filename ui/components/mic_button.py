"""
ui/components/mic_button.py
Circular mic status indicator matching the "Ready to Assist" pill in
the splash art. Pulses/glows while Marcus is actively listening.
Purely visual — reflects state pushed from main.py's voice_loop via
the UI event queue; it does not itself start/stop listening (Marcus
is wake-word driven, not click-to-talk).
"""

import customtkinter as ctk

from ui import theme

_STATUS_TEXT = {
    "idle": "Ready to Assist",
    "waiting_for_wake_word": "Ready to Assist",
    "listening": "Listening...",
    "thinking": "Thinking...",
}

_STATUS_COLOR = {
    "idle": theme.STATUS_IDLE,
    "waiting_for_wake_word": theme.STATUS_IDLE,
    "listening": theme.STATUS_LISTENING,
    "thinking": theme.STATUS_THINKING,
}


class MicButton(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(
            master,
            fg_color=theme.BG_PANEL,
            corner_radius=30,
            **kwargs,
        )
        self._pulse_growing = True
        self._pulse_size = 46

        self.mic_circle = ctk.CTkLabel(
            self,
            text="\U0001F3A4",  # microphone emoji as a simple built-in icon
            font=(theme.FONT_FAMILY, 20),
            width=46,
            height=46,
            corner_radius=23,
            fg_color=theme.STATUS_IDLE,
            text_color="#FFFFFF",
        )
        self.mic_circle.pack(side="left", padx=(12, 10), pady=10)

        text_frame = ctk.CTkFrame(self, fg_color="transparent")
        text_frame.pack(side="left", padx=(0, 20), pady=10)

        self.status_label = ctk.CTkLabel(
            text_frame,
            text=_STATUS_TEXT["idle"],
            font=(theme.FONT_FAMILY, 13, "bold"),
            text_color=theme.TEXT_PRIMARY,
            anchor="w",
        )
        self.status_label.pack(anchor="w")

        self.sub_label = ctk.CTkLabel(
            text_frame,
            text='Say "Hey Marcus" any time',
            font=theme.FONT_STATUS,
            text_color=theme.TEXT_SECONDARY,
            anchor="w",
        )
        self.sub_label.pack(anchor="w")

        self._pulsing = False

    def set_status(self, status: str):
        text = _STATUS_TEXT.get(status, status)
        color = _STATUS_COLOR.get(status, theme.STATUS_IDLE)
        self.status_label.configure(text=text)
        self.mic_circle.configure(fg_color=color)

        if status == "listening":
            self._start_pulse()
        else:
            self._pulsing = False

    def _start_pulse(self):
        if self._pulsing:
            return
        self._pulsing = True
        self._pulse_step()

    def _pulse_step(self):
        if not self._pulsing:
            return
        # Simple two-frame glow pulse using corner radius/size toggle.
        self._pulse_growing = not self._pulse_growing
        size = 50 if self._pulse_growing else 46
        self.mic_circle.configure(width=size, height=size, corner_radius=size // 2)
        self.after(450, self._pulse_step)
