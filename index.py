from app import app
import dash_bootstrap_components as dbc
import page1FarmView as F
from dash import html
from page1FarmView import CONTENT_STYLE
import callbacks

import dash_auth

VALID_USERNAME_PASSWORD_PAIRS = {
    'hello': 'world'
}
auth = dash_auth.BasicAuth(
    app,
    VALID_USERNAME_PASSWORD_PAIRS
)

app.layout = dbc.Container([

    F.generate_navbar(app),
    html.Br(),
    dbc.Tabs(
        [
            dbc.Tab(label="Summary",active_tab_style={"textTransform": "uppercase"},active_label_style={"color": '#FF0000'},tab_id='summary-tab'),
            dbc.Tab(label="Energy and financial flows", active_tab_style={"textTransform": "uppercase"},active_label_style={"color": '#FF0000'},tab_id='flows-tab'),
            dbc.Tab(label="Geothermal potential", active_tab_style={"textTransform": "uppercase"},
            active_label_style={"color": '#FF0000'}, tab_id='geothermal-tab'),
            dbc.Tab(label="Decarbonization scenarios", active_tab_style={"textTransform": "uppercase"},active_label_style={"color": '#FF0000'},tab_id='decrb-tab'),
        ],
        id="tabs",
        active_tab="summary-tab",
    ),
    html.Br(),
    html.Div(id="Visible-content", style=CONTENT_STYLE),
    html.Br(),
], fluid=True)

app.title = "Pacific Island Countries"

if __name__ == '__main__':
    # app.run_server(host='0.0.0.0',debug=False,port=8080,dev_tools_ui=False,dev_tools_props_check=False)#MapnaMind
    app.run_server(debug=True,dev_tools_ui=False,dev_tools_props_check=False)#ShayanLaptop


