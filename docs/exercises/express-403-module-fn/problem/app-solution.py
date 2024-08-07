from shiny.express import ui, render, module

@module
def card_mod(input, output, session, title, body:
    with ui.card():
        ui.card_header(title)
        body
        @render.text
        def _text_out():
            return fn

## server ------------------

def foo(x = ""):
    return "foo" + x


## ui ------------------

# This card displays correctly
with ui.card():
    ui.card_header("Card header")
    "Card content"
    @render.text
    def _():
        return foo()

## this card is generated automatically via a module
card_mod(
    "card1", # id
    "Card header...", 
    "This is the body...",
    foo("bar")
    )
