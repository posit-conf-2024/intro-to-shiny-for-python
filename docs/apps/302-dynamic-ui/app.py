from shiny.express import render, ui, input

with ui.card():
    ui.input_checkbox("show_checkbox", "Show Checkbox")
    with ui.panel_conditional( "input.show_checkbox"):
        ui.input_checkbox("show_slider", "Show Slider"),
    @render.ui
    def dynamic_slider():
        if input.show_slider():
            return ui.input_slider("n", "N", 0, 100, 20)




