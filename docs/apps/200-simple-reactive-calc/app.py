import pandas as pd
from plotnine import ggplot, geom_density, labs, aes
import numpy as np

from shiny.express import render, ui, input
from shiny import reactive, req

ui.input_slider("n_rows", "Sample rows", 0, 100, 20)

@render.plot
def hist():
    rand = np.random.rand(input.n_rows(), 1)
    df = pd.DataFrame(rand, columns=["col_1"])
    return (
        ggplot(df, aes(x="col_1"))
        + geom_density()
        + labs(x="Random Values", y="Density", title="Distribution of Random Data")
    )

@render.data_frame
def df():
    rand = np.random.rand(input.n_rows(), 1)
    return pd.DataFrame(rand, columns=["col_1"])



