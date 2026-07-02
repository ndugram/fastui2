"""Absolute minimal FastUI app — 7 lines."""

from fastui import App, ui

app = App()

@app.page("/")
def index():
    return [ui.heading("Minimal", level=1)]

app.run(open_browser=False)
