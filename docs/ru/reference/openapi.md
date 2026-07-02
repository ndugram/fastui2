# OpenAPI

FastUI автоматически генерирует OpenAPI 3.0 схемы и предоставляет встроенный Swagger UI.

## `generate_openapi_schema()`

```python
generate_openapi_schema(routes, title="FastUI API", version="0.1.0", ...)
```

Генерирует OpenAPI 3.0 схему из маршрутов FastUI.

## `get_docs_html()`

```python
get_docs_html(openapi_url="/openapi.json") -> str
```

Возвращает HTML-страницу Swagger UI.

## `get_not_found_html()`

```python
get_not_found_html(docs_url="/docs", openapi_url="/openapi.json") -> str
```

Возвращает стилизованную HTML-страницу 404.
