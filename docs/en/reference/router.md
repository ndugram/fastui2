# Router

Pattern-based URL router with typed parameter extraction.

## `Route`

```python
@dataclass
class Route(
    pattern: str,
    handler: Callable,
    param_names: list[str],
    param_converters: list[Callable],
    regex: re.Pattern,
    title: str = "",
    tags: list[str] = [],
)
```

A registered route that maps a URL pattern to a handler function.

**Attributes:**

| Attribute | Type | Description |
|---|---|---|
| `pattern` | `str` | URL pattern string (e.g. `/user/{id:int}`). |
| `handler` | `Callable` | Handler callable invoked for this route. |
| `param_names` | `list[str]` | Names of path parameters extracted from the URL. |
| `param_converters` | `list[Callable]` | Type converters (`int`, `str`) for each parameter. |
| `regex` | `re.Pattern` | Compiled regular expression for URL matching. |
| `title` | `str` | Optional page title for the HTML template. |
| `tags` | `list[str]` | OpenAPI tags for grouping routes. |

---

## `Router`

```python
class Router()
```

### `router.add()`

```python
def add(
    pattern: str,
    handler: Callable,
    title: str = "",
    tags: list[str] | None = None,
) -> None
```

Register a new route. Parses the pattern, extracts parameter definitions, compiles the matching regex, and appends a `Route` to the route list.

**Raises:** `ValueError` if a parameter definition is malformed (empty name).

### `router.match()`

```python
def match(path: str) -> Route | None
```

Match a path against the registered routes. Iterates through the route list in registration order. On the first match, stores extracted keyword arguments in `route._match_kwargs` and returns the route. Returns `None` when no pattern matches.

**Example:**

```python
router = Router()
router.add("/", home_handler)
router.add("/user/{id:int}", user_handler)

route = router.match("/user/42")
if route:
    handler(**route._match_kwargs)  # {'id': 42}
```

## Pattern Syntax

| Pattern | Regex | Converter |
|---|---|---|
| `{name}` | `([^/]+)` | `str` |
| `{name:int}` | `(\d+)` | `int` |

Examples:

- `/` — root path
- `/about` — static path
- `/user/{id:int}` — integer parameter
- `/hello/{name}` — string parameter
- `/post/{year:int}/{slug}` — multiple parameters
- `/product/{category}/{id:int}` — mixed types
