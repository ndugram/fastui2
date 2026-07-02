# About FastUI

FastUI is a Python library for building server-rendered web interfaces using decorators and Pydantic-validated components. It is designed for developers who want to create functional web UIs without writing HTML, CSS, or JavaScript.

## Philosophy

- **Python-only** — everything from page definition to component rendering is pure Python.
- **Minimal dependencies** — only Pydantic and annotated-doc are required.
- **No build step** — no webpack, no npm, no bundler. Just `pip install` and `python main.py`.
- **Transparent** — components compile directly to HTML. What you see is what you get.
- **Progressive** — start with a single page, add more as needed. No boilerplate.

## When to Use FastUI

FastUI is a good fit for:

- **Internal tools** — admin panels, dashboards, monitoring pages
- **Prototypes** — ship a working UI in minutes
- **Small to medium apps** — a few dozen pages with server-side logic
- **Educational projects** — teach web concepts without JS complexity
- **Server-driven UIs** — where the backend controls rendering entirely

## When Not to Use FastUI

FastUI is not a good fit for:

- Rich single-page applications with client-side state
- Complex reactive UIs with real-time updates
- Applications requiring WebSocket or SSE (coming eventually)
- Large-scale consumer-facing web apps

## Status

FastUI is in early development (v0.1.0). The API is subject to change. It is suitable for
internal tools and prototypes but not yet for production customer-facing applications.

## Roadmap

- [ ] Production ASGI/WSGI support
- [ ] Form submission handling
- [ ] More components (tables, images, modals)
- [ ] Async handler support
- [ ] WebSocket support
- [ ] CLI for scaffolding projects

## License

FastUI is released under the MIT License.
