from shiny.express import ui

ui.input_slider(
    id="n", 
    label="Choose n", 
    min=0, 
    max=100, 
    value=20
)