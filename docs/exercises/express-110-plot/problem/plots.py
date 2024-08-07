import plotly.express as px
from pandas import DataFrame

def plot_weather_scatterplot(df: DataFrame, trendline: bool):
    """
    Plots a scatter plot of observed_temp vs forecasted_temp colored by city.
    Adds a trendline if the trendline argument is True.

    Parameters:
    df (DataFrame): The DataFrame containing the data.
    trendline (bool): Whether to add an OLS trendline or not.

    Returns:
    fig (plotly.graph_objs._figure.Figure): The resulting Plotly figure.
    """
    if trendline:
        fig = px.scatter(df, x='observed_temp', y='forecast_temp', trendline='ols')
    else:
        fig = px.scatter(df, x='observed_temp', y='forecast_temp')
    
    return fig