from dash import html
from dash import dcc
import dash_bootstrap_components as dbc
import pandas as pd
import os
from EnergyFlows import generate_select_country_drpdwn

Country_List = ['Samoa','Nauru','Vanuatu','Palau','Kiribati','Cook Islands','Solomon Islands','Tonga','New Caledonia','French Polynesia','Micronesia','Niue','Tuvalu','PNG','Fiji']
Year_List = ['2019','2018','2017']
CONTENT_STYLE = {
    "margin-left": "0rem",
    "margin-right": "1rem",
    # "padding": "1rem 1rem",
    "border-style": "solid",
}

figure_border_style = {"border-style": "solid",
                          'border-color': '#ff4d4d', 'border-width': '1px', 'border-radius': "0.25rem"
                          }

Interest_list = ['Crude Petroleum', 'Refined Petroleum', 'Petroleum', 'Petroleum Gas', 'Coal Briquettes',
                 'Petroleum Coke', 'Fuel Wood', 'Coconut Oil', 'Ferroalloys', 'Nickel Mattes', 'Nickel Ore',
                 'Aluminium Ore', 'Non-Petroleum Gas', 'Hydrogen', 'Tug Boats', 'Fishing Ships',
                 'Non-fillet Frozen Fish',
                 'Cars', 'Busses', 'Delivery Trucks', 'Motorcycles', 'Bicycles',
                 'Combustion Engines', 'Engine Parts', 'Gas Turbines', 'Spark-Ignition Engines',
                 'Planes, Helicopters, and/or Spacecraft', 'Aircraft Parts',
                 'Passenger and Cargo Ships']

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
                    dbc.Row([
                        dbc.Col([
                        generate_select_country_drpdwn()
                        ]),
                    ]),
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




BODY = dbc.Container(
    [
        dbc.Row([dbc.Col(dbc.Card(TOP_BIGRAM_COMPS)),], style={"marginTop": 30,
                           }),
    ],
    # className="mt-12",
    fluid=True
)

content = html.Div(id="financial-flows", children=[BODY], style=CONTENT_STYLE)