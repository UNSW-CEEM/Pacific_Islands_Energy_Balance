from dash.dependencies import Input, Output, ALL, State, MATCH, ALLSMALLER
from app import app
from dash import html
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


    return figures.import_export_figure(df_imp,df_exp,selected_products,year)



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



@app.callback(
    Output('Sankey_figure', 'figure'),
    [Input("year_drpdwn_Sankey", "value"),
     Input("select-country", "value"),
]
)
def sensor_checklist(year,country):
    return figures.Generate_Sankey(year,country)


@app.callback(
    [Output('generation-cost', 'value'),
     Output('power-generated', 'value'),
     Output('lost-cost', 'value'),
     Output('generation-efficiency', 'value'),
     Output('required_RE', 'figure'),
     Output('oil_to_RE', 'figure')],
    [Input("year_drpdwn_gauge", "value"),
     Input("select-country", "value"),
    Input("diesel_price_slider", "value"),
     Input("PV-cost", "value"),
     Input("PV-battery-cost", "value"),
]
)
def sensor_checklist(year,country,diesel_price,PV_cost,PVBatt_cost):
    diesel_HHV = 3.74/1000000
    df = pd.read_csv("Data/Sankey/csv/{}/{}.csv".format(year,country))

    oil_supplied_TJ = df[(df[' (from)'] == 'Oil: Supplied') & (df[' (to)'] == 'PowerStations')][' (weight)'] # Tj- Modifty the units

    oil_supplied_litre = oil_supplied_TJ/diesel_HHV
    oil_supplied_cost = int(oil_supplied_litre * diesel_price/1000000)#$MM

    power_generated_TJ = df[(df[' (from)'] == 'PowerStations') & (df[' (to)'] == 'Electricity & Heat: Supplied')][' (weight)'] #TJ
    power_generated_GWh = int(power_generated_TJ * 0.2777)
    power_stations_input_TJ = df[df[' (to)'] == 'PowerStations'][' (weight)'].sum()
    Efficiency = int(100*(power_generated_TJ/power_stations_input_TJ))

    transformation_losses_cost = int(oil_supplied_cost * Efficiency/100)
    #44 MJ/kg
    # 0.85 kg/l
    #37.4e-6 TJ/l

    df_p = pd.read_excel('Data/Potentials.xlsx')
    print(df_p.loc[2, country],power_generated_GWh)
    Wind_pot = df_p.loc[2, country] #GWh/MW/year
    PV_pot = df_p.loc[0, country] #GWh/MW/year

    PV_decarb_MW = 1.2 * power_generated_GWh/ PV_pot
    wind_decarb_MW = 1.2 * power_generated_GWh / Wind_pot

    PV_install_with_oil = (oil_supplied_cost * 1000000/PV_cost)/1000000
    PV_bat_install_with_oil = (oil_supplied_cost * 1000000/PVBatt_cost)/1000000


    x = max(PV_decarb_MW,wind_decarb_MW,PV_install_with_oil,PV_bat_install_with_oil)
    return [oil_supplied_cost,power_generated_GWh,transformation_losses_cost,Efficiency,figures.potentials_bar(wind_decarb_MW,PV_decarb_MW,x),
            figures.oil_to_RE(PV_install_with_oil,PV_bat_install_with_oil,x)]