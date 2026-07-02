"""URL patterns with typed path parameters."""

from fastui import App, ui

app = App()

@app.page("/")
def index():
    return [
        ui.heading("Route Parameters", level=1),
        ui.text("Try these URLs:"),
        ui.link("String param: /hello/fastui", url="/hello/fastui"),
        ui.link("Integer param: /item/42", url="/item/42"),
        ui.link("Two params: /post/2025/welcome", url="/post/2025/welcome"),
    ]

@app.page("/hello/{name}")
def greet(name: str):
    return [
        ui.heading(f"Hello, {name}!", level=1),
        ui.link("Back", url="/"),
    ]

@app.page("/item/{id:int}")
def item(id: int):
    return [
        ui.heading(f"Item #{id}", level=1),
        ui.text(f"You requested item with ID = {id}."),
        ui.link("Back", url="/"),
    ]

@app.page("/post/{year:int}/{slug}")
def blog_post(year: int, slug: str):
    return [
        ui.heading(f"Blog Post: {slug}", level=1),
        ui.text(f"Published in {year}."),
        ui.link("Back", url="/"),
    ]


if __name__ == "__main__":
    app.run()
