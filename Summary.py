from dash import html
from dash import dcc
import dash_bootstrap_components as dbc

from app import app
import pandas as pd
import dash
import os
import dash_daq as daq
from EnergyFlows import figure_border_style
import EnergyFlows
from dash import dash_table
import figures
summary_df = pd.read_csv('Data/SummaryTable.csv')
table = dbc.Table.from_dataframe(summary_df, striped=True, bordered=True, hover=True,style={'color':'red'},responsive=True)

dataTable = dash_table.DataTable(
    data=summary_df.to_dict('records'),
    columns=[{'id': c, 'name': c} for c in summary_df.columns],
    style_cell={'textAlign': 'left','padding': '5px',
                    'backgroundColor': 'rgb(50, 50, 50)',
                    'color': 'white'
                },
    style_as_list_view=False,
    style_header={
        'backgroundColor': 'rgb(30, 30, 30)',
        'fontWeight': 'bold',
        'border': '1px solid grey',
        # 'textAlign': 'left',
    },
    style_data={ 'border': '1px solid grey',        'whiteSpace': 'normal',
        'height': 'auto',},
    style_cell_conditional=[            # style_cell_c. refers to the whole table
        {
            'if': {'column_id': 'Country / Territory'},
            'textAlign': 'left'
        }
    ],

    style_table={
        'width': '100%',
        'margin': '0 0 0 0px',
        'padding': '0 0px',
        'overflowX': 'auto',
        'overflowY': 'auto',
    },
    # fixed_rows={'data': 0},
    fixed_columns={'headers': True, 'data': 0},  # 'headers': True,

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
                    dbc.Row([
                        # figures.Update_UNstats_database(20),
                        # figures.validation(),
                        dbc.Col(dataTable)
                    ]),
                    html.Br(),
                    # EnergyFlows.generate_single_year_drpdwn(),
                    # html.Br(),
                    dbc.Row([
                        dbc.Col(html.Div(dcc.Graph(id="generation_mix_GWh",figure=figures.generation_mix_plot()[0]), style=figure_border_style), md=6),
                        dbc.Col(html.Div(dcc.Graph(id="generation_mix_MW",figure=figures.generation_mix_plot()[1]), style=figure_border_style), md=6),
                    ]),
                    html.Br(),
                    dbc.Row([
                        dbc.Col(html.Div(dcc.Graph(id="final-demand", figure=figures.UNstats_plots(2019)[4]),
                                         style=figure_border_style), md=6),
                        dbc.Col(html.Div(dcc.Graph(id="transit_figure1", figure=figures.UNstats_plots(2019)[7]),
                                         style=figure_border_style), md=6),
                    ]),
                    html.Br(),
                    dbc.Row([
                        dbc.Col(html.Div(dcc.Graph(id="Oil-imports", figure=figures.UNstats_plots(2019)[3]),
                                         style=figure_border_style), md=6),

                        dbc.Col(html.Div(dcc.Graph(id="imports-to-GDP", figure=figures.imports_to_GDP(2019)[0]),
                                         style=figure_border_style), md=6),
                    ]),
                    html.Br(),
                    dbc.Row([
                        dbc.Col(html.Div(dcc.Graph(id="import-per-capita", figure=figures.imports_to_GDP(2019)[1]),
                                         style=figure_border_style), md=6),
                        dbc.Col(html.Div(dcc.Graph(id="renewables-per-capita", figure=figures.UNstats_plots(2019)[8]),
                                         style=figure_border_style), md=6),
                    ]),
                    html.Br(),

                    dbc.Row([
                        dbc.Col(html.Div(dcc.Graph(id="transit_figure3", figure=figures.UNstats_plots(2019)[2]),
                                         style=figure_border_style), md=6),

                        dbc.Col(html.Div(dcc.Graph(id="transit_figure2", figure=figures.UNstats_plots(2019)[1]),
                                         style=figure_border_style), md=6),
                    ]),
                    html.Br(),
                    dbc.Row([
                        dbc.Col(html.Div(dcc.Graph(id="final-demand", figure=figures.UNstats_plots(2019)[0]),
                                         style=figure_border_style), md=6),
                        dbc.Col(html.Div(dcc.Graph(id="total renewables", figure=figures.UNstats_plots(2019)[5]),
                                         style=figure_border_style), md=6),
                    ]),
                    html.Br(),
                    dbc.Row([
                        dbc.Col(html.Div(dcc.Graph(id="final-vs-non-re-demand", figure=figures.land_use_plot()[5]),
                                         style=figure_border_style), md=6),

                        dbc.Col(html.Div(dcc.Graph(id="demand-per-capita", figure=figures.land_use_plot()[4]),
                                         style=figure_border_style), md=6),
                    ]),
                    html.Br(),
                    dbc.Row([
                        dbc.Col(html.Div(dcc.Graph(id="demand-per-capita-world", figure=figures.per_capita_comparison()),
                                         style=figure_border_style), md=12),

                    ]),
                    html.Br(),
                    dbc.Row([
                        dbc.Col(html.Div(dcc.Graph(id="demand-per-capita-world", figure=figures.per_capita_renewables()),
                                         style=figure_border_style), md=6),
                        dbc.Col(html.Div(dcc.Graph(id="intensity-capita-world", figure=figures.per_capita_intensity()),
                                         style=figure_border_style), md=6),
                    ]),
                    html.Br(),
                    dbc.Row([
                        dbc.Col(html.Div(dcc.Graph(id="share-of-imports", figure=figures.percentage_of_imports()),
                                         style=figure_border_style), md=12),
                    ]),
                    html.Br(),
                    dbc.Row([
                        dbc.Col(html.Div(dcc.Graph(id="dependance-on-imports", figure=figures.dependance_on_imports()),
                                         style=figure_border_style), md=6),
                        dbc.Col(html.Div(dcc.Graph(id="GDP-per-capita", figure=figures.GDP_per_capita()),
                                         style=figure_border_style), md=6),
                    ]),
                    html.Br(),
                    dbc.Row([
                        dbc.Col(html.Div(dcc.Graph(id="dependance-on-imports", figure=figures.navigation_and_int_maritime()),
                                         style=figure_border_style), md=6),
                        dbc.Col(html.Div(dcc.Graph(id="lad-percentage", figure=figures.land_use_plot()[6]),
                                         style=figure_border_style), md=6),
                    ]),
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
    ],
    # className="mt-12",
    fluid=True
)


content = [EnergyFlows.generate_single_year_drpdwn(),BODY]