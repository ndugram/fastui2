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
input {
    width: 100%; padding: 0.5rem; border: 1px solid #ccc;
    border-radius: 6px; font-size: 1rem; margin-top: 0.25rem;
}
input:focus { outline: none; border-color: #4f46e5; }
label { font-size: 0.875rem; color: #555; font-weight: 500; }
p { margin: 0.5rem 0; }
hr { border: none; border-top: 1px solid #e5e7eb; margin: 1.5rem 0; }
a { color: #4f46e5; text-decoration: none; }
a:hover { text-decoration: underline; }
pre { background: #f0f0f0; padding: 1rem; border-radius: 6px; overflow-x: auto; }"""
)

ActionHandler: TypeAlias = Callable[[], list["Component"]]
"""Signature for click handlers: a zero-argument callable that returns a list of components."""


@runtime_checkable
class Component(Protocol):
    """
    Protocol that every UI component must satisfy.

    Any object with a ``to_html()`` method returning a ``str`` is structurally
    compatible with ``Component``. This allows Pydantic models, plain objects,
    and third-party wrappers to be used interchangeably in component trees.
    """

    def to_html(self) -> str:
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
    it with a generated action URL before rendering.
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


ui = _UI()
"""Module-level convenience builder for creating components.

Example:
    >>> from fastui import ui
    >>> ui.heading("Hello")
    Heading(text='Hello', level=1, ...)
"""
