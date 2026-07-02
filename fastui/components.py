from __future__ import annotations

from html import escape
from typing import Annotated, Callable, Protocol, TypeAlias, runtime_checkable

from pydantic import BaseModel, Field

from annotated_doc import Doc

DEFAULT_CSS: str = (
    """
body {
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
    max-width: 800px; margin: 0 auto; padding: 2rem;
    background: #fafafa; color: #1a1a1a; line-height: 1.6;
}
h1, h2, h3 { margin: 1.5rem 0 0.5rem; color: #111; }
button {
    background: #4f46e5; color: #fff; border: none; padding: 0.5rem 1rem;
    border-radius: 6px; font-size: 1rem; cursor: pointer;
}
button:hover { background: #4338ca; }
input, select, textarea {
    width: 100%; padding: 0.5rem; border: 1px solid #ccc;
    border-radius: 6px; font-size: 1rem; margin-top: 0.25rem;
    box-sizing: border-box; font-family: inherit;
}
input:focus, select:focus, textarea:focus { outline: none; border-color: #4f46e5; }
label { font-size: 0.875rem; color: #555; font-weight: 500; }
p { margin: 0.5rem 0; }
hr { border: none; border-top: 1px solid #e5e7eb; margin: 1.5rem 0; }
a { color: #4f46e5; text-decoration: none; }
a:hover { text-decoration: underline; }
pre { background: #f0f0f0; padding: 1rem; border-radius: 6px; overflow-x: auto; }
img { max-width: 100%; height: auto; border-radius: 6px; }
table { width: 100%; border-collapse: collapse; margin: 1rem 0; }
th, td { padding: 0.5rem 0.75rem; border: 1px solid #e5e7eb; text-align: left; }
th { background: #f3f4f6; font-weight: 600; }
.alert { padding: 0.75rem 1rem; border-radius: 6px; margin: 0.5rem 0; }
.alert-info { background: #eff6ff; color: #1e40af; border: 1px solid #bfdbfe; }
.alert-success { background: #f0fdf4; color: #166534; border: 1px solid #bbf7d0; }
.alert-warning { background: #fffbeb; color: #92400e; border: 1px solid #fde68a; }
.alert-error { background: #fef2f2; color: #991b1b; border: 1px solid #fecaca; }
.badge {
    display: inline-block; padding: 0.125rem 0.5rem; border-radius: 999px;
    font-size: 0.75rem; font-weight: 600; line-height: 1.4;
}
.badge-default { background: #f3f4f6; color: #374151; }
.badge-primary { background: #eef2ff; color: #3730a3; }
.badge-success { background: #f0fdf4; color: #166534; }
.badge-warning { background: #fffbeb; color: #92400e; }
.badge-error { background: #fef2f2; color: #991b1b; }
.card {
    background: #fff; border: 1px solid #e5e7eb; border-radius: 8px;
    overflow: hidden; margin: 1rem 0;
}
.card-header { padding: 0.75rem 1rem; border-bottom: 1px solid #e5e7eb;
    font-weight: 600; background: #fafafa; }
.card-body { padding: 1rem; }
.card-footer { padding: 0.75rem 1rem; border-top: 1px solid #e5e7eb;
    background: #fafafa; }
nav {
    display: flex; align-items: center; gap: 1rem; padding: 0.75rem 1rem;
    background: #fff; border-bottom: 1px solid #e5e7eb; margin-bottom: 1rem;
}
.nav-brand { font-weight: 700; font-size: 1.125rem; color: #111; }
.nav-link { color: #4f46e5; font-size: 0.875rem; }
.checkbox-group { display: flex; align-items: center; gap: 0.5rem; margin: 0.5rem 0; }
.checkbox-group input { width: auto; margin: 0; }"""
)

ActionHandler: TypeAlias = Callable[[], list["Component"]]
"""Signature for click handlers: a zero-argument callable that returns a list of components."""

FormActionHandler: TypeAlias = Callable[[dict[str, str]], list["Component"]]
"""Signature for form submit handlers: receives submitted field values, returns a component list."""

ACTION_URL_PREFIX: str = "/_ui/action/"
"""URL prefix used for server-side action/submit endpoints registered by :class:`App`."""


@runtime_checkable
class Component(Protocol):
    """
    Protocol that every UI component must satisfy.

    Any object with a ``to_html()`` method returning a ``str`` is structurally
    compatible with ``Component``. This allows Pydantic models, plain objects,
    and third-party wrappers to be used interchangeably in component trees.
    """

    def to_html(self) -> str: # type: ignore
        """
        Render the component to an HTML string.

        Returns:
            A valid HTML snippet representing this component.
        """


