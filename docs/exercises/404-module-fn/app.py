from shiny.express import ui, input, render, module
from shiny import reactive

@module
def card_mod(input, output, session):
    with ui.card():
        ui.card_header("What is your name?")
        ui.input_text("text", "Your name?")
        # Your task:
        # Insert a render.text element here
        # The element should return "Hello, {name}!" if the input is not empty
        # But only if the input is not empty


card_mod("card1")