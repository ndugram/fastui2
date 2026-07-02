# Server Actions

Server actions allow buttons to call Python functions on the server via HTTP POST requests.

## Basic Action

```python
def handle_click() -> list:
    return [
        ui.heading("Clicked!", level=2, style="color: green;"),
        ui.link("Back", url="/"),
    ]

@app.page("/")
def index():
    return [
        ui.button("Click me", on_click=handle_click),
    ]
```

When `on_click` receives a callable:

1. The framework registers it as a POST endpoint at `/_ui/action/<id>`
2. Before rendering, `_walk_components()` replaces the callable with the action URL
3. The button renders `onclick="return _fastuiAction('/_ui/action/a1')"` — a small inline script
   (shipped on every page) that fetches that URL via `POST` and swaps `document.body.innerHTML`
   with the response, so no full page reload happens
4. The server calls the handler and returns the rendered components as HTML

## How It Works

```
Browser                          Server
  │                                │
  ├── GET / ──────────────────────►│
  │                                ├── Button(on_click=handle_click)
  │                                ├── _walk_components() replaces it
  │                                ├── Renders: <button onclick="return _fastuiAction('/_ui/action/a1')">
  │◄──── HTML ─────────────────────┤
  │                                │
  ├── click button ───────────────►│
  ├── fetch POST /_ui/action/a1 ──►│
  │                                ├── Calls handle_click()
  │                                ├── Renders returned components
  │◄──── HTML fragment ────────────┤
  ├── document.body.innerHTML = … │
```

## State Management

Actions can use global state:

```python
counter = 0

def increment() -> list:
    global counter
    counter += 1
    return [
        ui.heading(f"Count: {counter}", level=1),
        ui.button("+1", on_click=increment),
        ui.link("Back", url="/counter"),
    ]

@app.page("/counter")
def counter_page():
    return [
        ui.heading(f"Count: {counter}", level=1),
        ui.button("+1", on_click=increment),
    ]
```

:::warning Important
Server actions use global variables. For concurrent access in production,
use thread-safe data structures or locks.
:::

## Multiple Actions

You can register multiple action handlers:

```python
todos = []


def add_todo():
    todos.append({"text": "New task", "done": False})
    return todo_list()


def clear_all():
    todos.clear()
    return todo_list()


def todo_list():
    items = [ui.heading("Todos", level=1)]
    items.append(ui.button("+ Add", on_click=add_todo))
    items.append(ui.button("Clear All", on_click=clear_all))
    for todo in todos:
        items.append(ui.text(f"• {todo['text']}"))
    return items
```

## Return Values

Action handlers must return a `list` of components. The returned HTML replaces the
current page content (it is not inserted in-place).

## Compared to URL Navigation

| Feature | String `on_click` | Callable `on_click` |
|---|---|---|
| Method | GET | POST |
| Use case | Navigation | State mutation |
| Speed | Instant (cached) | Server round-trip |
| State | No server state | Can modify state |

Use string URLs for navigation and callables for server-side logic.

## Forms: actions with field values

A `Button.on_click` action takes no arguments — it's built for clicks, not data entry. For actual
form fields, use `ui.form()`: it collects every named field inside it and passes them to the handler
as a `dict[str, str]`.

```python
def handle_submit(data: dict):
    return [ui.heading(f"Hi, {data.get('name')}!", level=2)]

ui.form([
    ui.input(label="Name", name="name"),
    ui.button("Submit"),  # no on_click — submits the form natively
], on_submit=handle_submit)
```

Under the hood this uses the same `/_ui/action/<id>` + `fetch` + body-swap mechanism as button
actions — the only difference is the request body carries the form's `FormData`, and the server
parses it into the `dict` your handler receives. See [Components → Form](components.md#form-real-form-submission)
for details.

## Next Steps

Continue to [Layout and Navigation](layout-and-navigation.md) to learn about multi-page apps.
