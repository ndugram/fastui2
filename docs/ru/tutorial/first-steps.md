# Первые шаги

Начните работу с FastUI менее чем за 2 минуты.

## Установка

```bash
pip install fastui2
```

## Ваша первая страница

Создайте файл `main.py`:

```python
from fastui import App, ui

app = App()


@app.page("/")
def home():
    return [
        ui.heading("Добро пожаловать в FastUI", level=1),
        ui.text("Это ваша первая страница."),
    ]


if __name__ == "__main__":
    app.run()
```

Запустите:

```bash
python main.py
```

Откройте `http://127.0.0.1:8000` в браузере.

## Добавление второй страницы

```python
from fastui import App, ui

app = App()


@app.page("/")
def home():
    return [
        ui.heading("Главная", level=1),
        ui.link("О проекте", url="/about"),
    ]


@app.page("/about")
def about():
    return [
        ui.heading("О проекте", level=1),
        ui.text("FastUI компилирует компоненты в HTML."),
        ui.link("Назад", url="/"),
    ]


if __name__ == "__main__":
    app.run()
```

## Заголовок страницы

Установите HTML-тег `<title>` через параметр `title`:

```python
@app.page("/about", title="О нас")
def about():
    return [ui.heading("О проекте", level=1)]
```

## Возвращаемые значения

Обработчики могут возвращать:

- `list[Component]` — список компонентов (основной паттерн)
- Один `Component` — рендерится напрямую
- `None` или строку — рендерится как есть

```python
@app.page("/single")
def single():
    return ui.heading("Один компонент", level=1)
```

## Далее

Переходите к разделу [Компоненты](components.md).
