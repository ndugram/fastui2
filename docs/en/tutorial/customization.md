# Customization

FastUI supports multiple levels of styling: global CSS, external stylesheets, and inline styles.

## Global CSS

Pass custom CSS to the `App` constructor:

```python
CUSTOM_CSS = """
body {
    font-family: 'Georgia', serif;
    max-width: 700px;
    margin: 0 auto;
    padding: 2rem;
    background: #1a1a2e;
    color: #e0e0e0;
    line-height: 1.8;
}
h1, h2, h3 { color: #e94560; }
button {
    background: #e94560;
    color: #fff;
    border: none;
    padding: 0.6rem 1.2rem;
    border-radius: 4px;
    cursor: pointer;
}
button:hover { background: #c73650; }
a { color: #0f3460; }
"""

app = App(css=CUSTOM_CSS)
```

Or pass CSS per-session in `run()`:

```python
app.run(css=CUSTOM_CSS)
```

## External Stylesheets

Add external CSS frameworks:

```python
app = App()
app.stylesheets = [
    "https://cdn.jsdelivr.net/npm/bootstrap@5.3/dist/css/bootstrap.min.css",
]
```

Now you can use Bootstrap classes:

```python
ui.button("Primary", class_name="btn btn-primary")
ui.button("Secondary", class_name="btn btn-secondary")
ui.heading("Bootstrap", level=1, class_name="text-primary")
```

## Inline Styles

Every component accepts a `style` parameter with inline CSS:

```python
ui.heading("Red heading", level=2, style="color: #e94560;")
ui.text("Big text", style="font-size: 1.2rem; font-weight: bold;")
ui.text("Box", style="border: 2px solid #4f46e5; padding: 1rem; border-radius: 8px;")
ui.button("Small", style="font-size: 0.75rem; padding: 0.25rem 0.5rem;")
ui.button("Rounded", style="border-radius: 999px;")
```

## CSS Classes

Use the `class_name` parameter to apply CSS classes:

```python
ui.heading("Title", level=1, class_name="main-title")
ui.button("Save", class_name="btn-save btn-primary")
```

## Default CSS

The default CSS provides a clean, minimal base:

```css
body {
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
    max-width: 800px; margin: 0 auto; padding: 2rem;
    background: #fafafa; color: #1a1a1a; line-height: 1.6;
}
h1, h2, h3 { margin: 1.5rem 0 0.5rem; color: #111; }
button { background: #4f46e5; color: #fff; border: none; ... }
input { width: 100%; padding: 0.5rem; border: 1px solid #ccc; ... }
```

You can override any of these by passing `css` to `App()`.

## Styling Priority

1. **Inline styles** (`style=""`) — highest priority
2. **CSS classes** (`class_name=""`) — medium priority
3. **Global CSS** (`App(css=...)`) — base styles
4. **Default CSS** — fallback

## Next Steps

Continue to [OpenAPI](openapi.md) to learn about API documentation configuration.
