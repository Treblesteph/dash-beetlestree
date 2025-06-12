import dash_mantine_components as dmc
from dash import callback, dcc, Output, Input, State, no_update, ctx, ClientsideFunction

from components.DescriptionCard import create_description_card
from components.PictureCard import create_picture_card
from scripts.find_node_by_family import find_family_node
from scripts.get_wiki_pics import get_wiki_pics_cached as get_wiki_pics

def create_sidebar():
    sidebar = dmc.AppShellNavbar(
        bg="teal.9",
        c="teal.0",
        id="navbar",
        p="md",
        children=[
            dcc.Store(id="sidebar-state", data="idle"), # for determining loading state
            dcc.Store(id="all-images-store"),           # for storing fetched imgs
            dcc.Store(id="images-to-show", data=10),    # for determinding how many loaded
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
    return sidebar

def callbacks_sidebar(app, tree_data):
    # @callback(
    #     Output("sidebar-state", "data"),
    #     Input("d3tree", "activeNode"),
    #     prevent_initial_call=True
    # )
    # def start_loading(node):
    #     sb_state = no_update
    #     if node and node.endswith("dae"): sb_state = "loading"
    #     return sb_state

    @callback(
        Output("appshell", "navbar"),
        Output("burger-tooltip", "opened"),
        Output("all-images-store", "data"),
        Output("images-to-show", "data"),
        Output("sidebar-state", "data"),
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
                "images": images,
                "family": activeNode,
                "has_more": len(images) > 10
            }
            new_num_shown = 10
            tooltip_open = True

        # If 'show more images' button was pressed then show more (up to the total)
        if trigger_id == "more-imgs-btn" and all_images:
            all_images_copy = all_images.copy()
            total_available = len(all_images_copy["images"])
            next_count = min(total_available, num_shown + 10)
            
            new_num_shown = next_count
            all_images_copy["has_mode"] = next_count < total_available
            new_all_images = all_images_copy
            
        return new_navbar, tooltip_open, new_all_images, new_num_shown, "ready"
    
    @callback(
        Output("pics", "children"),
        Input("sidebar-state", "data"),
        Input("all-images-store", "data"),
        Input("images-to-show", "data"),
    )
    def update_sidebar_content(state, data, count):
        sb_content = no_update
        
        if state == "idle" or not state:
            sb_content = ["Explore the tree and click on a family (ending in 'dae') to see images"]

        if state == "loading":
            sb_content = [
                dmc.LoadingOverlay(
                    visible=True,
                    children=dmc.Center(dmc.Text("Loading images...")),
                    loaderProps={"variant": "dots", "color": "teal", "size": "lg"}
                )
            ]
        
        if state == "ready" and data:
            desc_card = data["description_card"]
            imgs = [create_picture_card(img) for img in data["images"][:count]]
            sb_content = [desc_card] + imgs
    
        return sb_content
    
    @callback(
        Output("more-imgs-btn", "style"),
        Input("all-images-store", "data"),
    )
    def toggle_btn(data):

        if not data: return {"display": "none"}
        if not data.get("has_more", True): return {"display": "none"}        
        
        return {"display": "block"}



