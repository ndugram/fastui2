# OpenAPI

FastUI automatically generates OpenAPI 3.0 schemas and provides a built-in Swagger UI.

## Module Functions

### `generate_openapi_schema()`

```python
def generate_openapi_schema(
    routes: list[Route],
    *,
    title: str = "FastUI API",
    version: str = "0.1.0",
    description: str = "",
    docs_url: str = "/docs",
    openapi_url: str = "/openapi.json",
) -> dict[str, Any]
```

Generate an OpenAPI 3.0 schema from FastUI routes. Each registered page route becomes a `GET` path in the schema. URL path parameters (`{id:int}`, `{slug}`) are documented as path parameters.

**Parameters:**

| Parameter | Type | Default | Description |
|---|---|---|---|
| `routes` | `list[Route]` | required | List of registered Route objects. |
| `title` | `str` | `"FastUI API"` | API title for the OpenAPI info section. |
| `version` | `str` | `"0.1.0"` | API version string. |
| `description` | `str` | `""` | API description (supports Markdown). |

**Features:**

- Path parameters are converted to OpenAPI syntax: `{id:int}` → `{id}`
- Parameter types are extracted: `int` → `{"type": "integer"}`, `str` → `{"type": "string"}`
- Route summaries are extracted from handler docstrings
- Route tags are included
- Custom `x-page-title` extension preserves HTML page titles

### `get_docs_html()`

```python
def get_docs_html(*, openapi_url: str = "/openapi.json") -> str
```

Return the Swagger UI HTML page with embedded JavaScript from CDN.

### `get_not_found_html()`

```python
def get_not_found_html(
    *, docs_url: str = "/docs", openapi_url: str = "/openapi.json"
) -> str
```

Return a styled 404 HTML page with links to the documentation.
