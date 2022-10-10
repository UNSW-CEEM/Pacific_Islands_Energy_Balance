from dash import html
from dash import dcc
import dash_bootstrap_components as dbc
from app import app
import pandas as pd
import dash
import os
import dash_daq as daq
from EnergyFlows import figure_border_style
from EnergyFlows import Year_List
from EnergyFlows import CONTENT_STYLE
from EnergyFlows import generate_select_country_drpdwn



radioitems_diesel_price = html.Div(
    [
    dbc.Label("Choose diesel price ($/litre)"),
    html.Br(),html.Br(),html.Br(),
    # dcc.Slider(0.5, 2, 0.1, value=0.9,marks=None,id='diesel_price_slider',
    # tooltip={"placement": "bottom", "always_visible": True}),
    daq.Slider(
    min=0.4,
    max=8,
    value=1.5,
    handleLabel={"showCurrentValue": True,"label": "$/litre"},
    step=0.1,
    marks={'0.5': '0.5','2.5': '2.5'},
    id='diesel_price_slider',
    size=200
)
    ],
    style={"margin-bottom": "15px","margin-top": "0px",}
)
RE_share_slider = html.Div([
    html.Br(),
    dbc.Label("PV and wind mix for decarbonization"),
    html.Br(),    html.Br(),html.Br(),

    daq.Slider(
    min=0,
    max=100,
    value=0,
    handleLabel={"showCurrentValue": True,"label": "Wind"},
    step=5,
    marks={'0': '100% PV','25': '75% PV', '50': '50-50','75': '75% Wind','100': '100% Wind'},
    id = 'Wind_PV_share',
    size=200
)
])
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

gauge_size = "auto"


def generate_card_deck():
    cards = html.Div([
        dbc.Label("Statistics for the latest available data in 2019",),

        dbc.Row([
            dbc.Col(dbc.Card(
                [
                    dbc.CardBody(
                        [
                            dbc.Row([
                                dbc.Col(dbc.CardImg(src="/assets/electricity.png", bottom=True), width=3),
                                dbc.Col([html.H4(id='power-generated', className="card-title"),
                                         html.H6("Output of Power stations, GWh")])

                            ]),
                        ], style={'padding': '0.25rem'}
                    )
                ],
                color="danger",
            )),
            dbc.Col(dbc.Card(
                [
                    dbc.CardBody(
                        [
                            dbc.Row([
                                dbc.Col(dbc.CardImg(src="/assets/import-money.png", bottom=True), width=3),
                                dbc.Col([html.H4(id='generation-cost', className="card-title"), html.H6("Diesel for power generation, $MM")])

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
                                dbc.Col(dbc.CardImg(src="/assets/waste-money.png", bottom=True), width=3),
                                dbc.Col([html.H4(id='lost-cost', className="card-title"), html.H6("Lost diesel Cost, $MM")])
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
                                dbc.Col(dbc.CardImg(src="/assets/power-plant.png", bottom=True, ), width=3),
                                dbc.Col([html.H4(id='generation-efficiency',className="card-title"), html.H6("Conversion Efficiency, %")])
                            ]),
                        ],style={'padding':'0.25rem'}
                    )
                ],
                color="danger",

            ))
        ])
    ],style={'padding':'1rem'})
    return cards

