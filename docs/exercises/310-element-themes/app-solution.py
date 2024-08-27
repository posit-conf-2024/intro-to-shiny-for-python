from shiny.express import input, render, ui
from shiny import reactive
from plots import plot_auc_curve, plot_precision_recall_curve, plot_score_distribution
from data_import import scores
from shinyswatch import theme


app_theme = theme.cerulean

ui.page_opts(
    title="Model scoring dashboard",
   # theme = app_theme
)

with ui.sidebar(class_="bg-primary-subtle"):
    ui.input_select(
        "account",
        "Account",
        choices=[
            "Berge & Berge",
            "Fritsch & Fritsch",
            "Hintz & Hintz",
            "Mosciski and Sons",
            "Wolff Ltd",
        ],
    )

ui.nav_spacer(),

with ui.nav_panel("Training Dashboard"):

    with ui.navset_card_underline(title="Model Metrics"):

        with ui.nav_panel("ROC Curve"):
            @render.plot
            def roc_curve():
                return plot_auc_curve(
                    dat(), 
                    "is_electronics", 
                    "training_score", 
                    color = app_theme.colors.primary,
                    line_color = app_theme.colors.secondary
                )

        with ui.nav_panel("Precision/Recall"):
            @render.plot
            def precision_recall():
                return plot_precision_recall_curve(dat(), "is_electronics", "training_score", color = app_theme.colors.primary)

    with ui.card():
        ui.card_header("Training Scores")
        @render.plot
        def score_dist():
            return plot_score_distribution(dat(), color = app_theme.colors.primary)

with ui.nav_panel("View Data"):

    with ui.layout_columns():

        with ui.value_box(theme = "info-subtle"):
            "Row count"
            @render.text
            def row_count():
                return dat().shape[0]

        with ui.value_box(theme="success"):
            "Mean training score"
            @render.text
            def mean_score():
                return round(dat()["training_score"].mean(), 2)
                
    with ui.card():
        @render.data_frame
        def data():
            return dat()

@reactive.calc()
def dat() -> pd.DataFrame:
    return scores.loc[scores["account"] == input.account()]


