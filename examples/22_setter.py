"""Setter — @app.setter(primary_page=True) редиректит 404 на эту страницу."""

from fastui import App, ui

app = App()


@app.page("/")
@app.setter(primary_page=True)
def home():
    return [
        ui.heading("Home", level=1),
        ui.text("Это главная страница — цель для редиректа с 404."),
        ui.text("Попробуй перейти на /xyz — попадёшь сюда."),
        ui.divider(),
        ui.link("→ /xyz (несуществующий URL)", url="/xyz"),
    ]


@app.page("/hello", title="Hello")
def hello():
    return [
        ui.heading("Hello", level=1),
        ui.text("А сюда редиректа нет — setter только на home()."),
    ]


if __name__ == "__main__":
    app.run(hot_reload=True)
