from dash import html
from dash import dcc
import dash_bootstrap_components as dbc
import pandas as pd
# import turbineView.Analysis_Tools as AT
# from page1TurbineView import  *


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
        style={'marginLeft':35,'marginTop':25,'fontSize':30}
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
                            dbc.Col(html.P("Select year and products to update plot:"), md=12),
                            dbc.Col(
                                [
                                    dcc.Dropdown(
                                        id="year_drpdwn_IO",
                                        options=[
                                            {"label": i, "value": i}
                                            for i in Year_List
                                        ],
                                        value=Year_List[0],
                                        style={'fontSize':15,'color':'black'}
                                    )
                                ],
                                md=1,
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
                                md=11,
                            ),
                        ]
                    ),
                    # dcc.Graph(id="bigrams-comps"),
                    # html.Div(id='figure1',style={'margin-top': '15px', 'margin-left': '20px'}),
                    html.Br(),
                    dcc.Graph(id="figure1",    style = {"border-style": "solid",
                           'border-color': '#ff4d4d', 'border-width': '1px', 'border-radius': "0.25rem"
                           }),

                ],
                type="default",
            )
        ],
        style={"marginTop": 0, "marginBottom": 0},
    ),
]
BODY = dbc.Container(
    [
        dbc.Row([dbc.Col(dbc.Card(TOP_BIGRAM_COMPS)),], style={"marginTop": 30,"marginLeft": 0,"border-style": "solid",
                           'border-color': '#ff4d4d',}),
        # dbc.Row([dbc.Col(dbc.Card(TOP_BIGRAM_PLOT)),], style={"marginTop": 30}),
        # dbc.Row(
        #     [
        #         dbc.Col(LEFT_COLUMN, md=4, align="center"),
        #         dbc.Col(dbc.Card(TOP_BANKS_PLOT), md=8),
        #     ],
        #     style={"marginTop": 30},
        # ),
        # dbc.Card(WORDCLOUD_PLOTS),
        # dbc.Row([dbc.Col([dbc.Card(LDA_PLOTS)])], style={"marginTop": 50}),
    ],
    # className="mt-12",
    fluid=True
)

content = html.Div(id="page1-content", children=[generate_select_country_drpdwn(),BODY], style=CONTENT_STYLE)
