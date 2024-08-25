from shiny import reactive
from shiny.express import ui, render, input


ui.input_action_button("show", "Show modal dialog")

@render.text
def txt():
    return "Some text"

@reactive.effect
@reactive.event(input.show)
def show_modal():
    m = ui.modal(
        "This is a somewhat important message.",
        title="Click outside the modal to close",
        easy_close=True,
        footer=None,
    )
    ui.modal_show(m)