def _build_attrs(
    id: Annotated[str, Doc("HTML ``id`` attribute value.")] = "",
    class_name: Annotated[str, Doc("CSS class name (rendered as ``class``).")] = "",
    style: Annotated[str, Doc("Inline CSS style string.")] = "",
    **extra: Annotated[
        str | None, Doc("Additional HTML attributes as keyword arguments.")
    ],
) -> str:
    """Build an HTML attribute string from component styling properties.

    Args:
        id: The element's ``id`` attribute.
        class_name: CSS class name (mapped to ``class`` in HTML).
        style: Inline style declarations.
        **extra: Any other attributes passed as keyword arguments.

    Returns:
        A space-separated string of HTML attributes, or an empty string when
        no attributes are provided.

    Example:
        >>> _build_attrs(id="hero", class_name="title", data_role="main")
        'id="hero" class="title" data_role="main"'
    """
    parts: list[str] = []
    if id:
        parts.append(f'id="{escape(id)}"')
    if class_name:
        parts.append(f'class="{escape(class_name)}"')
    if style:
        parts.append(f'style="{escape(style)}"')
    for key, value in extra.items():
        if value is not None:
            parts.append(f'{key}="{escape(str(value))}"')
    return " ".join(parts)


class Heading(BaseModel):
    """
    A heading element (``<h1>``–``<h6>``).

    The ``level`` attribute controls which heading tag is rendered.
    Pydantic validation ensures ``level`` stays within the 1–6 range.
    """

    text: Annotated[
        str, Doc("Heading text content. Must be at least one character.")
    ] = Field(min_length=1)
    level: Annotated[
        int, Doc("Heading level (1–6). Defaults to 1.")
    ] = Field(default=1, ge=1, le=6)
    id: Annotated[str, Doc("HTML ``id`` attribute.")] = ""
    class_name: Annotated[str, Doc("CSS class name.")] = ""
    style: Annotated[str, Doc("Inline CSS style string.")] = ""

    def to_html(self) -> str:
        a = _build_attrs(self.id, self.class_name, self.style)
        a = f" {a}" if a else ""
        return f"<h{self.level}{a}>{escape(self.text)}</h{self.level}>"


class Button(BaseModel):
    """
    A clickable button element.

    The ``on_click`` field accepts either a URL string (rendered as a client-side
    ``location.href`` navigation) or a callable (registered as a server-side action).
    When a callable is provided, the :meth:`App._walk_components` method replaces
    it with a generated action URL before rendering, and the button issues a
    ``fetch()`` POST to that URL on click, replacing the page body with the
    returned HTML fragment.
    """

    model_config = {"arbitrary_types_allowed": True}

    text: Annotated[
        str, Doc("Button label. Must be at least one character.")
    ] = Field(min_length=1)
    on_click: Annotated[
        str | ActionHandler | None,
        Doc(
            "URL string for client navigation or a zero-argument callable "
            "that returns a component list for server-side handling."
        ),
    ] = None
    id: Annotated[str, Doc("HTML ``id`` attribute.")] = ""
    class_name: Annotated[str, Doc("CSS class name.")] = ""
    style: Annotated[str, Doc("Inline CSS style string.")] = ""

    def to_html(self) -> str:
        extra: dict[str, str | None] = {}
        if isinstance(self.on_click, str) and self.on_click:
            if self.on_click.startswith(ACTION_URL_PREFIX):
                extra["onclick"] = f"return _fastuiAction('{escape(self.on_click)}')"
            else:
                extra["onclick"] = f"location.href='{escape(self.on_click)}'"
        attrs = _build_attrs(self.id, self.class_name, self.style, **extra)
        attrs = f" {attrs}" if attrs else ""
        return f"<button{attrs}>{escape(self.text)}</button>"


class Input(BaseModel):
    """
    A labelled text input field (``<label>`` + ``<input>``).

    The placeholder defaults to the label text when not explicitly provided.
    The ``type`` attribute controls the HTML input type (``text``, ``email``, etc.).
    """

    label: Annotated[str, Doc("Text displayed as the field label.")] = ""
    name: Annotated[
        str, Doc("Value of the HTML ``name`` attribute for form submission.")
    ] = ""
    placeholder: Annotated[
        str, Doc("Placeholder text. Falls back to ``label`` when empty.")
    ] = ""
    type: Annotated[
        str, Doc("HTML input type (``text``, ``email``, ``password``, etc.).")
    ] = "text"
    id: Annotated[str, Doc("HTML ``id`` attribute.")] = ""
    class_name: Annotated[str, Doc("CSS class name.")] = ""
    style: Annotated[str, Doc("Inline CSS style string.")] = ""

    def to_html(self) -> str:
        placeholder = self.placeholder or self.label
        extra: dict[str, str | None] = {
            "type": self.type,
            "placeholder": escape(placeholder) if placeholder else None,
        }
        if self.name:
            extra["name"] = self.name
        attrs = _build_attrs(self.id, self.class_name, self.style, **extra)
        attrs = f" {attrs}" if attrs else ""
        return f"<label>{escape(self.label)}<input{attrs}></label>"


