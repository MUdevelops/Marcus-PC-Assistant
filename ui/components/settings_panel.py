"""Settings controls for Marcus's local assistant behavior."""

import customtkinter as ctk

from ui import theme


class SettingsPanel(ctk.CTkFrame):
    def __init__(self, master, volume, on_volume_change, **kwargs):
        super().__init__(
            master,
            fg_color="#08111D",
            border_width=1,
            border_color=theme.BORDER_GLOW,
            corner_radius=theme.CORNER_RADIUS,
            **kwargs,
        )
        self._on_volume_change = on_volume_change
        self._volume_value = ctk.StringVar(value=f"{round(volume * 100)}%")
        self._build(volume)

    def _build(self, volume):
        ctk.CTkLabel(
            self,
            text="SETTINGS",
            font=(theme.FONT_FAMILY, 24, "bold"),
            text_color=theme.TEXT_PRIMARY,
            anchor="w",
        ).pack(fill="x", padx=22, pady=(24, 2))
        ctk.CTkLabel(
            self,
            text="Tune how Marcus responds to you.",
            font=theme.FONT_STATUS,
            text_color=theme.TEXT_SECONDARY,
            anchor="w",
        ).pack(fill="x", padx=22, pady=(0, 26))

        volume_header = ctk.CTkFrame(self, fg_color="transparent")
        volume_header.pack(fill="x", padx=22)
        ctk.CTkLabel(
            volume_header,
            text="Assistant volume",
            font=theme.FONT_BODY,
            text_color=theme.TEXT_PRIMARY,
            anchor="w",
        ).pack(side="left")
        ctk.CTkLabel(
            volume_header,
            textvariable=self._volume_value,
            font=theme.FONT_BODY,
            text_color=theme.ACCENT_CYAN,
        ).pack(side="right")

        self.volume_slider = ctk.CTkSlider(
            self,
            from_=0,
            to=100,
            number_of_steps=100,
            height=20,
            command=self._set_volume,
            button_color=theme.ACCENT_BLUE,
            button_hover_color=theme.ACCENT_CYAN,
            progress_color=theme.ACCENT_BLUE_DIM,
        )
        self.volume_slider.set(volume * 100)
        self.volume_slider.pack(fill="x", padx=22, pady=(14, 8))
        ctk.CTkLabel(
            self,
            text="Controls Marcus's speech output only; system volume remains available in Tools.",
            font=theme.FONT_STATUS,
            text_color=theme.TEXT_DISABLED,
            anchor="w",
            wraplength=560,
            justify="left",
        ).pack(fill="x", padx=22, pady=(0, 24))

    def _set_volume(self, value):
        percent = round(float(value))
        self._volume_value.set(f"{percent}%")
        self._on_volume_change(percent / 100)