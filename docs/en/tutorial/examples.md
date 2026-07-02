# Examples

Complete, runnable examples are available in the [examples directory](https://github.com/ndugram/fastui2/tree/master/examples).

## Example Index

| # | File | What it demonstrates |
|---|---|---|
| 1 | [hello_world.py](https://github.com/ndugram/fastui2/tree/master/examples/01_hello_world.py) | Minimal app — one page, one heading |
| 2 | [all_components.py](https://github.com/ndugram/fastui2/tree/master/examples/02_all_components.py) | Every built-in component type |
| 3 | [route_params.py](https://github.com/ndugram/fastui2/tree/master/examples/03_route_params.py) | URL patterns with typed parameters |
| 4 | [server_actions.py](https://github.com/ndugram/fastui2/tree/master/examples/04_server_actions.py) | POST callback handlers |
| 5 | [custom_css.py](https://github.com/ndugram/fastui2/tree/master/examples/05_custom_css.py) | Dark theme with custom CSS |
| 6 | [forms.py](https://github.com/ndugram/fastui2/tree/master/examples/06_forms.py) | Input fields and form layout |
| 7 | [navigation.py](https://github.com/ndugram/fastui2/tree/master/examples/07_navigation.py) | Multi-page navigation with links |
| 8 | [docs_config.py](https://github.com/ndugram/fastui2/tree/master/examples/08_docs_config.py) | Custom OpenAPI docs metadata |
| 9 | [layout_page.py](https://github.com/ndugram/fastui2/tree/master/examples/09_layout_page.py) | Page component for grouping |
| 10 | [counter.py](https://github.com/ndugram/fastui2/tree/master/examples/10_counter.py) | Interactive counter with actions |
| 11 | [todo.py](https://github.com/ndugram/fastui2/tree/master/examples/11_todo.py) | Simple todo application |
| 12 | [hot_reload.py](https://github.com/ndugram/fastui2/tree/master/examples/12_hot_reload.py) | Hot reload demo |
| 13 | [multi_page.py](https://github.com/ndugram/fastui2/tree/master/examples/13_multi_page.py) | Shared navigation layout |
| 14 | [no_docs.py](https://github.com/ndugram/fastui2/tree/master/examples/14_no_docs.py) | Running without docs |
| 15 | [external_stylesheets.py](https://github.com/ndugram/fastui2/tree/master/examples/15_external_stylesheets.py) | Bootstrap integration |
| 16 | [single_component.py](https://github.com/ndugram/fastui2/tree/master/examples/16_single_component.py) | Returning single vs list |
| 17 | [advanced_routing.py](https://github.com/ndugram/fastui2/tree/master/examples/17_advanced_routing.py) | Complex multi-param routes |
| 18 | [inline_styles.py](https://github.com/ndugram/fastui2/tree/master/examples/18_inline_styles.py) | All style combinations |
| 19 | [minimal.py](https://github.com/ndugram/fastui2/tree/master/examples/19_minimal.py) | Absolute minimal app (7 lines) |
| 20 | [dynamic_routes.py](https://github.com/ndugram/fastui2/tree/master/examples/20_dynamic_routes.py) | Dynamically generated routes |

## Running Examples

```bash
# Clone the repository
git clone https://github.com/ndugram/fastui2.git
cd fastui

# Run any example
python examples/01_hello_world.py
python examples/04_server_actions.py
python examples/10_counter.py
```

## Creating Your Own

Start from the minimal example:

```python
from fastui import App, ui

app = App()

@app.page("/")
def index():
    return [ui.heading("My App", level=1)]

if __name__ == "__main__":
    app.run()
```

Then add more pages, components, and actions as needed.
