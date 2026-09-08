"""One-click controls for the commands Marcus already supports."""

import customtkinter as ctk

from ui import theme


TOOL_GROUPS = (
    (
        "SYSTEM CONTROLS",
        (
            ("Volume up", "volume up"),
            ("Volume down", "volume down"),
            ("Mute", "mute"),
            ("Unmute", "unmute"),
            ("Brightness up", "brightness up"),
            ("Brightness down", "brightness down"),
        ),
    ),
    (
        "WINDOWS & DEVICES",
        (
            ("Minimize window", "minimize"),
            ("Maximize window", "maximize"),
            ("Restore window", "restore"),
            ("Take screenshot", "take a screenshot"),
            ("Open camera", "open camera"),
            ("Close camera", "close camera"),
            ("Lock screen", "lock the screen"),
        ),
    ),
    (
        "SYSTEM INFORMATION",
        (
            ("Battery status", "check battery"),
            ("Wi-Fi status", "check wifi"),
            ("Disk space", "check disk space"),
            ("Date and time", "what time is it"),
        ),
    ),
    (
        "APPS & PRODUCTIVITY",
        (
            ("Open Chrome", "open chrome"),
            ("Open Notepad", "open notepad"),
            ("Open Downloads", "open downloads"),
            ("Five-minute timer", "set a timer for 5 minutes"),
            ("Ten-minute timer", "set a timer for 10 minutes"),
            ("List active timers", "list active timers"),
        ),
    ),
    (
        "WEB & SEARCH",
        (
            ("Open GitHub", "go to github.com"),
            ("Search Google", "search google for "),
            ("Search YouTube", "search youtube for "),
        ),
    ),
)


class ToolsPanel(ctk.CTkScrollableFrame):
    def __init__(self, master, on_command, **kwargs):
        super().__init__(
            master,
            fg_color="#08111D",
            border_width=1,
            border_color=theme.BORDER_GLOW,
            corner_radius=theme.CORNER_RADIUS,
            **kwargs,
        )
        self._on_command = on_command
        self._build()

    def _build(self):
        ctk.CTkLabel(
            self,
            text="TOOLS",
            font=(theme.FONT_FAMILY, 24, "bold"),
            text_color=theme.TEXT_PRIMARY,
            anchor="w",
        ).pack(fill="x", padx=22, pady=(20, 2))
        ctk.CTkLabel(
            self,
            text="Run supported Marcus commands with one click.",
            font=theme.FONT_STATUS,
            text_color=theme.TEXT_SECONDARY,
            anchor="w",
        ).pack(fill="x", padx=22, pady=(0, 18))

        for group_name, tools in TOOL_GROUPS:
            ctk.CTkLabel(
                self,
                text=group_name,
                font=theme.FONT_BUBBLE_SENDER,
                text_color=theme.ACCENT_CYAN,
                anchor="w",
            ).pack(fill="x", padx=22, pady=(10, 8))

            row = ctk.CTkFrame(self, fg_color="transparent")
            row.pack(fill="x", padx=18, pady=(0, 8))
            row.grid_columnconfigure((0, 1), weight=1)

            for index, (label, command) in enumerate(tools):
                button = ctk.CTkButton(
                    row,
                    text=label,
                    font=theme.FONT_BODY,
                    height=38,
                    fg_color=theme.BG_PANEL,
                    hover_color=theme.ACCENT_BLUE_DIM,
                    text_color=theme.TEXT_PRIMARY,
                    corner_radius=8,
                    command=lambda value=command: self._on_command(value),
                )
                button.grid(
                    row=index // 2,
                    column=index % 2,
                    sticky="ew",
                    padx=4,
                    pady=4,
                )

        ctk.CTkLabel(
            self,
            text="Shutdown, restart, sleep, and app closing remain voice-confirmed for safety.",
            font=theme.FONT_STATUS,
            text_color=theme.TEXT_DISABLED,
            anchor="w",
            wraplength=520,
            justify="left",
        ).pack(fill="x", padx=22, pady=(14, 24))
