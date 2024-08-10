from shiny.express import ui, render, module

@module
def insert_card(input, output, session, title, body):
    with ui.card():
        ui.card_header(title)
        body


with ui.card():
    ui.card_header("Made by hand")
    "Card 1 is a basic card"

insert_card(
    "card2", # id
    "Made by module", # title
    "This is the body of card 2",
)

insert_card(
    "card3", # id
    "Also made by module", # title
    "This is the body of card 3",
)