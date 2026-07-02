# Серверные действия

Серверные действия позволяют кнопкам вызывать Python-функции на сервере через HTTP POST.

## Базовое действие

```python
def handle_click() -> list:
    return [
        ui.heading("Нажато!", level=2, style="color: green;"),
        ui.link("Назад", url="/"),
    ]

@app.page("/")
def index():
    return [
        ui.button("Нажми меня", on_click=handle_click),
    ]
```

Когда `on_click` получает callable:

1. Фреймворк регистрирует POST-эндпоинт по адресу `/_ui/action/<id>`
2. Перед рендерингом `_walk_components()` заменяет callable на URL действия
3. Кнопка рендерится с `onclick="return _fastuiAction('/_ui/action/a1')"` — небольшой встроенный
   скрипт (есть на каждой странице) делает `fetch` POST на этот URL и заменяет
   `document.body.innerHTML` на ответ, без перезагрузки страницы
4. Сервер вызывает обработчик и возвращает HTML-фрагмент, который приходит в ответе

## Управление состоянием

```python
counter = 0

def increment() -> list:
    global counter
    counter += 1
    return [
        ui.heading(f"Счёт: {counter}", level=1),
        ui.button("+1", on_click=increment),
    ]

@app.page("/counter")
def counter_page():
    return [
        ui.heading(f"Счёт: {counter}", level=1),
        ui.button("+1", on_click=increment),
    ]
```

## Несколько действий

```python
def add_todo():
    todos.append({"text": "Новая задача", "done": False})
    return todo_list()

def clear_all():
    todos.clear()
    return todo_list()
```

## Сравнение

| Особенность | String `on_click` | Callable `on_click` |
|---|---|---|
| Метод | GET | POST |
| Назначение | Навигация | Изменение состояния |
| Скорость | Мгновенно | Требуется запрос к серверу |
| Состояние | Нет серверного состояния | Может изменять состояние |

## Формы: действия со значениями полей

`Button.on_click` не принимает аргументов — он для кликов, не для ввода данных. Для реальных полей
формы используй `ui.form()`: он собирает значения всех именованных полей внутри и передаёт их в
обработчик как `dict[str, str]`.

```python
def handle_submit(data: dict):
    return [ui.heading(f"Привет, {data.get('name')}!", level=2)]

ui.form([
    ui.input(label="Имя", name="name"),
    ui.button("Отправить"),  # без on_click — сабмитит форму нативно
], on_submit=handle_submit)
```

Под капотом используется тот же механизм `/_ui/action/<id>` + `fetch` + замена body, что и у кнопок —
разница в том, что в теле запроса едет `FormData` формы, а сервер разбирает его в `dict`, который
получает обработчик. Подробнее — в [Компоненты → Form](components.md#form).

## Далее

Переходите к разделу [Макет и навигация](layout-and-navigation.md).
