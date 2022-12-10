from app import app,application
import dash_bootstrap_components as dbc
from dash import html
from EnergyFlows import CONTENT_STYLE
from dash import dcc
import callbacks
import callbacks_sankey
import callbacks_FinancialFlows
import callbacks_modeling
import dash_auth
# import warnings
# warnings.filterwarnings('ignore')

# VALID_USERNAME_PASSWORD_PAIRS = {
#     'hello': 'world'
# }
# auth = dash_auth.BasicAuth(
#     app,
#     VALID_USERNAME_PASSWORD_PAIRS
# )

app.layout = dbc.Container([

     dbc.Row(
        [
            dbc.Col(
                [
                    dcc.Markdown(
                        """
            # Pacific Islands Energy Balance


            [Source code and user guide](https://github.com/UNSW-CEEM/PICTs_Decarbonization) 

            """,
                        style={"color": "green"},
                    )
                ],
                # width=True,
                lg=6,
                sm=12,
                md=12,
            ),
            dbc.Col(
                [
                    html.Img(
                        src="assets/UNSWLogo.png", alt="UNSW Logo", height="100px"
                    ),
                ],
                lg=2,
                sm=12,
                md=4,
            ),
            dbc.Col(
                [
                    html.Img(
                        src="assets/CEEMLogo.png", alt="CEEM Logo", height="100px"
                    ),
                ],
                lg=2,
                md=4,
                sm=12,
            ),
            dbc.Col(
                [
                    html.Img(
                        src="assets/edf-logo.png", alt="EDF Logo", height="100px"
                    ),
                ],
                lg=2,
                md=4,
                sm=12,
            ),
        ],
        align="end",
        style={"background-color": "white"},
    ),
    html.Br(),
    dbc.Tabs(
        [
            dbc.Tab(label="Summary",active_tab_style={"textTransform": "uppercase"},active_label_style={"color": '#FF0000'},tab_id='summary-tab'),
            dbc.Tab(label="Energy flows", active_tab_style={"textTransform": "uppercase"},
                    active_label_style={"color": '#FF0000'}, tab_id='energy-flows-tab'),

            dbc.Tab(label="Energy related financial flows", active_tab_style={"textTransform": "uppercase"},active_label_style={"color": '#FF0000'},
                    tab_id='financial-flows-tab'),
            dbc.Tab(label="Wind and solar potential", active_tab_style={"textTransform": "uppercase"},
            active_label_style={"color": '#FF0000'}, tab_id='windSolar-tab'),
            dbc.Tab(label="Geothermal potential", active_tab_style={"textTransform": "uppercase"},
                    active_label_style={"color": '#FF0000'}, tab_id='geothermal-tab'),
            dbc.Tab(label="Bioenergy potential", active_tab_style={"textTransform": "uppercase"},
                    active_label_style={"color": '#FF0000'}, tab_id='bioenergy-tab'),
            dbc.Tab(label="Simulation tool", active_tab_style={"textTransform": "uppercase"},active_label_style={"color": '#FF0000'},tab_id='decrb-tab'),
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
    # # app.run_server(host='0.0.0.0',debug=False,port=8080,dev_tools_ui=False,dev_tools_props_check=False)
    # app.run_server(debug=True,dev_tools_ui=False,dev_tools_props_check=False)
    application.run(debug=True, port=8080)  # ShayanLaptop



