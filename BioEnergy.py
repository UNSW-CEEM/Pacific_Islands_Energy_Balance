from dash import html
from dash import dcc
import dash_bootstrap_components as dbc
import pandas as pd
from dash import dash_table


# bioEnergy_df = pd.read_csv('Data/Bioenergy quantification.csv',encoding = 'unicode_escape')
bioEnergy_df = pd.read_excel('Data/Bioenergy quantification.xlsx')

bio_table = dash_table.DataTable(
    data=bioEnergy_df.to_dict('records'),
    # sort_action='native',
    style_header={
        'backgroundColor': 'rgb(30, 30, 30)',
        'fontWeight': 'bold',
        'marginLeft': 0,
        'textAlign': 'center',
        'font-family':'Calibri'
    },
    style_cell={
        'backgroundColor': 'rgb(50, 50, 50)',
        'color': 'white',
        'textAlign': 'left','fontSize':18, 'font-family':'Calibri',
        'height': 'auto',
        'overflow': 'hidden',
        'textOverflow': 'ellipsis',
    },
    style_data={
        # 'whiteSpace': 'normal'
                'whiteSpace': 'pre-line'},
    css=[{
        'selector': '.dash-cell div.dash-cell-value',
        'rule': 'display: inline; white-space: inherit; overflow: inherit; text-overflow: inherit;'
    }],
    virtualization=False,
    page_action='none',
    columns=[{'name': i, 'id': i} for i in bioEnergy_df.columns],
    editable=False,
    # page_size=20,

    style_cell_conditional=([
        {'if': {'column_id': 'Country'},
         'width': '6%'},
        {'if': {'column_id': 'Bioenergy potential'},
         'width': '11%'},
        {'if': {'column_id': 'Experience with bioenergy'},
         'width': '41.5%'},
        {'if': {'column_id': 'Bioenergy potential'},
         'width': '41.5%'},
        ]),

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


bio = [
    dbc.CardHeader(html.H5("Bioenergy Potential")),
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

                    html.Label([html.A('Overview of the bioenergy potential in all pacific island countries')]),
                    dbc.Row([
                        dbc.Col(bio_table)
                    ]),
                    html.Label(['', html.A(
                        'Source: Country Profiles, IRENA',
                        href='https://www.irena.org/Statistics/Statistical-Profiles')]),
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

        dbc.Row([dbc.Col(dbc.Card(bio)),], style={"marginTop": 30,
                                                                }),
    ],
    # className="mt-12",
    fluid=True
)


content = [BODY]
