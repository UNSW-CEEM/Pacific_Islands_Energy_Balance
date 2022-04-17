from dash import html
from dash import dcc
import dash_bootstrap_components as dbc
import pandas as pd
from dash import dash_table

import figures
from page1FarmView import figure_border_style


geothermal_df = pd.read_csv('Data/Geothermal.csv')

table = dbc.Table.from_dataframe(geothermal_df, striped=False, bordered=True, hover=True,style={'color':'white','fontSize':'18'},responsive=True)

dataTable = dash_table.DataTable(
    data=geothermal_df.to_dict('records'),
    # sort_action='native',
    style_header={
        'backgroundColor': 'rgb(30, 30, 30)',
        'fontWeight': 'bold',
        'marginLeft': 0,
        'textAlign': 'left',
        'font-family':'Calibri'
    },
    style_cell={
        'backgroundColor': 'rgb(50, 50, 50)',
        'color': 'white',
        'textAlign': 'center','fontSize':18, 'font-family':'Calibri',
    },

    fixed_rows={'headers': True, 'data': 0},
    page_action='none',
    style_table={'height': '2000px','overflowY': 'auto'},
    columns=[{'name': i, 'id': i} for i in geothermal_df.columns],
    editable=False,
    # page_size=20,
    # style_data_conditional=[
    #     {
    #         'if': {'row_index': 'odd'},
    #         'backgroundColor': 'rgb(40, 60, 50)'
    #     }
    # ],
    style_cell_conditional=([
        {'if': {'column_id': 'Country'},
         'width': '10%'},
        {'if': {'column_id': 'Youngest volcanism'},
         'width': '20%'},
        {'if': {'column_id': 'Known geothermal locations'},
         'width': '20%'},
        {'if': {'column_id': 'Geothermal investigations'},
         'width': '15%'},
        {'if': {'column_id': 'Observed hot spring temperature'},
         'width': '20%'},
        {'if': {'column_id': 'Potentials'},
         'width': '17.5%'}]),

    style_data_conditional=[
        {
            'if': {
                'filter_query': '{Potentials} = High',
                'column_id': ['Potentials','Observed hot spring temperature','Geothermal investigations','Known geothermal locations',
                              'Youngest volcanism','Country']
            },
            # 'color': 'tomato',
            'backgroundColor': 'red',

            'fontWeight': 'bold',
            'color': 'black',

        },
        {
            'if': {
                'filter_query': '{Potentials} = Moderate-to-High',
                'column_id': ['Potentials','Observed hot spring temperature','Geothermal investigations','Known geothermal locations',
                              'Youngest volcanism','Country']
            },
            # 'textDecoration': 'underline',
            'backgroundColor': '#FE4C40',
            'color': 'black',

        },

        {
            'if': {
                'filter_query': '{Potentials} = Moderate',
                'column_id': ['Potentials','Observed hot spring temperature','Geothermal investigations','Known geothermal locations',
                              'Youngest volcanism','Country']
            },
            # 'textDecoration': 'underline',
            'backgroundColor': 'tomato',
            'color': 'black',

        },
        {
            'if': {
                'filter_query': '{Potentials} = Low-to-Moderate',
                'column_id': ['Potentials','Observed hot spring temperature','Geothermal investigations','Known geothermal locations',
                              'Youngest volcanism','Country']
            },
            # 'textDecoration': 'underline',
            'backgroundColor': '#FFAE42',
            'color': 'black',

        },
        {
            'if': {
                'filter_query': '{Potentials} = Low',
                'column_id': ['Potentials','Observed hot spring temperature','Geothermal investigations','Known geothermal locations',
                              'Youngest volcanism','Country']
            },
            # 'textDecoration': 'underline',
            'backgroundColor': '#F1E788',
            'color': 'black',

        },

        {
            'if': {
                'filter_query': '{Potentials} = Extremely-Low',
                'column_id': ['Potentials','Observed hot spring temperature','Geothermal investigations','Known geothermal locations',
                              'Youngest volcanism','Country']
            },
            # 'textDecoration': 'underline',
            'backgroundColor': '#FFFF9F',
            'color': 'black',

        },
    ]



)




RE = [
    dbc.CardHeader(html.H5("Summary of wind and solar potentials")),
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
                        dbc.Col(html.Div(dcc.Graph(id="Wind_to_final",figure=figures.land_use_plot()[1]), style=figure_border_style), md=6),
                    ]),
                    html.Br(),
                    dbc.Row([
                        dbc.Col(html.Div(dcc.Graph(id="Wind_to_final",figure=figures.land_use_plot()[2]), style=figure_border_style), md=6),

                        dbc.Col(html.Div(dcc.Graph(id="land-use",figure=figures.land_use_plot()[3]), style=figure_border_style), md=6),
                    ]),

                    html.Br(),

                    # html.Br(),
                    # dbc.Row([
                    #     dbc.Col(html.Div(dcc.Graph(id="transit_figure1"),style=figure_border_style),md=6),
                    #     dbc.Col(html.Div(dcc.Graph(id="transit_figure2"), style=figure_border_style), md=6),
                    #
                    # ]),
                    # html.Br(),
                    # dbc.Row([
                    #     dbc.Col(html.Div(dcc.Graph(id="transit_figure3"), style=figure_border_style), md=6),
                    #     dbc.Col(html.Div(dcc.Graph(id="transit_figure4"), style=figure_border_style), md=6),
                    # ]),

                ],
                type="default",
            )
        ],
        style={"marginTop": 0, "marginBottom": 0},
    ),
]


geo = [
    dbc.CardHeader(html.H5("Geothermal Potential")),
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


                    dbc.Row([
                        dbc.Col(dataTable)
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

        dbc.Row([dbc.Col(dbc.Card(RE)),], style={"marginTop": 30,
                                                                }),
        dbc.Row([dbc.Col(dbc.Card(geo)), ], style={"marginTop": 30,
                                                  }),
    ],
    # className="mt-12",
    fluid=True
)


content = [BODY]

