<p align="center">
  <img src="../logo.svg" style="background:white; padding:12px; border-radius:10px; width:350">
</p>
<p align="center">
    <em>Создавайте веб-интерфейсы на Python с помощью декораторов. Компиляция в HTML, ноль JavaScript.</em>
</p>
<p align="center">
<a href="https://github.com/ndugram/fastui2/actions/workflows/tests.yml" target="_blank">
    <img src="https://github.com/ndugram/fastui2/actions/workflows/tests.yml/badge.svg" alt="Tests">
</a>
<a href="https://pypi.org/project/fastui2" target="_blank">
    <img src="https://img.shields.io/pypi/v/fastui2?color=%2334D058&label=pypi%20package" alt="Package version">
</a>
<a href="https://pypi.org/project/fastui2" target="_blank">
    <img src="https://img.shields.io/pypi/pyversions/fastui.svg?color=%2334D058" alt="Supported Python versions">
</a>
</p>

---

**Документация**: <a href="https://fastui.ndugram.dev/ru/latest/" target="_blank">https://fastui.ndugram.dev/ru/latest/</a>

**Исходный код**: <a href="https://github.com/ndugram/fastui2" target="_blank">https://github.com/ndugram/fastui2</a>

---

FastUI — современная библиотека для создания **серверных веб-интерфейсов** на Python. Decorator-based API, вдохновлённый FastAPI, Pydantic-валидация компонентов, маршрутизация URL, серверные действия и встроенный Swagger UI.

Ключевые возможности:

* **Быстро**: компоненты компилируются напрямую в HTML, без шаблонизаторов. Встроенный hot reload.
* **Просто**: страницы — это функции с декораторами, возвращающие список компонентов.
* **Типизировано**: полная аннотация типов, все компоненты — Pydantic-модели со строгой валидацией.
* **Без JS**: всё компилируется в чистый HTML. Серверные действия — через лёгкий POST-механизм.
* **Маршрутизация**: URL-паттерны с типизированными параметрами (`/user/{id:int}`, `/post/{year:int}/{slug}`).
* **Интерактивно**: встроенный Swagger UI по `/docs` для просмотра и тестирования роутов.

---

## Требования

Python 3.10+

FastUI использует:

* <a href="https://docs.pydantic.dev/" target="_blank"><code>pydantic</code></a> — валидация и сериализация компонентов.
* <a href="https://pypi.org/project/annotated-doc/" target="_blank"><code>annotated-doc</code></a> — документирование параметров через `Annotated[type, Doc("...")]`.

## Установка

```console
$ pip install fastui2

---> 100%
```

## Пример

### Создайте

Файл `main.py`:

```python
from fastui import App, ui

app = App()


@app.page("/")
def home():
    return [
        ui.heading("FastUI", level=1),
        ui.text("Создавайте UI на Python. Без JavaScript."),
        ui.button("О проекте", on_click="/about"),
    ]


@app.page("/about")
def about():
    return [
        ui.heading("О проекте", level=1),
        ui.text("FastUI компилирует Pydantic-компоненты в HTML."),
        ui.link("Назад", url="/"),
    ]


if __name__ == "__main__":
    app.run()
```

### Запустите

```console
$ python main.py
```

### Проверьте

Откройте `http://127.0.0.1:8000` в браузере.

### Интерактивная документация

Перейдите на <a href="http://127.0.0.1:8000/docs" target="_blank">http://127.0.0.1:8000/docs</a>.

Вы увидите автоматическую документацию со всеми зарегистрированными маршрутами.

## Далее

- [Первые шаги](tutorial/first-steps.md) — подробное руководство
- [Компоненты](tutorial/components.md) — все встроенные компоненты
- [Маршрутизация](tutorial/routing.md) — URL-паттерны
- [Справочник](reference/index.md) — полный API reference
