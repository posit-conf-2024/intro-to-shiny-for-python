# modify to also import the module function
from shiny.express import ui, render, module


# Fix this module:
# 1. Use the `@module` decorator to define a module function.
# 2. The module function should take the following arguments:
#    - `input`
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


# Now insert a card using the module function.
insert_card(
    ---, # unique id
    ---, # title
    ---,
)

# Bonus points: 
insert_card(
    "card3", # id
    "Also made by module", # title
    "This is the body of card 3",
)