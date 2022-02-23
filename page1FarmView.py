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
        ],
        inline=True,
        style={'marginLeft':35,'marginTop':25,'fontSize':25}
    )
    return farm_drpdwn_dbc

def generate_check_list():
    checklist = dcc.Checklist(
        id='checklist-WT-selection',
        # className = 'my_box_container',
        inputClassName='my_box_input',
        labelClassName='my_box_label',
    )
    return checklist


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


def generate_card_deck():
    cards = html.Div([
        dbc.Row([
            dbc.Col(dbc.Card(
                [
                    dbc.CardBody(
                        [
                            dbc.Row([
                                dbc.Col(dbc.CardImg(src="/assets/WindTurbine2.png", bottom=True), width=3),
                                dbc.Col([html.H4(id='farm-speed-card', className="card-title"), html.H6("wind Speed, m/s")])

                            ]),
                        ],style={'padding':'0.25rem'}
                    )
                ],
                color="danger",
            )),
            dbc.Col(dbc.Card(
                [
                    dbc.CardBody(
                        [
                            dbc.Row([
                                dbc.Col(dbc.CardImg(src="/assets/electricity.png", bottom=True), width=3),
                                dbc.Col([html.H4(id='farm-generation-card', className="card-title"), html.H6("Total Generation, kW")])

                            ]),
                        ],style={'padding':'0.25rem'}
                    )
                ],
                color="danger",
            )),
            dbc.Col(dbc.Card(
                [
                    dbc.CardBody(
                        [
                            dbc.Row([
                                dbc.Col(dbc.CardImg(src="/assets/frequency.jpg", bottom=True), width=3),
                                dbc.Col([html.H4(id='farm-freq-card', className="card-title"), html.H6("Frequency, Hz")])
                            ]),
                        ],style={'padding':'0.25rem'}
                    )
                ],
                color="danger",
                inverse=True,

            )),
            dbc.Col(dbc.Card(
                [
                    dbc.CardBody(
                        [
                            dbc.Row([
                                dbc.Col(dbc.CardImg(src="/assets/temp_icon.png", bottom=True, ), width=3),
                                dbc.Col([html.H4(id='farm-temperature-card',className="card-title"), html.H6("Ambient Temperature, °C")])
                            ]),
                        ],style={'padding':'0.25rem'}
                    )
                ],
                color="danger",

            ))
        ])
    ])
    return cards


def generate_liveData_farm():
    # AT.generate_hdf_live_data()
    livedata = [html.Br(), generate_select_country_drpdwn(), html.Br(), generate_check_list(), html.Br(), html.Div(id='table-container-live-data'),
                html.Br(), generate_card_deck()]
    return livedata


farm_view_tabs = html.Div(
    [
        dbc.Tabs(
            [
                dbc.Tab(label="Live Data", tab_id="tab-live-data"),
                # dbc.Tab(label="Favorites", tab_id="tab-favorites"),
                # dbc.Tab(label="Tab3", tab_id="tab-3-internal"),
            ],
            id="farm-view-tabs",
            active_tab="tab-live-data",
        ),
        html.Div(id="tabs-farm-view-div", style={'padding': '1rem' '1rem'}),
    ]
)

card = dbc.Card(
    [
        dbc.CardHeader(
            dbc.Tabs(
                [
                    dbc.Tab(label="Farm View", tab_id="farm-view"),
                    dbc.Tab(label="Turbine View", tab_id="turbine-view"),
                    dbc.Tab(label="DB Manager", tab_id="db-manager"),
                    dbc.Tab(label="Trend Monitoring", tab_id="trend-monitoring")
                ],
                id="overview-card-tabs",
                # card=True,
                active_tab="farm-view",
                # style = {}
            )
        ),
        html.Br(),
        dbc.CardBody(html.Div(id="farm-view", style={'padding': '1rem' '1rem'})),
    ]
)

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
                            dbc.Col(html.P("Select year and products to update plot:"), md=2),
                            dbc.Col(
                                [
                                    dcc.Dropdown(
                                        id="year_drpdwn_IO",
                                        options=[
                                            {"label": i, "value": i}
                                            for i in Year_List
                                        ],
                                        value=Year_List[0],
                                        style={'fontSize':12,'color':'black'},
                                        clearable=False

                                    )
                                ],
                                md=2,
                            ),
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

