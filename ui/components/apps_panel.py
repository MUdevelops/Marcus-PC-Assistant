"""Manual command entry point for Marcus."""

import customtkinter as ctk

from ui import theme


class AppsPanel(ctk.CTkFrame):
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
            text="MANUAL COMMAND",
            font=(theme.FONT_FAMILY, 24, "bold"),
            text_color=theme.TEXT_PRIMARY,
            anchor="w",
        ).pack(fill="x", padx=22, pady=(24, 2))
        ctk.CTkLabel(
            self,
            text="Type any supported command and let Marcus execute it.",
            font=theme.FONT_STATUS,
            text_color=theme.TEXT_SECONDARY,
            anchor="w",
        ).pack(fill="x", padx=22, pady=(0, 22))

        command_row = ctk.CTkFrame(self, fg_color="transparent")
        command_row.pack(fill="x", padx=22, pady=(0, 8))
        command_row.grid_columnconfigure(0, weight=1)

        self.command_entry = ctk.CTkEntry(
            command_row,
            placeholder_text="Example: open Chrome, volume up, or search Google for ...",
            height=42,
            font=theme.FONT_BODY,
        )
        self.command_entry.grid(row=0, column=0, sticky="ew", padx=(0, 10))
        self.command_entry.bind("<Return>", self._submit)

        ctk.CTkButton(
            command_row,
            text="EXECUTE",
            width=120,
            height=42,
            font=theme.FONT_BODY,
            fg_color=theme.ACCENT_BLUE,
            hover_color=theme.ACCENT_BLUE_DIM,
            command=self._submit,
        ).grid(row=0, column=1)

        ctk.CTkLabel(
            self,
            text="Examples",
            font=theme.FONT_BUBBLE_SENDER,
            text_color=theme.ACCENT_CYAN,
            anchor="w",
        ).pack(fill="x", padx=22, pady=(24, 8))

        examples = ctk.CTkFrame(self, fg_color="transparent")
        examples.pack(fill="x", padx=18)
        examples.grid_columnconfigure((0, 1), weight=1)
        for index, command in enumerate(
            ("open Chrome", "open Notepad", "check battery", "what time is it")
        ):
            ctk.CTkButton(
                examples,
                text=command,
                height=38,
                font=theme.FONT_BODY,
                fg_color=theme.BG_PANEL,
                hover_color=theme.ACCENT_BLUE_DIM,
                text_color=theme.TEXT_PRIMARY,
                command=lambda value=command: self._on_command(value),
            ).grid(row=index // 2, column=index % 2, sticky="ew", padx=4, pady=4)

    def _submit(self, _event=None):
        command = self.command_entry.get().strip()
        if not command:
            return
        self.command_entry.delete(0, "end")
        self._on_command(command)