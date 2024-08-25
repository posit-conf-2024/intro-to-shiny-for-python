
from shiny.express import ui, render, input, module
from shiny import reactive
import pandas as pd
from pathlib import Path
import plots
from filter import filter_weather

infile = Path(__file__).parent / "weather.csv"
weather = pd.read_csv(infile)
weather["error"] = weather["observed_temp"] - weather["forecast_temp"]

@module
def card_module(input, output, session, title, fn):
    with ui.card():
        ui.card_header(title)
        @render.plot
        def _plot_out():
            return fn()

@reactive.calc
def filtered_data():
    return filter_weather(weather, input.cities(), input.dates())

ui.page_opts(title = "Weather error")
with ui.layout_sidebar():
    with ui.sidebar():
        ui.input_date_range("dates", "Date", start="2022-01-01", end="2022-01-30")
        ui.input_selectize(
            "cities",
            "Select Cities",
            weather["city"].unique().tolist(),
            selected="BUFFALO",
            multiple=True,
        )
            
    card_module(
        "card_1", 
        "Distribution", 
        # Task: use a lambda to make an inline function
        # this will delay execution of the reactive code
        # until in the reactive context of the module, 
        # i.e rendering the plot
        plots.temp_distribution(filtered_data())
    )