class Text(BaseModel):
    """
    A paragraph element (``<p>``).

    Use for body text, descriptions, and other prose content.
    """

    content: Annotated[
        str, Doc("Paragraph text. Must be at least one character.")
    ] = Field(min_length=1)
    id: Annotated[str, Doc("HTML ``id`` attribute.")] = ""
    class_name: Annotated[str, Doc("CSS class name.")] = ""
    style: Annotated[str, Doc("Inline CSS style string.")] = ""

    def to_html(self) -> str:
        attrs = _build_attrs(self.id, self.class_name, self.style)
        attrs = f" {attrs}" if attrs else ""
        return f"<p{attrs}>{escape(self.content)}</p>"


class Divider(BaseModel):
    """
    A horizontal rule (``<hr>``).

    Renders a thematic break between sections of content.
    """

    id: Annotated[str, Doc("HTML ``id`` attribute.")] = ""
    class_name: Annotated[str, Doc("CSS class name.")] = ""
    style: Annotated[str, Doc("Inline CSS style string.")] = ""

    def to_html(self) -> str:
        attrs = _build_attrs(self.id, self.class_name, self.style)
        attrs = f" {attrs}" if attrs else ""
        return f"<hr{attrs}>"


class Link(BaseModel):
    """
    An anchor element (``<a>``).

    Renders a hyperlink with an ``href`` attribute pointing to the given ``url``.
    When ``url`` is empty the ``href`` attribute is omitted, producing a
    placeholder link.
    """

    text: Annotated[
        str, Doc("Link text displayed to the user. Must be at least one character.")
    ] = Field(min_length=1)
    url: Annotated[str, Doc("Target URL for the ``href`` attribute.")] = ""
    id: Annotated[str, Doc("HTML ``id`` attribute.")] = ""
    class_name: Annotated[str, Doc("CSS class name.")] = ""
    style: Annotated[str, Doc("Inline CSS style string.")] = ""

    def to_html(self) -> str:
        extra: dict[str, str | None] = {"href": self.url or None}
        attrs = _build_attrs(self.id, self.class_name, self.style, **extra)
        attrs = f" {attrs}" if attrs else ""
        return f"<a{attrs}>{escape(self.text)}</a>"


class Code(BaseModel):
    """
    A code block (``<pre><code>``).

    Renders preformatted text with syntax-preserving whitespace.
    Content is HTML-escaped before rendering.
    """

    content: Annotated[
        str,
        Doc(
            "Source code or preformatted text. Must be at least one character."
        ),
    ] = Field(min_length=1)
    id: Annotated[str, Doc("HTML ``id`` attribute.")] = ""
    class_name: Annotated[str, Doc("CSS class name.")] = ""
    style: Annotated[str, Doc("Inline CSS style string.")] = ""

    def to_html(self) -> str:
        attrs = _build_attrs(self.id, self.class_name, self.style)
        attrs = f" {attrs}" if attrs else ""
        return f"<pre{attrs}><code>{escape(self.content)}</code></pre>"


class Page(BaseModel):
    """
    A container component that groups child components.

    Renders as a ``<div>`` wrapping the concatenated HTML of its children.
    Useful for grouping related components or applying shared styles to a
    section of the page.
    """

    model_config = {"arbitrary_types_allowed": True}

    components: Annotated[
        list[Component],
        Doc("List of child components to render inside the container."),
    ] = Field(default_factory=list)
    id: Annotated[str, Doc("HTML ``id`` attribute.")] = ""
    class_name: Annotated[str, Doc("CSS class name.")] = ""
    style: Annotated[str, Doc("Inline CSS style string.")] = ""

    def to_html(self) -> str:
        inner = "\n".join(c.to_html() for c in self.components)
        attrs = _build_attrs(self.id, self.class_name, self.style)
        attrs = f" {attrs}" if attrs else ""
        return f"<div{attrs}>\n{inner}\n</div>"


class Image(BaseModel):
    """
    An image element (``<img>``).

    Renders a self-closing ``img`` tag with ``src`` and ``alt`` attributes.
    """

    src: Annotated[
        str, Doc("Image source URL. Must be at least one character.")
    ] = Field(min_length=1)
    alt: Annotated[str, Doc("Alternative text for accessibility.")] = ""
    width: Annotated[
        str | None, Doc("Image width (e.g. ``\"100%\"``, ``\"200px\"``).")
    ] = None
    height: Annotated[
        str | None, Doc("Image height (e.g. ``\"auto\"``, ``\"150px\"``).")
    ] = None
    id: Annotated[str, Doc("HTML ``id`` attribute.")] = ""
    class_name: Annotated[str, Doc("CSS class name.")] = ""
    style: Annotated[str, Doc("Inline CSS style string.")] = ""

    def to_html(self) -> str:
        extra: dict[str, str | None] = {"src": self.src, "alt": self.alt or None}
        if self.width:
            extra["width"] = self.width
        if self.height:
            extra["height"] = self.height
        attrs = _build_attrs(self.id, self.class_name, self.style, **extra)
        attrs = f" {attrs}" if attrs else ""
        return f"<img{attrs}>"


