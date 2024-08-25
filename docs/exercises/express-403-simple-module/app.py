# Part 1: modify to also import the module function
from shiny.express import ui, render


# Part 2: fix this module:
# 1. Use the `@module` decorator to define a module function.
# 2. The module function should take the following arguments:
#    - `input``
#    - `output`
#    - `session`
#    - `title`
#    - `body`
@___
def insert_card(___):
    with ui.card():
        ui.card_header(title)
        body


# Leave this code as is.
# It generates a basic card.
with ui.card():
    ui.card_header("Made by hand")
    "Card 1 is a basic card"


# Part 3: Insert a card using the module function.
insert_card(
    ---, # unique id
    ---, # title
    ---, # body
)

# Part 4: bonus points for inserting another card
