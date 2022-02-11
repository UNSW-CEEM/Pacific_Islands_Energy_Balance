from dash.dependencies import Input, Output, ALL, State, MATCH, ALLSMALLER
from app import app
import dash_html_components as html
import numpy as np
import pandas as pd
import figures



@app.callback(
    Output('figure1', 'figure'),
    [Input("year_drpdwn_IO", "value"),
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
    df_imp['Trade Value'] = -df_imp['Trade Value']/1000000
    df_exp['Trade Value'] = df_exp['Trade Value']/1000000


    return figures.import_export_figure(df_imp,df_exp,selected_products)



@app.callback(
    Output('product_drpdwn', 'options'),
    [Input("year_drpdwn_IO", "value"),
     Input("select-country", "value")]
)
def update_options(year,country):
    items = []
    df_exp= pd.read_csv("Data/{}/Exports-{}---Click-to-Select-a-Product.csv".format(country,year))
    df_imp = pd.read_csv("Data/{}/Imports-{}---Click-to-Select-a-Product.csv".format(country,year))

    for i in df_exp['HS4']:
        items.append(i)
    for i in df_imp['HS4']:
        items.append(i)
    product_list = set(items)
    return [{"label": i, "value": i} for i in product_list]



