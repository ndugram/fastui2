"""Override the default CSS with a custom theme."""

from fastui import App, ui

CUSTOM_CSS = """
body {
    font-family: 'Georgia', serif;
    max-width: 700px;
    margin: 0 auto;
    padding: 2rem;
    background: #1a1a2e;
    color: #e0e0e0;
    line-height: 1.8;
}
h1, h2, h3 { color: #e94560; }
button {
    background: #e94560; color: #fff; border: none;
    padding: 0.6rem 1.2rem; border-radius: 4px; cursor: pointer;
}
button:hover { background: #c73650; }
a { color: #0f3460; }
pre { background: #16213e; padding: 1rem; border-radius: 4px; }
"""

app = App(css=CUSTOM_CSS)

@app.page("/")
def index():
    return [
        ui.heading("Custom CSS Theme", level=1),
        ui.text("This page uses a dark theme with custom CSS."),
        ui.button("Styled button", on_click="/about"),
        ui.divider(),
        ui.heading("Code Block", level=2),
        ui.code("""
def greet(name):
    return f"Hello, {name}!"
        """.strip()),
    ]

@app.page("/about", title="About")
def about():
    return [
        ui.heading("About", level=1),
        ui.text("Custom CSS is passed to the App constructor or the run() method."),
        ui.link("Back", url="/"),
    ]

if __name__ == "__main__":
    app.run(css=CUSTOM_CSS)
