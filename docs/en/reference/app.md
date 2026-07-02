# App

The `App` class is the main entry point for FastUI applications.

## `App()`

```python
class App(
    css: str = "",
    docs: bool = True,
    docs_url: str = "/docs",
    openapi_url: str = "/openapi.json",
    title: str = "FastUI API",
    version: str = "0.1.0",
    description: str = "",
)
```

Create a new FastUI application.

**Parameters:**

| Parameter | Type | Default | Description |
|---|---|---|---|
| `css` | `str` | `""` | Custom CSS override. Falls back to built-in DEFAULT_CSS when empty. |
| `docs` | `bool` | `True` | Enable OpenAPI documentation at `/docs`. |
| `docs_url` | `str` | `"/docs"` | URL path for the Swagger UI page. |
| `openapi_url` | `str` | `"/openapi.json"` | URL path for the OpenAPI JSON schema. |
| `title` | `str` | `"FastUI API"` | API title shown in Swagger UI. |
| `version` | `str` | `"0.1.0"` | API version string. |
| `description` | `str` | `""` | API description shown in Swagger UI (supports Markdown). |

**Attributes:**

| Attribute | Type | Description |
|---|---|---|
| `css` | `str` | Current CSS styles. |
| `stylesheets` | `list[str]` | List of external stylesheet URLs. |

**Example:**

```python
from fastui import App

app = App(
    title="My API",
    version="2.0.0",
    description="My API description.",
    docs_url="/api-docs",
)
app.stylesheets.append("https://example.com/theme.css")
```

---

## `@app.page()`

```python
@app.page(
    pattern: str,
    title: str = "",
    tags: list[str] | None = None,
)
```

Register a page route via decorator.

**Parameters:**

| Parameter | Type | Description |
|---|---|---|
| `pattern` | `str` | URL pattern. Supports static paths (`/about`) and typed parameters (`/user/{id:int}`). |
| `title` | `str` | Optional page title rendered inside the HTML `<title>` tag. |
| `tags` | `list[str]` | OpenAPI tags for grouping routes in documentation. |

**Example:**

```python
@app.page("/", title="Home", tags=["pages"])
def home():
    return [ui.heading("Home", level=1)]
```

---

## `@app.setter()`

```python
@app.setter(
    primary_page: bool = True,
)
```

Mark the decorated route as the 404 redirect target. Must be placed **below** `@app.page()`.

When `primary_page=True`, visiting a non-existent URL redirects to this route.

Can only be used **once** — applying it to a second route raises `ValueError`.

**Parameters:**

| Parameter | Type | Default | Description |
|---|---|---|---|
| `primary_page` | `bool` | `True` | When `True`, 404 errors redirect to this route's URL. |

**Example:**

```python
@app.page("/")
@app.setter(primary_page=True)
def home():
    return [ui.heading("Home", level=1)]

# Visiting /xyz redirects to /
```

---

## `app.action()`

```python
app.action(handler: ActionHandler) -> str
```

Register a server-side action handler and return its URL.

**Parameters:**

| Parameter | Type | Description |
|---|---|---|
| `handler` | `ActionHandler` | Zero-argument callable that returns a list of components. |

**Returns:** `str` — the action URL (e.g. `/_ui/action/a1`).

---

## `app.run()`

```python
app.run(
    host: str = "127.0.0.1",
    port: int = 8000,
    open_browser: bool = True,
    css: str = "",
    hot_reload: bool = False,
)
```

Start the development server.

**Parameters:**

| Parameter | Type | Default | Description |
|---|---|---|---|
| `host` | `str` | `"127.0.0.1"` | Host address. |
| `port` | `int` | `8000` | TCP port. |
| `open_browser` | `bool` | `True` | Open browser on startup. |
| `css` | `str` | `""` | Override CSS for this session. |
| `hot_reload` | `bool` | `False` | Auto-refresh browser on file changes. |
