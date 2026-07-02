"""Customize OpenAPI documentation metadata and tags."""

from fastui import App, ui

app = App(
    title="My Custom API",
    version="2.0.0",
    description="A **custom** API description with *Markdown* support.",
    docs_url="/api-docs",
    openapi_url="/api-schema.json",
)


@app.page("/", title="Home", tags=["pages"])
def home():
    """Home page of the application."""
    return [
        ui.heading("Custom Docs", level=1),
        ui.text("The OpenAPI docs are available at /api-docs"),
        ui.text("The JSON schema is at /api-schema.json"),
        ui.divider(),
        ui.link("OpenAPI Docs", url="/api-docs"),
    ]


@app.page("/users", title="Users", tags=["users"])
def users():
    """List all users."""
    return [
        ui.heading("Users", level=1),
        ui.text("User list page."),
        ui.link("Back", url="/"),
    ]


@app.page("/items", title="Items", tags=["items"])
def items():
    """Browse available items."""
    return [
        ui.heading("Items", level=1),
        ui.text("Item list page."),
        ui.link("Back", url="/"),
    ]


if __name__ == "__main__":
    app.run()
