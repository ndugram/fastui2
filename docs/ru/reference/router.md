# Router

Маршрутизатор URL с извлечением типизированных параметров.

## Route

```python
@dataclass
class Route(pattern, handler, param_names, param_converters, regex, title="", tags=[])
```

Зарегистрированный маршрут.

## Router

```python
class Router()
```

### `router.add(pattern, handler, title="", tags=None)`

Зарегистрировать новый маршрут.

### `router.match(path) -> Route | None`

Сопоставить путь с маршрутами.

## Синтаксис паттернов

| Паттерн | Regex | Конвертер |
|---|---|---|
| `{name}` | `([^/]+)` | `str` |
| `{name:int}` | `(\d+)` | `int` |

Примеры: `/`, `/about`, `/user/{id:int}`, `/post/{year:int}/{slug}`.
