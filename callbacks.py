from dash.dependencies import Input, Output, ALL, State, MATCH, ALLSMALLER
from app import app
from dash import html
import numpy as np
import pandas as pd
import figures
import Summary
import EnergyFlows
import Decarbonization
import Geothermal
import FinancialFlows
import BioEnergy
Country_List = ['Samoa','Nauru','Vanuatu','Palau','Kiribati','Cook Islands','Solomon Islands','Tonga','New Caledonia','French Polynesia','Micronesia','Niue','Tuvalu','PNG','Fiji']

@app.callback(
    Output('Visible-content', 'children'),
    Input("tabs", "active_tab")
)
def switch_tab(tab):
    if tab == 'summary-tab':
        return Summary.content
    elif tab == 'energy-flows-tab':
        return EnergyFlows.content
    elif tab == 'decrb-tab':
        return Decarbonization.content
    elif tab == 'geothermal-tab':
        return Geothermal.content
    elif tab == 'financial-flows-tab':
        return FinancialFlows.content
    elif tab == 'bioenergy-tab':
        return BioEnergy.content

@app.callback(
    [Output('transit_figure1', 'figure'),
     Output('transit_figure2', 'figure'),
     Output('transit_figure3', 'figure'),
     Output('transit_figure4', 'figure'),
     Output('generation_mix_GWh', 'figure'),
     Output('generation_mix_MW', 'figure')],
    [Input("select-year", "value")]
)
def update_options(year):
    # figures.Update_UNstats_database(year)
    # figures.validation()
    return figures.UNstats_plots(year)[0],figures.UNstats_plots(year)[1],figures.UNstats_plots(year)[2],\
            figures.imports_to_GDP(year),\
           figures.generation_mix_plot()[0],figures.generation_mix_plot()[1]















@app.callback(
    [Output('generation-cost', 'children'),
     Output('power-generated', 'children'),
     Output('lost-cost', 'children'),
     Output('generation-efficiency', 'children'),
     Output('annual_demand', 'figure'),
     Output('scenarios-plot', 'figure'),
     Output('scenarios-plot-cum', 'figure'),
     Output('scenarios-annaul-RE', 'figure'),
     Output('scenarios-annual-carbon', 'figure'),
     Output('scenarios-annaul-diesel', 'figure'),
     Output('emission-quantity', 'children'),
     Output('emission-cost', 'children'),
     # Output('rooftop-MW', 'children'),
     # Output('rooftop-GWh', 'children')
     ],
    Input('update-button','n_clicks'),
    [State("select-year", "value"),
     State("select-country", "value"),
    State("diesel_price_slider", "value"),
     State("PV-cost", "value"),
     State("PV-battery-cost", "value"),
    State("wind-battery-cost", "value"),
     State("wind-large-cost", "value"),
     State("demand-growth", "value"),
    State('decarb-year', "value"),
     State('rooftop-size', "value"),
    State('emissions-rate', "value"),
     State('carbon-price', "value"),
     State('Wind_PV_share', "value"),
     State('small-PV-share', "value"),
     State('small-wind-share', "value"),
    State('switches-geothermal', "value"),
     State('geothermal-completion', "value"),
     State('geothermal-MW', "value"),
     State('geothermal-CF', "value"),
     State('geothermal-cost', "value"),
     State('discount-rate', "value"),
     State('inflation-rate', "value"),
     State('ComBattery-MWh', "value"),
     State('ComBattery-cost', "value"),
     State('ComBattery-installationYear', "value"),
     State('switches-communityBattery', "value"),

     ])
