"""Simple todo application with server actions."""

from fastui import App, ui

app = App()

todos: list[dict] = []


def add_todo():
    global todos
    todos.append({"text": "New task", "done": False})
    return _todo_list()


def toggle_todo(idx: int):
    def _toggle():
        global todos
        if 0 <= idx < len(todos):
            todos[idx]["done"] = not todos[idx]["done"]
        return _todo_list()
    return _toggle


def remove_todo(idx: int):
    def _remove():
        global todos
        if 0 <= idx < len(todos):
            todos.pop(idx)
        return _todo_list()
    return _remove


def _todo_list():
    items = []
    items.append(ui.heading("Todo App", level=1))
    items.append(ui.button("+ Add Todo", on_click=add_todo))
    items.append(ui.divider())

    if not todos:
        items.append(ui.text("No todos yet. Click '+ Add Todo' to start."))
    else:
        for i, todo in enumerate(todos):
            status = "✅" if todo["done"] else "⬜"
            items.append(ui.text(f"{status} {todo['text']}"))
            items.append(ui.page([
                ui.button("Toggle", on_click=toggle_todo(i)),
                ui.button("Delete", on_click=remove_todo(i)),
            ], style="display: flex; gap: 0.5rem;"))
            items.append(ui.divider())

    items.append(ui.link("Home", url="/"))
    return items


@app.page("/todo", title="Todo")
def todo_page():
    return _todo_list()


@app.page("/")
def index():
    return [
        ui.heading("Examples", level=1),
        ui.link("Go to Todo", url="/todo"),
    ]

if __name__ == "__main__":
    app.run()
