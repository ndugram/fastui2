"""Return a single component instead of a list."""

from fastui import App, ui

app = App()

@app.page("/")
def index():
    return ui.heading("Single Component", level=1, style="color: #4f46e5;")

@app.page("/list")
def list_page():
    return [
        ui.heading("Multiple Components", level=1),
        ui.text("This page returns a list — the normal pattern."),
    ]

@app.page("/raw")
def raw_string():
    return "Raw string content works too"

if __name__ == "__main__":
    app.run()
