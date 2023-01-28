from dash import html
from dash import dcc
import dash_bootstrap_components as dbc
import pandas as pd
from dash import dash_table


geothermal_df = pd.read_csv('Data/Geothermal.csv')

dataTable = dash_table.DataTable(
    data=geothermal_df.to_dict('records'),
    style_header={
        'backgroundColor': 'rgba(0, 0, 0,0)',
        'fontWeight': 'bold',
        'border': '1px solid grey',
        'textAlign': 'left',
        'whiteSpace': 'normal',
    },
    style_data={'border': '1px solid grey', 'whiteSpace': 'normal',
                'height': 'auto',         'textAlign': 'left',
},
    style_as_list_view=False,
    virtualization=False,
    page_action="none",
    css=[
        {
            "selector": ".dash-cell div.dash-cell-value",
            "rule": "display: inline; white-space: inherit; overflow: inherit; text-overflow: inherit;",
        }
    ],
    style_cell_conditional=[  # style_cell_c. refers to the whole table
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
    fixed_columns={'headers': True, 'data': 0},

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
            'backgroundColor': 'tomato',
            'color': 'black',

        },
        {
            'if': {
                'filter_query': '{Potentials} = Low-to-Moderate',
                'column_id': ['Potentials','Observed hot spring temperature','Geothermal investigations','Known geothermal locations',
                              'Youngest volcanism','Country']
            },
            'backgroundColor': '#FFAE42',
            'color': 'black',

        },
        {
            'if': {
                'filter_query': '{Potentials} = Low',
                'column_id': ['Potentials','Observed hot spring temperature','Geothermal investigations','Known geothermal locations',
                              'Youngest volcanism','Country']
            },
            'backgroundColor': '#F1E788',
            'color': 'black',

        },

        {
            'if': {
                'filter_query': '{Potentials} = Extremely-Low',
                'column_id': ['Potentials','Observed hot spring temperature','Geothermal investigations','Known geothermal locations',
                              'Youngest volcanism','Country']
            },
            'backgroundColor': '#FFFF9F',
            'color': 'black',

        },
    ]



)

high_pot_df = pd.read_csv('Data/Geothermal_high_potentials.csv',encoding='cp1252')
Table_high_pot = dash_table.DataTable(
    data=high_pot_df.to_dict('records'),
    style_header={
        'backgroundColor': 'rgba(0, 0, 0,0)',
        'fontWeight': 'bold',
        'border': '1px solid grey',
        'textAlign': 'left',
        "font-family": "Calibri",

    },
    style_data={'border': '1px solid grey', 'whiteSpace': 'normal',
                'height': 'auto', 'textAlign': 'left',
                'backgroundColor': 'rgba(0, 0, 0,0)',

                },
    style_as_list_view=False,
    virtualization=False,
    page_action="none",
    editable=False,
    style_cell_conditional=[  # style_cell_c. refers to the whole table
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
    },)



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

                    html.Label([html.A('Overview of the geothermal potential in all pacific island countries, sorted from high to low')]),
                    dbc.Row([
                        dbc.Col(dataTable)
                    ]),
                    html.Label(['', html.A(
                        'Source: 2011, McCoy et al., GEOTHERMAL RESOURCES IN THE PACIFIC ISLANDS:THE POTENTIAL OF POWER GENERATION TO BENEFIT INDIGENOUS COMMUNITIES',
                        href='https://www.researchgate.net/profile/Michael-Petterson/publication/322568615_Geothermal_Energy_prospects_in_Selected_Pacific_Island_Countries_and_Territories/links/5a6018ef458515b4377b8d38/Geothermal-Energy-prospects-in-Selected-Pacific-Island-Countries-and-Territories.pdf?_sg%5B0%5D=qlcAJYqCdX4n-Tbf96cHYPV55iexCiJynRkzNAT4kwnj6F7kJkhmpIycPik8UR6hoWJ-5C8YQZDX_MeHvthUKA.dtJ1AXphNuV5q__fbWpN20lKArc2jZQIoEtIbirF68OJcOwt-aZYO6lycEmbNfJCuzNhdb7wm9GIxr6ye-bQfw&_sg%5B1%5D=chEPfQMwWWAcnxdn97WrOqLEtMhVaGSmnN_qpaWFZ95ivR_C8Bf1Gm_q3I_KY0s2wDDULD6SpL6I3K_3VdD0j69J9AyHXUxBgYsmzq_8rbZi.dtJ1AXphNuV5q__fbWpN20lKArc2jZQIoEtIbirF68OJcOwt-aZYO6lycEmbNfJCuzNhdb7wm9GIxr6ye-bQfw&_iepl=')]),
                    html.Br(),
                    html.Br(),

                    html.Label([html.A('Quantified potential in countries with high geothermal potential')]),
                    dbc.Row([
                        dbc.Col(Table_high_pot)
                    ]),
                    html.Label(['Source for ', html.A(
                        'PNG',
                        href='https://prdrse4all.spc.int/system/files/geothermal_potential.pdf')]),
                    html.Label([', ', html.A(
                        'Fiji',
                        href='https://www.irena.org/-/media/Files/IRENA/Agency/Publication/2015/IRENA_RRA_Fiji_2015.pdf')]),
                    html.Label([', ', html.A(
                        'Vanuatu',
                        href='https://prdrse4all.spc.int/system/files/vanuatu_geothermal_inception_report_final.pdf')]),
                    html.Label([', ', html.A(
                        'Solomon Islands',
                        href='https://reneweconomy.com.au/solomon-islands-could-go-near-100-renewable-with-geothermal-25317/')]),
                ],
                type="default",
            )
        ],
        style={"marginTop": 0, "marginBottom": 0},
    ),
]


BODY = dbc.Container(

    [
        dbc.Row([dbc.Col(dbc.Card(geo)), ], style={"marginTop": 30,
                                                 }),
    ],
    fluid=True
)


content = [BODY]