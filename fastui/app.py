from __future__ import annotations

import http.server
import json
import os
import threading
import time
import webbrowser
from typing import Annotated, Callable
import re as _re
import unicodedata as _uc


from annotated_doc import Doc

from .components import (
    DEFAULT_CSS,
    ActionHandler,
    Button,
    Component,
    Page,
)
from .openapi import generate_openapi_schema, get_docs_html
from .router import Route, Router

RELOAD_SCRIPT: str = (
    '<script>'
    '(function(){'
    'var v=0;'
    'setInterval(function(){'
    'var x=new XMLHttpRequest();'
    "x.open('GET','/_ui/version',true);"
    'x.onload=function(){'
    'var n=parseInt(x.responseText,10);'
    'if(v&&n!==v)location.reload();'
    'v=n;};'
    'x.send();'
    '},1000);'
    '})();'
    '</script>'
)

TEMPLATE: str = (
    '<!DOCTYPE html>\n'
    '<html lang="ru">\n'
    '<head>\n'
    '    <meta charset="utf-8">\n'
    '    <meta name="viewport" content="width=device-width, initial-scale=1">\n'
    '    <title>{title}</title>\n'
    '    {stylesheets}\n'
    '    <style>{css}</style>\n'
    '</head>\n'
    '<body>\n'
    '{body}\n'
    '{reload_script}\n'
    '</body>\n'
    '</html>'
)


class _Handler(http.server.BaseHTTPRequestHandler):
    """
    Internal HTTP request handler.

    Dispatches:
    - ``GET`` requests to page handlers or internal API endpoints.
    - ``POST`` requests to registered action handlers (``/_ui/action/<id>``).
    """

    app_instance: App | None = None

    def do_GET(self) -> None:
        """Handle incoming GET requests."""
        path = self.path.rstrip("/") or "/"
        app = self.app_instance
        assert app is not None

        if path == "/_ui/version":
            self.send_json({"version": app._build_id})
            return

        if path == "/_ui/routes":
            self.send_json(
                {"routes": [r.pattern for r in app._router.routes]}
            )
            return

        if app._docs_enabled:
            if path == app._openapi_url:
                schema = generate_openapi_schema(
                    app._router.routes,
                    title=app._docs_title,
                    version=app._docs_version,
                    description=app._docs_description,
                    docs_url=app._docs_url,
                    openapi_url=app._openapi_url,
                )
                self.send_json(schema)
                self._log(200)
                return
            if path == app._docs_url:
                html = get_docs_html(openapi_url=app._openapi_url)
                self.send_html(html, 200)
                self._log(200)
                return

        route = app._router.match(path)
        if route:
            html = app._render_page(route)
            self.send_html(html, 200)
            self._log(200)
        elif app._primary_redirect_target:
            self.send_redirect(app._primary_redirect_target)
            self._log(302)
        else:
            self.send_html("<h1>404</h1>", 404)
            self._log(404)

    def do_POST(self) -> None:
        """Handle incoming POST requests."""
        path = self.path.rstrip("/") or "/"
        app = self.app_instance
        assert app is not None

        if path.startswith("/_ui/action/"):
            action_id = path.split("/_ui/action/")[-1]
            handler = app._action_handlers.get(action_id)
            if handler:
                try:
                    components = handler()
                    html = app._render_fragment(components)
                    self.send_html(html, 200)
                    self._log(200)
                    return
                except Exception as exc:
                    self.send_html(
                        f"<h1>500</h1><p>{exc}</p>", 500
                    )
                    self._log(500)
                    return

        self.send_html("<h1>404</h1>", 404)
        self._log(404)

    def send_redirect(
        self,
        location: Annotated[str, Doc("Redirect target URL.")],
    ) -> None:
        self.send_response(302)
        self.send_header("Location", location)
        self.end_headers()

    def send_html(
        self,
        html: Annotated[str, Doc("HTML string to send.")],
        status: Annotated[int, Doc("HTTP status code.")],
    ) -> None:
        self.send_response(status)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.end_headers()
        self.wfile.write(html.encode("utf-8"))

    def send_json(
        self,
        data: Annotated[dict, Doc("JSON-serialisable dictionary.")],
    ) -> None:
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps(data).encode())

    def _log(
        self,
        status: Annotated[int, Doc("HTTP status code to log.")],
    ) -> None:
        colour = "\033[92m" if status == 200 else "\033[91m"
        reset = "\033[0m"
        bold = "\033[1m"
        blue = "\033[94m"
        url = f"http://{self.server.server_name}:{self.server.server_port}{self.path}"  # type: ignore[attr-defined]
        print(f"  {blue}{bold}{self.command}{reset} {url} {colour}{status}{reset}")

    def log_message(
        self, format: Annotated[str, Doc("Format string.")], *args: object
    ) -> None:
        pass


