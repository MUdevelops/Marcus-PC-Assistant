"""
ui/components/chat_bubble.py
Scrollable transcript panel showing "you said" / "MARCUS said" bubbles,
matching the speech-bubble response box in the splash art.
"""

import os
import tkinter as tk

import customtkinter as ctk
from PIL import Image, ImageTk

from ui import theme


class ChatBubblePanel(ctk.CTkScrollableFrame):
    def __init__(self, master, **kwargs):
        super().__init__(
            master,
            fg_color="transparent",
            corner_radius=theme.CORNER_RADIUS,
            **kwargs,
        )
        self._resize_job = None
        self._background_source = Image.open(
            os.path.join(os.path.dirname(__file__), "..", "..", "background.png")
        )
        self._background_label = tk.Label(
            self, bd=0, highlightthickness=0, bg=theme.BG_DARK
        )
        self._background_label.place(relx=0, rely=0, relwidth=1, relheight=1)
        self.bind("<Configure>", self._resize_background)
        self._add_heading()
        self._add_placeholder()

    def _resize_background(self, event):
        if self._resize_job is not None:
            self.after_cancel(self._resize_job)
        self._resize_job = self.after(
            80, lambda: self._render_background(event.width, event.height)
        )

    def _render_background(self, width, height):
        if width < 2 or height < 2:
            return
        source_ratio = self._background_source.width / self._background_source.height
        target_ratio = width / height
        if target_ratio > source_ratio:
            scaled_size = (width, round(width / source_ratio))
        else:
            scaled_size = (round(height * source_ratio), height)
        image = self._background_source.resize(scaled_size, Image.Resampling.LANCZOS)
        left = max(0, (image.width - width) // 2)
        top = max(0, (image.height - height) // 2)
        image = image.crop((left, top, left + width, top + height))
        rendered = ImageTk.PhotoImage(image)
        self._background_label.configure(image=rendered)
        self._background_label.image = rendered

    def _add_heading(self):
        ctk.CTkLabel(
            self,
            text="TRANSCRIPT",
            font=theme.FONT_BUBBLE_SENDER,
            text_color=theme.ACCENT_CYAN,
            anchor="w",
        ).pack(anchor="w", padx=18, pady=(14, 2))

        ctk.CTkLabel(
            self,
            text="Recognized speech and Marcus responses",
            font=theme.FONT_STATUS,
            text_color=theme.TEXT_SECONDARY,
            anchor="w",
        ).pack(anchor="w", padx=18, pady=(0, 8))

    def _add_placeholder(self):
        self.placeholder = ctk.CTkLabel(
            self,
            text='Waiting for speech...\nSay a command or "Hey Marcus" first.',
            font=theme.FONT_BODY,
            text_color=theme.TEXT_SECONDARY,
            justify="left",
        )
        self.placeholder.pack(anchor="w", padx=18, pady=(12, 24))

    def add_message(self, sender: str, text: str, label: str | None = None):
        """Add a transcript entry for detected speech or an action result."""
        if self.placeholder is not None:
            self.placeholder.destroy()
            self.placeholder = None

        is_marcus = sender == "marcus"
        is_detected = sender == "detected"
        bubble_bg = theme.BUBBLE_MARCUS_BG if is_marcus else theme.BUBBLE_USER_BG
        sender_label = label or ("MARCUS" if is_marcus else "YOU")
        sender_color = theme.ACCENT_CYAN if is_marcus else theme.TEXT_SECONDARY
        if is_detected:
            sender_color = theme.ACCENT_BLUE

        bubble = ctk.CTkFrame(
            self, fg_color=bubble_bg, corner_radius=theme.CORNER_RADIUS
        )
        bubble.pack(anchor="w", padx=16, pady=6, fill="x")

        ctk.CTkLabel(
            bubble,
            text=sender_label,
            font=theme.FONT_BUBBLE_SENDER,
            text_color=sender_color,
            anchor="w",
        ).pack(anchor="w", padx=14, pady=(10, 0))

        ctk.CTkLabel(
            bubble,
            text=text,
            font=theme.FONT_BUBBLE_TEXT,
            text_color=theme.TEXT_PRIMARY,
            anchor="w",
            justify="left",
            wraplength=390,
        ).pack(anchor="w", padx=14, pady=(2, 10))

        # Auto-scroll to the newest message.
        self.after(50, lambda: self._parent_canvas.yview_moveto(1.0))
