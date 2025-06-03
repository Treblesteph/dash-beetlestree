import dash_mantine_components as dmc
from dash import html, dcc, callback, Input, Output, State


def truncate(text, max_chars=250):
        if len(text) <= max_chars:
             return text
        return text[:max_chars].rsplit(" ", 1)[0] + "..."


def create_description_card(fam, fam_description, common_names):
    
    common_name_tags = [dmc.Badge(c_name, color="red.6") for c_name in common_names]

    is_long = len(fam_description) > 250

    children = [
        dmc.Text(fam, fw=500, size="xl"),
        dmc.Text(id="fam-desc-text", size="md", c="dimmed"),
        dmc.Text(
            truncate(fam_description) if is_long else fam_description,
            id="fam-desc-text",
            size="md",
            c="dimmed"
        ),
        dcc.Store(id="desc-expanded", data=False),
        dcc.Store(id="desc-content", data=fam_description)
    ]

    if is_long:
        children.append(
            dmc.Button(
                "See more...",
                id="toggle-desc",
                variant="subtle",
                color="teal.9",
                size="xs",
            )
        )

    children.append(
        dmc.Stack(
            [
                dmc.Text("Common Name(s)", fw=500),
                dmc.Group(children=common_name_tags)
            ],
        )
    )

    return dmc.Card(children=children)

def callbacks_description_card(app):
    @callback(
        Output("fam-desc-text", "children"),
        Output("toggle-desc", "children"),
        Output("desc-expanded", "data"),
        Input("toggle-desc", "n_clicks"),
        State("desc-expanded", "data"),
        State("desc-content", "data"),
        prevent_initial_call=True
    )
    def toggle_description(n_clicks, expanded, fam_desc):
        new_state = not expanded
        if new_state:
            return fam_desc, "See less", new_state
        else:
            return truncate(fam_desc), "See more...", new_state
