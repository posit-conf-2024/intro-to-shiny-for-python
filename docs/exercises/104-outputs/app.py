from shiny.express import render, ui

from data_import import df # loads accounts data

ui.input_select(
    id="account",
    label="Account",
    choices=[
        "Berge & Berge",
        "Fritsch & Fritsch",
        "Hintz & Hintz",
        "Mosciski and Sons",
        "Wolff Ltd",
    ],
)

ui.input_radio_buttons(
    "variable",
    "Select a variable to plot",
    choices={
        "prod_score": "Product Score", 
        "training_score": "Training Score"
    }
)

@render.data_frame
def table():
    tbl=df[df.account == "Wolff Ltd"]
    return tbl
