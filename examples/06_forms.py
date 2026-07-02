"""Real forms — ui.form() collects field values and POSTs them to the server."""

from fastui import App, ui

app = App()


@app.page("/", title="Forms")
def index():
    return [
        ui.heading("Form Examples", level=1),
        ui.divider(),
        ui.heading("Registration", level=2),
        ui.form([
            ui.input(label="Full Name", name="name", placeholder="John Doe"),
            ui.input(label="Email", name="email", type="email", placeholder="you@example.com"),
            ui.select("Role", "role", [
                ui.option("Developer", "dev"),
                ui.option("Designer", "design"),
                ui.option("Manager", "pm"),
            ]),
            ui.checkbox("Subscribe to newsletter", name="newsletter"),
            ui.button("Register"),
        ], on_submit=handle_registration),
        ui.divider(),
        ui.text("The button has no on_click — a <button> inside a <form> submits it natively."),
        ui.text("ui.form() intercepts that submit, collects every named field, and POSTs them to on_submit."),
    ]


def handle_registration(data: dict):
    return [
        ui.heading("Registered!", level=2, style="color: green;"),
        ui.text(f"Name: {data.get('name', '')}"),
        ui.text(f"Email: {data.get('email', '')}"),
        ui.text(f"Role: {data.get('role', '')}"),
        ui.text(f"Newsletter: {'yes' if data.get('newsletter') else 'no'}"),
        ui.divider(),
        ui.link("← Back", url="/"),
    ]


if __name__ == "__main__":
    app.run()
