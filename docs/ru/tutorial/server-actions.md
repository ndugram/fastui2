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
3. В браузере кнопка отправляет POST-запрос
4. Сервер вызывает обработчик и возвращает HTML

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

## Далее

Переходите к разделу [Макет и навигация](layout-and-navigation.md).
