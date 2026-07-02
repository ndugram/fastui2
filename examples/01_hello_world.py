"""Minimal FastUI application — one page, one heading."""

from fastui import App, ui

app = App()

@app.page("/")
def index():
    return [ui.heading("Hello, World!", level=1)]

if __name__ == "__main__":
    app.run()
