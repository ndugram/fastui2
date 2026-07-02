"""Use the Page component for grouping and layout."""

from fastui import App, ui

app = App()


@app.page("/")
def index():
    return [
        ui.heading("Page Layout", level=1),
        ui.text("The Page component wraps children in a div for grouping."),
        ui.divider(),

        ui.heading("Card 1: Info", level=2),
        ui.page([
            ui.text("This content is inside a Page component."),
            ui.text("Pages can have their own styles and classes."),
        ], style="background: #f0f0ff; padding: 1rem; border-radius: 8px; border: 1px solid #d0d0ff;"),

        ui.heading("Card 2: Actions", level=2),
        ui.page([
            ui.button("Home", on_click="/"),
            ui.button("About", on_click="/about"),
        ], style="background: #f0fff0; padding: 1rem; border-radius: 8px; border: 1px solid #d0ffd0;"),

        ui.divider(),
        ui.text("Nested pages are also supported."),
    ]


@app.page("/about")
def about():
    return [
        ui.heading("About", level=1),
        ui.link("Back", url="/"),
    ]

if __name__ == "__main__":
    app.run()
