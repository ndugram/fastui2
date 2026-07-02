# Components

All built-in UI components, their parameters, and HTML output.

## `Heading`

```python
class Heading(
    text: str = Field(min_length=1),
    level: int = Field(default=1, ge=1, le=6),
    id: str = "",
    class_name: str = "",
    style: str = "",
)
```

Renders `<h1>` through `<h6>`.

| Parameter | Type | Default | Validation |
|---|---|---|---|
| `text` | `str` | required | `min_length=1` |
| `level` | `int` | `1` | `ge=1, le=6` |
| `id` | `str` | `""` | — |
| `class_name` | `str` | `""` | — |
| `style` | `str` | `""` | — |

**Example:** `Heading(text="Hello", level=2)` → `<h2>Hello</h2>`

---

## `Button`

```python
class Button(
    text: str = Field(min_length=1),
    on_click: str | ActionHandler | None = None,
    id: str = "",
    class_name: str = "",
    style: str = "",
)
```

```python
model_config = {"arbitrary_types_allowed": True}
```

Renders `<button>text</button>`.

| Parameter | Type | Default | Description |
|---|---|---|---|
| `text` | `str` | required | Button label. |
| `on_click` | `str \| ActionHandler \| None` | `None` | URL for navigation or callable for server action. |
| `id` | `str` | `""` | HTML id attribute. |
| `class_name` | `str` | `""` | CSS class. |
| `style` | `str` | `""` | Inline CSS. |

**Example:** `Button(text="Click", on_click="/about")` → `<button onclick="location.href='/about'">Click</button>`

---

## `Input`

```python
class Input(
    label: str = "",
    name: str = "",
    placeholder: str = "",
    type: str = "text",
    id: str = "",
    class_name: str = "",
    style: str = "",
)
```

Renders `<label>text<input type="..." name="..."></label>`.

| Parameter | Type | Default | Description |
|---|---|---|---|
| `label` | `str` | `""` | Label text. |
| `name` | `str` | `""` | HTML name attribute. |
| `placeholder` | `str` | `""` | Placeholder (falls back to label). |
| `type` | `str` | `"text"` | HTML input type. |
| `id` | `str` | `""` | HTML id attribute. |
| `class_name` | `str` | `""` | CSS class. |
| `style` | `str` | `""` | Inline CSS. |

---

## `Text`

```python
class Text(
    content: str = Field(min_length=1),
    id: str = "",
    class_name: str = "",
    style: str = "",
)
```

Renders `<p>content</p>`.

---

## `Divider`

```python
class Divider(
    id: str = "",
    class_name: str = "",
    style: str = "",
)
```

Renders `<hr>`.

---

## `Link`

```python
class Link(
    text: str = Field(min_length=1),
    url: str = "",
    id: str = "",
    class_name: str = "",
    style: str = "",
)
```

Renders `<a href="url">text</a>`. When `url` is empty, the `href` attribute is omitted.

---

## `Code`

```python
class Code(
    content: str = Field(min_length=1),
    id: str = "",
    class_name: str = "",
    style: str = "",
)
```

Renders `<pre><code>content</code></pre>`. Content is HTML-escaped.

---

## `Page`

```python
class Page(
    components: list[Component] = [],
    id: str = "",
    class_name: str = "",
    style: str = "",
)
```

```python
model_config = {"arbitrary_types_allowed": True}
```

Renders `<div>children...</div>`. Wraps child components in a container.

## `Component` Protocol

```python
@runtime_checkable
class Component(Protocol):
    def to_html(self) -> str: ...
```

Any object with a `to_html()` method returning a string is a valid component. This allows
custom components, third-party wrappers, and Pydantic models to be used interchangeably.

## `ActionHandler` TypeAlias

```python
ActionHandler: TypeAlias = Callable[[], list[Component]]
```

Zero-argument callable that returns a list of components. Used for server-side click handlers.

## `_UI` Builder

The `ui` object provides convenience methods for creating components:

```python
ui = _UI()

ui.heading(...)     # → Heading
ui.button(...)      # → Button
ui.input(...)       # → Input
ui.text(...)        # → Text
ui.divider(...)     # → Divider
ui.link(...)        # → Link
ui.code(...)        # → Code
ui.page(...)        # → Page
```
