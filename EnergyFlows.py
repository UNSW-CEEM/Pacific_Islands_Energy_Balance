from dash import html
from dash import dcc
import dash_bootstrap_components as dbc
import pandas as pd
import os


CONTENT_STYLE = {
    "margin-left": "0rem",
    "margin-right": "1rem",
    "border-style": "solid",
}

Country_List = [
    "Samoa",
    "Nauru",
    "Vanuatu",
    "Palau",
    "Kiribati",
    "Cook Islands",
    "Solomon Islands",
    "Tonga",
    "New Caledonia",
    "French Polynesia",
    "Micronesia",
    "Niue",
    "Tuvalu",
    "PNG",
    "Fiji",
]

Year_List = ["2020","2019", "2018", "2017"]


def generate_select_country_drpdwn():
    farm_drpdwn_dbc = dbc.FormGroup(
        [
            dbc.Label("Select Country"),
            dbc.Select(
                id="select-country",
                options=[{"label": i, "value": i} for i in Country_List],
                value="New Caledonia",
                style={"width": "15%", "margin-left": "15px"},
            ),
            dbc.Label("Select Year", style={"margin-left": "15px"}),
            dbc.Select(
                id="select-year",
                options=[{"label": i, "value": i} for i in Year_List],
                value=Year_List[0],
                style={"width": "15%", "margin-left": "15px"},
            ),
        ],
        inline=True,
        style={"marginLeft": 35, "marginTop": 25, "fontSize": 20},
    )
    return farm_drpdwn_dbc


def select_sankey_flows():
    df = pd.read_csv("Data/Sankey/csv/{}/{}.csv".format(2019, "PNG"))
    from_ = df[" (from)"].tolist()
    from_ = list(set(from_))
    to = df[" (to)"].tolist()

    flow_list = []
    farm_drpdwn_dbc = dbc.FormGroup(
        [
            dbc.Label("From"),
            dbc.Select(
                id="select-from",
                options=[{"label": i, "value": i} for i in from_],
                value=from_[0],
                style={"width": "20%", "margin-left": "15px"},
            ),
            dbc.Label("to", style={"margin-left": "15px"}),
            dbc.Select(id="select-to", style={"width": "20%", "margin-left": "15px"}),
            html.Div(
                [
                    dbc.RadioItems(
                        id="radio-normalization-sankey",
                        options=[
                            {"label": "Real values", "value": 1},
                            {"label": "Normalize with destination", "value": " (to)"},
                            {"label": "Normalize with origin", "value": " (from)"},
                        ],
                        value=1,
                        inline=True,
                        style={"fontSize": 14},
                    )
                ]
            ),
            dbc.Button(
                "Add Figure",
                color="danger",
                id="update-button-cross-country-figure",
                n_clicks=0,
                className="me-1",
            ),
            dbc.Button(
                "Clear Canvas",
                color="primary",
                id="update-button-sankey-clear-canvas",
                n_clicks=0,
                className="me-1",
            ),
            dcc.Checklist(
                ['Export data'],
                inline=True,
                id="export-df-sankey-cross-country"
            )
        ],
        inline=True,
        style={"marginLeft": 35, "marginTop": 25, "fontSize": 25},
    )
    return farm_drpdwn_dbc


def generate_single_year_drpdwn():
    farm_drpdwn_dbc = dbc.FormGroup(
        [
            dbc.Label("Select year"),
            dbc.Select(
                id="select-year",
                options=[{"label": i, "value": i} for i in Year_List],
                value=Year_List[0],
                style={"width": "15%", "margin-left": "15px"},
            ),
        ],
        inline=True,
        style={"marginLeft": 35, "marginTop": 25, "fontSize": 25},
    )
    return farm_drpdwn_dbc


