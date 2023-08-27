from dash.dependencies import Input, Output, ALL, State, MATCH, ALLSMALLER
from app import app
import EnergyFlows
import figures
import pandas as pd
from dash import html
from dash import dcc
Country_List = ['Samoa','Nauru','Vanuatu','Palau','Kiribati','Cook Islands','Solomon Islands','Tonga','New Caledonia','French Polynesia','Micronesia','Niue','Tuvalu','PNG','Fiji']

@app.callback(
    [Output('Sankey_figure', 'figure'),
     Output('Sankey_elec_figure', 'figure')],
     [Input("select-year", "value"),
     Input("select-country", "value"),
]
)
def sensor_checklist(year,country):
    return figures.Generate_Sankey(year,country)[0],figures.Generate_Sankey(year,country)[1]


@app.callback(
    [Output('select-to', 'options'),
     Output('select-to', 'value')
     ],
    Input("select-from", "value"),

)
def update_options3(from_):
    items = []
    df = pd.read_csv("Data/Sankey/csv/{}/{}.csv".format(2019, 'PNG'))
    df = df[df[' (from)'] == from_]

    for i in df[' (to)']:
        items.append(i)

    product_list = set(items)
    options = [{"label": i, "value": i} for i in product_list]
    return options,options[0]['label']




@app.callback(
    [
    Output('Hidden-Div_trend', "children"),
    Output('dynamic_callback_container', 'children')],
    [Input('update-button-cross-country-figure', 'n_clicks'),
    Input('update-button-sankey-clear-canvas', 'n_clicks')],
    [State("select-from", "value"),
    State("select-to", "value"),
    State("radio-normalization-sankey", "value"),
    State("export-df-sankey-cross-country", "value"),
    State('Hidden-Div_trend', "children"),
    State('dynamic_callback_container', 'children')
     ]
)
def update_cross_country_comparison(n_clicks,clear_canvas,from_,to_,normalization,export_df,hidden_div,div_children):
    import re
    if n_clicks != hidden_div[0]:
        values = []
        normalized_values = []
        df_cross_country = pd.DataFrame()
        for country in Country_List:
            df1 = pd.read_csv("Data/Sankey/csv/{}/{}.csv".format(2019, country))
            df = df1[(df1[' (from)'] == from_)&(df1[' (to)']==to_)].reset_index()
            a = df[' (weight)']
            if normalization == ' (from)':
                denominator_df = df1[df1[normalization]==from_]
                denominator = denominator_df[' (weight)'].sum()
            elif normalization == ' (to)':
                denominator_df = df1[df1[normalization]==to_]
                denominator = denominator_df[' (weight)'].sum()
            elif normalization == 1:
                denominator = 1

            if len(a) == 0:
                a = 0
            else:
                a=a[0]
            if denominator == 0:
               normalized_value = 0
            elif denominator > 0:
                normalized_value = 100*a/denominator
            normalized_values.append(round(normalized_value,1))
            values.append(a)

        df_cross_country['Country'] = Country_List

        df_cross_country['Values'] = values
        if normalization != 1:
            df_cross_country['Values'] = normalized_values

        fig = figures.cross_country_sankey(df_cross_country,from_,to_,normalization)
        new_child = html.Div(
            style={'display': 'inline-block', 'outline': 'thin lightgrey solid', 'padding': 10},
            children=[
                dcc.Graph(
                    id={
                        'type': 'dynamic-graph',
                        'index': n_clicks
                    },
                    figure=fig,
                ),
            ]
        )
        div_children.append(new_child)
        if export_df !=[]:
            # from_ = re.sub("\s\s+" , " ", from_)
            # to_ = re.sub("\s\s+" , " ", to_)
            # df_cross_country.to_csv("Results/cross_country/cross_country_sankey.csv".format(from_.replace(" ", "_"),
            #                                                                                           to_.replace(" ", "_"),
            #                                                                                           str(normalization).replace(" ", "_")))
            pass # This is disabled for the online version. This feature is used for generating reports


    elif clear_canvas != hidden_div[1]:
        div_children = []

    hidden_div = [n_clicks,clear_canvas]

    return hidden_div,div_children



