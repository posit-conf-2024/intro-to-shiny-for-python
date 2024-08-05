from shiny.express import ui

@render.plot
def penguins_df():
    return df
