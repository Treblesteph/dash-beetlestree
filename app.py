import requests
import json
import dash_tree
import dash_mantine_components as dmc
from dash import Dash, html

from components.Header import create_header
from components.Sidebar import create_sidebar, callbacks_sidebar
from components.Buttons import create_buttons, callbacks_buttons
from components.DescriptionCard import callbacks_description_card

app = Dash(__name__, suppress_callback_exceptions=True)
server = app.server

img_page_url = "https://www.naturespot.org/family/"
data_url = "https://raw.githubusercontent.com/Treblesteph/beetlestree/gh-pages/fams_taxonomy.json"
tree_data = requests.get(data_url).json()
logo = "https://raw.githubusercontent.com/Treblesteph/beetlestree/refs/heads/gh-pages/assets/12beetlefav.png"

header_component = create_header(logo)
sidebar_component = create_sidebar()
buttons_component = create_buttons()

layout = dmc.AppShell(
    [
        header_component,
        sidebar_component,
        dmc.AppShellMain(
            html.Div([
                buttons_component,
                dash_tree.DashTree(
                    id='d3tree',
                    data=tree_data,
                ),
            ])
        ),
    ],
    header={"height": 60},
    navbar={
        "width": 300,
        "breakpoint": "sm",
        "collapsed": {"mobile": True},
    },
    id="appshell"
)

app.layout = dmc.MantineProvider(layout)

callbacks_sidebar(app, tree_data)
callbacks_buttons(app)
callbacks_description_card(app)



if __name__ == '__main__':
    app.run(debug=True)
