import pandas as pd
from pathlib import Path
from plots import dist_plot, scatter_plot

from shiny.express import render, ui, input

infile = Path(__file__).parent / "penguins.csv"
penguins = pd.read_csv(infile)

ui.h1("Hello Penguins!")
with ui.layout_sidebar():
    with ui.sidebar():
        ui.input_slider( "mass", "Mass", 2000, 8000, 6000,)
        ui.input_checkbox("trend", "Add trendline")


    @render.plot
    def scatter():
        df = penguins.copy()
        filtered = df.loc[df["body_mass"] < input.mass()]
        return scatter_plot(filtered, input.trend())

    @render.data_frame
    def table():
        df = penguins.copy()
        filtered = df.loc[df["body_mass"] < input.mass()]
        summary = (
            filtered.set_index("species")
            .groupby(level="species")
            .agg({"bill_length": "mean", "bill_depth": "mean"})
            .reset_index()
        )
        return summary


