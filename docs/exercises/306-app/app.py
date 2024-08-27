from shiny.express import input, render, ui
from shiny import reactive
from plots import plot_auc_curve, plot_precision_recall_curve, plot_score_distribution
from data_import import scores

# Model scoring dashboard

# Sidebar
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

# Page 1 - Training Dashboard

## A navset card featuring underlines named Model Metrics with two panels:

### ROC Curve
@render.plot
def roc_curve():
    return plot_auc_curve(dat(), "is_electronics", "training_score")

### Precision/Recall
@render.plot
def precision_recall():
    return plot_precision_recall_curve(dat(), "is_electronics", "training_score")


## Card named Training Scores
@render.plot
def score_dist():
    return plot_score_distribution(dat())

# Page 2 - View Data

## Row one has two columns:

### Column 1: A value box titled Row Count
@render.text
def row_count():
    return dat().shape[0]

### Column 2: A value box titled Mean training score"
@render.text
def mean_score():
    return round(dat()["training_score"].mean(), 2)

## Row two has one column:

### A card
@render.data_frame
def data():
    return dat()

@reactive.calc()
def dat() -> pd.DataFrame:
    return scores.loc[scores["account"] == input.account()]