def sensor_checklist(n_clicks,year,country,diesel_price,PV_cost,PVBatt_cost,WindBatt_cost,Wind_cost,demand_growth,decarb_year,rooftop_size,
                     emission_tonneperMWh, emission_dollarpertonne,
                     wind_share, small_PV_share,small_wind_share,
                     geothermal_switch,geothermal_completion_year,geothermal_MW,geothermal_CF,geothermal_CAPEX,
                     discount_rate,inflation_rate,
                     CommBattery_size,CommBatery_cost,CommBattery_year,switch_battery):
    if n_clicks:
        diesel_HHV = 3.74/1000000
        df = pd.read_csv("Data/Sankey/csv/{}/{}.csv".format(year,country))

        oil_supplied_TJ = df[(df[' (from)'] == 'Oil: Supplied') & (df[' (to)'] == 'PowerStations')][' (weight)'] # Tj- Modifty the units
        Natural_gas_supplied = df[(df[' (from)'] == 'Natural Gas: Supplied') & (df[' (to)'] == 'PowerStations')][' (weight)'] # Tj- Modifty the units
        #Method1
        # oil_supplied_litre = oil_supplied_TJ/diesel_HHV
        # oil_supplied_cost = int(oil_supplied_litre * diesel_price/1000000)#$MM


        power_generated_TJ = df[(df[' (from)'] == 'PowerStations') & (df[' (to)'] == 'Electricity & Heat: Supplied')][' (weight)'] #TJ
        power_generated_GWh = float(power_generated_TJ * 0.2777)
        #Method 2
        oil_supplied_litre = power_generated_GWh * 1000000/2.5 # Litre refined oil for power generation
        oil_supplied_cost = oil_supplied_litre * diesel_price/1000000 #$MM


        power_stations_input_TJ = df[df[' (to)'] == 'PowerStations'][' (weight)'].sum()
        Efficiency = round(float(100*(power_generated_TJ/power_stations_input_TJ)),1)



        oil_import_TJ = df[df[' (from)'] == 'Oil Products: Imports'][' (weight)'].values[0] # Tj-
        oil_import_litre = oil_import_TJ/diesel_HHV
        oil_import_mlitre = oil_import_litre/1000000

        oil_export_TJ = df[(df[' (from)'] == 'Oil: Supplied') & (df[' (to)'] == 'Exports: Secondary')][' (weight)'] # Tj- Modifty the units
        oil_export_litre = oil_export_TJ/diesel_HHV
        oil_export_mlitre= oil_export_litre/1000000
        if len(oil_export_mlitre)>0:
            net_oil_product_import_ml = oil_import_mlitre - oil_export_mlitre
            net_oil_product_import_ml = net_oil_product_import_ml.values[0]
        else:
            net_oil_product_import_ml = oil_import_mlitre



        transformation_losses_cost = int(oil_supplied_cost * (1-Efficiency/100))
        #44 MJ/kg
        # 0.85 kg/l
        #37.4e-6 TJ/l

        df_p = pd.read_excel('Data/Potentials.xlsx')
        # print(df_p.loc[2, country],power_generated_GWh)
        Wind_pot = df_p.loc[2, country] #GWh/MW/year
        PV_pot = df_p.loc[0, country] #GWh/MW/year


        #Emissions
        emissions_mtonne = power_generated_GWh * emission_tonneperMWh/1000

        emission_cost_mdollar = float(emission_dollarpertonne * emissions_mtonne)
        emissions_mtonne = round(emissions_mtonne, 3)
        emission_cost_mdollar = round(emission_cost_mdollar, 2)
        oil_supplied_cost = round(oil_supplied_cost,1)
        power_generated_GWh = round(power_generated_GWh,1)
        fig_lists = figures.decarbonization_scenarios(Efficiency/100,net_oil_product_import_ml,power_generated_GWh, demand_growth, PV_cost, PVBatt_cost,
                                                  WindBatt_cost, Wind_cost, decarb_year, wind_share, small_PV_share,
                                                  small_wind_share, PV_pot, Wind_pot, diesel_HHV, diesel_price,
                                                  geothermal_switch,geothermal_completion_year,geothermal_MW,geothermal_CF,geothermal_CAPEX,
                                                  discount_rate,inflation_rate,
                                                      emission_tonneperMWh,
                                                      CommBattery_size,CommBatery_cost,CommBattery_year,switch_battery,
                                                      emission_dollarpertonne)



        return [f'{oil_supplied_cost:,}',
                f'{power_generated_GWh:,}',
                f'{transformation_losses_cost:,}',
                Efficiency,
                figures.annual_demand(power_generated_GWh, demand_growth, decarb_year),
                fig_lists[0],
                fig_lists[1],
                fig_lists[2],
                fig_lists[3],
                fig_lists[4],
                f'{emissions_mtonne:,}', f'{emission_cost_mdollar:,}',
                # f'{rooftop_capacity_MW:,}',f'{rooftop_PV_generation_GWh:,}'
                ]
    else:
        pass




