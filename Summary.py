from dash import html
from dash import dcc
import dash_bootstrap_components as dbc

from app import app
import pandas as pd

from EnergyFlows import figure_border_style
from dash import dash_table
import figures

summary_df = pd.read_csv("Data/SummaryTable.csv")
table = dbc.Table.from_dataframe(
    summary_df,
    striped=True,
    bordered=True,
    hover=True,
    style={"color": "red"},
    responsive=True,
)

dataTable = dash_table.DataTable(
    data=summary_df.to_dict("records"),
    columns=[{"id": c, "name": c} for c in summary_df.columns],
    style_cell={
        "textAlign": "left",
        "padding": "5px",
        "backgroundColor": "rgb(50, 50, 50)",
        "color": "white",
    },
    style_as_list_view=False,
    style_header={
        "backgroundColor": "rgb(30, 30, 30)",
        "fontWeight": "bold",
        "border": "1px solid grey",
        "whiteSpace": "normal",
    },
    style_data={
        "border": "1px solid grey",
        "whiteSpace": "normal",
        "height": "auto",
    },
    style_cell_conditional=[  # style_cell_c. refers to the whole table
        {"if": {"column_id": "Country / Territory"}, "textAlign": "left"}
    ],
    style_table={
        "width": "100%",
        "margin": "0 0 0 0px",
        "padding": "0 0px",
        "overflowX": "auto",
        "overflowY": "auto",
    },
    fixed_columns={"headers": True, "data": 0},  # 'headers': True,
)
Transit = [
    dbc.CardHeader(html.H5("Status of all countries")),
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
                    dbc.Row([dbc.Col(dataTable)]),
                    html.Br(),
                    dbc.Row(
                        [
                            dbc.Col(
                                html.Div(
                                    dcc.Graph(
                                        id="generation_mix_GWh",
                                        figure=figures.generation_mix_plot()[0],
                                    ),
                                    style=figure_border_style,
                                ),
                                lg=12,
                                md=12,
                            ),

                        ]
                    ),
                    html.Br(),
                    dbc.Row([                            dbc.Col(
                                html.Div(
                                    dcc.Graph(
                                        id="generation_mix_MW",
                                        figure=figures.generation_mix_plot()[1],
                                    ),
                                    style=figure_border_style,
                                ),
                                lg=12,
                                md=12,
                            )]),
                    html.Br(),
                    dbc.Row(
                        [
                            dbc.Col(
                                html.Div(
                                    dcc.Graph(
                                        id="final-demand",
                                        figure=figures.UNstats_plots(2020)[4],
                                    ),
                                    style=figure_border_style,
                                ),
                                lg=6,
                                md=12,
                            ),
                            dbc.Col(
                                html.Div(
                                    dcc.Graph(
                                        id="transit_figure1",
                                        figure=figures.UNstats_plots(2020)[7],
                                    ),
                                    style=figure_border_style,
                                ),
                                lg=6,
                                md=12,
                            ),
                        ]
                    ),
                    html.Br(),
                    dbc.Row(
                        [
                            dbc.Col(
                                html.Div(
                                    dcc.Graph(
                                        id="Oil-imports",
                                        figure=figures.UNstats_plots(2020)[3],
                                    ),
                                    style=figure_border_style,
                                ),
                                lg=6,
                                md=12,
                            ),
                            dbc.Col(
                                html.Div(
                                    dcc.Graph(
                                        id="imports-to-GDP",
                                        figure=figures.imports_to_GDP(2020)[0],
                                    ),
                                    style=figure_border_style,
                                ),
                                lg=6,
                                md=12,
                            ),
                        ]
                    ),
                    html.Br(),
                    dbc.Row(
                        [
                            dbc.Col(
                                html.Div(
                                    dcc.Graph(
                                        id="import-per-capita",
                                        figure=figures.imports_to_GDP(2020)[1],
                                    ),
                                    style=figure_border_style,
                                ),
                                lg=6,
                                md=12,
                            ),
                            dbc.Col(
                                html.Div(
                                    dcc.Graph(
                                        id="renewables-per-capita",
                                        figure=figures.UNstats_plots(2020)[8],
                                    ),
                                    style=figure_border_style,
                                ),
                                lg=6,
                                md=12,
                            ),
                        ]
                    ),
                    html.Br(),
                    dbc.Row(
                        [
                            dbc.Col(
                                html.Div(
                                    dcc.Graph(
                                        id="transit_figure3",
                                        figure=figures.UNstats_plots(2020)[2],
                                    ),
                                    style=figure_border_style,
                                ),
                                lg=12,
                                md=12,
                            ),
                        ]
                    ),
                    html.Br(),
                    dbc.Row([dbc.Col(
                                html.Div(
                                    dcc.Graph(
                                        id="transit_figure2",
                                        figure=figures.UNstats_plots(2020)[1],
                                    ),
                                    style=figure_border_style,
                                ),
                                lg=12,
                                md=12,
                            ),]),
                    html.Br(),
                    dbc.Row(
                        [
                            dbc.Col(
                                html.Div(
                                    dcc.Graph(
                                        id="final-demand",
                                        figure=figures.UNstats_plots(2020)[0],
                                    ),
                                    style=figure_border_style,
                                ),
                                lg=6,
                                md=12,
                            ),
                            dbc.Col(
                                html.Div(
                                    dcc.Graph(
                                        id="total renewables",
                                        figure=figures.UNstats_plots(2020)[5],
                                    ),
                                    style=figure_border_style,
                                ),
                                lg=6,
                                md=12,
                            ),
                        ]
                    ),
                    html.Br(),
                    dbc.Row(
                        [
                            dbc.Col(
                                html.Div(
                                    dcc.Graph(
                                        id="final-vs-non-re-demand",
                                        figure=figures.land_use_plot()[5],
                                    ),
                                    style=figure_border_style,
                                ),
                                lg=6,
                                md=12,
                            ),
                            dbc.Col(
                                html.Div(
                                    dcc.Graph(
                                        id="demand-per-capita",
                                        figure=figures.land_use_plot()[4],
                                    ),
                                    style=figure_border_style,
                                ),
                                lg=6,
                                md=12,
                            ),
                        ]
                    ),
                    html.Br(),
                    dbc.Row(
                        [
                            dbc.Col(
                                html.Div(
                                    dcc.Graph(
                                        id="demand-per-capita-world",
                                        figure=figures.per_capita_renewables(),
                                    ),
                                    style=figure_border_style,
                                ),
                                lg=6,
                                md=12,
                            ),
                            dbc.Col(
                                html.Div(
                                    dcc.Graph(
                                        id="intensity-capita-world",
                                        figure=figures.per_capita_intensity(),
                                    ),
                                    style=figure_border_style,
                                ),
                                lg=6,
                                md=12,
                            ),
                        ]
                    ),
                    html.Br(),
                    dbc.Row(
                        [
                            dbc.Col(
                                html.Div(
                                    dcc.Graph(
                                        id="dependance-on-imports",
                                        figure=figures.dependance_on_imports(),
                                    ),
                                    style=figure_border_style,
                                ),
                                lg=6,
                                md=12,
                            ),
                            dbc.Col(
                                html.Div(
                                    dcc.Graph(
                                        id="GDP-per-capita",
                                        figure=figures.GDP_per_capita(),
                                    ),
                                    style=figure_border_style,
                                ),
                                lg=6,
                                md=12,
                            ),
                        ]
                    ),
                    dbc.Row(
                        [
                            dbc.Col(
                                html.Div(
                                    dcc.Graph(
                                        id="three-demand-scenarios",
                                        figure=figures.land_use_plot()[6],
                                    ),
                                    style=figure_border_style,
                                ),
                                lg=6,
                                md=12,
                            ),
                        ]
                    ),
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
        dbc.Row(
            [
                dbc.Col(dbc.Card(Transit)),
            ],
            style={
                "marginTop": 30,
            },
        ),
    ],
    # className="mt-12",
    fluid=True,
)


# content = [EnergyFlows.generate_single_year_drpdwn(),BODY]
content = [BODY]
