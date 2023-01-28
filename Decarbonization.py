from dash import html
from dash import dcc
import dash_bootstrap_components as dbc

from EnergyFlows import figure_border_style


dataset_year = dbc.FormGroup(
    [
        dbc.Label("Choose the year of the dataset you want to use for the analysis"),
        dbc.Select(
            id="year-for-decarbonization",
            options=[
                {"label": i, "value": i} for i in ['2017','2018','2019','2020']
            ],
            value='2019',
            style={'width': "15%", 'margin-left': "15px"},
            disabled=True

        )])

def generate_select(id, title, min, max, step, value):
    content = html.Div(
        [
            dbc.InputGroup(
                [
                    dbc.InputGroupText(title),
                    dbc.Input(
                        placeholder="Amount",
                        value=value,
                        step=step,
                        type="number",
                        id=id,
                        min=min,
                        max=max,
                    ),
                ],
                className="mb-3",
            ),
        ]
    )
    return content



Decarbonization = [
    dbc.CardHeader(html.H5("Replacing the fossil-based generators with renewable energy")),
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
                            dbc.Col(
                                [
                                    dbc.Label("Select a demand scenario"),
                                    dbc.RadioItems(
                                            id="radio-demand-scenario",
                                            options=[
                                                {"label": "Decarbonization", "value": 'Decarbonization'},
                                                {"label": "Electrification of all sectors", "value": 'Electrification'},
                                                {"label": "Net zero scenario by 2050 (10 MWh/person/year)", "value": 'Net_zero'},
                                            ],
                                            value='Electrification',
                                            inline=False,
                                            style={"fontSize": 14}
                                        ),
                                    html.Br(),
                                    dbc.Label("Fuel price and new genset cost"),
                                    generate_select(
                                        "genset-cost",
                                        "Genset cost: $/W",
                                        5,
                                        15,
                                        1,
                                        9,
                                    ),

                                    generate_select(
                                        "diesel-price",
                                        "Diesel: $/L",
                                        0.5,
                                        2.5,
                                        0.1,
                                        1.1,
                                    ),
                                    generate_select(
                                        "coal-price",
                                        "Coal: $/tonne",
                                        200,
                                        600,
                                        5,
                                        400,
                                    ),
                                    dbc.Label("Emission Parameters"),
                                    generate_select(
                                        "carbon-price",
                                        "Carbon price: $/ton",
                                        0,
                                        250,
                                        5,
                                        50,
                                    ),
                                    dbc.Label("RE potential"),
                                    generate_select(
                                        "available-land",
                                        "% Available land(Arable and pasture):",
                                        0,
                                        100,
                                        1,
                                        2,
                                    ),
                                    generate_select(
                                        "available-coastline",
                                        "% Available coastline:",
                                        0,
                                        100,
                                        1,
                                        10,
                                    ),
                                    generate_select(
                                        "available-buildings",
                                        "% Available buildings:",
                                        0,
                                        100,
                                        1,
                                        30,
                                    ),
                                    dbc.Label("RE size and installation cost"),
                                    generate_select(
                                        "large-PV-cost",
                                        "Large scale PV: $/W",
                                        0.5,
                                        8,
                                        0.1,
                                        4.5,
                                    ),
                                    generate_select(
                                        "rooftop-PV-cost",
                                        "Rooftop PV: $/W",
                                        1,
                                        15,
                                        0.1,
                                        4.5,
                                    ),
                                    generate_select(
                                        "res-battery-cost",
                                        "Residential Battery: $/W",
                                        1,
                                        15,
                                        0.1,
                                        4,
                                    ),
                                    generate_select(
                                        "wind-large-cost",
                                        "Large scale wind: $/W",
                                        1,
                                        8,
                                        0.1,
                                        6,
                                    ),
                                    generate_select(
                                        "rooftop-size",
                                        "Rooftop PV size: kW",
                                        0.5,
                                        5,
                                        0.1,
                                        2.5,
                                    ),
                                    generate_select(
                                        "res-battery-size",
                                        "Residential battery size: kWh",
                                        1,
                                        15,
                                        0.5,
                                        5,

                                    ),


                                    dbc.Label("Community battery parameters"),
                                    generate_select(
                                        "storage-days",
                                        "Total storage capacity (days):",
                                        0,
                                        15,
                                        1,
                                        5,
                                    ),
                                    generate_select(
                                        "ComBattery-cost",
                                        "Cost(millions of $/MWh):",
                                        0,
                                        10,
                                        0.05,
                                        3,
                                    ),
                                    html.Br(),

                                    generate_select(
                                        "decarb-year",
                                        "100% RE target:",
                                        2022,
                                        2060,
                                        1,
                                        2030,
                                    ),
                                    generate_select(
                                        "discount-rate",
                                        "Discount rate: %",
                                        0,
                                        100,
                                        1,
                                        7,
                                    ),
                                    generate_select(
                                        "inflation-rate",
                                        "Inflation rate: %",
                                        0,
                                        100,
                                        1,
                                        3,
                                    ),
                                    dbc.Button(
                                        "Update",
                                        color="danger",
                                        id="update-button",
                                        n_clicks=1,
                                        className="me-1",
                                    ),
                                ],
                                md=12,
                                sm=12,
                                lg=4,
                            ),
                            dbc.Col(
                                [
                                    dbc.Row(
                                        [
                                            dbc.Col(
                                                html.Div(
                                                    dcc.Graph(id="payback-periods"),
                                                    style=figure_border_style,
                                                    # id = 'payback-periods',
                                                ),
                                                md=12,
                                            ),
                                            html.Br(),
                                            dbc.Col(
                                                html.Div(
                                                    dcc.Graph(id="installed-storage"),
                                                    style=figure_border_style,
                                                ),
                                                md=12,
                                            ),
                                            html.Br(),
                                            dbc.Col(
                                                html.Div(
                                                    dcc.Graph(id="installed-MW"),
                                                    style=figure_border_style,
                                                ),
                                                md=12,
                                            ),
                                        ],
                                        style={
                                            "marginTop": 30,
                                        },
                                    ),

                                    html.Br(),

                                ]
                            ),
                        ],
                        justify="end",
                        style={"marginTop": "3%"},
                    ),

                    html.Br(),
                ],
                type="default",
            )
        ],
        style={"marginTop": 0, "paddingTop": 0, "marginBottom": 0},
    ),
]

BODY = dbc.Container(
    [
        dbc.Row(
            [
                dbc.Col(dbc.Card(Decarbonization)),
            ],
            style={"marginTop": 30},
        ),
    ],
    # className="mt-12",
    fluid=True,
)

content = [dataset_year, BODY]

# Add carbon cost to the annual costs
# add discount rate to financial flows
# Lit review for another method of decarbonization
# Start writing the paper
