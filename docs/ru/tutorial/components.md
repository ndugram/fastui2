# Компоненты

FastUI предоставляет набор Pydantic-валидированных компонентов, которые компилируются в HTML. Все компоненты доступны через объект `ui`.

## Билдер

Объект `ui` предоставляет фабричные методы для каждого компонента:

```python
from fastui import ui

ui.heading("Заголовок", level=1)
ui.text("Текст")
ui.button("Кнопка")
```

## Heading

```python
ui.heading(text="Добро пожаловать", level=1, style="color: #4f46e5;")
```

Рендерится как `<h1>Добро пожаловать</h1>` — `<h6>`.

## Text

```python
ui.text("Абзац текста.")
```

Рендерится как `<p>Абзац текста.</p>`.

## Button

```python
ui.button("О проекте", on_click="/about")
```

`on_click` может быть:
- **Строкой** — клиентская навигация: `on_click="/about"`
- **Callable** — серверное действие: `on_click=my_handler`
- **None** — без действия

## Input

```python
ui.input(label="Email", name="email", type="email", placeholder="you@example.com")
```

Рендерится как `<label>Email<input type="email" name="email"></label>`.

## Link

```python
ui.link("О проекте", url="/about")
```

Рендерится как `<a href="/about">О проекте</a>`.

## Code

```python
ui.code("def hello():\n    print('Привет, мир!')")
```

Рендерится как `<pre><code>...</code></pre>`.

## Divider

```python
ui.divider()
```

Рендерится как `<hr>`.

## Page

```python
ui.page([
    ui.heading("Карточка", level=2),
    ui.text("Содержимое карточки."),
], style="background: #f0f0ff; padding: 1rem; border-radius: 8px;")
```

Рендерится как `<div>...</div>`.

## Image

```python
ui.image("/logo.png", alt="Логотип", width="200px")
```

Рендерится как `<img src="/logo.png" alt="Логотип" width="200px">`.

## Select

```python
ui.select("Страна", "country", [
    ui.option("Выберите...", ""),
    ui.option("Россия", "ru"),
    ui.option("США", "us", selected=True),
])
```

`ui.option()` используется только внутри `options=[...]` у `ui.select()`.

## Checkbox

```python
ui.checkbox("Согласен с условиями", name="terms")
```

Рендерится как чекбокс, обёрнутый в `<label>`.

## Textarea

```python
ui.textarea("Комментарий", "comment", placeholder="Напишите что-нибудь...", rows=4)
```

Рендерится как `<label>` с `<textarea>` внутри.

## Table

```python
ui.table(
    headers=["Имя", "Роль"],
    rows=[["Алиса", "Админ"], ["Боб", "Пользователь"]],
)
```

Рендерится как `<table>` с `<thead>` и `<tbody>`.

## Alert

```python
ui.alert("Сохранено!", type="success")
```

`type`: `info`, `success`, `warning`, `error`.

## Badge

```python
ui.badge("Новое", type="primary")
```

`type`: `default`, `primary`, `success`, `warning`, `error`.

## Card

```python
ui.card(
    header=[ui.heading("Заголовок карточки", level=3)],
    body=[ui.text("Содержимое карточки.")],
    footer=[ui.button("Действие")],
)
```

Пустые секции (`header`/`body`/`footer`) просто не рендерятся.

## Navbar

```python
ui.navbar("MyApp", [
    ("Главная", "/"),
    ("О нас", "/about"),
])
```

Рендерится как `<nav>` с брендом и ссылками — удобно для общей шапки на всех страницах.

## Form — настоящая отправка формы

В отличие от остальных компонентов, `ui.form()` реально общается с сервером. Он оборачивает детей в
`<form>`; обычная `ui.button("Отправить")` внутри (без `on_click`) сабмитит её нативно, а `on_submit`
получает собранные значения полей:

```python
def handle_submit(data: dict):
    return [
        ui.heading("Спасибо!", level=2),
        ui.text(f"Имя: {data.get('name')}"),
    ]

ui.form([
    ui.input(label="Имя", name="name"),
    ui.input(label="Email", name="email", type="email"),
    ui.button("Отправить"),
], on_submit=handle_submit)
```

Под капотом: на каждой странице есть небольшой встроенный скрипт, который перехватывает событие
submit, собирает `FormData` из всех именованных полей формы и постит её на сгенерированный
`/_ui/action/...` URL. Обработчик выполняется на сервере, а вернувшийся список компонентов заменяет
всё содержимое страницы — тот же механизм, что и у серверного действия кнопки, только с переданными
значениями полей.

Это же значит, что клик по кнопке-действию (`ui.button("...", on_click=my_handler)`) работает так же
под капотом — POST и замена body, просто без полей для сбора.

## Протокол Component

Вы можете создать свой компонент:

```python
class MyWidget:
    def to_html(self) -> str:
        return '<div class="my-widget">Мой виджет</div>'
```

Любой объект с методом `to_html()` является валидным компонентом.

## Далее

Переходите к разделу [Маршрутизация](routing.md).