figure_border_style = {
    "border-style": "solid",
    "border-color": "#ff4d4d",
    "border-width": "1px",
    "border-radius": "0.25rem",
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
                    html.Div(dcc.Graph(id="Sankey_figure"), style=figure_border_style),
                    html.Br(),
                    html.Div(
                        dcc.Graph(id="Sankey_elec_figure"), style=figure_border_style
                    ),
                ],
                type="default",
            )
        ],
        style={"marginTop": 0, "marginBottom": 0},
    ),
]


def select_flow():
    import os

    path = "Data/EnergyBalance"
    files = os.listdir(path)

    df = pd.read_csv("Data/EnergyBalance/{}/all_countries_df.csv".format(files[-1]))
    input_from = [
        "Imports",
        "Primary production",
        "Total energy supply",
        "Final consumption",
        "Transformation",
        "Exports",
    ]
    input_source = [
        "Primary Coal and Peat",
        "Coal and Peat Products",
        "Primary Oil",
        "Oil Products",
        "Natural Gas",
        "Biofuels and Waste",
        "Nuclear",
        "Electricity",
        "Heat",
        "Total Energy",
        "All Coal",
        "All Oil",
        "memo: Of which Renewables",
    ]

    consumer_list = df["Transactions(down)/Commodity(right)"].unique()

    farm_drpdwn_dbc = dbc.FormGroup(
        [
            dbc.Row(
                [
                    dbc.Col(
                        [
                            dbc.Label(
                                "Energy supplied from", style={"margin-right": "5px",
                                                               "font-size":16}
                            )
                        ],
                        md=1.5,
                    ),
                    dbc.Col(
                        [
                            dcc.Dropdown(
                                id="select-flow-provider",
                                options=[{"label": i, "value": i} for i in input_from],
                                value=[input_from[0]],
                                style={
                                    "width": "90%",
                                    "margin-left": "0px",
                                    "margin-right": "10px",
                                    "fontColor": "black",
                                    "fontSize": 15,
                                    "color": "black",
                                },
                                multi=True,
                                searchable=True,
                                clearable=False,
                            ),
                        ],
                        md=4,
                    ),
                    dbc.Col(
                        [dbc.Label("In the form of", style={"margin-right": "5px",
                                                            "font-size":16})],
                        md=1.5,
                    ),
                    dbc.Col(
                        [
                            dbc.Select(
                                id="select-flow-provider-source",
                                options=[
                                    {"label": i, "value": i} for i in input_source
                                ],
                                value="All Oil",
                                style={
                                    "width": "80%",
                                    "margin-left": "0px",
                                    "margin-right": "10px",
                                    "fontColor": "black",
                                    "fontSize": 15,
                                    "color": "black",
                                },
                            ),
                        ],
                        md=4,
                    ),
                ]
            ),
            html.Br(),
            dbc.Row(
                [
                    dbc.Col([dbc.Label("To",style={"font-size":16})], md=0.5),
                    dbc.Col(
                        [
                            dcc.Dropdown(
                                id="select-flow-cunsumer",
                                options=[
                                    {"label": i, "value": i} for i in consumer_list
                                ],
                                value=[
                                    "International marine bunkers",
                                    "International aviation bunkers",
                                ],
                                style={
                                    "width": "100%",
                                    "margin-left": "0px",
                                    "fontColor": "black",
                                    "fontSize": 15,
                                    "color": "black",
                                },
                                multi=True,
                                searchable=True,
                                clearable=False,
                            )
                        ],
                        md=6,
                    ),
                    dbc.Col([dbc.Label("in the form of",style={"font-size":16})], md=1.5),
                    dbc.Col(
                        [
                            dbc.Select(
                                id="destination-carrier",
                                options=[
                                    {"label": i, "value": i} for i in input_source
                                ],
                                value="All Oil",
                                style={
                                    "width": "80%",
                                    "margin-left": "0px",
                                    "fontColor": "black",
                                    "fontSize": 15,
                                    "color": "black",
                                },
                            )
                        ],
                        md=4,
                    ),
                ]
            ),
            html.Br(),
            dbc.Input(
                placeholder="Y axis title",
                id="y_axis_title",
                className="mb-3",
                style={
                    "width": "40%",
                },
            ),
            dbc.Button(
                "Add Figure",
                color="danger",
                id="update-button-cross-country-flow",
                n_clicks=0,
                className="me-1",
            ),
            dbc.Button(
                "Clear Canvas",
                color="primary",
                id="update-button-flow-clear",
                n_clicks=0,
                className="me-1",
            ),
        ],
        inline=True,
        style={"marginLeft": 35, "marginTop": 25, "fontSize": 25},
    )
    return farm_drpdwn_dbc