class SelectOption(BaseModel):
    """A single ``<option>`` inside a :class:`Select` component."""

    label: Annotated[
        str, Doc("Display text for the option.")
    ] = Field(min_length=1)
    value: Annotated[str, Doc("Value submitted when this option is selected.")] = ""
    selected: Annotated[bool, Doc("Whether this option is pre-selected.")] = False

    def to_html(self) -> str:
        attrs = _build_attrs(value=self.value)
        attrs = f" {attrs}" if attrs else ""
        selected = " selected" if self.selected else ""
        return f"<option{attrs}{selected}>{escape(self.label)}</option>"


class Select(BaseModel):
    """
    A dropdown select element (``<label>`` + ``<select>``).

    Renders a ``select`` tag containing the given ``options``.
    """

    model_config = {"arbitrary_types_allowed": True}

    label: Annotated[str, Doc("Text displayed as the field label.")] = ""
    name: Annotated[str, Doc("HTML ``name`` attribute for form submission.")] = ""
    options: Annotated[
        list[SelectOption], Doc("List of options to render inside the select.")
    ] = Field(default_factory=list)
    id: Annotated[str, Doc("HTML ``id`` attribute.")] = ""
    class_name: Annotated[str, Doc("CSS class name.")] = ""
    style: Annotated[str, Doc("Inline CSS style string.")] = ""

    def to_html(self) -> str:
        extra: dict[str, str | None] = {"name": self.name or None}
        attrs = _build_attrs(self.id, self.class_name, self.style, **extra)
        attrs = f" {attrs}" if attrs else ""
        options = "\n".join(f"  {o.to_html()}" for o in self.options)
        select = f"<select{attrs}>\n{options}\n</select>"
        return f"<label>{escape(self.label)}{select}</label>" if self.label else select


class Checkbox(BaseModel):
    """
    A checkbox input (``<input type="checkbox">``).

    Renders a labelled checkbox within a ``<label>`` wrapper.
    """

    label: Annotated[str, Doc("Text displayed next to the checkbox.")] = ""
    name: Annotated[str, Doc("HTML ``name`` attribute for form submission.")] = ""
    checked: Annotated[bool, Doc("Whether the checkbox is pre-checked.")] = False
    id: Annotated[str, Doc("HTML ``id`` attribute.")] = ""
    class_name: Annotated[str, Doc("CSS class name.")] = ""
    style: Annotated[str, Doc("Inline CSS style string.")] = ""

    def to_html(self) -> str:
        extra: dict[str, str | None] = {"type": "checkbox"}
        if self.name:
            extra["name"] = self.name
        attrs = _build_attrs(self.id, self.class_name, self.style, **extra)
        attrs = f" {attrs}" if attrs else ""
        checked = " checked" if self.checked else ""
        return (
            f'<label class="checkbox-group"><input{attrs}{checked}>'
            f"{escape(self.label)}</label>"
        )


class Textarea(BaseModel):
    """
    A multi-line text input (``<label>`` + ``<textarea>``).

    Renders a ``textarea`` element with optional placeholder and row count.
    """

    label: Annotated[str, Doc("Text displayed as the field label.")] = ""
    name: Annotated[str, Doc("HTML ``name`` attribute for form submission.")] = ""
    placeholder: Annotated[str, Doc("Placeholder text inside the textarea.")] = ""
    rows: Annotated[int, Doc("Number of visible text rows.")] = 3
    value: Annotated[str, Doc("Pre-filled text content.")] = ""
    id: Annotated[str, Doc("HTML ``id`` attribute.")] = ""
    class_name: Annotated[str, Doc("CSS class name.")] = ""
    style: Annotated[str, Doc("Inline CSS style string.")] = ""

    def to_html(self) -> str:
        extra: dict[str, str | None] = {
            "rows": str(self.rows),
            "placeholder": escape(self.placeholder) if self.placeholder else None,
        }
        if self.name:
            extra["name"] = self.name
        attrs = _build_attrs(self.id, self.class_name, self.style, **extra)
        attrs = f" {attrs}" if attrs else ""
        textarea = f"<textarea{attrs}>{escape(self.value)}</textarea>"
        return f"<label>{escape(self.label)}{textarea}</label>" if self.label else textarea


class Table(BaseModel):
    """
    A data table (``<table>``).

    Renders ``headers`` as a header row and ``rows`` as body rows.
    """

    headers: Annotated[list[str], Doc("Column header labels.")] = Field(default_factory=list)
    rows: Annotated[
        list[list[str]], Doc("Table body rows, each a list of cell values.")
    ] = Field(default_factory=list)
    id: Annotated[str, Doc("HTML ``id`` attribute.")] = ""
    class_name: Annotated[str, Doc("CSS class name.")] = ""
    style: Annotated[str, Doc("Inline CSS style string.")] = ""

    def to_html(self) -> str:
        attrs = _build_attrs(self.id, self.class_name, self.style)
        attrs = f" {attrs}" if attrs else ""
        thead = ""
        if self.headers:
            cells = "".join(f"<th>{escape(h)}</th>" for h in self.headers)
            thead = f"<thead><tr>{cells}</tr></thead>\n"
        body_rows = "\n".join(
            "<tr>" + "".join(f"<td>{escape(cell)}</td>" for cell in row) + "</tr>"
            for row in self.rows
        )
        return f"<table{attrs}>\n{thead}<tbody>\n{body_rows}\n</tbody>\n</table>"


