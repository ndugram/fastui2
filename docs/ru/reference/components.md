# Компоненты

Все встроенные UI-компоненты, их параметры и HTML-результат.

## Heading

```python
class Heading(text: str, level: int = 1, id: str = "", class_name: str = "", style: str = "")
```

Рендерит `<h1>`–`<h6>`.

## Button

```python
class Button(text: str, on_click=None, id: str = "", class_name: str = "", style: str = "")
```

Рендерит `<button>text</button>`.

## Input

```python
class Input(label: str = "", name: str = "", placeholder: str = "", type: str = "text", id: str = "", class_name: str = "", style: str = "")
```

Рендерит `<label>text<input ...></label>`.

## Text

```python
class Text(content: str, id: str = "", class_name: str = "", style: str = "")
```

Рендерит `<p>content</p>`.

## Divider

```python
class Divider(id: str = "", class_name: str = "", style: str = "")
```

Рендерит `<hr>`.

## Link

```python
class Link(text: str, url: str = "", id: str = "", class_name: str = "", style: str = "")
```

Рендерит `<a href="url">text</a>`.

## Code

```python
class Code(content: str, id: str = "", class_name: str = "", style: str = "")
```

Рендерит `<pre><code>content</code></pre>`.

## Page

```python
class Page(components: list[Component] = [], id: str = "", class_name: str = "", style: str = "")
```

Рендерит `<div>children...</div>`.

## Image

```python
class Image(src: str, alt: str = "", width: str | None = None, height: str | None = None, id: str = "", class_name: str = "", style: str = "")
```

Рендерит `<img src="..." alt="...">`. `width`/`height` добавляются только если заданы.

## SelectOption

```python
class SelectOption(label: str, value: str = "", selected: bool = False)
```

Один `<option>` внутри `Select.options` — самостоятельно не рендерится на странице, только вложенно через `ui.select(..., options=[...])`.

## Select

```python
class Select(label: str = "", name: str = "", options: list[SelectOption] = [], id: str = "", class_name: str = "", style: str = "")
```

Рендерит `<label>text<select name="...">...options...</select></label>`.

## Checkbox

```python
class Checkbox(label: str = "", name: str = "", checked: bool = False, id: str = "", class_name: str = "", style: str = "")
```

Рендерит `<label class="checkbox-group"><input type="checkbox" ...>text</label>`.

## Textarea

```python
class Textarea(label: str = "", name: str = "", placeholder: str = "", rows: int = 3, value: str = "", id: str = "", class_name: str = "", style: str = "")
```

Рендерит `<label>text<textarea rows="..." placeholder="...">value</textarea></label>`.

## Table

```python
class Table(headers: list[str] = [], rows: list[list[str]] = [], id: str = "", class_name: str = "", style: str = "")
```

Рендерит `<table>` с `<thead>` (если заданы `headers`) и `<tbody>` из `rows`.

## Alert

```python
class Alert(content: str, type: str = "info", id: str = "", class_name: str = "", style: str = "")
```

Рендерит `<div class="alert alert-{type}">content</div>`. `type`: `info`, `success`, `warning`, `error`.

## Badge

```python
class Badge(content: str, type: str = "default", id: str = "", class_name: str = "", style: str = "")
```

Рендерит `<span class="badge badge-{type}">content</span>`. `type`: `default`, `primary`, `success`, `warning`, `error`.

## Card

```python
class Card(header: list[Component] = [], body: list[Component] = [], footer: list[Component] = [], id: str = "", class_name: str = "", style: str = "")
```

Рендерит `<div class="card">` с секциями `.card-header`/`.card-body`/`.card-footer` — каждая только если список не пуст.

## Navbar

```python
class Navbar(brand: str = "", links: list[tuple[str, str]] = [], id: str = "", class_name: str = "", style: str = "")
```

Рендерит `<nav>` с `.nav-brand` и ссылками `.nav-link` из пар `(label, url)`.

## `_UI` Builder

```python
ui.heading(...)     # → Heading
ui.button(...)      # → Button
ui.input(...)       # → Input
ui.text(...)        # → Text
ui.divider(...)     # → Divider
ui.link(...)        # → Link
ui.code(...)        # → Code
ui.page(...)        # → Page
ui.image(...)       # → Image
ui.select(...)      # → Select
ui.option(...)      # → SelectOption
ui.checkbox(...)    # → Checkbox
ui.textarea(...)    # → Textarea
ui.table(...)       # → Table
ui.alert(...)       # → Alert
ui.badge(...)       # → Badge
ui.card(...)        # → Card
ui.navbar(...)      # → Navbar
```
