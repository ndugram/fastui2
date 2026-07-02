# App

Класс `App` — главная точка входа в приложение FastUI.

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

**Параметры:**

| Параметр | Тип | По умолчанию | Описание |
|---|---|---|---|
| `css` | `str` | `""` | Пользовательский CSS. |
| `docs` | `bool` | `True` | Включить документацию по `/docs`. |
| `docs_url` | `str` | `"/docs"` | URL страницы Swagger UI. |
| `openapi_url` | `str` | `"/openapi.json"` | URL OpenAPI JSON схемы. |
| `title` | `str` | `"FastUI API"` | Заголовок API в Swagger UI. |
| `version` | `str` | `"0.1.0"` | Версия API. |
| `description` | `str` | `""` | Описание API (поддерживает Markdown). |

## `@app.page()`

```python
@app.page(pattern: str, title: str = "", tags: list[str] | None = None)
```

Зарегистрировать маршрут страницы.

## `@app.setter()`

```python
@app.setter(primary_page: bool = True)
```

Пометить маршрут как цель для редиректа с 404. Декоратор размещается **под** `@app.page()`.

Когда `primary_page=True`, переход на несуществующий URL редиректит на этот маршрут.

Можно использовать **только один раз** — повторное применение вызывает `ValueError`.

**Параметры:**

| Параметр | Тип | По умолчанию | Описание |
|---|---|---|---|
| `primary_page` | `bool` | `True` | Если `True`, 404 редиректят на URL этого маршрута. |

**Пример:**

```python
@app.page("/")
@app.setter(primary_page=True)
def home(): ...
```

## `app.action()`

```python
app.action(handler: ActionHandler) -> str
```

Зарегистрировать серверный обработчик действия. Возвращает URL действия.

## `app.run()`

```python
app.run(host="127.0.0.1", port=8000, open_browser=True, css="", hot_reload=False)
```

Запустить dev-сервер.
