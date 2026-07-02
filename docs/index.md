<p align="center">
  <img src="logo.svg" style="background:white; padding:12px; border-radius:10px; width:350">
</p>
<p align="center">
    <em>Build web UIs with Python decorators, compile to HTML, zero JavaScript required.</em>
</p>
<p align="center">
<a href="https://github.com/ndugram/fastui/actions/workflows/tests.yml" target="_blank">
    <img src="https://github.com/ndugram/fastui/actions/workflows/tests.yml/badge.svg" alt="Tests">
</a>
<a href="https://pypi.org/project/fastui2" target="_blank">
    <img src="https://img.shields.io/pypi/v/fastui2?color=%2334D058&label=pypi%20package" alt="Package version">
</a>
<a href="https://pypi.org/project/fastui2" target="_blank">
    <img src="https://img.shields.io/pypi/pyversions/fastui.svg?color=%2334D058" alt="Supported Python versions">
</a>
<a href="https://github.com/ndugram/fastui" target="_blank">
    <img src="https://img.shields.io/github/stars/ndugram/fastui?style=social" alt="GitHub Stars">
</a>
</p>

---

**Documentation**: <a href="https://fastui.ndugram.dev/en/latest/" target="_blank">https://fastui.ndugram.dev/en/latest/</a>

**Source Code**: <a href="https://github.com/ndugram/fastui" target="_blank">https://github.com/ndugram/fastui</a>

---

FastUI is a modern **server-rendered UI library** for Python. It brings a decorator-based API — similar to FastAPI, but for building HTML pages — with Pydantic-validated components, URL routing, server-side actions, and a built-in Swagger UI.

The key features are:

* **Fast**: components compile directly to HTML, no template engine overhead. Built-in hot reload for development.
* **Simple**: define pages as decorated Python functions, return component lists, no HTML templates.
* **Typed**: full type annotations throughout; all components are Pydantic-validated models with strict validation.
* **Zero JS**: everything compiles to plain HTML. Buttons with server actions use a lightweight POST mechanism.
* **Routed**: URL patterns with typed parameters (`/user/{id:int}`, `/post/{year:int}/{slug}`).
* **Interactive**: built-in Swagger UI via `/docs` to browse and test page routes in the browser.
* **Extensible**: custom CSS, external stylesheets, inline styles, component protocol for custom components.

---

## Requirements

Python 3.10+

FastUI stands on the shoulders of giants:

* <a href="https://docs.pydantic.dev/" target="_blank"><code>pydantic</code></a> — component model validation and serialization.
* <a href="https://pypi.org/project/annotated-doc/" target="_blank"><code>annotated-doc</code></a> — parameter documentation via `Annotated[type, Doc("...")]`.

## Installation

```console
$ pip install fastui2

---> 100%
```

## Example

### Create it

Create a file `main.py`:

```python
from fastui import App, ui

app = App()


@app.page("/")
def home():
    return [
        ui.heading("FastUI", level=1),
        ui.text("Build UIs with Python. No JavaScript required."),
        ui.button("About", on_click="/about"),
    ]


@app.page("/about")
def about():
    return [
        ui.heading("About", level=1),
        ui.text("FastUI compiles Pydantic components to HTML."),
        ui.link("Back", url="/"),
    ]


if __name__ == "__main__":
    app.run()
```

### Run it

```console
$ python main.py
```

### Check it

Open `http://127.0.0.1:8000` in your browser. You will see a page with a heading, text, and a button.

### Interactive API docs

Now go to <a href="http://127.0.0.1:8000/docs" target="_blank">http://127.0.0.1:8000/docs</a>.

You will see the automatic interactive API documentation with all registered routes:

<img src="photo/swagger_ui_home.png">

### Upgrade the example

<details markdown="1">
<summary>With typed URL parameters...</summary>

```python
@app.page("/user/{id:int}", title="Profile")
def user_profile(id: int):
    return [
        ui.heading(f"User #{id}", level=1),
        ui.text(f"Profile page for user {id}."),
        ui.link("Back", url="/"),
    ]
```

Visit `http://127.0.0.1:8000/user/42`. The `id` parameter is automatically converted to `int`.

</details>

<details markdown="1">
<summary>With server actions...</summary>

```python
counter = 0


def increment() -> list:
    global counter
    counter += 1
    return [
        ui.heading(f"Count: {counter}", level=1),
        ui.button("+1", on_click=increment),
    ]


@app.page("/counter")
def counter_page():
    return [
        ui.heading("Counter", level=1),
        ui.button("+1", on_click=increment),
    ]
```

When `on_click` receives a callable, the framework registers it as a POST endpoint.

</details>

<details markdown="1">
<summary>With custom CSS...</summary>

```python
CUSTOM = """
body { background: #1a1a2e; color: #e0e0e0; }
h1 { color: #e94560; }
button { background: #e94560; color: #fff; border: none; }
"""

app = App(css=CUSTOM)
```

</details>

<details markdown="1">
<summary>With OpenAPI tags...</summary>

```python
@app.page("/users", title="Users", tags=["users"])
def users():
    return [ui.heading("Users", level=1)]

@app.page("/items", title="Items", tags=["items"])
def items():
    return [ui.heading("Items", level=1)]
```

Tags appear as a filter in the Swagger UI header.

</details>

## Next Steps

Now you know the basics. Continue learning:

- [First Steps](en/tutorial/first-steps.md) — detailed walkthrough
- [Components](en/tutorial/components.md) — all built-in components
- [Routing](en/tutorial/routing.md) — URL patterns
- [Server Actions](en/tutorial/server-actions.md) — POST handlers
- [Reference](en/reference/index.md) — complete API reference

## FAQ

- **Why would I use FastUI instead of Flask + Jinja2?** FastUI eliminates the template layer — you write UIs entirely in Python without HTML files.
- **Why would I use FastUI instead of Streamlit?** FastUI gives you explicit control over routing, URL parameters, and page structure. Streamlit is script-based and re-runs everything on every interaction.
- **Does FastUI support async?** Not yet. Async support is planned.
- **Can I write my own components?** Yes. Any object with a `to_html()` method satisfies the `Component` protocol.
- **Is FastUI production-ready?** FastUI is in early development (v0.1.0). The API may change. Suitable for internal tools and prototypes.
