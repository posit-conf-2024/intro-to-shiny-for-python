from shiny.express import render, ui, input
from shiny import reactive
import pandas as pd
from pathlib import Path
from plots import temp_distirbution, daily_error

infile = Path(__file__).parent / "weather.csv"
weather = pd.read_csv(infile)
weather["error"] = weather["observed_temp"] - weather["forecast_temp"]

ui.page_opts(title = "Weather Error")
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
        ui.input_slider("alpha", "Plot Alpha", value=0.5, min=0, max=1)

    # insert navset_tab here
    # insert nav_panel here containing error_distribution and error_by_day

    @render.plot
    def error_distribution():
        return temp_distirbution(filtered_data())
    
    @render.plot
    def error_by_day():
        return daily_error(filtered_data(), input.alpha())
    
    # insert nav_panel here containing data
    
    @render.data_frame
    def data():
        return filtered_data()
    

@reactive.calc
def filtered_data():
    df = weather.copy()
    df = df[df["city"].isin(input.cities())]
    df["date"] = pd.to_datetime(df["date"])
    dates = pd.to_datetime(input.dates())
    df = df[(df["date"] > dates[0]) & (df["date"] <= dates[1])]
    return df

