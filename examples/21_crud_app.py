"""CRUD application — create, read, update, delete items via URL routes and server actions."""

from fastui import App, ui
from fastui.components import Component

app = App()

ITEMS: list[dict] = [
    {"id": 1, "name": "Laptop", "price": 999.99, "qty": 5},
    {"id": 2, "name": "Mouse", "price": 25.50, "qty": 42},
    {"id": 3, "name": "Keyboard", "price": 89.00, "qty": 18},
]
_next_id = 4


def _list_table() -> list[Component]:
    rows: list[Component] = [ui.heading(f"Inventory ({len(ITEMS)} items)", level=2)]
    if not ITEMS:
        rows.append(ui.text("No items yet."))
    else:
        for item in ITEMS:
            rows.append(
                ui.page([
                    ui.page([
                        ui.heading(item["name"], level=3, style="margin: 0;"),
                        ui.text(f"${item['price']:.2f} — Stock: {item['qty']}"),
                    ], style="flex: 1;"),
                    ui.page([
                        ui.button("View", on_click=f"/item/{item['id']}"),
                        ui.button("Edit", on_click=f"/item/{item['id']}/edit"),
                    ], style="display: flex; gap: 0.5rem;"),
                ], style="display: flex; align-items: center; padding: 0.75rem; "
                         "background: #fff; border: 1px solid #e5e7eb; border-radius: 8px; margin-bottom: 0.5rem;")
            )
    return rows


@app.page("/")
def index() -> list[Component]:
    return [
        ui.heading("FastUI Demo", level=1),
        ui.link("CRUD Inventory", url="/items", style="display: block; font-size: 1.2rem; margin: 0.5rem 0;"),
        ui.link("Todo App", url="/todo", style="display: block; font-size: 1.2rem; margin: 0.5rem 0;"),
    ]


@app.page("/items", title="Inventory")
def item_list() -> list[Component]:
    return [
        ui.heading("CRUD Inventory", level=1),
        ui.button("+ New Item", on_click="/items/new"),
        ui.divider(),
        *_list_table(),
        ui.divider(),
        ui.link("Home", url="/"),
    ]


@app.page("/items/new", title="New Item")
def item_new() -> list[Component]:
    return [
        ui.heading("New Item", level=1),
        ui.text("Select a price tier to create:"),
        ui.button("Budget ($10)", on_click=_create(10.00, 1)),
        ui.button("Standard ($50)", on_click=_create(50.00, 10)),
        ui.button("Premium ($200)", on_click=_create(200.00, 5)),
        ui.divider(),
        ui.link("← Back", url="/items"),
    ]


def _create(price: float, qty: int):
    def _inner() -> list[Component]:
        global _next_id
        name = f"Item #{_next_id}"
        ITEMS.append({"id": _next_id, "name": name, "price": price, "qty": qty})
        _next_id += 1
        return [
            ui.heading("Created!", level=2, style="color: green;"),
            ui.text(f"Added '{name}' — ${price:.2f} (qty: {qty})."),
            ui.link("← Back to Inventory", url="/items"),
        ]
    return _inner


@app.page("/item/{id:int}", title="Item Details")
def item_detail(id: int) -> list[Component]:
    item = next((i for i in ITEMS if i["id"] == id), None)
    if not item:
        return [ui.heading("Not Found", level=1), ui.link("← Back", url="/items")]

    return [
        ui.heading(item["name"], level=1),
        ui.text(f"Price: ${item['price']:.2f}"),
        ui.text(f"Stock: {item['qty']} units"),
        ui.divider(),
        ui.button("Edit", on_click=f"/item/{id}/edit"),
        ui.button("Delete", on_click=_delete(id), style="background: #dc3545;"),
        ui.divider(),
        ui.link("← Back to Inventory", url="/items"),
    ]


def _delete(item_id: int):
    def _inner() -> list[Component]:
        global ITEMS
        ITEMS = [i for i in ITEMS if i["id"] != item_id]
        return [
            ui.heading("Deleted", level=2, style="color: #dc3545;"),
            ui.text(f"Item #{item_id} has been removed."),
            ui.link("← Back to Inventory", url="/items"),
        ]
    return _inner


@app.page("/item/{id:int}/edit", title="Edit Item")
def item_edit(id: int) -> list[Component]:
    item = next((i for i in ITEMS if i["id"] == id), None)
    if not item:
        return [ui.heading("Not Found", level=1), ui.link("← Back", url="/items")]

    return [
        ui.heading(f"Edit: {item['name']}", level=1),
        ui.text(f"Current price: ${item['price']:.2f}, Stock: {item['qty']}"),
        ui.divider(),
        ui.heading("Set Price", level=3),
        ui.button("Set $10", on_click=_update(id, "price", 10.00)),
        ui.button("Set $50", on_click=_update(id, "price", 50.00)),
        ui.button("Set $100", on_click=_update(id, "price", 100.00)),
        ui.divider(),
        ui.heading("Set Quantity", level=3),
        ui.button("Set 0", on_click=_update(id, "qty", 0), style="background: #dc3545;"),
        ui.button("Set 5", on_click=_update(id, "qty", 5)),
        ui.button("Set 25", on_click=_update(id, "qty", 25)),
        ui.button("Set 100", on_click=_update(id, "qty", 100)),
        ui.divider(),
        ui.heading("Rename", level=3),
        ui.button(f"Rename to '{item['name']} v2'", on_click=_rename(id, f"{item['name']} v2")),
        ui.divider(),
        ui.link("← Cancel", url=f"/item/{id}"),
    ]


def _update(item_id: int, field: str, value):
    def _inner() -> list[Component]:
        item = next((i for i in ITEMS if i["id"] == item_id), None)
        if item:
            item[field] = value
        return [
            ui.heading("Updated!", level=2, style="color: green;"),
            ui.text(f"{field} changed to {value}."),
            ui.link(f"← Back to {item['name'] if item else 'item'}", url=f"/item/{item_id}"),
        ]
    return _inner


def _rename(item_id: int, new_name: str):
    def _inner() -> list[Component]:
        item = next((i for i in ITEMS if i["id"] == item_id), None)
        if item:
            old = item["name"]
            item["name"] = new_name
            return [
                ui.heading("Renamed!", level=2, style="color: green;"),
                ui.text(f"'{old}' → '{new_name}'"),
                ui.link(f"← Back to {new_name}", url=f"/item/{item_id}"),
            ]
        return [ui.heading("Error", level=1)]
    return _inner


@app.page("/todo", title="Todo")
def todo() -> list[Component]:
    return [
        ui.heading("Todo", level=1),
        ui.text("See examples/11_todo.py for the full todo implementation."),
        ui.link("Back", url="/"),
    ]


if __name__ == "__main__":
    app.run(hot_reload=True)
