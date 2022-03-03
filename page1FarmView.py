from dash import html
# import dash_core_components as dcc
from dash import dcc
import dash_bootstrap_components as dbc
from app import app
import pandas as pd
# import turbineView.Analysis_Tools as AT
# from page1TurbineView import  *
import dash
import os
import dash_daq as daq

import config
image_directory =  os.getcwd() + '/Data/Sankey/'

# sankey_PREFIX = '/{}/Data/Sankey/'.format(config.DASH_APP_NAME)
CONTENT_STYLE = {
    "margin-left": "0rem",
    "margin-right": "1rem",
    # "padding": "1rem 1rem",
    "border-style": "solid",
}

Country_List = ['Samoa','Nauru','Vanuatu','Palau','Kiribati','Cook Islands','Solomon Islands','Tonga','New Caledonia','French Polynesia','Micronesia','Niue','Tuvalu','PNG','Fiji']
Year_List = ['2019','2018','2017']
Interest_list = ['Crude Petroleum', 'Refined Petroleum', 'Petroleum', 'Petroleum Gas', 'Coal Briquettes',
                 'Petroleum Coke', 'Fuel Wood', 'Coconut Oil', 'Ferroalloys', 'Nickel Mattes', 'Nickel Ore',
                 'Aluminium Ore', 'Non-Petroleum Gas', 'Hydrogen', 'Tug Boats', 'Fishing Ships',
                 'Non-fillet Frozen Fish',
                 'Cars', 'Busses', 'Delivery Trucks', 'Motorcycles', 'Bicycles',
                 'Combustion Engines', 'Engine Parts', 'Gas Turbines', 'Spark-Ignition Engines',
                 'Planes, Helicopters, and/or Spacecraft', 'Aircraft Parts',
                 'Passenger and Cargo Ships']

def generate_select_country_drpdwn():
    farm_drpdwn_dbc = dbc.FormGroup(
        [
            dbc.Label("Select Country"),
            dbc.Select(
                id="select-country",
                options=[
                    {"label": i, "value": i} for i in Country_List
                ],
                value='PNG',
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
                html.Img(src=app.get_asset_url("CEEMLogo.png"), height="80px"),
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
                        dbc.Col(html.Img(src=app.get_asset_url("UNSWLogo.png"), height="80px"), md=6),
                        dbc.Col(dbc.NavbarBrand("Pacific Islands Energy Balance", className="ml-2",style={'fontSize':35}), md=4),
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

TOP_BIGRAM_COMPS = [
    dbc.CardHeader(html.H5("Import and export flows")),
    dbc.CardBody(
        [
            dcc.Loading(
                id="loading-bigrams-comps",
                children=[
                    dbc.Alert(
                        "Something's gone wrong! Give us a moment, but try loading this page again if problem persists.",
                        id="no-data-alert-bigrams_comp",
                        color="warning",
                        style={"display": "none"},
                    ),
                    dbc.Row(
                        [
                            dbc.Col(
                                [
                                    dcc.Dropdown(
                                        id="product_drpdwn",
                                        # options=[
                                        #     {"label": i, "value": i}
                                        #     for i in Interest_list
                                        # ],
                                        value=Interest_list,
                                        multi=True,
                                        searchable=True,
                                        style={'fontColor':'black','fontSize':15,'color':'black'}

                                    ),

                                ],
                                md=12,
                            ),
                        ]
                    ),
                    # dcc.Graph(id="bigrams-comps"),
                    # html.Div(id='figure1',style={'margin-top': '15px', 'margin-left': '20px'}),
                    html.Br(),
                    html.Div(dcc.Graph(id="figure1"),style=figure_border_style)

                ],
                type="default",
            )
        ],
        style={"marginTop": 0, "marginBottom": 0},
    ),
]



Sankey = [
    dbc.CardHeader(html.H5("Sankey Diagram for Energy Flows")),
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













BODY = dbc.Container(
    [
        dbc.Row([dbc.Col(dbc.Card(TOP_BIGRAM_COMPS)),], style={"marginTop": 30,
                           }),
        dbc.Row([dbc.Col(dbc.Card(Sankey)),], style={"marginTop": 30}),
        # dbc.Card(Decarbonization),
        # dbc.Row([dbc.Col([dbc.Card(LDA_PLOTS)])], style={"marginTop": 50}),
    ],
    # className="mt-12",
    fluid=True
)

content = html.Div(id="page1", children=[generate_select_country_drpdwn(),BODY], style=CONTENT_STYLE)
