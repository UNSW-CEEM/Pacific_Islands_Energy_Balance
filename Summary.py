from dash import html
from dash import dcc
import dash_bootstrap_components as dbc
import figures
import EnergyFlows
from app import app
import pandas as pd
import dash
import os
# import dash_daq as daq
from EnergyFlows import figure_border_style
from EnergyFlows import Year_List
from EnergyFlows import CONTENT_STYLE
from dash import dash_table
import plotly.figure_factory as ff

summary_df = pd.read_csv('Data/SummaryTable.csv')
table = dbc.Table.from_dataframe(summary_df, striped=False, bordered=True, hover=True,style={'color':'white','fontSize':'18'},responsive=True)
# table = dbc.Table(summary_df, striped=False, bordered=True, hover=True,style={'color':'white'},responsive=True)
# table = ff.create_table(summary_df, height_constant=1500)


dataTable = dash_table.DataTable(
    data=summary_df.to_dict('records'),
    columns=[{'id': c, 'name': c} for c in summary_df.columns],
    style_cell={'textAlign': 'left','padding': '5px',
                    'backgroundColor': 'rgb(50, 50, 50)',
                    'color': 'white'
                },
    style_as_list_view=False,
    style_header={
        'padding': '5px',
        'backgroundColor': 'rgb(30, 30, 30)',
        'fontWeight': 'bold',
        'border': '1px solid grey',
        'textAlign': 'left',
        'height': 'auto',
        'overflow': 'hidden',
        'textOverflow': 'ellipsis',
        'whiteSpace': 'normal',

    },
    style_data={ 'border': '0.15px solid white' },#ff4d4d
    # style_cell_conditional=([
    #     {'if': {'column_id': 'Population density (Person/km2)'},
    #      'width': '5%'},
    #     {'if': {'column_id': 'Youngest volcanism'},
    #      'width': '20%'},
    #     {'if': {'column_id': 'Known geothermal locations'},
    #      'width': '20%'},
    #     {'if': {'column_id': 'Geothermal investigations'},
    #      'width': '15%'},
    #     {'if': {'column_id': 'Observed hot spring temperature'},
    #      'width': '20%'},
    #     {'if': {'column_id': 'Potentials'},
    #      'width': '17.5%'}]),

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

                        dbc.Col(html.Div(dcc.Graph(id="transit_figure4", figure=figures.imports_to_GDP(2019)[0]),
                                         style=figure_border_style), md=6),
                    ]),
                    html.Br(),
                    dbc.Row([
                        dbc.Col(html.Div(dcc.Graph(id="import-per-capita", figure=figures.imports_to_GDP(2019)[1]),
                                         style=figure_border_style), md=6),
                        dbc.Col(html.Div(dcc.Graph(id="renewables-per-capita", figure=figures.UNstats_plots(2019)[8]),
                                         style=figure_border_style), md=6),
                    ]),
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
                        # dbc.Col(html.Div(dcc.Graph(id="renewable electricity", figure=figures.UNstats_plots(2019)[6]),
                        #                  style=figure_border_style), md=6),
                    ]),
                    html.Br(),
                    dbc.Row([
                        dbc.Col(html.Div(dcc.Graph(id="final-vs-non-re-demand", figure=figures.land_use_plot()[4]),
                                         style=figure_border_style), md=6),

                        dbc.Col(html.Div(dcc.Graph(id="demand-per-capita", figure=figures.land_use_plot()[5]),
                                         style=figure_border_style), md=6),
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
        dbc.Row([dbc.Col(dbc.Card(Transit)), ], style={"marginTop": 30,
                                                                }),
    ],
    # className="mt-12",
    fluid=True
)


content = [BODY]