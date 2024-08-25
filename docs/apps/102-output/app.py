from shiny.express import render

@render.code  
def text():
    txt="Some text to display in code format"
    return txt