def generate_card_deck_2():
    cards = html.Div([
        dbc.Row([
            dbc.Col(dbc.Card(
                [
                    dbc.CardBody(
                        [
                            dbc.Row([
                                dbc.Col(dbc.CardImg(src="/assets/emissions.png", bottom=True), width=3),
                                dbc.Col([html.H4(id='emission-quantity', className="card-title"), html.H6("Carbn emissions, Mt")])

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
                                dbc.Col(dbc.CardImg(src="/assets/waste-money.png", bottom=True), width=3),
                                dbc.Col([html.H4(id='emission-cost', className="card-title"), html.H6("Carbon cost, $MM")])
                            ]),
                        ], style={'padding': '0.25rem'}
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
                                dbc.Col(dbc.CardImg(src="/assets/rooftop.png", bottom=True), width=3),
                                dbc.Col([html.H4(id='rooftop-MW', className="card-title"), html.H6("Pot. Rooftop PV Capacity, MW")])

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
                                dbc.Col(dbc.CardImg(src="/assets/rooftop.png", bottom=True, ), width=3),
                                dbc.Col([html.H4(id='rooftop-GWh',className="card-title"), html.H6("Pot. Rooftop PV Generation, GWh")])
                            ]),
                        ],style={'padding':'0.25rem'}
                    )
                ],
                color="danger",

            ))
        ])
    ],style={'padding':'1rem'})
    return cards


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
                            dbc.Col([radioitems_diesel_price, html.Br(),
                                    html.Br(),
                                     html.Br(),
                                     dbc.Label("Emission Parameters"),

                                     generate_select('emissions-rate',"Emission intensity: t/MWh",0.2,7,0.1,0.8),
                                     generate_select('carbon-price', "Carbon price: $/ton", 0, 100, 0.1, 30),
                                     dbc.Label("RE size and installation cost"),

                                     generate_select('PV-cost',"Large scale PV: $/W",0.5,8,0.1,4.5),
                                     generate_select('PV-battery-cost',"Rooftop PV: $/W",1,15,0.1,4.5),
                                     generate_select('small-battery-cost', "Residential Battery: $/W", 1, 15, 0.1, 4),

                                     generate_select('wind-large-cost',"Large scale wind: $/W",1,8,0.1,6),
                                     generate_select('wind-battery-cost',"Small Wind+B: $/W",2.5,12,0.1,6),
                                     generate_select('rooftop-size', "Rooftop PV size: kW", 0.5, 5, 0.1,
                                                     2.5),
                                     html.Div(
                                         [
                                             dbc.Label("Community Battery "),
                                             dbc.Checklist(
                                                 options=[
                                                     {"label": "Community Battery", "value": 1},
                                                 ],
                                                 value=[1],
                                                 id="switches-communityBattery",
                                                 switch=True,
                                             ),
                                         ]
                                     ),
                                     generate_select('ComBattery-MWh', "Battery size (MWh):", 0, 50000, 0.5, 3),
                                     generate_select('ComBattery-cost', "Cost(M$/MWh):", 0, 10, 0.05, 3),
                                     html.Div(
                                [
                                    dbc.Label("Geothermal parameters"),
                                    dbc.Checklist(
                                        options=[
                                            {"label": "Geothermal", "value": 1},
                                        ],
                                        value=[0],
                                        id="switches-geothermal",
                                        switch=True,
                                    ),
                                    ]
                                    ),

                                     generate_select('geothermal-MW', "Geothermal (MW):", 0, 4000, 1, 0),
                                     generate_select('geothermal-completion', "Completion year:", 2022, 2050, 1, 2035),
                                     generate_select('geothermal-cost', "Geothermal cost (M$/MW):", 0.5, 10,
                                                     0.1, 5),
                                     generate_select('geothermal-CF', "Geothermal CF (%):", 0, 100, 1, 80),


                                     RE_share_slider,
                                     html.Br(),
                                     html.Br(),

                                     generate_select('small-PV-share', "PV+B to all PV: %", 0, 100, 5, 40),
                                     generate_select('small-wind-share', "Wind+B to all Wind: %", 0, 100, 5, 0),

                                     generate_select('demand-growth', "Demand growth: %/year", 0, 100, 1,
                                                     2),
                                     generate_select('decarb-year', "100% RE target:", 2022, 2060, 1,
                                                     2030),
                                     generate_select('discount-rate', "Discount rate: %", 0, 100, 1,
                                                     7),
                                     generate_select('inflation-rate', "Inflation rate: %", 0, 100, 1,
                                                     3),



                                     dbc.Button("Update", color="danger", id='update-button',n_clicks=1,className="me-1"),

                                     ],md=2,sm=3),
                            dbc.Col([

                                dbc.Row([
                                generate_card_deck(),
                                html.Br(),
                                generate_card_deck_2(),
                                ]),
                                html.Br(),
                                dbc.Row(
                                    [dbc.Col(html.Div(dcc.Graph(id='annual_demand'), style=figure_border_style), md=6),
                                     dbc.Col(html.Div(dcc.Graph(id='scenarios-annaul-RE'), style=figure_border_style), md=6)
                                     ], style={"marginTop": 30,
                                               }),
                                html.Br(),

                                dbc.Row([
                                    dbc.Col(html.Div(dcc.Graph(id='scenarios-plot'), style=figure_border_style), md=6),
                                    dbc.Col(html.Div(dcc.Graph(id='scenarios-plot-cum'), style=figure_border_style), md=6)
                                ]),
                                html.Br(),

                                dbc.Row([
                                    dbc.Col(html.Div(dcc.Graph(id='scenarios-annaul-diesel'), style=figure_border_style), md=6),
                                    dbc.Col(html.Div(dcc.Graph(id='scenarios-annual-carbon'), style=figure_border_style),
                                            md=6)
                                ]),

                            ])

                        ],
                        justify='end',
                        style={
                            "marginTop": "3%"
                        },
                    ),
                    # dbc.Row([dbc.Col(html.Div(dcc.Graph(id='required_RE'), style=figure_border_style), md=3),
                    #          dbc.Col(html.Div(dcc.Graph(id='oil_to_RE'), style=figure_border_style), md=6),
                    #         dbc.Col(html.Div(dcc.Graph(id='rooftop_PV_plot'), style=figure_border_style), md=3)
                    #          ], style={"marginTop": 30,
                    #                    }),

                    html.Br(),

                    # dcc.Graph(id="decarb_figure"),

                ],
                type="default",
            )
        ],
        style={"marginTop": 0,"paddingTop": 0, "marginBottom": 0},
    ),
]

BODY = dbc.Container(
    [
        dbc.Row([dbc.Col(dbc.Card(Decarbonization)), ], style={"marginTop": 30}),
    ],
    # className="mt-12",
    fluid=True
)

content = [generate_select_country_drpdwn(),BODY]

# Add carbon cost to the annual costs
# add discount rate to financial flows
# Lit review for another method of decarbonization
# Start writing the paper
