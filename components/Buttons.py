import dash_mantine_components as dmc
from dash_iconify import DashIconify
from dash import ctx, Input, Output, ALL, no_update

def create_buttons():
    buttons = dmc.Affix(
        dmc.Stack(
            [
                dmc.Tooltip(
                    dmc.ActionIcon(
                        id={"type": "collapse-btn", "index": "order"},
                        variant="filled",
                        color="lime.5",
                        size="lg",
                        children=DashIconify(icon="material-symbols:arrows-input", width=20),
                    ),
                    label="Collapse All"
                ),
                dmc.Tooltip(
                    dmc.ActionIcon(
                        id={"type": "collapse-btn", "index": "suborder"},
                        variant="filled",
                        color="yellow.4",
                        size="lg",
                        children=DashIconify(icon="material-symbols:arrows-input", width=20),        
                    ),
                    label="Collapse Suborders"
                ),
                dmc.Tooltip(
                    dmc.ActionIcon(
                        id={"type": "collapse-btn", "index": "infraorder"},
                        variant="filled",
                        color="orange.6",
                        size="lg",
                        children=DashIconify(icon="material-symbols:arrows-input", width=20),
                    ),
                    label=" Collapse Infraorders"
                ),
                dmc.Tooltip(
                    dmc.ActionIcon(
                        id={"type": "collapse-btn", "index": "superfamily"},
                        variant="filled",
                        color="red.6",
                        size="lg",
                        children=DashIconify(icon="material-symbols:arrows-input", width=20),
                    ),
                    label=" Collapse Superfamilies"
                ),
            ],
            gap="xs"
        ),
        position={"top": 80, "right": 20}
    )

    return buttons

def callbacks_buttons(app):
    @app.callback(
        Output("d3tree", "collapse"),
        Input({"type": "collapse-btn", "index": ALL}, "n_clicks"),
        prevent_initial_call=True
    )
    def display_output(n_clicks_list):
        triggered = ctx.triggered_id
        if not triggered: return no_update
        return triggered["index"]