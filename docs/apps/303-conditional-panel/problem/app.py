from shiny.express import input, render, ui
from shiny import reactive
import pandas as pd
from pathlib import Path
from plots import temp_distribution, daily_error

infile = Path(__file__).parent / "weather.csv"
weather = pd.read_csv(infile)
weather["error"] = weather["observed_temp"] - weather["forecast_temp"]

ui.page_opts(
    title="Weather Error"
)

with ui.layout_sidebar():
    with ui.sidebar():
        ui.input_date_range("dates", "Date", start="2022-01-01", end="2022-01-30"),
        ui.input_selectize(
            "states",
            "Select States",
            weather["state"].unique().tolist(),
            selected="CO",
            multiple=True,
        )

        @render.ui
        def cities_ui():
            df = weather.copy()
            df = df[df["state"].isin(input.states())]
            city_options = df["city"].unique().tolist()
            return ui.input_selectize(
                "cities",
                "Select Cities",
                choices=city_options,
                selected=city_options[0],
                multiple=True,
            )

        with ui.panel_conditional( "input.tabs === 'Data'"):
            ui.input_selectize(
                "columns",
                "Display Columns",
                choices=weather.columns.tolist(),
                selected=weather.columns.tolist(),
                multiple=True,
            )

    with ui.navset_tab(id="tabs"):
        with ui.nav_panel("Error plots"):
            with ui.layout_columns(col_widths=(4, 4, 4)):
                with ui.value_box():
                    # ui.output_text("hot_days")
                    "Hotter than forecast"
                    @render.text
                    def hot_days():
                        hot_days = filtered_data()["error"] > 0
                        return sum(hot_days)
                    
                with ui.value_box():
                    # ui.output_text("cold_days")
                    "Colder than forecast"
                    @render.text
                    def cold_days():
                        hot_days = filtered_data()["error"] < 0
                        return sum(hot_days)
                    
                with ui.value_box():
                    "Mean Error"
                    @render.text
                    def mean_error():
                        mean_error = filtered_data()["error"].mean()
                        return round(mean_error, 2)
            
            with ui.layout_columns(col_widths=(6, 6)):
                with ui.card():
                    ui.card_header("Distribution")
                    @render.plot
                    def error_distribution():
                        return temp_distribution(filtered_data())

                with ui.card():
                    ui.card_header("Error by day")
                    @render.plot
                    def error_by_day():
                        return daily_error(filtered_data(), input.alpha())
                    ui.input_slider("alpha", "Plot Alpha", value=0.5, min=0, max=1)

        with ui.nav_panel("Data"):
            @render.data_frame
            def data():
                return filtered_data().loc[:, input.columns()]


@reactive.calc
def filtered_data() -> pd.DataFrame:
    df = weather.copy()
    df = df[df["city"].isin(input.cities())]
    df["date"] = pd.to_datetime(df["date"])
    dates = pd.to_datetime(input.dates())
    df = df[(df["date"] > dates[0]) & (df["date"] <= dates[1])]
    return df