# Маршрутизация

FastUI использует маршрутизацию на основе URL-паттернов с типизированными параметрами.

## Базовые паттерны

### Статические пути

```python
@app.page("/")
def home(): ...

@app.page("/about")
def about(): ...
```

### Параметры пути

```python
@app.page("/user/{id:int}")
def user_profile(id: int): ...

@app.page("/hello/{name}")
def greet(name: str): ...

@app.page("/post/{year:int}/{slug}")
def blog_post(year: int, slug: str): ...
```

## Типы параметров

| Паттерн | Тип | Пример URL | В обработчике |
|---|---|---|---|
| `{name}` | `str` | `/hello/world` | `name='world'` |
| `{id:int}` | `int` | `/user/42` | `id=42` |
| `{slug}` | `str` | `/post/hello` | `slug='hello'` |

## Порядок маршрутов

Маршруты проверяются в порядке регистрации. Первый совпавший выигрывает:

```python
@app.page("/user/latest")     # проверяется первым
def latest_user(): ...

@app.page("/user/{id:int}")   # проверяется вторым
def user_profile(id: int): ...
```

Запрос к `/user/latest` попадёт на первый маршрут, а не на второй.

## Заголовок страницы

Параметр `title` устанавливает HTML-тег `<title>`:

```python
@app.page("/about", title="О нас")
def about(): ...
```

## Summary & Description

Параметры `summary` и `description` обогащают OpenAPI-схему:

```python
@app.page(
    "/",
    summary="Application home page",
    description="The main entry point showing links to all sections.",
)
def home(): ...
```

Если не указаны, извлекаются из docstring обработчика (первая строка → summary, остальное → description).

## Теги

Параметр `tags` группирует маршруты в документации:

```python
@app.page("/users", tags=["users"])
@app.page("/items", tags=["items"])
```

## Редирект с 404

Используйте `@app.setter(primary_page=True)`, чтобы перенаправлять неизвестные URL на нужную страницу. Декоратор ставится **под** `@app.page()`:

```python
@app.page("/")
@app.setter(primary_page=True)
def home():
    return [ui.heading("Home", level=1)]

@app.page("/about")
def about():
    return [ui.heading("About", level=1)]
```

Теперь любой запрос к несуществующему пути (например `/xyz`) редиректит на `/`.

Только один маршрут может быть целью редиректа. Повторное `@app.setter(primary_page=True)` вызывает ошибку.

## Далее

Переходите к разделу [Серверные действия](server-actions.md).
