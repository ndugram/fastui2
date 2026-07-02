"""All components with various inline style combinations."""

from fastui import App, ui

app = App()

@app.page("/", title="Inline Styles")
def index():
    return [
        ui.heading("Inline Style Examples", level=1),
        ui.divider(),

        ui.heading("Colored heading", level=2, style="color: #e94560;"),
        ui.text("Styled text", style="font-size: 1.2rem; font-weight: bold;"),
        ui.divider(),

        ui.heading("Borders & Backgrounds", level=3),
        ui.text("Box with border", style="border: 2px solid #4f46e5; padding: 1rem; border-radius: 8px;"),
        ui.text("Box with background", style="background: #f0f0ff; padding: 1rem; border-radius: 8px;"),
        ui.divider(),

        ui.heading("Buttons", level=3),
        ui.button("Small button", style="font-size: 0.75rem; padding: 0.25rem 0.5rem;"),
        ui.button("Large button", style="font-size: 1.5rem; padding: 1rem 2rem;"),
        ui.button("Rounded button", style="border-radius: 999px; padding: 0.5rem 1.5rem;"),
        ui.divider(),

        ui.heading("Responsive text", level=3),
        ui.text("Centered text", style="text-align: center;"),
        ui.text("Right-aligned", style="text-align: right; color: #666;"),
        ui.divider(),

        ui.heading("Links", level=3),
        ui.link("Big link", url="/", style="font-size: 1.5rem; display: block;"),
        ui.link("Subtle link", url="/", style="color: #999; text-decoration: none;"),
    ]

if __name__ == "__main__":
    app.run()
