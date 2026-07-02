"""Demonstrate hot-reload mode — edit this file and watch the browser refresh."""

from fastui import App, ui

app = App()

@app.page("/")
def index():
    return [
        ui.heading("Hot Reload Demo", level=1),
        ui.text("Edit this file and save — the browser will auto-refresh."),
        ui.text("Try changing the text below:"),
        ui.text("This text updates on save!", style="color: #4f46e5; font-weight: bold;"),
        ui.divider(),
        ui.text("Powered by file polling (os.stat)."),
    ]

if __name__ == "__main__":
    app.run(hot_reload=True)
