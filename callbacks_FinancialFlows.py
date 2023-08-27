from dash.dependencies import Input, Output, ALL, State, MATCH, ALLSMALLER
from app import app
import EnergyFlows
import figures
import pandas as pd
from dash import html
from dash import dcc
Country_List = ['Samoa','Nauru','Vanuatu','Palau','Kiribati','Cook Islands','Solomon Islands','Tonga','New Caledonia','French Polynesia','Micronesia','Niue','Tuvalu','PNG','Fiji']


@app.callback(
    Output('figure1', 'figure'),
    [Input("select-year", "value"),
     Input("select-country", "value"),
     Input("product_drpdwn", "value")]
)
def sensor_checklist(year,country,selected_products):

    Interest_list = ['Crude Petroleum', 'Refined Petroleum', 'Petroleum', 'Petroleum Gas', 'Coal Briquettes',
                     'Petroleum Coke', 'Fuel Wood', 'Coconut Oil', 'Ferroalloys', 'Nickel Mattes', 'Nickel Ore',
                     'Aluminium Ore', 'Non-Petroleum Gas', 'Hydrogen', 'Tug Boats', 'Fishing Ships',
                     'Non-fillet Frozen Fish',
                     'Cars', 'Busses', 'Delivery Trucks', 'Motorcycles', 'Bicycles',
                     'Combustion Engines', 'Engine Parts', 'Gas Turbines', 'Spark-Ignition Engines',
                     'Planes, Helicopters, and/or Spacecraft', 'Aircraft Parts',
                     'Passenger and Cargo Ships']


    df_exp= pd.read_csv("Data/{}/Exports-{}---Click-to-Select-a-Product.csv".format(country,year))
    df_imp = pd.read_csv("Data/{}/Imports-{}---Click-to-Select-a-Product.csv".format(country,year))
    df_imp['Trade Value'] = -df_imp['Trade Value']/1000000 #to million $
    df_exp['Trade Value'] = df_exp['Trade Value']/1000000 #to million $


    return figures.import_export_figure(df_imp,df_exp,selected_products,year)

@app.callback(
    Output('product_drpdwn', 'options'),
    [Input("select-year", "value"),
     Input("select-country", "value")]
)
def update_options(year,country):
    items = []
    df_exp= pd.read_csv("Data/{}/Exports-{}---Click-to-Select-a-Product.csv".format(country,year))
    df_imp = pd.read_csv("Data/{}/Imports-{}---Click-to-Select-a-Product.csv".format(country,year))

    for i in df_exp['HS4']:
        items.append(i)

    product_list = set(items)
    return [{"label": i, "value": i} for i in product_list]


@app.callback(
    [
        # Output('cross_country_sankey_figure', 'figure'),
    Output('Hidden-Div_trend_financial_flows', "children"),
    Output('dynamic_callback_container_financial_flows', 'children')],
    [Input('update-button-cross-country-products', 'n_clicks'),
    Input('update-button-products-clear-canvas', 'n_clicks')],
    [State("select-product-dynamic", "value"),
     State('Hidden-Div_trend_financial_flows', "children"),
    State('dynamic_callback_container_financial_flows', 'children')
     ]
)
def update_cross_country_comparison_financial(n_clicks,clear_canvas,product,hidden_div,div_children):
    selected_year = 2020
    if n_clicks != hidden_div[0]:
        import_values = []
        export_values = []
        df_cross_country = pd.DataFrame()


        for country in Country_List:
            df_exp = pd.read_csv("Data/{}/Exports-{}---Click-to-Select-a-Product.csv".format(country, selected_year))
            df_imp = pd.read_csv("Data/{}/Imports-{}---Click-to-Select-a-Product.csv".format(country, selected_year))
            df_imp['Trade Value'] = -df_imp['Trade Value']/1000000 #to million $
            df_exp['Trade Value'] = df_exp['Trade Value']/1000000 #to million $

            df_exp = df_exp[(df_exp['HS4'] == product)].reset_index()
            df_imp = df_imp[(df_imp['HS4'] == product)].reset_index()

            a_exp = df_exp['Trade Value']
            a_imp = df_imp['Trade Value']
            try:
                if len(a_exp) == 0:
                    a_exp = 0
                else:
                    a_exp = a_exp[0]

                if len(a_imp) == 0:
                    a_imp = 0
                else:
                    a_imp = a_imp[0]
            except Exception as e:
                print(e.message)
            export_values.append(a_exp)
            import_values.append(a_imp)


        df_cross_country['Country'] = Country_List
        df_cross_country['export_values'] = export_values
        df_cross_country['import_values'] = import_values
        df_cross_country = df_cross_country.sort_values('Country')
        fig = figures.import_export_figure_dynamic(df_cross_country,product,year = selected_year)

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

    elif clear_canvas != hidden_div[1]:
        div_children = []

    hidden_div = [n_clicks,clear_canvas]

    return hidden_div,div_children