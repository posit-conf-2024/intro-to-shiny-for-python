from shiny.express import input, render, ui

# UI section
ui.input_slider("n", "N", 0, 100, 20)


## Server section
@render.text
def txt():
    return f"2 * n is {input.n() * 2}"