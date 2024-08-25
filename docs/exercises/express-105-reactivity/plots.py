import plotly.express as px
from pandas import DataFrame

def plot_var_distribution(df: DataFrame, var="prod_score"):
    fig = px.histogram(df, x=var, nbins=50, title="Model scores")
    fig.update_layout(xaxis_title="Score", yaxis_title="Density")
    return fig