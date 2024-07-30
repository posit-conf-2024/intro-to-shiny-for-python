# from shiny import Inputs, Outputs, Session, App, reactive, render, req, ui
from shiny.express import ui, render, input

with ui.layout_columns(col_widths=(6, 6)):
    with ui.card():
        ui.card_header("Slider card")
        ui.input_slider("n", "N", 0, 100, 20)
        @render.text
        def txt():
            return f"2 * n is: {input.n() * 2}"
    


