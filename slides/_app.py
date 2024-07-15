
from shiny.express import input, render, ui

# UI section
ui.input_slider(id = "n", label = "N", min = 0, max = 100, value = 20)

## Server section
@render.text
def txt():
    return f"2 * n is {input.n() * 2}"