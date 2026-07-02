# Аннотации типов Python

FastUI активно использует аннотации типов Python. На этой странице объясняются ключевые концепции.

## Базовые типы

### `list[Component]`

Обработчики страниц и действий возвращают список компонентов:

```python
def index() -> list:
    return [ui.heading("Привет", level=1)]
```

Тип возврата может быть `list[Component]` или просто `list`.

### `str | ActionHandler | None`

Параметр `on_click` у `Button` принимает несколько типов:

```python
# Навигация по URL (на стороне клиента)
ui.button("О нас", on_click="/about")

# Серверное действие
ui.button("Нажми", on_click=my_handler)

# Без действия
ui.button("Отключено")
```

### `Annotated[type, Doc("...")]`

FastUI использует `Annotated` для документирования параметров:

```python
from typing import Annotated
from annotated_doc import Doc

def page(
    pattern: Annotated[str, Doc("URL-паттерн для сопоставления.")],
    title: Annotated[str, Doc("Заголовок страницы для HTML <title>.")] = "",
) -> None: ...
```

## Типы-протоколы

### `Component`

Протокол `Component` определяет, что значит быть компонентом:

```python
@runtime_checkable
class Component(Protocol):
    def to_html(self) -> str: ...
```

Любой объект с методом `to_html()`, возвращающим строку, удовлетворяет этому протоколу.

### `ActionHandler`

Псевдоним типа для серверных обработчиков кликов:

```python
ActionHandler: TypeAlias = Callable[[], list[Component]]
```

Функция без аргументов, возвращающая список компонентов.

## Pydantic-модели

Все встроенные компоненты — это `BaseModel` с валидацией:

```python
class Heading(BaseModel):
    text: str = Field(min_length=1)
    level: int = Field(default=1, ge=1, le=6)
```

Некорректные данные перехватываются на этапе создания:

```python
Heading(text="", level=1)  # ValidationError
Heading(text="Привет", level=7)  # ValidationError
```
