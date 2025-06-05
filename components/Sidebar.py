import dash_mantine_components as dmc
from dash import callback, dcc, Output, Input, State, no_update, ctx, ClientsideFunction

from components.DescriptionCard import create_description_card
from scripts.find_node_by_family import find_family_node
from scripts.get_wiki_pics import get_wiki_pics

def create_sidebar():
    sidebar = dmc.AppShellNavbar(
        bg="teal.9",
        c="teal.0",
        id="navbar",
        p="md",
        children=[
            dcc.Store(id="dummy-output"),
            dmc.Flex(
                direction="column",
                style={"height": "100%"},
                children=[
                    dmc.Box(
                        style={
                            "overflowY": "auto",
                            "flex": 1,
                            "paddingRight": "0.5rem"
                        },
                        children=[
                            dcc.Loading(
                                id="loading-pics",
                                type="cube",
                                style={"position": "sticky", "top": 0, "zIndex": 10},
                                children=[
                                    dmc.Stack(
                                        id='pics',
                                        gap="md",
                                        children=["Explore the tree and click on a family (ending in 'dae') to see images"]
                                    )
                                ]
                            )
                        ]
                    )
                ]
            )
        ]
    )
    return sidebar

def callbacks_sidebar(app, tree_data):
    @callback(
        Output("appshell", "navbar"),
        Output("burger-tooltip", "opened"),
        Output("pics", "children"),
        Input("burger", "opened"),
        Input('d3tree', 'activeNode'),
        State("appshell", "navbar"),
        prevent_initial_call=True,
    )
    def handle_sidebar_and_tooltip(burger_opened, activeNode, navbar):
        trigger_id = ctx.triggered_id
        
        new_navbar = no_update
        tooltip_open = no_update
        pics = no_update

        if trigger_id == "burger":
            new_navbar = navbar
            new_navbar["collapsed"] = {"mobile": not burger_opened}
            tooltip_open = False

        if trigger_id == "d3tree" and activeNode and activeNode.endswith("dae"):
            fam_desc, species_imgs = get_wiki_pics(activeNode)
            common_names = find_family_node(tree_data, activeNode).get("commonnames", [])
            description_card = create_description_card(activeNode, fam_desc, common_names)

            pics = [
                dmc.Card(
                    children = [
                        dmc.CardSection(
                            dmc.Image(
                                src=image["image_url"],
                                alt=image["species"],
                                style={"width": "100%", "height": "auto"}
                            )
                        ),
                        dmc.CardSection(
                            dmc.Flex(
                                direction="column",
                                justify="center",
                                align="center",
                                style={"height": "100%"},
                                children=[
                                    dmc.Text(
                                        image["species"].replace('-', ' ').capitalize(),
                                        fw=500,
                                        p="sm"
                                    ),
                                ]
                            )
                        ),
                    ],
                    withBorder=True,
                    shadow="sm",
                    radius="md",
                    p="md"
                )
                for image in species_imgs
            ]

            pics.insert(0, description_card)
            tooltip_open = True

        return new_navbar, tooltip_open, pics

    app.clientside_callback(
        ClientsideFunction(namespace="clientside", function_name="scrollToTop"),
        Output("dummy-output", "data"),
        Input("d3tree", "activeNode")
    )
