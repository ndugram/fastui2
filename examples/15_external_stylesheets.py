"""Add external stylesheets (e.g. Font Awesome, Google Fonts)."""

from fastui import App, ui

app = App()
app.stylesheets = [
    "https://cdn.jsdelivr.net/npm/bootstrap@5.3/dist/css/bootstrap.min.css",
]


@app.page("/")
def index():
    return [
        ui.heading("Bootstrap Styling", level=1, class_name="text-primary"),
        ui.text("This page uses Bootstrap via an external stylesheet.", class_name="lead"),
        ui.button("Primary Button", class_name="btn btn-primary"),
        ui.button("Secondary Button", class_name="btn btn-secondary"),
        ui.divider(),
        ui.text("Add stylesheets to app.stylesheets before running."),
    ]

if __name__ == "__main__":
    app.run()
