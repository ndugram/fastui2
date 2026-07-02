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

---

## `Image`

```python
class Image(
    src: str = Field(min_length=1),
    alt: str = "",
    width: str | None = None,
    height: str | None = None,
    id: str = "",
    class_name: str = "",
    style: str = "",
)
```

Renders `<img src="..." alt="...">`. `width`/`height` are only emitted when set.

**Example:** `Image(src="/logo.png", alt="Logo", width="200px")` → `<img src="/logo.png" alt="Logo" width="200px">`

---

## `SelectOption`

```python
class SelectOption(
    label: str = Field(min_length=1),
    value: str = "",
    selected: bool = False,
)
```

A single `<option>`, used inside `Select.options`. Not a top-level component (no route rendering) — always nested via `ui.select(..., options=[...])`.

---

## `Select`

```python
class Select(
    label: str = "",
    name: str = "",
    options: list[SelectOption] = [],
    id: str = "",
    class_name: str = "",
    style: str = "",
)
```

```python
model_config = {"arbitrary_types_allowed": True}
```

Renders `<label>text<select name="...">...options...</select></label>`.

**Example:**

```python
Select(label="Country", name="country", options=[
    SelectOption(label="USA", value="us"),
    SelectOption(label="Canada", value="ca", selected=True),
])
```

---

## `Checkbox`

```python
class Checkbox(
    label: str = "",
    name: str = "",
    checked: bool = False,
    id: str = "",
    class_name: str = "",
    style: str = "",
)
```

Renders `<label class="checkbox-group"><input type="checkbox" ...>text</label>`.

---

## `Textarea`

```python
class Textarea(
    label: str = "",
    name: str = "",
    placeholder: str = "",
    rows: int = 3,
    value: str = "",
    id: str = "",
    class_name: str = "",
    style: str = "",
)
```

Renders `<label>text<textarea rows="..." placeholder="...">value</textarea></label>`.

---

## `Table`

```python
class Table(
    headers: list[str] = [],
    rows: list[list[str]] = [],
    id: str = "",
    class_name: str = "",
    style: str = "",
)
```

Renders a `<table>` with an optional `<thead>` (when `headers` is non-empty) and a `<tbody>` built from `rows`.

**Example:**

```python
Table(headers=["Name", "Role"], rows=[["Alice", "Admin"], ["Bob", "User"]])
```

---

## `Alert`

```python
class Alert(
    content: str = Field(min_length=1),
    type: str = "info",
    id: str = "",
    class_name: str = "",
    style: str = "",
)
```

Renders `<div class="alert alert-{type}">content</div>`. `type` is one of `info`, `success`, `warning`, `error`.

---

## `Badge`

```python
class Badge(
    content: str = Field(min_length=1),
    type: str = "default",
    id: str = "",
    class_name: str = "",
    style: str = "",
)
```

Renders `<span class="badge badge-{type}">content</span>`. `type` is one of `default`, `primary`, `success`, `warning`, `error`.

---

## `Card`

```python
class Card(
    header: list[Component] = [],
    body: list[Component] = [],
    footer: list[Component] = [],
    id: str = "",
    class_name: str = "",
    style: str = "",
)
```

```python
model_config = {"arbitrary_types_allowed": True}
```

Renders a `<div class="card">` with `.card-header`/`.card-body`/`.card-footer` sections — each only rendered when its list is non-empty.

**Example:**

```python
Card(
    header=[Heading(text="Title", level=3)],
    body=[Text(content="Body copy.")],
    footer=[Button(text="OK")],
)
```

---

## `Navbar`

```python
class Navbar(
    brand: str = "",
    links: list[tuple[str, str]] = [],
    id: str = "",
    class_name: str = "",
    style: str = "",
)
```

Renders a `<nav>` with a `.nav-brand` span and one `.nav-link` anchor per `(label, url)` pair in `links`.

**Example:** `Navbar(brand="MyApp", links=[("Home", "/"), ("About", "/about")])`

---

## `Form`

```python
class Form(
    components: list[Component] = [],
    on_submit: str | FormActionHandler | None = None,
    id: str = "",
    class_name: str = "",
    style: str = "",
)
```

```python
model_config = {"arbitrary_types_allowed": True}
```

Renders `<form>...</form>`. When `on_submit` is a callable, `App._walk_components` registers it as a
server-side action and the form renders `onsubmit="return _fastuiSubmit(event, '/_ui/action/...')"`.
On submit, client-side JS (embedded in every page) collects the values of every named field inside the
form via `FormData`, POSTs them to the action URL, and replaces `document.body.innerHTML` with the
returned HTML fragment. A plain `Button(text="Submit")` (no `on_click`) inside the form triggers this
natively — `<button>` defaults to `type="submit"`.

**Example:**

```python
Form(
    components=[
        Input(label="Name", name="name"),
        Button(text="Send"),
    ],
    on_submit=handle_submit,  # def handle_submit(data: dict[str, str]) -> list[Component]
)
```

---

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

Zero-argument callable that returns a list of components. Used for server-side click handlers
(`Button.on_click`).

## `FormActionHandler` TypeAlias

```python
FormActionHandler: TypeAlias = Callable[[dict[str, str]], list[Component]]
```

Callable that receives the submitted field values as a `dict[str, str]` and returns a component
list. Used for form submit handlers (`Form.on_submit`).

## How server actions actually work

Every page includes a small inline `<script>` (`_fastuiAction` / `_fastuiSubmit`) that:

1. Intercepts the button click or form submit client-side.
2. Sends a `fetch(url, {method: "POST", body})` to the registered `/_ui/action/<id>` endpoint —
   `body` is a `URLSearchParams` built from the form's `FormData` for forms, or empty for buttons.
3. Replaces `document.body.innerHTML` with the HTML fragment returned by the handler.

The server parses the POST body with `urllib.parse.parse_qsl` and calls the handler with the parsed
`dict[str, str]` if it declares a parameter, or with no arguments otherwise — so the same `ActionHandler`
(zero-arg) and `FormActionHandler` (one-arg) callables both work through `Button.on_click` /
`Form.on_submit` without extra configuration.

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
ui.image(...)       # → Image
ui.select(...)      # → Select
ui.option(...)      # → SelectOption
ui.checkbox(...)    # → Checkbox
ui.textarea(...)    # → Textarea
ui.table(...)       # → Table
ui.alert(...)       # → Alert
ui.badge(...)       # → Badge
ui.card(...)        # → Card
ui.navbar(...)      # → Navbar
ui.form(...)        # → Form
```
