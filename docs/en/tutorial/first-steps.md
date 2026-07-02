# First Steps

Get started with FastUI in less than 2 minutes.

## How FastUI Works

Understanding the architecture helps you use FastUI more effectively.

### The Flow

When a browser requests a page, FastUI follows this sequence:

```
1. Browser sends GET request to a URL
         ↓
2. Server receives request in _Handler.do_GET()
         ↓
3. Router matches URL against registered patterns
         ↓
4. If matched, handler function is called with extracted parameters
         ↓
5. Handler returns a list of Component objects
         ↓
6. Each component's to_html() is called
         ↓
7. Components are assembled into an HTML page with TEMPLATE
         ↓
8. HTML is sent back to the browser
```

### Key Concepts

- **App**: The main application class. Register routes and run the server.
- **Route**: A mapping from a URL pattern to a handler function.
- **Handler**: A function decorated with `@app.page()` that returns components.
- **Component**: A Pydantic model with a `to_html()` method.
- **Action**: A server-side handler registered via `Button(on_click=callable)`.

## Installation

Install FastUI with pip:

```bash
pip install fastui2
```

## Your First Page

Create a file `main.py`:

```python
from fastui import App, ui

app = App()


@app.page("/")
def home():
    return [
        ui.heading("Welcome to FastUI", level=1),
        ui.text("This is your first page."),
    ]


if __name__ == "__main__":
    app.run()
```

Run it:

```bash
python main.py
```

Output:

```
  ╔════════════════════════════════════════════╗
  ║    FastUI Dev Server                       ║
  ╠════════════════════════════════════════════╣
  ║                                            ║
  ║  →  http://127.0.0.1:8000                 ║
  ║                                            ║
  ║  📖  Docs  http://127.0.0.1:8000/docs      ║
  ║                                            ║
  ║  Routes:                                   ║
  ║   • /                                     ║
  ║                                            ║
  ╚════════════════════════════════════════════╝
```

Open `http://127.0.0.1:8000` in your browser.

## Adding a Second Page

```python
from fastui import App, ui

app = App()


@app.page("/")
def home():
    return [
        ui.heading("Home", level=1),
        ui.link("Go to About", url="/about"),
    ]


@app.page("/about")
def about():
    return [
        ui.heading("About", level=1),
        ui.text("FastUI compiles components to HTML."),
        ui.link("Back", url="/"),
    ]


if __name__ == "__main__":
    app.run()
```

## Understanding the Page Title

You can set the HTML `<title>` tag with the `title` parameter:

```python
@app.page("/about", title="About Us")
def about():
    return [ui.heading("About", level=1)]
```

If `title` is not provided, it is derived from the URL pattern.

## Return Value

Handlers can return:

- `list[Component]` — a list of components (the normal pattern)
- A single `Component` — rendered directly
- `None` or a string — rendered as-is

```python
@app.page("/single")
def single():
    return ui.heading("Single component", level=1)

@app.page("/raw")
def raw():
    return "Raw HTML works too"
```

## Next Steps

Now you know the basics. Continue to [Components](components.md) to learn about all built-in UI elements.
