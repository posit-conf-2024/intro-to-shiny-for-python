from shiny.express import ui, render, input
from shiny import reactive

ui.input_text("input_txt", "Enter text")
ui.input_action_button("send", "Enter")
@render.text
@reactive.event(input.send)
def output_txt():
    return input.input_txt()


