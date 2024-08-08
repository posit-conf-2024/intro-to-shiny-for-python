from shiny.express import ui, render, input

ui.input_text("name", "Type a name", value="world")

@render.text
def greeting():
  return f"Hello {input.name()}!"