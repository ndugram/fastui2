# Настройка

FastUI поддерживает несколько уровней стилизации: глобальный CSS, внешние таблицы стилей и инлайн-стили.

## Глобальный CSS

```python
CUSTOM_CSS = """
body { background: #1a1a2e; color: #e0e0e0; }
h1 { color: #e94560; }
button { background: #e94560; color: #fff; border: none; }
"""

app = App(css=CUSTOM_CSS)
```

## Внешние таблицы стилей

```python
app = App()
app.stylesheets = [
    "https://cdn.jsdelivr.net/npm/bootstrap@5.3/dist/css/bootstrap.min.css",
]
```

Теперь можно использовать классы Bootstrap:

```python
ui.button("Primary", class_name="btn btn-primary")
```

## Инлайн-стили

```python
ui.heading("Красный заголовок", level=2, style="color: #e94560;")
ui.text("Жирный текст", style="font-weight: bold;")
ui.button("Закруглённая", style="border-radius: 999px;")
```

## CSS-классы

```python
ui.heading("Заголовок", level=1, class_name="main-title")
ui.button("Сохранить", class_name="btn-save")
```

## Приоритет стилей

1. **Инлайн-стили** (`style=""`) — наивысший приоритет
2. **CSS-классы** (`class_name=""`) — средний приоритет
3. **Глобальный CSS** (`App(css=...)`) — базовые стили
4. **Стандартный CSS** — запасной вариант

## Далее

Переходите к разделу [OpenAPI](openapi.md).