Transit = [
    dbc.CardHeader(html.H5("Energy for transit")),
    dbc.CardBody(
        [
            dcc.Loading(
                id="loading-bigrams-transit",
                children=[
                    dbc.Alert(
                        "Something's gone wrong! Give us a moment, but try loading this page again if problem persists.",
                        id="no-data-alert-transit_comp",
                        color="warning",
                        style={"display": "none"},
                    ),
                    dbc.Row(
                        [
                            dbc.Col(html.P("Select year and products to update plot:"), md=2),
                            dbc.Col(
                                [
                                    dcc.Dropdown(
                                        id="year_drpdwn_transit",
                                        options=[
                                            {"label": i, "value": i}
                                            for i in Year_List
                                        ],
                                        value=Year_List[0],
                                        style={'fontSize':12,'color':'black'},
                                        clearable=False

                                    )
                                ],
                                md=2,
                            ),
                        ]
                    ),
                    # dcc.Graph(id="bigrams-comps"),
                    # html.Div(id='figure1',style={'margin-top': '15px', 'margin-left': '20px'}),
                    dbc.Row([
                        dbc.Col(html.Div(dcc.Graph(id="transit_figure1"),style=figure_border_style),md=6),
                        dbc.Col(html.Div(dcc.Graph(id="transit_figure2"), style=figure_border_style), md=6),

                    ]),
                    html.Br(),
                    dbc.Row([
                        dbc.Col(html.Div(dcc.Graph(id="transit_figure3"), style=figure_border_style), md=6),
                        dbc.Col(html.Div(dcc.Graph(id="transit_figure4"), style=figure_border_style), md=6),
                    ])

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
                    dbc.Row(
                        [
                            dbc.Col(html.P("Select year to update Sankey diagram"), md=2),
                            dbc.Col(
                                [
                                    dcc.Dropdown(
                                        id="year_drpdwn_Sankey",
                                        options=[
                                            {"label": i, "value": i}
                                            for i in Year_List
                                        ],
                                        value=Year_List[0],
                                        style={'fontSize':15,'color':'black'},
                                        clearable=False

                                    )
                                ],
                                md=2,
                            ),
                        ]
                    ),
                    # dcc.Graph(id="bigrams-comps"),
                    # html.Div(id='figure1',style={'margin-top': '15px', 'margin-left': '20px'}),
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



def generate_gauge(id,title):
    g = dbc.Card(
    children=[
        dbc.CardHeader(
            title,
            style={
                "text-align": "center",
                "color": "white",
                "backgroundColor": "black",
                "border-radius": "1px",
                "border-width": "5px",
                "border-top": "1px solid rgb(216, 216, 216)",
            },
        ),
        dbc.CardBody(
            [
                html.Div(
                    daq.LEDDisplay(
                        id=id,
                        # min=min(df["WEC: ava. Power"]),
                        # max=None,  # This one should be the theoretical maximum
                        # value=100,
                        # showCurrentValue=True,
                        color="#fec036",
                        style={
                            "align": "center",
                            "display": "flex",
                            "marginTop": "0%",
                            "marginBottom": "0%",
                        },
                    ),
                    className="m-auto",
                    style={
                        "display": "flex",
                        "backgroundColor": "grey",
                        "border-radius": "1px",
                        "border-width": "5px",
                    },
                )
            ],
            className="d-flex",
            style={
                "backgroundColor": "grey",
                "border-radius": "1px",
                "border-width": "5px",
                "border-top": "1px solid rgb(216, 216, 216)",
            },
        ),
    ],
    style={"height": "100%"},

    )
    return g



radioitems_diesel_price = html.Div(
    [
    dbc.Label("Choose diesel price ($/litre)"),
    dcc.Slider(0.5, 2, 0.1, value=0.9,marks=None,id='diesel_price_slider',
    tooltip={"placement": "bottom", "always_visible": True}),
    ],
    style={'width':'90%'}
)
def generate_select(id,title,min,max,step,value):
    content = html.Div(
    [
        dbc.InputGroup(
            [
                dbc.InputGroupText(title),
                dbc.Input(placeholder="Amount",value=value, step=step, type="number",id=id,min=min,max=max),
                # dbc.InputGroupText(".00"),
            ],
            className="mb-3",
        ),]
        )
    return content





gauge_year = dcc.Dropdown(
    id="year_drpdwn_gauge",
    options=[
        {"label": i, "value": i}
        for i in Year_List
    ],
    value=Year_List[0],
    style={'fontSize': 12, 'color': 'black','width':'50%'},
    clearable=False,
)
gauge_size = "auto"



Decarbonization = [
    dbc.CardHeader(html.H5("Replacing the diesel fleet with renewable energy")),
    dbc.CardBody(
        [
            dcc.Loading(
                id="loading-decarb",
                children=[
                    dbc.Alert(
                        "Something's gone wrong! Give us a moment, but try loading this page again if problem persists.",
                        id="no-data-alert-decarb",
                        color="warning",
                        style={"display": "none"},
                    ),
                    dbc.Row(
                        [
                            dbc.Col([gauge_year, html.Br(), radioitems_diesel_price, html.Br(), generate_select('PV-cost',"PV: $/W",0.5,5,0.1,3),
                                     generate_select('PV-battery-cost',"PV + Battery: $/W",1,15,0.1,7),
                                     generate_select('wind-large-cost',"Large scale wind: $/W",1,5,0.1,3),
                                     generate_select('wind-battery-cost',"Small Wind + Battery: $/W",2.5,12,0.1,6),
                                     generate_select('demand-growth', "Demand growth: %/year", 0, 100, 1,
                                                     5),
                                    generate_select('decarb-rate', "Decarbonization: %/year", 0, 100, 1,
                                                     10),
                                     generate_select('rooftop-size', "Rooftop PV size: kW", 0.5, 5, 0.1,
                                                     2.5)

                                     ],md=2),
                            dbc.Col([
                                dbc.Row([
                                    dbc.Col(generate_gauge('generation-cost', 'Diesel cost for power generation [$MM]'),
                                    xs=gauge_size,
                                    md=gauge_size,
                                    lg=gauge_size,
                                    width=gauge_size),
                            dbc.Col(generate_gauge('power-generated', 'Power Generation from transformation [GWh]'),
                                    xs=gauge_size,
                                    md=gauge_size,
                                    lg=gauge_size,
                                    width=gauge_size),
                            dbc.Col(generate_gauge('lost-cost', 'Cost of losses through transformation [$MM]'),
                                    xs=gauge_size,
                                    md=gauge_size,
                                    lg=gauge_size,
                                    width=gauge_size),
                            dbc.Col(generate_gauge('generation-efficiency', 'Transformation efficiency [%]'),
                                    xs=gauge_size,
                                    md=gauge_size,
                                    lg=gauge_size,
                                    width=gauge_size),

                                ])

                            ])

                        ],
                        justify='end',
                        style={
                            "marginTop": "3%"
                        },
                    ),
                    dbc.Row([dbc.Col(html.Div(dcc.Graph(id='required_RE'), style=figure_border_style), md=3),
                             dbc.Col(html.Div(dcc.Graph(id='oil_to_RE'), style=figure_border_style), md=6),
                            dbc.Col(html.Div(dcc.Graph(id='rooftop_PV_plot'), style=figure_border_style), md=3)
                             ], style={"marginTop": 30,
                                       }),

                    html.Br(),
                    dbc.Row([dbc.Col(html.Div(dcc.Graph(id='annual_demand'), style=figure_border_style), md=6),
                             dbc.Col(html.Div(dcc.Graph(id='scenarios-plot'), style=figure_border_style), md=6)
                             ], style={"marginTop": 30,
                                       }),
                    # dcc.Graph(id="decarb_figure"),

                ],
                type="default",
            )
        ],
        style={"marginTop": 0, "marginBottom": 0},
    ),
]

BODY = dbc.Container(
    [
        dbc.Row([dbc.Col(dbc.Card(Transit)), ], style={"marginTop": 30,
                                                                }),
        dbc.Row([dbc.Col(dbc.Card(TOP_BIGRAM_COMPS)),], style={"marginTop": 30,
                           }),
        dbc.Row([dbc.Col(dbc.Card(Sankey)),], style={"marginTop": 30}),
        dbc.Row([dbc.Col(dbc.Card(Decarbonization)), ], style={"marginTop": 30}),

        # dbc.Card(Decarbonization),
        # dbc.Row([dbc.Col([dbc.Card(LDA_PLOTS)])], style={"marginTop": 50}),
    ],
    # className="mt-12",
    fluid=True
)

content = html.Div(id="page1-content", children=[generate_select_country_drpdwn(),BODY], style=CONTENT_STYLE)
