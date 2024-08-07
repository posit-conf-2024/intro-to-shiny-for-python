from shiny.express import render, ui
from shinywidgets import render_widget

from data_import import df # loads accounts data
from plots import plot_var_distribution # loads helper function

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

@render_widget
def plot():
    tbl=df[df.account == "Wolff Ltd"]
    return plot_var_distribution(tbl, var="training_score")

@render.data_frame
def table():
    tbl=df[df.account == "Wolff Ltd"]
    return tbl

