# UI assets

- `logo.png` / `icon_64.png` — auto-generated placeholder "M" mark in
  the app's color theme (theme.py). Swap these for your own exported
  art any time — `ui/app.py`'s `_build_header()` has a commented
  example showing how to load a PNG logo with Pillow/CTkImage.
- Drop your mascot/splash image here (e.g. `mascot.png`) if you want
  to feature it somewhere in the UI (About panel, Home background,
  etc.) — it isn't wired in automatically since the app is built
  around the theme colors, not a specific character illustration.
