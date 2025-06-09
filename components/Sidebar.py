import dash_mantine_components as dmc
from dash import callback, dcc, Output, Input, State, no_update, ctx, ClientsideFunction

from components.DescriptionCard import create_description_card
from components.PictureCard import create_picture_card
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
            dcc.Store(id="all-images-store"),
            dcc.Store(id="images-to-show", data=10),
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
                                    ),
                                    dmc.Center(
                                        dmc.Button(
                                            "Load more images...",
                                            id="more-imgs-btn",
                                            variant="subtle",
                                            color="teal.9",
                                            mt="md"
                                        )
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
        Output("all-images-store", "data"),
        Output("images-to-show", "data"),
        Input("burger", "opened"),
        Input("d3tree", "activeNode"),
        Input("more-imgs-btn", "n_clicks"),
        State("appshell", "navbar"),
        State("all-images-store", "data"),
        State("images-to-show", "data"),
        prevent_initial_call=True
    )
    def handle_sidebar_and_node(
        burger_opened,
        activeNode,
        more_clicks,
        navbar,
        all_images,
        num_shown
    ):
        trigger_id = ctx.triggered_id

        new_navbar = no_update
        tooltip_open = no_update
        new_all_images = no_update
        new_num_shown = no_update

        # If burger clicked then open the sidebar and close the tooltip
        if trigger_id == "burger":
            new_navbar = navbar
            new_navbar["collapsed"] = {"mobile": not burger_opened}
            tooltip_open = False

        # If a family node was clicked then create the description card and get the images
        if trigger_id == "d3tree" and activeNode and activeNode.endswith("dae"):
            fam_desc, images = get_wiki_pics(activeNode)
            common_names = find_family_node(tree_data, activeNode).get("commonnames", [])
            description_card = create_description_card(activeNode, fam_desc, common_names)

            new_all_images = {
                "description_card": description_card,
                "images": images
            }
            new_num_shown = 10

        # If 'show more images' button was pressed then show more (up to the total)
        if trigger_id == "more-imgs-btn" and all_images:
            total = len(all_images["images"])
            if num_shown < total: new_num_shown = min(num_shown + 10, total)

        return new_navbar, tooltip_open, new_all_images, new_num_shown
    
    @callback(
        Output("pics", "children"),
        Input("all-images-store", "data"),
        Input("images-to-show", "data"),
        prevent_initial_call=True
    )
    def render_images(data, count):
        if not data: return no_update
        desc_card = data["description_card"]
        imgs = [create_picture_card(img) for img in data["images"][:count]]
        return [desc_card] + imgs
    
    @callback(
        Output("more-imgs-btn", "style"),
        Input("all-images-store", "data"),
        Input("images-to-show", "data"),
    )
    def toggle_btn(data, shown):

        if not data: return {"display": "none"}
        if shown >= len(data["images"]): return {"display": "none"}
        
        return {"display": "block"}



