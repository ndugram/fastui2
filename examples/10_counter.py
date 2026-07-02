"""Interactive counter with server-side actions."""

from fastui import App, ui

app = App()
count = 0


def increment():
    global count
    count += 1
    return [
        ui.heading(f"Count: {count}", level=1),
        ui.text("Incremented by 1."),
        ui.button("+1", on_click=increment),
        ui.button("Reset", on_click=reset),
        ui.link("Back to home", url="/counter"),
    ]


def reset():
    global count
    count = 0
    return [
        ui.heading(f"Count: {count}", level=1),
        ui.text("Counter reset."),
        ui.button("+1", on_click=increment),
        ui.button("Reset", on_click=reset),
        ui.link("Back to home", url="/counter"),
    ]


@app.page("/counter", title="Counter")
def counter():
    return [
        ui.heading(f"Count: {count}", level=1),
        ui.button("+1", on_click=increment),
        ui.button("Reset", on_click=reset),
    ]


@app.page("/")
def index():
    return [
        ui.heading("Examples", level=1),
        ui.link("Go to Counter", url="/counter"),
    ]

if __name__ == "__main__":
    app.run()
