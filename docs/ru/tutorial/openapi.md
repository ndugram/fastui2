# OpenAPI

FastUI автоматически генерирует OpenAPI 3.0 схему для всех маршрутов со встроенным Swagger UI.

## По умолчанию

- `/docs` — страница Swagger UI
- `/openapi.json` — OpenAPI JSON схема

```python
app = App()  # документация включена по умолчанию
```

## Конфигурация

```python
app = App(
    title="Моё приложение",
    version="2.0.0",
    description="Описание API с **Markdown**.",
    docs_url="/api-docs",
    openapi_url="/api-schema.json",
)
```

## Отключение

```python
app = App(docs=False)
```

## Теги для группировки

```python
@app.page("/", title="Главная", tags=["pages"])
def home(): ...

@app.page("/users", title="Пользователи", tags=["users"])
def users(): ...

@app.page("/items", title="Товары", tags=["items"])
def items(): ...
```

## Содержимое схемы

Сгенерированная OpenAPI схема включает:

- Пути в OpenAPI-совместимом синтаксисе (`{id}` вместо `{id:int}`)
- Типы параметров пути (integer, string)
- Краткие описания из docstring обработчиков
- Схемы ответов (text/html, 200/404)
- Пользовательское расширение `x-page-title`
- Список тегов верхнего уровня

## Далее

Переходите к разделу [Hot Reload](hot-reload.md).
