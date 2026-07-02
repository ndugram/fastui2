"""OpenAPI schema generator for FastUI applications."""

from __future__ import annotations

import inspect
import re
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from fastui.router import Route


def _param_from_pattern(pattern: str) -> list[dict[str, Any]]:
    """Extract OpenAPI parameter definitions from a URL pattern.

    Parses ``/user/{id:int}`` into a path parameter with type ``integer``.

    Args:
        pattern: URL pattern string.

    Returns:
        List of OpenAPI parameter objects.
    """
    params: list[dict[str, Any]] = []
    for segment in pattern.strip("/").split("/"):
        if segment.startswith("{") and segment.endswith("}"):
            inner = segment[1:-1]
            name, _, typ = inner.partition(":")
            param: dict[str, Any] = {
                "name": name,
                "in": "path",
                "required": True,
            }
            if typ == "int":
                param["schema"] = {"type": "integer"}
            else:
                param["schema"] = {"type": "string"}
            params.append(param)
    return params


def _extract_summary(handler: Any) -> str:
    """Extract a short summary from a handler docstring.

    Args:
        handler: The handler callable.

    Returns:
        The first line of the docstring or the handler name.
    """
    if handler and hasattr(handler, "__doc__") and handler.__doc__:
        doc = inspect.getdoc(handler)
        if doc:
            first = doc.strip().split("\n")[0]
            return first
    return getattr(handler, "__name__", "Unknown")


def _extract_description(handler: Any) -> str:
    """Extract full description from a handler docstring.

    Args:
        handler: The handler callable.

    Returns:
        The full docstring (everything after the first line).
    """
    if handler and hasattr(handler, "__doc__") and handler.__doc__:
        doc = inspect.getdoc(handler)
        if doc:
            lines = doc.strip().split("\n")
            if len(lines) > 1:
                return "\n".join(lines[1:]).strip()
    return ""


def generate_openapi_schema(
    routes: list[Route],
    *,
    title: str = "FastUI API",
    version: str = "0.1.0",
    description: str = "",
    docs_url: str = "/docs",
    openapi_url: str = "/openapi.json",
) -> dict[str, Any]:
    """Generate an OpenAPI 3.0 schema from FastUI routes.

    Each registered page route becomes a ``GET`` path in the schema.
    URL path parameters (``{id:int}``, ``{slug}``) are documented as
    path parameters. Action handlers are documented as ``POST`` endpoints.

    Args:
        routes: List of registered :class:`Route` objects.
        title: API title for the OpenAPI info section.
        version: API version string.
        description: API description (supports Markdown).
        docs_url: URL of the Swagger UI page.
        openapi_url: URL of the OpenAPI JSON endpoint.

    Returns:
        An OpenAPI 3.0 schema dictionary.
    """
    paths: dict[str, Any] = {}

    for route in routes:
        if not hasattr(route.handler, "__name__"):
            continue

        summary = route.summary or _extract_summary(route.handler)
        description = route.description or _extract_description(route.handler)
        handler_name = route.handler.__name__

        path_key = re.sub(r"\{(\w+):\w+\}", r"{\1}", route.pattern)
        if not path_key.startswith("/"):
            path_key = f"/{path_key}"
        method = "get"

        operation: dict[str, Any] = {
            "summary": summary or route.pattern,
            "operationId": f"get_{handler_name}",
            "parameters": _param_from_pattern(route.pattern),
            "responses": {
                "200": {
                    "description": "HTML page",
                    "content": {
                        "text/html": {
                            "schema": {"type": "string", "description": "Rendered HTML"}
                        }
                    },
                },
                "404": {"description": "Page not found"},
            },
        }

        if description:
            operation["description"] = description

        if route.title:
            operation["x-page-title"] = route.title

        if route.tags:
            operation["tags"] = route.tags

        paths[path_key] = {method: operation}

    all_tags = sorted(
        {tag for route in routes if hasattr(route, "tags") for tag in route.tags}
    )

    schema: dict[str, Any] = {
        "openapi": "3.0.3",
        "info": {
            "title": title,
            "version": version,
            "description": description,
        },
        "paths": paths,
    }

    if all_tags:
        schema["tags"] = [{"name": t} for t in all_tags]

    return schema
