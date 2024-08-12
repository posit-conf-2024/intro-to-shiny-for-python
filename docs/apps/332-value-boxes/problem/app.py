import faicons as fa
from shiny.express import input, render, ui

ui.input_slider("number", "Select an amount", 0, 100, 20)

with ui.value_box(
    showcase=fa.icon_svg("piggy-bank", width="50px"),
    theme="green"
):
    "Save"
    @render.text 
    def save(): 
        return f"${input.number()}"