class Alert(BaseModel):
    """
    A dismissible-style alert banner.

    ``type`` controls the visual variant: ``info``, ``success``, ``warning``,
    or ``error``.
    """

    content: Annotated[str, Doc("Alert message text.")] = Field(min_length=1)
    type: Annotated[
        str, Doc("Alert variant: ``info``, ``success``, ``warning``, or ``error``.")
    ] = "info"
    id: Annotated[str, Doc("HTML ``id`` attribute.")] = ""
    class_name: Annotated[str, Doc("CSS class name.")] = ""
    style: Annotated[str, Doc("Inline CSS style string.")] = ""

    def to_html(self) -> str:
        class_name = f"alert alert-{self.type} {self.class_name}".strip()
        attrs = _build_attrs(self.id, class_name, self.style)
        attrs = f" {attrs}" if attrs else ""
        return f"<div{attrs}>{escape(self.content)}</div>"


class Badge(BaseModel):
    """
    A small status badge (``<span>``).

    ``type`` controls the visual variant: ``default``, ``primary``,
    ``success``, ``warning``, or ``error``.
    """

    content: Annotated[str, Doc("Badge text.")] = Field(min_length=1)
    type: Annotated[
        str,
        Doc("Badge variant: ``default``, ``primary``, ``success``, ``warning``, or ``error``."),
    ] = "default"
    id: Annotated[str, Doc("HTML ``id`` attribute.")] = ""
    class_name: Annotated[str, Doc("CSS class name.")] = ""
    style: Annotated[str, Doc("Inline CSS style string.")] = ""

    def to_html(self) -> str:
        class_name = f"badge badge-{self.type} {self.class_name}".strip()
        attrs = _build_attrs(self.id, class_name, self.style)
        attrs = f" {attrs}" if attrs else ""
        return f"<span{attrs}>{escape(self.content)}</span>"


class Card(BaseModel):
    """
    A card container with optional header, body, and footer sections.

    Each section accepts a list of :class:`Component` instances and renders
    only if non-empty.
    """

    model_config = {"arbitrary_types_allowed": True}

    header: Annotated[
        list[Component], Doc("Components rendered in the card header.")
    ] = Field(default_factory=list)
    body: Annotated[
        list[Component], Doc("Components rendered in the card body.")
    ] = Field(default_factory=list)
    footer: Annotated[
        list[Component], Doc("Components rendered in the card footer.")
    ] = Field(default_factory=list)
    id: Annotated[str, Doc("HTML ``id`` attribute.")] = ""
    class_name: Annotated[str, Doc("CSS class name.")] = ""
    style: Annotated[str, Doc("Inline CSS style string.")] = ""

    def to_html(self) -> str:
        class_name = f"card {self.class_name}".strip()
        attrs = _build_attrs(self.id, class_name, self.style)
        attrs = f" {attrs}" if attrs else ""
        sections = ""
        if self.header:
            sections += '<div class="card-header">\n' + "\n".join(c.to_html() for c in self.header) + "\n</div>\n"
        if self.body:
            sections += '<div class="card-body">\n' + "\n".join(c.to_html() for c in self.body) + "\n</div>\n"
        if self.footer:
            sections += '<div class="card-footer">\n' + "\n".join(c.to_html() for c in self.footer) + "\n</div>\n"
        return f"<div{attrs}>\n{sections}</div>"


class Navbar(BaseModel):
    """A simple navigation bar with a brand label and a list of links."""

    brand: Annotated[str, Doc("Brand text shown on the left.")] = ""
    links: Annotated[
        list[tuple[str, str]], Doc("List of ``(label, url)`` pairs.")
    ] = Field(default_factory=list)
    id: Annotated[str, Doc("HTML ``id`` attribute.")] = ""
    class_name: Annotated[str, Doc("CSS class name.")] = ""
    style: Annotated[str, Doc("Inline CSS style string.")] = ""

    def to_html(self) -> str:
        attrs = _build_attrs(self.id, self.class_name, self.style)
        attrs = f" {attrs}" if attrs else ""
        brand = f'<span class="nav-brand">{escape(self.brand)}</span>\n' if self.brand else ""
        links = "\n".join(
            f'<a class="nav-link" href="{escape(url)}">{escape(label)}</a>'
            for label, url in self.links
        )
        return f"<nav{attrs}>\n{brand}{links}\n</nav>"