def _watch_files(
    paths: Annotated[list[str], Doc("List of file paths to watch.")],
    on_change: Annotated[
        Callable[[str], None], Doc("Callback invoked when a file changes.")
    ],
    interval: Annotated[
        float, Doc("Polling interval in seconds.")
    ] = 1.0,
) -> None:
    mtimes: dict[str, float] = {}
    for path in paths:
        try:
            mtimes[path] = os.stat(path).st_mtime
        except FileNotFoundError:
            pass

    while True:
        time.sleep(interval)
        for path in paths:
            try:
                mtime = os.stat(path).st_mtime
                if path in mtimes and mtime != mtimes[path]:
                    on_change(path)
                mtimes[path] = mtime
            except FileNotFoundError:
                pass


def _collect_py_files(
    root: Annotated[str, Doc("Root directory to scan.")],
) -> list[str]:
    files: list[str] = []
    for dirpath, _, filenames in os.walk(root):
        for filename in filenames:
            if filename.endswith(".py"):
                files.append(os.path.join(dirpath, filename))
    return files


class App:
    """
    FastUI application — the main entry point for defining routes and
    running the development server.
    """

    def __init__(
        self,
        css: Annotated[
            str,
            Doc("Custom CSS override. Falls back to built-in DEFAULT_CSS when empty.")
        ] = "",
        docs: Annotated[
            bool, Doc("Enable OpenAPI documentation at ``/docs``.")
        ] = True,
        docs_url: Annotated[
            str, Doc("URL path for the Swagger UI page.")
        ] = "/docs",
        openapi_url: Annotated[
            str, Doc("URL path for the OpenAPI JSON schema.")
        ] = "/openapi.json",
        title: Annotated[
            str, Doc("API title shown in Swagger UI.")
        ] = "FastUI API",
        version: Annotated[
            str, Doc("API version string.")
        ] = "0.1.0",
        description: Annotated[
            str, Doc("API description shown in Swagger UI.")
        ] = "",
    ) -> None:
        self._router: Router = Router()
        self.css: str = css or DEFAULT_CSS
        self.stylesheets: list[str] = []
        self._build_id: int = 0
        self._hot_reload: bool = False
        self._action_handlers: dict[str, ActionHandler] = {}
        self._action_counter: int = 0
        self._primary_redirect_target: str = ""
        self._docs_enabled: bool = docs
        self._docs_url: str = docs_url
        self._openapi_url: str = openapi_url
        self._docs_title: str = title
        self._docs_version: str = version
        self._docs_description: str = description

    def page(
        self,
        pattern: Annotated[
            str,
            Doc(
                "URL pattern. Supports static paths (``/about``) and "
                "typed parameters (``/user/{id:int}``)."
            ),
        ],
        title: Annotated[
            str,
            Doc(
                "Optional page title rendered inside the HTML ``<title>`` tag."
            ),
        ] = "",
        tags: Annotated[
            list[str] | None,
            Doc("OpenAPI tags for grouping routes in documentation."),
        ] = None,
        summary: Annotated[
            str,
            Doc("Short description for the OpenAPI operation summary. "
                "Overrides the docstring-based summary."),
        ] = "",
        description: Annotated[
            str,
            Doc("Full description for the OpenAPI operation. "
                "Overrides the docstring-based description."),
        ] = "",
    ) -> Callable:
        """Register a page handler via decorator."""
        def decorator(func: Callable) -> Callable:
            self._router.add(pattern, func, title=title, tags=tags,
                             summary=summary, description=description)
            if getattr(func, "_fastui_primary", False):
                if self._primary_redirect_target:
                    msg = (
                        f"primary_page already set on "
                        f"{self._primary_redirect_target!r}, cannot set "
                        f"on {pattern!r}"
                    )
                    raise ValueError(msg)
                self._primary_redirect_target = pattern
            return func
        return decorator

    def setter(
        self,
        primary_page: Annotated[
            bool,
            Doc(
                "If True, 404 errors redirect to this route's URL."
            ),
        ] = True,
    ) -> Callable:
        """Mark the decorated function's route as the 404 redirect target.

        Applied as a decorator **below** ``@app.page()``:

        ```python
        @app.page("/hello")
        @app.setter(primary_page=True)
        def handler(): ...
        ```

        When ``primary_page=True`` and a user visits a non-existent URL,
        they are redirected to this route's URL instead of seeing a 404.
        """
        def decorator(func: Callable) -> Callable:
            if primary_page:
                func._fastui_primary = True  # type: ignore
            return func
        return decorator

    def action(
        self,
        handler: Annotated[ActionHandler, Doc("Zero-argument callable.")],
    ) -> str:
        """Register a server-side action handler and return its URL."""
        self._action_counter += 1
        action_id = f"a{self._action_counter}"
        self._action_handlers[action_id] = handler
        return f"/_ui/action/{action_id}"

    def _walk_components(
        self,
        components: Annotated[list[Component], Doc("Component list to walk.")],
    ) -> None:
        """Walk a component tree and resolve callable action handlers."""
        for i, comp in enumerate(components):
            if isinstance(comp, Page):
                self._walk_components(comp.components)
            elif isinstance(comp, Button) and callable(comp.on_click):
                comp.on_click = self.action(comp.on_click)
                components[i] = comp

    def _render_fragment(
        self,
        components: Annotated[list[Component], Doc("Component list to render.")],
    ) -> str:
        self._walk_components(components)
        return "\n".join(c.to_html() for c in components)

    def _render_page(self, route: Route) -> str:
        kwargs = getattr(route, "_match_kwargs", {})
        components = route.handler(**kwargs)

        if components is None:
            body = ""
        elif isinstance(components, list):
            body = self._render_fragment(components)
        else:
            body = components.to_html()

        stylesheets = "\n".join(
            f'<link rel="stylesheet" href="{url}">' for url in self.stylesheets
        )

        title = (
            route.title
            or route.pattern.strip("/").replace("-", " ").title()
            or "FastUI"
        )
        reload_script = RELOAD_SCRIPT if self._hot_reload else ""
        return TEMPLATE.format(
            title=title,
            css=self.css,
            stylesheets=stylesheets,
            body=body,
            reload_script=reload_script,
        )

    def run(
        self,
        host: Annotated[str, Doc("Host address.")] = "127.0.0.1",
        port: Annotated[int, Doc("TCP port.")] = 8000,
        open_browser: Annotated[bool, Doc("Open browser on startup.")] = True,
        css: Annotated[str, Doc("Override CSS for this session.")] = "",
        hot_reload: Annotated[
            bool,
            Doc("Auto-refresh browser on file changes."),
        ] = False,
    ) -> None:
        """Start the development server."""
        if css:
            self.css = css
        self._hot_reload = hot_reload

        if hot_reload:
            _start_watcher(self)

        _Handler.app_instance = self
        server = http.server.HTTPServer((host, port), _Handler)

        reset = "\033[0m"
        bold = "\033[1m"
        dim = "\033[2m"
        green = "\033[92m"
        cyan = "\033[96m"
        yellow = "\033[93m"

        W = 44

        _ansi = _re.compile(r"\033\[[0-9;]*m")

        def vlen(s: str) -> int:
            plain = _ansi.sub("", s)
            n = 0
            for ch in plain:
                ea = _uc.east_asian_width(ch)
                n += 2 if ea in ("W", "F") else 1
            return n

        def inner(content: str = "") -> str:
            return f"  {bold}║{reset}{content}{' ' * (W - vlen(content))}{bold}║{reset}"

        def top() -> str:
            return f"  {bold}╔{'═' * W}╗{reset}"

        def mid() -> str:
            return f"  {bold}╠{'═' * W}╣{reset}"

        def bot() -> str:
            return f"  {bold}╚{'═' * W}╝{reset}"

        lines: list[str] = []
        lines.append(top())
        lines.append(inner(f"    {cyan}FastUI Dev Server{reset}"))
        lines.append(mid())
        lines.append(inner())
        lines.append(inner(f"  {green}→  http://{host}:{port}{reset}"))
        lines.append(inner())
        if hot_reload:
            lines.append(inner(f"  {cyan}♻  Hot reload{reset}"))
            lines.append(inner())
        if self._docs_enabled:
            lines.append(
                inner(f"  {cyan}📖  Docs{reset}  {green}http://{host}:{port}{self._docs_url}{reset}")
            )
            lines.append(inner())
        lines.append(inner("  Routes:"))
        for r in self._router.routes:
            lines.append(inner(f"   {dim}•{reset} {yellow}{r.pattern}{reset}"))
        lines.append(inner())
        lines.append(bot())

        print()
        print("\n".join(lines))
        print()

        if open_browser:
            threading.Timer(
                1.0, lambda: webbrowser.open(f"http://{host}:{port}/")
            ).start()

        try:
            print(f"  {dim}Ctrl+C to stop{reset}")
            print()
            server.serve_forever()
        except KeyboardInterrupt:
            print()
            print(f"  {yellow}Server stopped.{reset}")
            server.server_close()


def _start_watcher(app: App) -> None:
    cwd = os.getcwd()
    package_dir = os.path.dirname(os.path.abspath(__file__))
    paths = _collect_py_files(cwd) + _collect_py_files(package_dir)
    paths = list(set(paths))

    def on_change(path: str) -> None:
        name = os.path.relpath(path, cwd)
        print(f"  \033[93m♻  changed: {name}\033[0m")
        app._build_id += 1

    watcher_thread = threading.Thread(
        target=_watch_files, args=(paths, on_change), daemon=True
    )
    watcher_thread.start()
