"""Multi-page application with shared navigation layout."""

from fastui import App, ui

app = App()


def nav():
    return ui.page([
        ui.link("Home", url="/", style="margin-right: 1rem;"),
        ui.link("Blog", url="/blog", style="margin-right: 1rem;"),
        ui.link("About", url="/about", style="margin-right: 1rem;"),
        ui.link("Contact", url="/contact"),
    ], style="padding: 1rem; background: #f0f0f0; border-radius: 8px; margin-bottom: 1rem;")


@app.page("/", title="Home")
def home():
    return [
        nav(),
        ui.heading("Welcome", level=1),
        ui.text("This is a multi-page site with shared navigation."),
    ]


@app.page("/blog", title="Blog")
def blog():
    return [
        nav(),
        ui.heading("Blog", level=1),
        ui.text("Blog posts will appear here."),
        ui.link("Read: Hello World", url="/blog/hello-world"),
    ]


@app.page("/blog/{slug}", title="Post")
def blog_post(slug: str):
    return [
        nav(),
        ui.heading(f"Post: {slug}", level=1),
        ui.text(f"This is the content of '{slug}'."),
        ui.link("← Back to Blog", url="/blog"),
    ]


@app.page("/about", title="About")
def about():
    return [
        nav(),
        ui.heading("About", level=1),
        ui.text("FastUI — build UIs with Python."),
    ]


@app.page("/contact", title="Contact")
def contact():
    return [
        nav(),
        ui.heading("Contact", level=1),
        ui.input(label="Name", name="name"),
        ui.input(label="Message", name="msg", placeholder="Your message..."),
        ui.button("Send (not yet implemented)", on_click="/"),
    ]

if __name__ == "__main__":
    app.run()
