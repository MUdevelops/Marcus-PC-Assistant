"""Responsive startup splash using the supplied Marcus artwork."""

import os
import tkinter as tk

import customtkinter as ctk
from PIL import Image, ImageTk

from ui import theme


class SplashScreen(ctk.CTk):
    def __init__(self, on_complete, duration=1800):
        super().__init__()
        self.on_complete = on_complete
        self._source = Image.open(self._asset_path())

        self.title("Marcus")
        self.geometry("560x560")
        self.minsize(360, 360)
        self.configure(fg_color=theme.BG_DARK)

        self._image_label = tk.Label(self, bd=0, highlightthickness=0)
        self._image_label.place(relx=0, rely=0, relwidth=1, relheight=1)
        self.bind("<Configure>", self._resize_image)
        self.after(duration, self._finish)

    @staticmethod
    def _asset_path():
        root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
        requested = os.path.join(root, "Splash.png")
        fallback = os.path.join(root, "Splash Screen.png")
        return requested if os.path.exists(requested) else fallback

    def _resize_image(self, event):
        if event.width < 2 or event.height < 2:
            return
        image = self._source.copy()
        image.thumbnail((event.width, event.height), Image.Resampling.LANCZOS)
        canvas = Image.new("RGB", (event.width, event.height), theme.BG_DARK)
        canvas.paste(
            image,
            ((event.width - image.width) // 2, (event.height - image.height) // 2),
        )
        rendered = ImageTk.PhotoImage(canvas)
        self._image_label.configure(image=rendered)
        self._image_label.image = rendered

    def _finish(self):
        self.destroy()
        self.on_complete()