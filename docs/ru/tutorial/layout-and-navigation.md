# Макет и навигация

FastUI поддерживает многостраничные приложения с общей навигацией и компонентными макетами.

## Общая навигация

```python
def nav():
    return ui.page([
        ui.link("Главная", url="/", style="margin-right: 1rem;"),
        ui.link("О проекте", url="/about", style="margin-right: 1rem;"),
        ui.link("Контакты", url="/contact"),
    ], style="padding: 1rem; background: #f0f0f0; border-radius: 8px;")

@app.page("/")
def home():
    return [nav(), ui.heading("Главная", level=1)]

@app.page("/about")
def about():
    return [nav(), ui.heading("О проекте", level=1)]
```

## Page для макета

```python
ui.page([
    ui.heading("Карточка", level=2),
    ui.text("Содержимое карточки."),
], style="background: #fff; padding: 1.5rem; border-radius: 12px;")
```

## Вложенные страницы

```python
ui.page([
    ui.heading("Внешняя", level=2),
    ui.page([
        ui.text("Внутреннее содержимое"),
    ], style="background: #f9f9f9; padding: 1rem;"),
], style="border: 2px solid #ddd; padding: 1rem;")
```

## Полный пример

```python
from fastui import App, ui

app = App()

def nav():
    return ui.page([
        ui.link("Главная", url="/"),
        ui.link("Блог", url="/blog"),
    ], style="padding: 0.5rem; background: #eee; border-radius: 6px;")

@app.page("/")
def home():
    return [nav(), ui.heading("Главная", level=1)]

@app.page("/blog")
def blog():
    return [nav(), ui.heading("Блог", level=1), ui.link("Пост 1", url="/blog/hello")]

@app.page("/blog/{slug}")
def blog_post(slug: str):
    return [nav(), ui.heading(f"Пост: {slug}", level=1), ui.link("Назад", url="/blog")]

if __name__ == "__main__":
    app.run()
```

## Далее

Переходите к разделу [Настройка](customization.md).