# relative comparison of different rows
@app.callback(
    [
    Output('Hidden_Div_breakdown', "children"),
    Output('dynamic_callback_container_energy_breakdown', 'children')],
    [Input('update-button-cross-country-flow', 'n_clicks'),
    Input('update-button-flow-clear', 'n_clicks')],
    [State("select-flow-provider", "value"),
     State("select-flow-cunsumer", "value"),
     State("select-flow-provider-source", "value"),
     State("destination-carrier", "value"),
    State('Hidden_Div_breakdown', "children"),
    State('dynamic_callback_container_energy_breakdown', 'children'),
     State("y_axis_title","value")
     ]
)
def update_cross_country_comparison(n_clicks,clear_canvas,from_,consumer_list,carrier,carrier_destination,hidden_div,div_children,y_axis_title):
    if n_clicks != hidden_div[0]:
        fig = figures.dynamic_breakdown_figure_generation(y_axis_title=y_axis_title,from_=from_,list_of_consumers=consumer_list,carrier=carrier,destination_carrier=carrier_destination)
        new_child = html.Div(
            style={ 'outline': 'thin lightgrey solid', 'padding': 5,'marginLeft': 10, 'marginRight': 10,},#'display': 'inline-block',
            children=[
                dcc.Graph(
                    id={
                        'type': 'dynamic-graph',
                        'index': n_clicks
                    },
                    figure=fig,
                ),
            ]
        )
        div_children.append(new_child)
        if figures.mode == 'report':
            fig.write_image("Results/high_res_figs/from{}_to_{}.png".format(from_,consumer_list[0]), scale=7,width=1500)



    elif clear_canvas != hidden_div[1]:
        div_children = []

    hidden_div = [n_clicks,clear_canvas]

    return hidden_div,div_children




# Breakdown of one row
@app.callback(
    [
    Output('Hidden_Div_breakdown_by_source', "children"),
    Output('dynamic_callback_container_energy_breakdown_by_source', 'children')],
    [Input('update-button-sector-breakdown', 'n_clicks'),
    Input('update-button-sector-breakdown-clear', 'n_clicks')],
    [State("select-row-for-breakdown", "value"),
    State('Hidden_Div_breakdown_by_source', "children"),
    State('dynamic_callback_container_energy_breakdown_by_source', 'children'),
     ]
)
def update_cross_country_comparison(n_clicks,clear_canvas,row,hidden_div,div_children):

    if n_clicks != hidden_div[0]:

        fig = figures.dynamic_breakdown_of_one_row(row=row)
        new_child = html.Div(
            style={ 'outline': 'thin lightgrey solid', 'padding': 5,'marginLeft': 10, 'marginRight': 10,},#'display': 'inline-block',
            children=[
                dcc.Graph(
                    id={
                        'type': 'dynamic-graph',
                        'index': n_clicks
                    },
                    figure=fig,
                ),
            ]
        )
        div_children.append(new_child)

    elif clear_canvas != hidden_div[1]:
        div_children = []

    hidden_div = [n_clicks,clear_canvas]

    return hidden_div,div_children

@app.callback(
    [
    Output('Hidden-Div_dynamic_column', "children"),
    Output('dynamic_callback_container_dynamic_column', 'children')],
    [Input('update-button-dynamic-column', 'n_clicks'),
    Input('update-button-dynamic-column-clear', 'n_clicks')],
    [State("select-rows-for-column-comparison", "value"),
    State("select-dynamic-column", "value"),
    State("y_axis_title_dynamic_column", "value"),
    State('Hidden-Div_dynamic_column', "children"),
    State('dynamic_callback_container_dynamic_column', 'children'),
     ]
)
def update_dynamic_column(n_clicks,clear_canvas,provider,column,y_axis_title,hidden_div,div_children):
    if n_clicks != hidden_div[0]:
        fig = figures.dynamic_one_column_multiple_source(provider=provider,column=column,y_axis_title=y_axis_title)
        new_child = html.Div(
            style={ 'outline': 'thin lightgrey solid', 'padding': 5,'marginLeft': 10, 'marginRight': 10,},#'display': 'inline-block',
            children=[
                dcc.Graph(
                    id={
                        'type': 'dynamic-graph',
                        'index': n_clicks
                    },
                    figure=fig,
                ),
            ]
        )
        div_children.append(new_child)

    elif clear_canvas != hidden_div[1]:
        div_children = []

    hidden_div = [n_clicks,clear_canvas]

    return hidden_div,div_children

