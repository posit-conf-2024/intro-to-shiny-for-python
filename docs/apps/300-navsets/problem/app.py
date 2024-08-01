from shiny.express import ui

with ui.navset_tab():
    with ui.nav_panel( "Panel 1"):
        ui.input_slider("slider", "Slider", 0, 100, 20)
    with ui.nav_panel("Panel 2"):
        ui.input_action_button("button", "Button A")
    with ui.nav_panel("Panel 3"):
        ui.input_action_button("button2", "Button B")
