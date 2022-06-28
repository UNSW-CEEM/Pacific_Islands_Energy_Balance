from dash import html
from dash import dcc
import dash_bootstrap_components as dbc
import pandas as pd
import os

# image_directory =  os.getcwd() + '/Data/Sankey/'

CONTENT_STYLE = {
    "margin-left": "0rem",
    "margin-right": "1rem",
    # "padding": "1rem 1rem",
    "border-style": "solid",
}

Country_List = ['Samoa','Nauru','Vanuatu','Palau','Kiribati','Cook Islands','Solomon Islands','Tonga','New Caledonia','French Polynesia','Micronesia','Niue','Tuvalu','PNG','Fiji']
Year_List = ['2019','2018','2017']


def generate_select_country_drpdwn():
    farm_drpdwn_dbc = dbc.FormGroup(
        [
            dbc.Label("Select Country"),
            dbc.Select(
                id="select-country",
                options=[
                    {"label": i, "value": i} for i in Country_List
                ],
                value='New Caledonia',
                style={'width': "15%", 'margin-left': "15px"}

            ),
            dbc.Label("Select Year",style={'margin-left': "15px"}
),
            dbc.Select(
                id="select-year",
                options=[
                    {"label": i, "value": i}
                    for i in Year_List
                ],
                value=Year_List[0],
                style={'width': "15%", 'margin-left': "15px"}
            ),
        ],
        inline=True,
        style={'marginLeft':35,'marginTop':25,'fontSize':20}
    )
    return farm_drpdwn_dbc

def select_sankey_flows():
    df = pd.read_csv("Data/Sankey/csv/{}/{}.csv".format(2019,'PNG'))
    from_ = df[' (from)'].tolist()
    from_ = list(set(from_))
    to = df[' (to)'].tolist()


    flow_list=[]
    farm_drpdwn_dbc = dbc.FormGroup(
        [
            dbc.Label("From"),
            dbc.Select(
                id="select-from",
                options=[
                    {"label": i, "value": i} for i in from_
                ],
                value=from_[0],
                style={'width': "20%", 'margin-left': "15px"}
            ),
            dbc.Label("to",style={'margin-left': "15px"}
),
            dbc.Select(
                id="select-to",
                style={'width': "20%", 'margin-left': "15px"}
            ),
            html.Div([
            dbc.RadioItems(
                    id="radio-normalization-sankey",
                    options=[
                        {"label": "Real values", "value": 1},
                        {"label": "Normalize with destination", "value": ' (to)'},
                        {"label": "Normalize with origin", "value": ' (from)'},
                    ],
                value=1,
                inline=True,
                style={"fontSize":14}
                )]),
            dbc.Button("Add Figure", color="danger", id='update-button-cross-country-figure', n_clicks=0, className="me-1"),
            dbc.Button("Clear Canvas", color="primary", id='update-button-sankey-clear-canvas', n_clicks=0,
                       className="me-1"),

        ],
        inline=True,
        style={'marginLeft':35,'marginTop':25,'fontSize':25}
    )
    return farm_drpdwn_dbc



def generate_single_year_drpdwn():
    farm_drpdwn_dbc = dbc.FormGroup(
        [
            dbc.Label("Select year"),
            dbc.Select(
                id="select-year",
                options=[
                    {"label": i, "value": i}
                    for i in Year_List
                ],
                value=Year_List[0],
                style={'width': "15%", 'margin-left': "15px"}
            ),
        ],
        inline=True,
        style={'marginLeft':35,'marginTop':25,'fontSize':25}
    )
    return farm_drpdwn_dbc



def generate_navbar(app):
    MAPNAlogo = dbc.Row(
        [
            dbc.Col(
                html.Img(src=app.get_asset_url("CEEMLogo.png"), height="120px"),
                md=4,
            ),
        ],
        no_gutters=True,
        className="ml-auto flex-nowrap mt-3 mt-md-0",
        align="center",
        justify="start",
    )

    navbar = dbc.Navbar(
        [
            html.A(
                dbc.Row(
                    [
                        dbc.Col([html.Img(src=app.get_asset_url("UNSWLogo.png"), height="120px"),
                                 html.Br(),

                                     html.Label(['Developed by: ', html.A(' Shayan Naderi', href='https://www.linkedin.com/in/shayan-naderi-461aa097/')]),
                                 # html.Br(),
                                 # html.A('s.naderi@unsw.edu.au')
                                 ], md=6),

                        dbc.Col([dbc.NavbarBrand("Pacific Islands Energy Balance",
                                                className="ml-2",style={'fontSize':34}),
                                 ], md=4),
                    ],
                    align="center",
                    no_gutters=True,
                    justify="start",

                ),
            ),
            MAPNAlogo,
        ],
        color="dark",
        dark=True,
    )
    return navbar


figure_border_style = {"border-style": "solid",
                          'border-color': '#ff4d4d', 'border-width': '1px', 'border-radius': "0.25rem"
                          }

Sankey = [
    dbc.CardHeader(html.H5("Sankey diagram for energy flows of individual countries")),
    dbc.CardBody(
        [
            dcc.Loading(
                id="loading-sankey",
                children=[
                    dbc.Alert(
                        "Something's gone wrong! Give us a moment, but try loading this page again if problem persists.",
                        id="no-data-alert-sankey",
                        color="warning",
                        style={"display": "none"},
                    ),

                    generate_select_country_drpdwn(),
                    html.Br(),
                    html.Div(dcc.Graph(id="Sankey_figure"),style=figure_border_style),
                    html.Br(),
                    html.Div(dcc.Graph(id="Sankey_elec_figure"),style=figure_border_style)

                ],
                type="default",
            )
        ],
        style={"marginTop": 0, "marginBottom": 0},
    ),
]

Cross_country_sankey = [

    dbc.CardHeader(html.H5("Cross-country comparison of Sankey diagrams")),
    dbc.CardBody(
        [
            dcc.Loading(
                id="loading-sankey",
                children=[
                    dbc.Alert(
                        "Something's gone wrong! Give us a moment, but try loading this page again if problem persists.",
                        id="no-data-alert-sankey",
                        color="warning",
                        style={"display": "none"},
                    ),
                    select_sankey_flows(),
                    html.Br(),
                    # html.Div(dcc.Graph(id="cross_country_sankey_figure"),style=figure_border_style),
                    html.Div(id='Hidden-Div_trend', children=[0, 0], style={'display': 'none'}),
                    html.Div(id='dynamic_callback_container', children=[],
                             style={'margin-top': '15px', 'margin-left': '20px','margin-right': '20px'}),

                    html.Br(),

                ],
                type="default",
            )
        ],
        style={"marginTop": 0, "marginBottom": 0},
    ),
]

style = {'border': 'solid', 'padding-top': '10px', 'align': 'center', 'justify': 'center', 'padding-left': '1px',
         'padding-right': '1px', }#'margin': "2px"

BODY = dbc.Container(
    [
        dbc.Row([dbc.Col(dbc.Card(Sankey)),], style={"marginTop": 30}),
        # dbc.Row([dbc.Col(dbc.Card(dynamic_callback)), ], style={"marginTop": 30}),
        dbc.Row([dbc.Col(dbc.Card(Cross_country_sankey)), ], style={"marginTop": 30}),

    ],
    # className="mt-12",
    fluid=True
)

content = html.Div(id="page1", children=[BODY], style=CONTENT_STYLE)
