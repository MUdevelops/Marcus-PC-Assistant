"""
ui/components/sidebar.py
Left navigation: Home / Apps / Tools / Settings — matching the splash
art layout. Purely visual navigation for now (switches which panel is
shown in the main content area); it doesn't affect the voice engine.
"""

import customtkinter as ctk

from ui import theme

NAV_ITEMS = ["Home", "Manual", "Tools", "Settings"]
NAV_ICONS = {"Home": "🏠", "Manual": "📝", "Tools": "🛠", "Settings": "⚙"}


class Sidebar(ctk.CTkFrame):
    def __init__(self, master, on_select=None, **kwargs):
        super().__init__(
            master,
            width=theme.SIDEBAR_WIDTH,
            fg_color=theme.BG_SIDEBAR,
            corner_radius=0,
            **kwargs,
        )
        self.on_select = on_select
        self._buttons = {}
        self._active = "Home"

        self.grid_propagate(False)

        # Logo / brand mark
        brand = ctk.CTkLabel(
            self,
            text="MARCUS",
            font=(theme.FONT_FAMILY, 18, "bold"),
            text_color=theme.ACCENT_BLUE,
            anchor="w",
        )
        brand.pack(fill="x", padx=20, pady=(24, 30))

        for item in NAV_ITEMS:
            btn = ctk.CTkButton(
                self,
                text=f"  {NAV_ICONS[item]}   {item}",
                anchor="w",
                font=theme.FONT_NAV,
                fg_color="transparent",
                hover_color="#17385A",
                text_color=theme.TEXT_PRIMARY,
                corner_radius=8,
                height=42,
                command=lambda i=item: self._select(i),
            )
            btn.pack(fill="x", padx=12, pady=4)
            self._buttons[item] = btn

        self._select("Home")

        # Footer tagline, matching "YOUR DIGITAL PARTNER / ALWAYS ON
        # YOUR SIDE" caption from the splash art.
        tagline = ctk.CTkLabel(
            self,
            text="YOUR DIGITAL PARTNER\nALWAYS ON YOUR SIDE",
            font=(theme.FONT_FAMILY, 9),
            text_color=theme.TEXT_SECONDARY,
            justify="left",
            anchor="w",
        )
        tagline.pack(side="bottom", fill="x", padx=20, pady=20)

    def _select(self, item: str):
        self._active = item
        for name, btn in self._buttons.items():
            if name == item:
                btn.configure(fg_color=theme.ACCENT_BLUE_DIM, text_color="#FFFFFF")
            else:
                btn.configure(fg_color="transparent", text_color=theme.TEXT_PRIMARY)
        if self.on_select:
            self.on_select(item)
