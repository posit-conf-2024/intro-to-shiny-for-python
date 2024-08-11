from shiny.express import ui, render, input
from shiny import reactive
import pandas as pd
from data_import import df as weather
import plots

ui.input_date_range("dates", "Date", start="2022-01-01", end="2022-01-30")

ui.input_selectize(
    "cities",
    "Select Cities",
    weather["city"].unique().tolist(),
    selected="BUFFALO",
    multiple=True,
)

with ui.card():
    ui.card_header("Distribution"),
    @render.plot
    def error_distribution():
        return plots.temp_distribution(filtered_data())
        
with ui.card():
    ui.card_header("Error by day")
    @render.plot
    def error_by_day():
        return plots.daily_error(filtered_data(), input.alpha())
    ui.input_slider("alpha", "Plot Alpha", value=0.5, min=0, max=1)

@reactive.Calc
def filtered_data() -> pd.DataFrame:
    df = weather.copy()
    df = df[df["city"].isin(input.cities())]
    dates = pd.to_datetime(input.dates())
    df = df[(df["date"] > dates[0]) & (df["date"] <= dates[1])]
    return df