def select_row_breakdown_details():
    path = "Data/EnergyBalance"
    files = os.listdir(path)
    df = pd.read_csv("Data/EnergyBalance/{}/all_countries_df.csv".format(files[-1]))
    row_list = df["Transactions(down)/Commodity(right)"].unique()
    dbc.Label("Select s sector", style={"margin-right": "5px"}),

    farm_drpdwn_dbc = dbc.FormGroup(
        [
            dbc.Label("Select a row  "),
            html.Br(),
            dbc.Select(
                id="select-row-for-breakdown",
                options=[{"label": i, "value": i} for i in row_list],
                value="Primary production",
                style={
                    "width": "30%",
                    "margin-left": "0px",
                    "margin-right": "10px",
                    "fontColor": "black",
                    "fontSize": 15,
                    "color": "black",
                },
            ),
            html.Br(),
            dbc.Button(
                "Add Figure",
                color="danger",
                id="update-button-sector-breakdown",
                n_clicks=0,
                className="me-1",
            ),
            dbc.Button(
                "Clear Canvas",
                color="primary",
                id="update-button-sector-breakdown-clear",
                n_clicks=0,
                className="me-1",
            ),
        ]
    )
    return farm_drpdwn_dbc


def dynamic_column_components():
    path = "Data/EnergyBalance"
    files = os.listdir(path)
    df = pd.read_csv("Data/EnergyBalance/{}/all_countries_df.csv".format(files[-1]))
    provider_list = df["Transactions(down)/Commodity(right)"].unique()
    dbc.Label("Select s column", style={"margin-right": "5px"}),
    columns = df.iloc[:, 3:-1]
    farm_drpdwn_dbc = dbc.FormGroup(
        [
            dbc.Label("Select rows  "),
            dcc.Dropdown(
                id="select-rows-for-column-comparison",
                options=[{"label": i, "value": i} for i in provider_list],
                value=["Primary production"],
                style={
                    "width": "60%",
                    "margin-left": "0px",
                    "margin-right": "10px",
                    "fontColor": "black",
                    "fontSize": 15,
                    "color": "black",
                },
                # style={"width": '60%'},
                multi=True,
                searchable=True,
                clearable=False,
            ),
            dbc.Label("Select a column"),
            html.Br(),
            dbc.Select(
                id="select-dynamic-column",
                options=[{"label": i, "value": i} for i in columns],
                value="Electricity",
                style={
                    "width": "30%",
                    "margin-left": "0px",
                    "margin-right": "10px",
                    "fontColor": "black",
                    "fontSize": 15,
                    "color": "black",
                },
            ),
            html.Br(),
            dbc.Label("Write the label for y axis"),
            html.Br(),
            dbc.Input(
                placeholder="Y axis title",
                id="y_axis_title_dynamic_column",
                className="mb-3",
                style={
                    "width": "30%",
                },
            ),
            html.Br(),
            dbc.Button(
                "Add Figure",
                color="danger",
                id="update-button-dynamic-column",
                n_clicks=0,
                className="me-1",
            ),
            dbc.Button(
                "Clear Canvas",
                color="primary",
                id="update-button-dynamic-column-clear",
                n_clicks=0,
                className="me-1",
            ),
        ]
    )
    return farm_drpdwn_dbc


