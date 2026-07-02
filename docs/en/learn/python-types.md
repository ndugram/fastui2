# Python Type Annotations

FastUI makes extensive use of Python type annotations. This page explains the key type concepts used throughout the library.

## Basic Types

### `list[Component]`

All page handlers and action handlers return a list of components:

```python
def index() -> list:
    return [ui.heading("Hello", level=1)]
```

The return type can be `list[Component]` or simply `list`.

### `str | ActionHandler | None`

The `on_click` parameter of `Button` accepts multiple types:

```python
# URL navigation (client-side)
ui.button("About", on_click="/about")

# Server-side action
ui.button("Click", on_click=my_handler)

# No action
ui.button("Disabled")
```

### `Annotated[type, Doc("...")]`

FastUI uses `Annotated` for parameter documentation, similar to FastAPI:

```python
from typing import Annotated
from annotated_doc import Doc

def page(
    pattern: Annotated[str, Doc("URL pattern to match.")],
    title: Annotated[str, Doc("Page title for HTML <title>.")] = "",
) -> None: ...
```

## Protocol Types

### `Component`

The `Component` protocol defines what it means to be a component:

```python
@runtime_checkable
class Component(Protocol):
    def to_html(self) -> str: ...
```

Any object with a `to_html()` method that returns a string satisfies this protocol.

### `ActionHandler`

A type alias for server-side click handlers:

```python
ActionHandler: TypeAlias = Callable[[], list[Component]]
```

A zero-argument callable that returns a list of components.

## Pydantic Models

All built-in components are Pydantic `BaseModel` subclasses with validation:

```python
class Heading(BaseModel):
    text: str = Field(min_length=1)
    level: int = Field(default=1, ge=1, le=6)
```

This means invalid data is caught at construction time:

```python
Heading(text="", level=1)  # ValidationError: text is too short
Heading(text="Hi", level=7)  # ValidationError: level is too high
```
