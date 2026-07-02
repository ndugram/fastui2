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
3. In the browser, clicking the button navigates to the action URL via POST
4. The server calls the handler and returns the rendered components as HTML

## How It Works

```
Browser                          Server
  │                                │
  ├── GET / ──────────────────────►│
  │                                ├── Button(on_click=handle_click)
  │                                ├── _walk_components() replaces it
  │                                ├── Renders: <button onclick="location.href='/_ui/action/a1'">
  │◄──── HTML ─────────────────────┤
  │                                │
  ├── click button ───────────────►│
  ├── POST /_ui/action/a1 ───────►│
  │                                ├── Calls handle_click()
  │                                ├── Renders returned components
  │◄──── HTML ─────────────────────┤
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

## Next Steps

Continue to [Layout and Navigation](layout-and-navigation.md) to learn about multi-page apps.
