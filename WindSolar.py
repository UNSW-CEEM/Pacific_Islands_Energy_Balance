from dash import html
from dash import dcc
import dash_bootstrap_components as dbc
import pandas as pd
from dash import dash_table
from EnergyFlows import Country_List
import figures
from EnergyFlows import figure_border_style

styles = ["open-street-map", "carto-positron", "carto-darkmatter", "stamen-terrain", "stamen-toner",
          "stamen-watercolor"]
def select_map_style():
    farm_drpdwn_dbc = dbc.FormGroup(
        [
            dbc.Label("Map style"),
            dbc.RadioItems(
                id="select-map-style",
                options=[
                    {"label": i, "value": i}
                    for i in styles
                ],
                value=styles[3],
                inline=True
                # style={'width': "25%", 'margin-left': "15px"}
            ),
        ],
        inline=True,
        style={'marginLeft':35,'marginTop':25,'fontSize':20}
    )
    return farm_drpdwn_dbc


def generate_single_country_drpdwn():
    farm_drpdwn_dbc = dbc.FormGroup(
        [
            dbc.Label("Select Country"),
            dbc.Select(
                id="select-justcountry",
                options=[
                    {"label": i, "value": i}
                    for i in Country_List
                ],
                value=Country_List[0],
                style={'width': "20%", 'margin-left': "15px"},
            ),
        ],
        inline=True,
        style={'marginLeft':35,'marginTop':25,'fontSize':20}
    )
    return farm_drpdwn_dbc

Physical = [
    dbc.CardHeader(html.H5("Available wind and solar resources")),
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
                    dbc.Row([
                        dbc.Col(html.Div(dcc.Graph(id="PV_physical_resource",figure=figures.Solar_physical_resources()[0]), style=figure_border_style), md=6),
                        dbc.Col(html.Div(dcc.Graph(id="Wind_physical_resource",figure=figures.Solar_physical_resources()[1]), style=figure_border_style), md=6),
                    ]),
                    html.Br(),
                ],
                type="default",
            )
        ],
        style={"marginTop": 0, "marginBottom": 0},
    ),
]

Required_capacity = [
    dbc.CardHeader(html.H5("Required capacity of wind and solar to meet the demand")),
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
                    dbc.Row([
                        dbc.Col(html.Div(dcc.Graph(id="wind_to_non_RE",figure=figures.land_use_plot()[0]), style=figure_border_style), md=6),
                        dbc.Col(html.Div(dcc.Graph(id="Wind_to_final",figure=figures.land_use_plot()[2]), style=figure_border_style), md=6),

                    ]),
                ],
                type="default",
            )
        ],
        style={"marginTop": 0, "marginBottom": 0},
    ),
]

RE = [
    dbc.CardHeader(html.H5("Coastline and land required for wind turbine and PV installations")),
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
                    dbc.Row([
                        dbc.Col(html.Div(dcc.Graph(id="Wind_to_final",figure=figures.land_use_plot()[1]), style=figure_border_style), md=6),
                        dbc.Col(html.Div(dcc.Graph(id="land-use", figure=figures.land_use_plot()[3]),
                                         style=figure_border_style), md=6),

                    ]),
                ],
                type="default",
            )
        ],
        style={"marginTop": 0, "marginBottom": 0},
    ),
]

Map = [
    dbc.CardHeader(html.H5("Visual representation of land requirement for PV installation")),
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
                    dbc.Row([
                        dbc.Col([generate_single_country_drpdwn(), select_map_style()], md=12),
                    ]),
                    dbc.Row([
                        dbc.Col(html.Div(dcc.Graph(id="PV-map"), style=figure_border_style), md=12),
                    ]),
                ],
                type="default",
            )
        ],
        style={"marginTop": 0, "marginBottom": 0},
    ),
]
rooftop = [
    dbc.CardHeader(html.H5("Rooftop PV potential")),
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
                    dbc.Row([
                        dbc.Col(html.Div(dcc.Graph(id="Pop-and-famil-size",figure=figures.rooftop_PV_plot(0.75,2.5)[0]), style=figure_border_style), md=6),
                        dbc.Col(html.Div(dcc.Graph(id="number-of-buildings-PV-pot",figure=figures.rooftop_PV_plot(0.75,2.5)[1]), style=figure_border_style), md=6),
                    ]),
                    html.Br(),
                    dbc.Row([
                        dbc.Col(html.Div(dcc.Graph(id="Wind_to_final",figure=figures.rooftop_PV_plot(0.75,2.5)[2]), style=figure_border_style), md=6),
                    ]),
                    html.Br(),
                ],
                type="default",
            )
        ],
        style={"marginTop": 0, "marginBottom": 0},
    ),
]


BODY = dbc.Container(

    [
        dbc.Row([dbc.Col(dbc.Card(Physical)), ], style={"marginTop": 30,
                                                  }),
        dbc.Row([dbc.Col(dbc.Card(Required_capacity)), ], style={"marginTop": 30,
                                                  }),
        dbc.Row([dbc.Col(dbc.Card(RE)),], style={"marginTop": 30,
                                                                }),
        dbc.Row([dbc.Col(dbc.Card(Map)), ], style={"marginTop": 30,
                                                  }),
        dbc.Row([dbc.Col(dbc.Card(rooftop)), ], style={"marginTop": 30,
                                                  }),
    ],
    # className="mt-12",
    fluid=True
)


content = [BODY]