class Form(BaseModel):
    """
    A real HTML form that submits its named fields to a server action.

    Wraps ``components`` in a ``<form>``. When ``on_submit`` is a callable,
    :meth:`App._walk_components` registers it as a server-side action and the
    form intercepts its ``submit`` event, collects the values of every named
    ``Input``/``Select``/``Checkbox``/``Textarea`` inside it, and POSTs them
    to the server — the handler receives a ``dict[str, str]`` of field values
    and returns a component list that replaces the page body.

    A plain ``ui.button("Submit")`` (``on_click=None``) placed inside the form
    triggers this natively, since ``<button>`` defaults to ``type="submit"``.
    """

    model_config = {"arbitrary_types_allowed": True}

    components: Annotated[
        list[Component], Doc("Form fields and other child components.")
    ] = Field(default_factory=list)
    on_submit: Annotated[
        str | FormActionHandler | None,
        Doc(
            "URL string or a callable receiving submitted field values "
            "(``dict[str, str]``) and returning a component list."
        ),
    ] = None
    id: Annotated[str, Doc("HTML ``id`` attribute.")] = ""
    class_name: Annotated[str, Doc("CSS class name.")] = ""
    style: Annotated[str, Doc("Inline CSS style string.")] = ""

    def to_html(self) -> str:
        inner = "\n".join(c.to_html() for c in self.components)
        attrs = _build_attrs(self.id, self.class_name, self.style)
        attrs = f" {attrs}" if attrs else ""
        onsubmit = ""
        if isinstance(self.on_submit, str) and self.on_submit:
            onsubmit = f" onsubmit=\"return _fastuiSubmit(event, '{escape(self.on_submit)}')\""
        return f"<form{attrs}{onsubmit}>\n{inner}\n</form>"


