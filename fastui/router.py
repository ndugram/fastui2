from __future__ import annotations

import re
from dataclasses import dataclass, field
from typing import Annotated, Callable

from annotated_doc import Doc


@dataclass
class Route:
    """
    A registered route that maps a URL pattern to a handler function.

    The route stores the compiled regex, parameter metadata, and an
    optional page title used in the HTML ``<title>`` tag.

    Attributes:
        pattern: The original URL pattern string (e.g. ``/user/{id:int}``).
        handler: The callable invoked when this route is matched.
        param_names: Names of extracted path parameters.
        param_converters: Type converters for extracted parameters.
        regex: Compiled regular expression for path matching.
        title: Optional page title for the HTML template.
    """

    pattern: Annotated[str, Doc("URL pattern string (e.g. ``/user/{id:int}``).")]
    handler: Annotated[Callable, Doc("Handler callable invoked for this route.")]
    param_names: Annotated[
        list[str], Doc("Names of path parameters extracted from the URL.")
    ]
    param_converters: Annotated[
        list[Callable], Doc("Type converters (``int``, ``str``) for each parameter.")
    ]
    regex: Annotated[
        re.Pattern, Doc("Compiled regular expression for URL matching.")
    ]
    title: Annotated[str, Doc("Optional page title for the HTML template.")] = ""
    tags: Annotated[list[str], Doc("OpenAPI tags for grouping routes.")] = field(default_factory=list)
    summary: Annotated[str, Doc("Short description for OpenAPI operation summary.")] = ""
    description: Annotated[str, Doc("Full description for OpenAPI operation.")] = ""


class Router:
    """
    Pattern-based URL router with typed parameter extraction.

    Supports:
    - Static paths: ``/about``
    - Integer parameters: ``/user/{id:int}``
    - String parameters: ``/user/{slug}``
    - Mixed segments: ``/post/{year:int}/{slug}``

    Example:
        ```python
        router = Router()

        router.add("/", home_handler)
        router.add("/user/{id:int}", user_handler)

        route = router.match("/user/42")
        if route:
            handler(**route._match_kwargs)  # {'id': 42}
        ```
    """

    def __init__(self) -> None:
        """Initialize an empty router."""
        self.routes: Annotated[list[Route], Doc("List of registered routes.")] = []

    def add(
        self,
        pattern: Annotated[str, Doc("URL pattern (e.g. ``/user/{id:int}``).")],
        handler: Annotated[Callable, Doc("Handler callable.")],
        title: Annotated[str, Doc("Optional page title.")] = "",
        tags: Annotated[
            list[str], Doc("OpenAPI tags for grouping routes in docs.")
        ] | None = None,
        summary: Annotated[
            str, Doc("Short description for OpenAPI operation summary.")
        ] = "",
        description: Annotated[
            str, Doc("Full description for OpenAPI operation.")
        ] = "",
    ) -> None:
        """Register a new route.

        Parses the pattern, extracts parameter definitions, compiles the
        matching regex, and appends a :class:`Route` to the route list.

        Args:
            pattern: URL pattern supporting ``{name}`` and ``{name:type}``
                syntax. Supported types are ``int`` and ``str`` (default).
            handler: Callable invoked when the route is matched.
            title: Optional title passed to the HTML template.
            tags: OpenAPI tags for grouping routes in the documentation.
            summary: Short description for the OpenAPI operation summary.
            description: Full description for the OpenAPI operation.

        Raises:
            ValueError: If a parameter definition is malformed (empty name).
        """
        param_names: list[str] = []
        param_converters: list[Callable] = []
        regex_parts: list[str] = []

        for segment in pattern.strip("/").split("/"):
            if segment.startswith("{") and segment.endswith("}"):
                inner = segment[1:-1]
                name, _, typ = inner.partition(":")
                if not name:
                    msg = f"Invalid parameter definition in pattern {pattern!r}"
                    raise ValueError(msg)
                param_names.append(name)
                if typ == "int":
                    param_converters.append(int)
                    regex_parts.append(r"(\d+)")
                else:
                    param_converters.append(str)
                    regex_parts.append(r"([^/]+)")
            elif segment:
                regex_parts.append(re.escape(segment))

        regex_str = "^/" + "/".join(regex_parts) + "/?$"
        self.routes.append(
            Route(
                pattern=pattern,
                handler=handler,
                param_names=param_names,
                param_converters=param_converters,
                regex=re.compile(regex_str),
                title=title,
                tags=tags or [],
                summary=summary,
                description=description,
            )
        )

    def match(
        self,
        path: Annotated[str, Doc("Request path to match (e.g. ``/user/42``).")],
    ) -> Route | None:
        """Match a path against the registered routes.

        Iterates through the route list in registration order. On the first
        match, stores extracted keyword arguments in ``route._match_kwargs``
        and returns the route. Returns ``None`` when no pattern matches.

        Args:
            path: The request path (leading and trailing slashes are
                normalised before matching).

        Returns:
            The matching :class:`Route` with ``_match_kwargs`` populated,
            or ``None`` if no route matches the path.

        Example:
            >>> route = router.match("/user/42")
            >>> route.pattern
            '/user/{id:int}'
            >>> route._match_kwargs
            {'id': 42}
        """
        for route in self.routes:
            match = route.regex.match(path)
            if match:
                route._match_kwargs = { # type: ignore
                    name: route.param_converters[i](match.group(i + 1))
                    for i, name in enumerate(route.param_names)
                }
                return route
        return None
