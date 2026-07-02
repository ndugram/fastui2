# Layout and Navigation

FastUI supports multi-page applications with shared navigation and component-based layouts.

## Shared Navigation

Create a navigation function that returns a `Page` component:

```python
def nav():
    return ui.page([
        ui.link("Home", url="/", style="margin-right: 1rem;"),
        ui.link("About", url="/about", style="margin-right: 1rem;"),
        ui.link("Contact", url="/contact"),
    ], style="padding: 1rem; background: #f0f0f0; border-radius: 8px;")


@app.page("/")
def home():
    return [nav(), ui.heading("Home", level=1)]

@app.page("/about")
def about():
    return [nav(), ui.heading("About", level=1)]

@app.page("/contact")
def contact():
    return [nav(), ui.heading("Contact", level=1)]
```

## Page Component for Layout

Use `ui.page()` to group components and apply shared styles:

```python
ui.page([
    ui.heading("Card", level=2),
    ui.text("This is a card."),
], style="background: #fff; padding: 1.5rem; border-radius: 12px; box-shadow: 0 2px 8px rgba(0,0,0,0.1);")
```

## Nested Pages

Pages can be nested inside other pages:

```python
ui.page([
    ui.heading("Outer", level=2),
    ui.page([
        ui.text("Inner content"),
        ui.button("Inner button", on_click="/"),
    ], style="background: #f9f9f9; padding: 1rem;"),
], style="border: 2px solid #ddd; padding: 1rem;")
```

## Multi-Page Example

Complete example with navigation, dynamic routes, and server actions:

```python
from fastui import App, ui

app = App()


def nav():
    return ui.page([
        ui.link("Home", url="/"),
        ui.link("Blog", url="/blog"),
    ], style="padding: 0.5rem; background: #eee; border-radius: 6px;")


@app.page("/")
def home():
    return [nav(), ui.heading("Home", level=1)]


@app.page("/blog")
def blog():
    return [
        nav(),
        ui.heading("Blog", level=1),
        ui.link("Post 1", url="/blog/hello"),
        ui.link("Post 2", url="/blog/world"),
    ]


@app.page("/blog/{slug}")
def blog_post(slug: str):
    return [
        nav(),
        ui.heading(f"Post: {slug}", level=1),
        ui.text(f"Content of '{slug}'."),
        ui.link("Back", url="/blog"),
    ]


if __name__ == "__main__":
    app.run()
```

## Navigation Patterns

### Link Navigation

```python
ui.link("Go to Profile", url="/profile")
```

### Button Navigation

```python
ui.button("Go to Profile", on_click="/profile")
```

### Dynamic Links

```python
for i in range(1, 4):
    items.append(ui.link(f"User #{i}", url=f"/user/{i}"))
```

## Next Steps

Continue to [Customization](customization.md) to learn about CSS and styling.