Tracing_energy_flows = [
    dbc.CardHeader(
        html.H5(
            "Cross-country comparison of % one row to other rows (e.g., % of imported oil products consumed for international transit)"
        )
    ),
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
                    select_flow(),
                    html.Br(),
                    # html.Div(dcc.Graph(id="cross_country_sankey_figure"),style=figure_border_style),
                    html.Div(
                        id="Hidden_Div_breakdown",
                        children=[0, 0],
                        style={"display": "none"},
                    ),
                    html.Div(
                        id="dynamic_callback_container_energy_breakdown",
                        children=[],
                        style={
                            "margin-top": "15px",
                            "margin-left": "20px",
                            "margin-right": "20px",
                        },
                    ),
                    html.Br(),
                ],
                type="default",
            )
        ],
        style={"marginTop": 0, "marginBottom": 0},
    ),
]


breakdown_of_source_in_a_sector = [
    dbc.CardHeader(
        html.H5(
            "Breakdown of rows by energy sources in all countries (e.g., % final consumption from different energy sources)"
        )
    ),
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
                    select_row_breakdown_details(),
                    html.Br(),
                    # html.Div(dcc.Graph(id="cross_country_sankey_figure"),style=figure_border_style),
                    html.Div(
                        id="Hidden_Div_breakdown_by_source",
                        children=[0, 0],
                        style={"display": "none"},
                    ),
                    html.Div(
                        id="dynamic_callback_container_energy_breakdown_by_source",
                        children=[],
                        style={
                            "margin-top": "15px",
                            "margin-left": "20px",
                            "margin-right": "20px",
                        },
                    ),
                    html.Br(),
                ],
                type="default",
            )
        ],
        style={"marginTop": 0, "marginBottom": 0},
    ),
]


dynamic_column_cross_country = [
    dbc.CardHeader(
        html.H5(
            "Cross-country comparison of a column (i.e., Electricity primary production [TJ])"
        )
    ),
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
                    dynamic_column_components(),
                    html.Br(),
                    html.Div(
                        id="Hidden-Div_dynamic_column",
                        children=[0, 0],
                        style={"display": "none"},
                    ),
                    html.Div(
                        id="dynamic_callback_container_dynamic_column",
                        children=[],
                        style={
                            "margin-top": "15px",
                            "margin-left": "20px",
                            "margin-right": "20px",
                        },
                    ),
                    html.Br(),
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
                    html.Div(
                        id="Hidden-Div_trend",
                        children=[0, 0],
                        style={"display": "none"},
                    ),
                    html.Div(
                        id="dynamic_callback_container",
                        children=[],
                        style={
                            "margin-top": "15px",
                            "margin-left": "20px",
                            "margin-right": "20px",
                        },
                    ),
                    html.Br(),
                ],
                type="default",
            )
        ],
        style={"marginTop": 0, "marginBottom": 0},
    ),
]

style = {
    "border": "solid",
    "padding-top": "10px",
    "align": "center",
    "justify": "center",
    "padding-left": "1px",
    "padding-right": "1px",
}

BODY = dbc.Container(
    [
        dbc.Row(
            [
                dbc.Col(dbc.Card(Sankey)),
            ],
            style={"marginTop": 30},
        ),
        dbc.Row(
            [
                dbc.Col(dbc.Card(Tracing_energy_flows)),
            ],
            style={"marginTop": 30},
        ),
        dbc.Row(
            [
                dbc.Col(dbc.Card(breakdown_of_source_in_a_sector)),
            ],
            style={"marginTop": 30},
        ),
        dbc.Row(
            [
                dbc.Col(dbc.Card(dynamic_column_cross_country)),
            ],
            style={"marginTop": 30},
        ),
        dbc.Row(
            [
                dbc.Col(dbc.Card(Cross_country_sankey)),
            ],
            style={"marginTop": 30},
        ),
    ],
    fluid=True,
)

content = html.Div(id="page1", children=[BODY], style=CONTENT_STYLE)
