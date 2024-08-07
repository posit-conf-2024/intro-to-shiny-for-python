from shiny.express import render, ui
from shinywidgets import render_plotly

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
        "product_score": "Product Score", 
        "training_score": "Training Score"
    }
)

@render_plotly
def plot():
    return plot_var_distribution(df)

@render.data_frame
def table():
    return df


from shiny.express import render, ui, input
import pandas as pd
from pathlib import Path
from data_import import df

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


@render.data_frame
def table():
    # When we call the account input with `input.account()` we can use its value
    # with regular Python code. This will also cause the rendering function
    # to rerun whenever the user changes the account value.
    account_subset = df[df["account"] == input.account()]
    account_counts = (
        account_subset.groupby(["account", "sub_account"])
        .size()
        .reset_index(name="count")
    )
    return account_counts
