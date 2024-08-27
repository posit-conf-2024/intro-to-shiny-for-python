# Intro to Shiny for Python / Posit Conf::20204

This is the repository for the "Intro to Shiny for Python" workshop.


## For students

If you're a student, please visit the course pages at https://posit-dev.github.io/intro-to-shiny-for-python/

## Installation - for instructors only

Note: These instructions are to build the website locally, and is should only be necessary if you want to teach this class.

You will need to install a few things to render the website locally:

1) [Install quarto](https://quarto.org/docs/get-started/)

2) Install the shinylive python package `pip install shinylive --upgrade`

3) Install the shinylive quarto materials `quarto add quarto-ext/shinylive`

### How to edit the materials

This is a quarto website, so to make changes to the course text modify the `.qmd` files, or the `_quarto.yml`.

For a quick preview, use:

```sh
quarto preview
```

But for a more accurate preview, use:

```sh
quarto preview --render html
```

Note that while `--render html` is rather slow, it's the best way to see changes with the included applications. 

### Creating and including Shiny Apps

All of the apps live in the `apps` folder, which means that you can use VS Code to edit and test them out. 

To include an application insert an `asis` quarto chunk which looks like this:

`````` python
```{python}
##| echo: false
##| output: asis

include_shiny_folder("apps/basic-app")
```
``````

You can also pass options to this function to modify the behaviour of the included app. 

To include a set of problem tabs, your app should have two application files. `app.py` which shows the starting point for the problem and `app-solution.py` which shows the target application. 

You can then use the `problem_tabs_express` function to include the tabs.

`````` python
```{python}
##| echo: false
##| output: asis

problem_tabs_express("apps/basic-app")
```
```````

### Inserting multiple choice questions

You can insert a shinylive app which displays sets of multiple choice questions by supplying a dictionary. 

It is a good idea to always wrap this dictionary with the `Quiz` class which validates that it is the right format for the application.

````` python
```{python}
## | echo: false
## | output: asis

from helpers import multiple_choice_app, Quiz

questions = Quiz(
    {
        "What ui input is used for plots?": {
            "choices": ["ui.input_plot", "ui.plot_input", "ui.plotInput"],
            "answer": "ui.Input_plot",
        },
        "How do you remove a reactive link??": {
            "choices": ["reactive.isolate", "req", "reactive.Effect"],
            "answer": "reactive.isolate",
        },
        "What should you use to save an image of a plot to disk?": {
            "choices": ["reactive.Calc", "@ui.output_plot", "reactive.Effect"],
            "answer": "reactive.Effect",
        },
    }
)

multiple_choice_app(questions)
```
``````
