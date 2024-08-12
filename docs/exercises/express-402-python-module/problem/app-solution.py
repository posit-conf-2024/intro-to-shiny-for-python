from shiny.express import ui, render, input
from shiny import reactive
import pandas as pd
from pathlib import Path
import plots

# Import from solution.py

from solution import filter_weather

infile = Path(__file__).parent / "weather.csv"
weather = pd.read_csv(infile)
weather["error"] = weather["observed_temp"] - weather["forecast_temp"]

# This is the reactive function:
@reactive.calc
def filtered_data():
    return filter_weather(weather, input.cities(), input.dates())


ui.page_opts(title="Weather error")
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

    with ui.navset_tab():
        with ui.nav_panel("Error"):

            with ui.card():
                ui.card_header("Distribution")
                @render.plot
                def error_distribution():
                    return plots.temp_distribution(filtered_data())


            with ui.card():
                ui.card_header("Error by day")
                @render.plot
                def error_by_day():
                    return plots.daily_error(filtered_data(), input.alpha())
                
                ui.input_slider("alpha", "Plot Alpha", value=0.5, min=0, max=1)

        with ui.nav_panel("Data"):
            @render.data_frame
            def data():
                return filtered_data()
    

