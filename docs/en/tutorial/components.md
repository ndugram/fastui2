# Components

FastUI provides a set of Pydantic-validated components that compile to HTML. All components are accessible through the `ui` builder object.

## Builder Pattern

The `ui` object is an instance of `_UI` that provides factory methods for every component:

```python
from fastui import ui

ui.heading("Title", level=1)
ui.text("Body content")
ui.button("Click")
```

## Heading

```python
ui.heading(
    text="Welcome",       # str, min_length=1
    level=1,              # int, 1-6, default 1
    id="",                # HTML id attribute
    class_name="",        # CSS class
    style="",             # Inline CSS
)
```

Renders as `<h1>Welcome</h1>` through `<h6>`.

```python
ui.heading("Big Title", level=1)
ui.heading("Section", level=2, style="color: #4f46e5;")
ui.heading("Subsection", level=3, class_name="subsection")
```

## Text

```python
ui.text(
    content="Hello",      # str, min_length=1
    id="",
    class_name="",
    style="",
)
```

Renders as `<p>Hello</p>`.

```python
ui.text("A paragraph of body text.")
ui.text("Styled text", style="font-weight: bold; color: #333;")
```

## Button

```python
ui.button(
    text="Click",         # str, min_length=1
    on_click=None,        # str | Callable | None
    id="",
    class_name="",
    style="",
)
```

Renders as `<button>Click</button>`.

The `on_click` parameter controls what happens on click:

- **String** — client-side navigation: `on_click="/about"`
- **Callable** — server-side action: `on_click=my_handler` (registers POST endpoint)
- **None** — no action (static button)

```python
ui.button("Go to About", on_click="/about")
ui.button("Save", on_click=save_handler)
ui.button("Disabled")
```

## Input

```python
ui.input(
    label="Name",         # Label text
    name="name",          # HTML name attribute
    placeholder="",       # Placeholder (falls back to label)
    type="text",          # HTML input type
    id="",
    class_name="",
    style="",
)
```

Renders as `<label>Name<input type="text" name="name"></label>`.

```python
ui.input(label="Email", name="email", type="email", placeholder="you@example.com")
ui.input(label="Password", name="password", type="password")
ui.input(label="Search", name="q", placeholder="Search...")
```

## Link

```python
ui.link(
    text="Home",          # Link text, min_length=1
    url="/",              # href attribute
    id="",
    class_name="",
    style="",
)
```

Renders as `<a href="/">Home</a>`.

```python
ui.link("About", url="/about")
ui.link("External", url="https://example.com")
ui.link("Big link", url="/", style="font-size: 1.5rem; display: block;")
```

## Code

```python
ui.code(
    content="print('hi')",  # Preformatted text
    id="",
    class_name="",
    style="",
)
```

Renders as `<pre><code>print('hi')</code></pre>`.

```python
ui.code("def hello():\n    print('Hello, World!')")
```

## Divider

```python
ui.divider(id="", class_name="", style="")
```

Renders as `<hr>`.

```python
ui.divider()
ui.divider(style="margin: 2rem 0; border-color: #ccc;")
```

## Page (Container)

```python
ui.page(
    components=[],        # list of child components
    id="",
    class_name="",
    style="",
)
```

Renders as `<div>...</div>` wrapping all children.

```python
ui.page([
    ui.heading("Card Title", level=2),
    ui.text("Card content."),
], style="background: #f0f0ff; padding: 1rem; border-radius: 8px;")
```

## Styling Every Component

All components accept `id`, `class_name`, and `style`:

```python
ui.heading("Styled", level=2,
    id="main-title",
    class_name="heading-primary",
    style="color: #4f46e5; font-size: 2rem;",
)
```

## Component Protocol

You can create custom components by satisfying the `Component` protocol:

```python
from fastui.components import Component

class MyWidget:
    def to_html(self) -> str:
        return '<div class="my-widget">Custom content</div>'
```

Any object with a `to_html()` method returning a string is a valid component.

## Next Steps

Now you know all components. Continue to [Routing](routing.md) to learn about URL patterns.
