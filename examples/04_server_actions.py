"""Server-side action handlers (POST callbacks)."""

from fastui import App, ui

app = App()

counter = 0


def increment() -> list:
    global counter
    counter += 1
    return [
        ui.heading("Incremented!", level=2, style="color: green;"),
        ui.text(f"Counter = {counter}"),
        ui.link("Back", url="/"),
    ]


def reset_counter() -> list:
    global counter
    counter = 0
    return [
        ui.heading("Reset!", level=2, style="color: orange;"),
        ui.text("Counter set back to 0."),
        ui.link("Back", url="/"),
    ]


@app.page("/", title="Server Actions")
def index():
    return [
        ui.heading("Server Actions", level=1),
        ui.text(f"Current counter value: {counter}"),
        ui.button("Increment (POST)", on_click=increment),
        ui.button("Reset (POST)", on_click=reset_counter),
        ui.divider(),
        ui.text("Actions are registered automatically when you pass a"),
        ui.code("Callable"),
        ui.text("to a button's on_click parameter."),
    ]

if __name__ == "__main__":
    app.run()
