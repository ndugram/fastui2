# Routing

FastUI uses a pattern-based URL router with typed parameter extraction.

## Basic Patterns

### Static Paths

```python
@app.page("/")
def home(): ...

@app.page("/about")
def about(): ...

@app.page("/contact")
def contact(): ...
```

### Path Parameters

```python
@app.page("/user/{id:int}")
def user_profile(id: int): ...

@app.page("/hello/{name}")
def greet(name: str): ...

@app.page("/post/{year:int}/{slug}")
def blog_post(year: int, slug: str): ...
```

## Parameter Types

| Pattern | Type | Example URL | Handler receives |
|---|---|---|---|
| `{name}` | `str` | `/hello/world` | `name='world'` |
| `{id:int}` | `int` | `/user/42` | `id=42` |
| `{slug}` | `str` | `/post/hello` | `slug='hello'` |

Multiple parameters are supported:

```python
@app.page("/product/{category}/{id:int}")
def product(category: str, id: int):
    return [
        ui.heading(f"Product #{id}", level=1),
        ui.text(f"Category: {category}"),
    ]
```

## How Routing Works

When a request arrives:

1. The path is normalized (trailing slashes removed)
2. Each registered route is checked in order
3. The first matching route is used
4. Path parameters are extracted and type-converted
5. The handler is called with extracted parameters as keyword arguments

```python
# Route: /user/{id:int}
# Request: /user/42
# Handler called with: user_profile(id=42)
```

## Route Order

Routes are matched in registration order. The first match wins:

```python
@app.page("/user/latest")    # checked first
def latest_user(): ...

@app.page("/user/{id:int}")  # checked second
def user_profile(id: int): ...
```

A request to `/user/latest` matches the first route (static), not the second.

## Page Title

The `title` parameter sets the HTML `<title>` tag:

```python
@app.page("/about", title="About Us")
def about():
    return [ui.heading("About", level=1)]
```

If not provided, the title is derived from the pattern:

| Pattern | Derived title |
|---|---|
| `/` | `FastUI` |
| `/about` | `About` |
| `/user/{id:int}` | `User` |

## Summary & Description

The `summary` and `description` parameters enrich the OpenAPI schema:

```python
@app.page(
    "/",
    summary="Application home page",
    description="The main entry point showing links to all sections.",
)
def home():
    return [ui.heading("Home", level=1)]
```

When not provided, they are extracted from the handler's docstring (first line → summary, rest → description).

## Tags

The `tags` parameter groups routes in the OpenAPI documentation:

```python
@app.page("/users", tags=["users"])
@app.page("/items", tags=["items"])
@app.page("/admin", tags=["admin", "users"])
```

## 404 Redirect

Use `@app.setter(primary_page=True)` to redirect unknown URLs to a specific page. The decorator must be placed **below** `@app.page()`:

```python
@app.page("/")
@app.setter(primary_page=True)
def home():
    return [ui.heading("Home", level=1)]

@app.page("/about")
def about():
    return [ui.heading("About", level=1)]
```

Now any request to a non-existent path (e.g. `/xyz`) redirects to `/`.

Only one route can be the primary redirect target. Using `@app.setter(primary_page=True)` on a second route raises an error.

## Next Steps

Now you understand routing. Continue to [Server Actions](server-actions.md) to learn about interactive buttons.
