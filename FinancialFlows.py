from dash import html
from dash import dcc
import dash_bootstrap_components as dbc
import pandas as pd
import os

import figures
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

Fuel_Price = [
    dbc.CardHeader(html.H5("Regional retail fuel and electricity prices")),
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
                        dbc.Col(html.Div(dcc.Graph(id="Diesel_price", figure=figures.diesel_petrol_price("Diesel")),
                                         style=figure_border_style), md=6),
                        dbc.Col(html.Div(dcc.Graph(id="Petrol_price", figure=figures.diesel_petrol_price("Petrol")),
                                         style=figure_border_style), md=6),

                    ]),
                    html.Br(),
                    dbc.Row([
                        dbc.Col(html.Div(dcc.Graph(id="Petrol_price", figure=figures.elec_price_plot()),
                                         style=figure_border_style), md=12),
                    ]),
                ],
                type="default",
            )
        ],
        style={"marginTop": 0, "marginBottom": 0},
    ),
]


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


def select_product():
    df = pd.read_csv("Data/Sankey/csv/{}/{}.csv".format(2019,'PNG'))
    from_ = df[' (from)'].tolist()
    from_ = list(set(from_))
    to = df[' (to)'].tolist()
    product_list = []
    for country in Country_List:
        df_exp= pd.read_csv("Data/{}/Exports-{}---Click-to-Select-a-Product.csv".format(country,2019))
        df_imp = pd.read_csv("Data/{}/Imports-{}---Click-to-Select-a-Product.csv".format(country,2019))
        for i in df_exp['HS4']:
            product_list.append(i)
        for i in df_imp['HS4']:
            product_list.append(i)

    product_list = list(set(product_list))


    flow_list=[]
    farm_drpdwn_dbc = dbc.FormGroup(
        [
            # dbc.Label("Product"),
            dcc.Dropdown(
                id="select-product-dynamic",
                options=[
                    {"label": i, "value": i} for i in product_list
                ],
                value=product_list[0],
                style={'width': "50%", 'margin-left': "0px",'fontColor':'black','fontSize':15,'color':'black'},
                multi=False,
                searchable=True,
                clearable=False,
            ),
            dbc.Button("Add Figure", color="danger", id='update-button-cross-country-products', n_clicks=0, className="me-1"),
            dbc.Button("Clear Canvas", color="primary", id='update-button-products-clear-canvas', n_clicks=0,
                       className="me-1"),

        ],
        inline=True,
        style={'marginLeft':35,'marginTop':25,'fontSize':25}
    )
    return farm_drpdwn_dbc

Cross_country_financial_flows = [

    dbc.CardHeader(html.H5("User-defined cross-country comparison of import and export of a product")),
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
                    select_product(),
                    html.Br(),
                    html.Div(id='Hidden-Div_trend_financial_flows', children=[0, 0], style={'display': 'none'}),
                    html.Div(id='dynamic_callback_container_financial_flows', children=[],
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
        dbc.Row([dbc.Col(dbc.Card(Fuel_Price)), ], style={"marginTop": 30,
                                                                }),
        dbc.Row([dbc.Col(dbc.Card(TOP_BIGRAM_COMPS)),], style={"marginTop": 30,
                           }),
        dbc.Row([dbc.Col(dbc.Card(Cross_country_financial_flows)), ], style={"marginTop": 30,
                                                                }),
    ],
    # className="mt-12",
    fluid=True
)

content = html.Div(id="financial-flows", children=[BODY], style=CONTENT_STYLE)