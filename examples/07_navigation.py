"""Navigation between pages with links and buttons."""

from fastui import App, ui

app = App()


@app.page("/", title="Home")
def home():
    return [
        ui.heading("Navigation Demo", level=1),
        ui.text("Click around to see navigation in action."),
        ui.divider(),
        ui.link("Go to About", url="/about", style="display: block; margin: 0.5rem 0;"),
        ui.link("Go to Contact", url="/contact", style="display: block; margin: 0.5rem 0;"),
        ui.link("Go to FAQ", url="/faq", style="display: block; margin: 0.5rem 0;"),
        ui.divider(),
        ui.text("You can also use buttons:"),
        ui.button("Go to About", on_click="/about"),
        ui.button("Go to Contact", on_click="/contact"),
    ]


@app.page("/about", title="About")
def about():
    return [
        ui.heading("About", level=1),
        ui.text("FastUI lets you build web UIs entirely in Python."),
        ui.divider(),
        ui.link("← Back to Home", url="/"),
    ]


@app.page("/contact", title="Contact")
def contact():
    return [
        ui.heading("Contact", level=1),
        ui.text("Email: hello@fastui.dev"),
        ui.text("GitHub: github.com/fastui"),
        ui.divider(),
        ui.link("← Back to Home", url="/"),
    ]


@app.page("/faq", title="FAQ")
def faq():
    return [
        ui.heading("FAQ", level=1),
        ui.text("Q: What is FastUI?"),
        ui.text("A: A Python library for building UI with decorators."),
        ui.divider(),
        ui.text("Q: Does it require JavaScript?"),
        ui.text("A: No — everything compiles to plain HTML."),
        ui.divider(),
        ui.link("← Back to Home", url="/"),
    ]


if __name__ == "__main__":
    app.run()