class _UI:
    """
    Convenience builder for creating component instances.

    Each method on this class constructs a single component with the given
    parameters and returns it. This avoids importing individual component
    classes and makes component trees more readable.

    Example:
        ```python
        from fastui import ui

        components = [
            ui.heading("Hello", level=1),
            ui.button("Click me"),
        ]
        ```
    """

    def heading(
        self,
        text: Annotated[str, Doc("Heading text.")],
        level: Annotated[int, Doc("Heading level (1–6).")] = 1,
        id: Annotated[str, Doc("HTML ``id`` attribute.")] = "",
        class_name: Annotated[str, Doc("CSS class name.")] = "",
        style: Annotated[str, Doc("Inline CSS style.")] = "",
    ) -> Heading:
        """Create a :class:`Heading` component.

        Args:
            text: Heading text content.
            level: Heading level (1–6, defaults to 1).
            id: HTML id attribute.
            class_name: CSS class name.
            style: Inline CSS style string.

        Returns:
            A new :class:`Heading` instance.

        Example:
            >>> ui.heading("Welcome", level=2, style="color: red;")
            Heading(text='Welcome', level=2, ...)
        """
        return Heading(text=text, level=level, id=id, class_name=class_name, style=style)

    def button(
        self,
        text: Annotated[str, Doc("Button label.")],
        on_click: Annotated[
            str | ActionHandler | None,
            Doc("URL or server-side callable invoked on click."),
        ] = None,
        id: Annotated[str, Doc("HTML ``id`` attribute.")] = "",
        class_name: Annotated[str, Doc("CSS class name.")] = "",
        style: Annotated[str, Doc("Inline CSS style.")] = "",
    ) -> Button:
        """Create a :class:`Button` component.

        Args:
            text: Button label.
            on_click: URL for client navigation or callable for server handling.
            id: HTML id attribute.
            class_name: CSS class name.
            style: Inline CSS style string.

        Returns:
            A new :class:`Button` instance.

        Example:
            >>> ui.button("Save", on_click=save_handler)
            Button(text='Save', on_click=<function save_handler at ...>)
        """
        return Button(text=text, on_click=on_click, id=id, class_name=class_name, style=style)

    def input(
        self,
        label: Annotated[str, Doc("Field label text.")] = "",
        name: Annotated[str, Doc("HTML ``name`` attribute.")] = "",
        placeholder: Annotated[str, Doc("Placeholder text.")] = "",
        type: Annotated[
            str, Doc("HTML input type (``text``, ``password``, etc.).")
        ] = "text",
        id: Annotated[str, Doc("HTML ``id`` attribute.")] = "",
        class_name: Annotated[str, Doc("CSS class name.")] = "",
        style: Annotated[str, Doc("Inline CSS style.")] = "",
    ) -> Input:
        """Create an :class:`Input` component.

        Args:
            label: Text displayed as the field label.
            name: Form submission name.
            placeholder: Placeholder text (falls back to ``label``).
            type: HTML input type.
            id: HTML id attribute.
            class_name: CSS class name.
            style: Inline CSS style string.

        Returns:
            A new :class:`Input` instance.
        """
        return Input(
            label=label,
            name=name,
            placeholder=placeholder,
            type=type,
            id=id,
            class_name=class_name,
            style=style,
        )

    def text(
        self,
        content: Annotated[str, Doc("Paragraph text.")],
        id: Annotated[str, Doc("HTML ``id`` attribute.")] = "",
        class_name: Annotated[str, Doc("CSS class name.")] = "",
        style: Annotated[str, Doc("Inline CSS style.")] = "",
    ) -> Text:
        """Create a :class:`Text` component.

        Args:
            content: Paragraph text content.
            id: HTML id attribute.
            class_name: CSS class name.
            style: Inline CSS style string.

        Returns:
            A new :class:`Text` instance.
        """
        return Text(content=content, id=id, class_name=class_name, style=style)

    def divider(
        self,
        id: Annotated[str, Doc("HTML ``id`` attribute.")] = "",
        class_name: Annotated[str, Doc("CSS class name.")] = "",
        style: Annotated[str, Doc("Inline CSS style.")] = "",
    ) -> Divider:
        """Create a :class:`Divider` component.

        Args:
            id: HTML id attribute.
            class_name: CSS class name.
            style: Inline CSS style string.

        Returns:
            A new :class:`Divider` instance.
        """
        return Divider(id=id, class_name=class_name, style=style)

    def link(
        self,
        text: Annotated[str, Doc("Link text.")],
        url: Annotated[str, Doc("Target URL.")] = "",
        id: Annotated[str, Doc("HTML ``id`` attribute.")] = "",
        class_name: Annotated[str, Doc("CSS class name.")] = "",
        style: Annotated[str, Doc("Inline CSS style.")] = "",
    ) -> Link:
        """Create a :class:`Link` component.

        Args:
            text: Link text displayed to the user.
            url: Target URL for navigation.
            id: HTML id attribute.
            class_name: CSS class name.
            style: Inline CSS style string.

        Returns:
            A new :class:`Link` instance.
        """
        return Link(text=text, url=url, id=id, class_name=class_name, style=style)

    def code(
        self,
        content: Annotated[str, Doc("Preformatted text content.")],
        id: Annotated[str, Doc("HTML ``id`` attribute.")] = "",
        class_name: Annotated[str, Doc("CSS class name.")] = "",
        style: Annotated[str, Doc("Inline CSS style.")] = "",
    ) -> Code:
        """Create a :class:`Code` component.

        Args:
            content: Code or preformatted text.
            id: HTML id attribute.
            class_name: CSS class name.
            style: Inline CSS style string.

        Returns:
            A new :class:`Code` instance.
        """
        return Code(content=content, id=id, class_name=class_name, style=style)

    def page(
        self,
        components: Annotated[list[Component], Doc("List of child components.")] = [],
        id: Annotated[str, Doc("HTML ``id`` attribute.")] = "",
        class_name: Annotated[str, Doc("CSS class name.")] = "",
        style: Annotated[str, Doc("Inline CSS style.")] = "",
    ) -> Page:
        """Create a :class:`Page` component.

        Args:
            components: List of child components to wrap.
            id: HTML id attribute.
            class_name: CSS class name.
            style: Inline CSS style string.

        Returns:
            A new :class:`Page` instance.
        """
        return Page(components=components, id=id, class_name=class_name, style=style)

    def image(
        self,
        src: Annotated[str, Doc("Image source URL.")],
        alt: Annotated[str, Doc("Alternative text.")] = "",
        width: Annotated[str | None, Doc("Image width.")] = None,
        height: Annotated[str | None, Doc("Image height.")] = None,
        id: Annotated[str, Doc("HTML ``id`` attribute.")] = "",
        class_name: Annotated[str, Doc("CSS class name.")] = "",
        style: Annotated[str, Doc("Inline CSS style.")] = "",
    ) -> Image:
        """Create an :class:`Image` component."""
        return Image(src=src, alt=alt, width=width, height=height, id=id, class_name=class_name, style=style)

    def select(
        self,
        label: Annotated[str, Doc("Field label.")] = "",
        name: Annotated[str, Doc("HTML ``name`` attribute.")] = "",
        options: Annotated[list[SelectOption], Doc("List of options.")] = [],
        id: Annotated[str, Doc("HTML ``id`` attribute.")] = "",
        class_name: Annotated[str, Doc("CSS class name.")] = "",
        style: Annotated[str, Doc("Inline CSS style.")] = "",
    ) -> Select:
        """Create a :class:`Select` component."""
        return Select(label=label, name=name, options=options, id=id, class_name=class_name, style=style)

    def option(
        self,
        label: Annotated[str, Doc("Option display text.")],
        value: Annotated[str, Doc("Submission value.")] = "",
        selected: Annotated[bool, Doc("Pre-selected.")] = False,
    ) -> SelectOption:
        """Create a :class:`SelectOption` for use in :class:`Select`."""
        return SelectOption(label=label, value=value, selected=selected)

    def checkbox(
        self,
        label: Annotated[str, Doc("Checkbox label text.")] = "",
        name: Annotated[str, Doc("HTML ``name`` attribute.")] = "",
        checked: Annotated[bool, Doc("Pre-checked state.")] = False,
        id: Annotated[str, Doc("HTML ``id`` attribute.")] = "",
        class_name: Annotated[str, Doc("CSS class name.")] = "",
        style: Annotated[str, Doc("Inline CSS style.")] = "",
    ) -> Checkbox:
        """Create a :class:`Checkbox` component."""
        return Checkbox(label=label, name=name, checked=checked, id=id, class_name=class_name, style=style)

    def textarea(
        self,
        label: Annotated[str, Doc("Field label.")] = "",
        name: Annotated[str, Doc("HTML ``name`` attribute.")] = "",
        placeholder: Annotated[str, Doc("Placeholder text.")] = "",
        rows: Annotated[int, Doc("Number of rows.")] = 3,
        value: Annotated[str, Doc("Pre-filled text.")] = "",
        id: Annotated[str, Doc("HTML ``id`` attribute.")] = "",
        class_name: Annotated[str, Doc("CSS class name.")] = "",
        style: Annotated[str, Doc("Inline CSS style.")] = "",
    ) -> Textarea:
        """Create a :class:`Textarea` component."""
        return Textarea(
            label=label, name=name, placeholder=placeholder, rows=rows,
            value=value, id=id, class_name=class_name, style=style,
        )

    def table(
        self,
        headers: Annotated[list[str], Doc("Column headers.")] = [],
        rows: Annotated[list[list[str]], Doc("Data rows.")] = [],
        id: Annotated[str, Doc("HTML ``id`` attribute.")] = "",
        class_name: Annotated[str, Doc("CSS class name.")] = "",
        style: Annotated[str, Doc("Inline CSS style.")] = "",
    ) -> Table:
        """Create a :class:`Table` component."""
        return Table(headers=headers, rows=rows, id=id, class_name=class_name, style=style)

    def alert(
        self,
        content: Annotated[str, Doc("Alert message.")],
        type: Annotated[str, Doc("Alert variant (info, success, warning, error).")] = "info",
        id: Annotated[str, Doc("HTML ``id`` attribute.")] = "",
        class_name: Annotated[str, Doc("CSS class name.")] = "",
        style: Annotated[str, Doc("Inline CSS style.")] = "",
    ) -> Alert:
        """Create an :class:`Alert` component."""
        return Alert(content=content, type=type, id=id, class_name=class_name, style=style)

    def badge(
        self,
        content: Annotated[str, Doc("Badge text.")],
        type: Annotated[str, Doc("Badge variant (default, primary, success, warning, error).")] = "default",
        id: Annotated[str, Doc("HTML ``id`` attribute.")] = "",
        class_name: Annotated[str, Doc("CSS class name.")] = "",
        style: Annotated[str, Doc("Inline CSS style.")] = "",
    ) -> Badge:
        """Create a :class:`Badge` component."""
        return Badge(content=content, type=type, id=id, class_name=class_name, style=style)

    def card(
        self,
        header: Annotated[list[Component], Doc("Header components.")] = [],
        body: Annotated[list[Component], Doc("Body components.")] = [],
        footer: Annotated[list[Component], Doc("Footer components.")] = [],
        id: Annotated[str, Doc("HTML ``id`` attribute.")] = "",
        class_name: Annotated[str, Doc("CSS class name.")] = "",
        style: Annotated[str, Doc("Inline CSS style.")] = "",
    ) -> Card:
        """Create a :class:`Card` component."""
        return Card(header=header, body=body, footer=footer, id=id, class_name=class_name, style=style)

    def navbar(
        self,
        brand: Annotated[str, Doc("Brand text.")] = "",
        links: Annotated[list[tuple[str, str]], Doc("List of (label, url) pairs.")] = [],
        id: Annotated[str, Doc("HTML ``id`` attribute.")] = "",
        class_name: Annotated[str, Doc("CSS class name.")] = "",
        style: Annotated[str, Doc("Inline CSS style.")] = "",
    ) -> Navbar:
        """Create a :class:`Navbar` component."""
        return Navbar(brand=brand, links=links, id=id, class_name=class_name, style=style)

    def form(
        self,
        components: Annotated[list[Component], Doc("Form fields and other child components.")] = [],
        on_submit: Annotated[
            str | FormActionHandler | None,
            Doc("URL or callable receiving submitted field values as a dict."),
        ] = None,
        id: Annotated[str, Doc("HTML ``id`` attribute.")] = "",
        class_name: Annotated[str, Doc("CSS class name.")] = "",
        style: Annotated[str, Doc("Inline CSS style.")] = "",
    ) -> Form:
        """Create a :class:`Form` component."""
        return Form(components=components, on_submit=on_submit, id=id, class_name=class_name, style=style)


ui = _UI()
"""Module-level convenience builder for creating components.

Example:
    >>> from fastui import ui
    >>> ui.heading("Hello")
    Heading(text='Hello', level=1, ...)
"""
