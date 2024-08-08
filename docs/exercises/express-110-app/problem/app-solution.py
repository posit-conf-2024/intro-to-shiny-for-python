from shiny.express import input, ui
from data_import import df
from plots import plot_weather_scatterplot
from shinywidgets import render_plotly

ui.h1("Accuracy of forecasts by city")

ui.input_select(
    "city",
    "Select a city to display",
    choices=df['city'].unique().tolist(),
    selected="ALBANY"
)

ui.input_switch("trendline", "Add trendline")

@render_plotly
def plot():
    filtered_df = df[df['city'] == input.city()]
    return plot_weather_scatterplot(filtered_df, input.trendline())
