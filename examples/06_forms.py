"""Form inputs and labels."""

from fastui import App, ui

app = App()


@app.page("/", title="Forms")
def index():
    return [
        ui.heading("Form Examples", level=1),
        ui.divider(),
        ui.heading("Login Form", level=2),
        ui.input(label="Email", name="email", type="email", placeholder="you@example.com"),
        ui.input(label="Password", name="password", type="password", placeholder="••••••••"),
        ui.divider(),
        ui.heading("Registration", level=2),
        ui.input(label="Full Name", name="name", placeholder="John Doe"),
        ui.input(label="Phone", name="phone", type="tel", placeholder="+7 (999) 123-45-67"),
        ui.divider(),
        ui.text("Forms are client-side only for now — no backend handling yet."),
        ui.text("Inputs render as label + input pairs."),
    ]

if __name__ == "__main__":
    app.run()
