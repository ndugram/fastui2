# OpenAPI Documentation

FastUI automatically generates OpenAPI 3.0 schema for all registered routes, with a built-in Swagger UI.

## Default Behavior

By default, FastUI provides:

- `/docs` — Swagger UI page
- `/openapi.json` — OpenAPI 3.0 JSON schema

```python
app = App()  # docs enabled by default
```

## Configuration

Customize the documentation metadata:

```python
app = App(
    title="My Application API",
    version="2.0.0",
    description="API description with **Markdown** support.",
    docs_url="/api-docs",
    openapi_url="/api-schema.json",
)
```

## Disabling Docs

```python
app = App(docs=False)
# /docs and /openapi.json will return 404
```

## Tags for Grouping

Tags group related routes in the Swagger UI:

```python
@app.page("/", title="Home", tags=["pages"])
def home(): ...

@app.page("/users", title="Users", tags=["users"])
def users(): ...

@app.page("/items", title="Items", tags=["items"])
def items(): ...

@app.page("/admin", title="Admin", tags=["admin", "users"])
def admin(): ...
```

Tags appear as a dropdown filter in the Swagger UI header.

## Schema Content

The generated OpenAPI schema includes:

- Route paths with OpenAPI-compatible parameter syntax (`{id}` instead of `{id:int}`)
- Path parameter types (integer, string)
- Route summaries from handler docstrings
- Response schemas (text/html, 200/404)
- Custom `x-page-title` extension with the page title
- Top-level tags list from all route tags

### Example Output

```json
{
  "openapi": "3.0.3",
  "info": {
    "title": "FastUI API",
    "version": "0.1.0"
  },
  "paths": {
    "/user/{id}": {
      "get": {
        "summary": "Get user profile",
        "operationId": "get_user_profile",
        "parameters": [
          {
            "name": "id",
            "in": "path",
            "required": true,
            "schema": {"type": "integer"}
          }
        ],
        "responses": {
          "200": {"description": "HTML page"},
          "404": {"description": "Page not found"}
        },
        "tags": ["users"]
      }
    }
  }
}
```

## Swagger UI Features

The built-in Swagger UI supports:

- **Route listing** — all registered GET routes
- **Parameter input** — fields for path parameters
- **Try it out** — execute requests from the browser
- **Response display** — status codes and response bodies
- **Tag filtering** — group routes by tag
- **Deep linking** — shareable URLs to specific operations

## Next Steps

Continue to [Hot Reload](hot-reload.md) to learn about auto-refresh during development.
