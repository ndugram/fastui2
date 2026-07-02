"""Dynamically generated route list via server action."""

from fastui import App, ui

app = App()
routes_db: list[dict] = [
    {"name": "Getting Started", "slug": "getting-started"},
    {"name": "Installation", "slug": "installation"},
    {"name": "Configuration", "slug": "configuration"},
]


def add_route() -> list:
    import time
    slug = f"route-{int(time.time())}"
    routes_db.append({"name": f"Route {len(routes_db) + 1}", "slug": slug})
    return _route_list()


def _route_list():
    items = [
        ui.heading("Dynamic Routes", level=1),
        ui.button("+ Add Route", on_click=add_route),
        ui.divider(),
    ]
    for r in routes_db:
        items.append(ui.link(r["name"], url=f"/doc/{r['slug']}", style="display: block;"))
    items.append(ui.divider())
    items.append(ui.link("Home", url="/"))
    return items


@app.page("/doc/{slug}")
def doc_page(slug: str):
    match = [r for r in routes_db if r["slug"] == slug]
    name = match[0]["name"] if match else slug
    return [
        ui.heading(name, level=1),
        ui.text(f"Documentation page for: {slug}"),
        ui.link("← Back", url="/dynamic"),
    ]


@app.page("/dynamic", title="Dynamic Routes")
def dynamic():
    return _route_list()


@app.page("/")
def index():
    return [
        ui.heading("Examples", level=1),
        ui.link("Dynamic Routes Demo", url="/dynamic"),
    ]

if __name__ == "__main__":
    app.run()
