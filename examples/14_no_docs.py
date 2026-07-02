"""Run the app without OpenAPI docs enabled."""

from fastui import App, ui

app = App(docs=False)

@app.page("/")
def index():
    return [
        ui.heading("No Docs Mode", level=1),
        ui.text("OpenAPI docs are disabled — /docs and /openapi.json return 404."),
        ui.text("Set docs=False in the App constructor to disable them."),
    ]

if __name__ == "__main__":
    app.run()
