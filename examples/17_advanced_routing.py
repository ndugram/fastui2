"""Complex URL patterns with multiple typed params."""

from fastui import App, ui

app = App()


@app.page("/")
def index():
    return [
        ui.heading("Advanced Routing", level=1),
        ui.text("URL patterns with multiple parameters:"),
        ui.link("/product/laptop/999", url="/product/laptop/999"),
        ui.link("/category/books/page/3", url="/category/books/page/3"),
        ui.link("/file/docs/report.pdf", url="/file/docs/report.pdf"),
        ui.link("/search/python/advanced", url="/search/python/advanced"),
    ]


@app.page("/product/{name}/{price:int}")
def product(name: str, price: int):
    return [
        ui.heading(f"Product: {name}", level=1),
        ui.text(f"Price: ${price}"),
        ui.link("Back", url="/"),
    ]


@app.page("/category/{cat}/page/{num:int}")
def category_page(cat: str, num: int):
    return [
        ui.heading(f"Category: {cat}", level=1),
        ui.text(f"Page {num}"),
        ui.link("Back", url="/"),
    ]


@app.page("/file/{folder}/{filename}")
def file_view(folder: str, filename: str):
    return [
        ui.heading(f"File: {filename}", level=1),
        ui.text(f"Location: {folder}/"),
        ui.link("Back", url="/"),
    ]


@app.page("/search/{query}/{scope}")
def search(query: str, scope: str):
    return [
        ui.heading(f"Search: {query}", level=1),
        ui.text(f"Scope: {scope}"),
        ui.link("Back", url="/"),
    ]

if __name__ == "__main__":
    app.run()
