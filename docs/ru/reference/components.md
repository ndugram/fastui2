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
```
