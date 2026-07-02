"""Showcase every built-in component type."""

from fastui import App, ui

app = App()

@app.page("/", title="Components")
def index():
    return [
        ui.heading("All Components", level=1),
        ui.text("This page demonstrates every built-in component."),
        ui.divider(),
        ui.heading("Heading (h2)", level=2),
        ui.heading("Heading (h3)", level=3),
        ui.divider(),
        ui.text("A paragraph of text with body content."),
        ui.divider(),
        ui.input(label="Text input", name="text"),
        ui.input(label="Email input", name="email", type="email"),
        ui.input(label="With placeholder", name="ph", placeholder="Type here..."),
        ui.divider(),
        ui.button("Client button", on_click="/about"),
        ui.divider(),
        ui.link("Clickable link", url="/about"),
        ui.divider(),
        ui.code("def hello():\n    print('Hello, World!')"),
        ui.divider(),
        ui.text("Components can have inline styles:"),
        ui.text("Styled text", style="color: #4f46e5; font-weight: bold;"),
        ui.divider(),
        ui.text("Components can have CSS classes:"),
        ui.heading("Classy heading", level=3, class_name="fancy"),
    ]

if __name__ == "__main__":
    app.run()
