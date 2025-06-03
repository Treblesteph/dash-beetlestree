import dash_mantine_components as dmc
from dash import callback, Output, Input, State, no_update

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
    return sidebar

def callbacks_sidebar(app, tree_data):
    @callback(
        Output("appshell", "navbar"),
        Input("burger", "opened"),
        State("appshell", "navbar"),
    )
    def navbar_is_open(opened, navbar):
        navbar["collapsed"] = {"mobile": not opened}
        return navbar
    
    @callback(
        Output("pics", "children"),
        Input('d3tree', 'activeNode'),
        prevent_initial_call=True,
    )
    def display_output(activeNode):
        if activeNode.endswith("dae"):

            # species_imgs = get_naturespot_imgs(activeNode)
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
            return pics
        return no_update