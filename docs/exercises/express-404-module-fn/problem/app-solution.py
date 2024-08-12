from shiny.express import ui, input, render, module
from shiny import reactive

@module
def card_mod(input, output, session):
    with ui.card():
        ui.card_header("What is your name?")
        ui.input_text("text", "Your name?")
        @render.text
        def _text_out():
            if input.text() == "":
                return ""
            return f"Hello, {input.text()}!"


card_mod("card1")