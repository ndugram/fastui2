"""Swagger UI and 404 page HTML templates."""

from __future__ import annotations

NOT_FOUND_HTML = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>404 — FastUI</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            min-height: 100vh; display: flex; align-items: center; justify-content: center;
            background: #f5f5f5; color: #1a1a1a;
        }
        .card { text-align: center; padding: 3rem; background: #fff; border-radius: 16px; box-shadow: 0 2px 8px rgba(0,0,0,0.08); }
        h1 { font-size: 5rem; color: #4f46e5; margin-bottom: 0.5rem; }
        p { color: #666; margin-bottom: 1.5rem; }
        a { color: #4f46e5; text-decoration: none; font-weight: 500; }
        a:hover { text-decoration: underline; }
        .links { display: flex; gap: 1rem; justify-content: center; }
        .btn {
            display: inline-block; padding: 0.5rem 1rem; border-radius: 8px;
            font-weight: 500; transition: all 0.2s;
        }
        .btn-primary { background: #4f46e5; color: #fff; }
        .btn-primary:hover { background: #4338ca; text-decoration: none; }
        .btn-outline { border: 2px solid #4f46e5; color: #4f46e5; }
        .btn-outline:hover { background: #f5f3ff; text-decoration: none; }
    </style>
</head>
<body>
    <div class="card">
        <h1>404</h1>
        <p>Page not found</p>
        <div class="links">
            <a href="__FASTUI_DOCS_URL__" class="btn btn-primary">API Docs</a>
            <a href="__FASTUI_OPENAPI_URL__" class="btn btn-outline">OpenAPI JSON</a>
        </div>
    </div>
</body>
</html>"""

DOCS_HTML = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>FastUI API Docs</title>
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/swagger-ui-dist@5/swagger-ui.css">
    <style>
        .topbar { display: none; }
        .swagger-ui .info { margin: 20px 0; }
        .swagger-ui .scheme-container { margin: 0; padding: 10px 0; }
    </style>
</head>
<body>
    <div id="swagger-ui"></div>
    <script src="https://cdn.jsdelivr.net/npm/swagger-ui-dist@5/swagger-ui-bundle.js"></script>
    <script>
        fetch('__FASTUI_OPENAPI_URL__')
            .then(function(r) { return r.json(); })
            .then(function(spec) {
                SwaggerUIBundle({
                    spec: spec,
                    dom_id: '#swagger-ui',
                    deepLinking: true,
                    presets: [SwaggerUIBundle.presets.apis],
                    layout: 'BaseLayout',
                });
            });
    </script>
</body>
</html>"""


def get_docs_html(*, openapi_url: str = "/openapi.json") -> str:
    """Return the Swagger UI HTML page.

    Args:
        openapi_url: URL of the OpenAPI JSON schema.

    Returns:
        HTML string with embedded Swagger UI.
    """
    return DOCS_HTML.replace("__FASTUI_OPENAPI_URL__", openapi_url)


def get_not_found_html(
    *, docs_url: str = "/docs", openapi_url: str = "/openapi.json"
) -> str:
    """Return a styled 404 HTML page.

    Args:
        docs_url: URL of the documentation page.
        openapi_url: URL of the OpenAPI JSON endpoint.

    Returns:
        HTML string for the 404 page.
    """
    return (
        NOT_FOUND_HTML.replace("__FASTUI_DOCS_URL__", docs_url).replace(
            "__FASTUI_OPENAPI_URL__", openapi_url
        )
    )
