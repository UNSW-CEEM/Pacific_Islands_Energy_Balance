import pandas as pd
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import plotly.express as px
from EnergyFlows import Country_List


def imports_to_GDP(year):
    net_imp_list= []
    interest_list = ['Refined Petroleum']
    for c in Country_List:
        df_exp= pd.read_csv("Data/{}/Exports-{}---Click-to-Select-a-Product.csv".format(c,year))
        df_imp = pd.read_csv("Data/{}/Imports-{}---Click-to-Select-a-Product.csv".format(c,year))

        df_imp['Trade Value'] = df_imp['Trade Value']/1000000 #to million $
        df_exp['Trade Value'] = df_exp['Trade Value']/1000000 #to million $

        df_GDP = pd.read_csv('Data/Economic Indicators.csv')


        imp = df_imp[df_imp['HS4'].isin(interest_list)]['Trade Value']
        exp = df_exp[df_exp['HS4'].isin(interest_list)]['Trade Value']

        net_imp = imp.values[0]
        if len(exp) > 0:
            net_imp = imp.values[0]-exp.values[0]

        net_imp_list.append(net_imp)
    df_GDP['Imp'] = net_imp_list
    df_GDP['net_imp_to_GDP'] = 100 * df_GDP['Imp']/df_GDP['GDP(million$)2019']
    # df_GDP.to_csv('GDPPPPP.csv')

    fig = go.Figure()
    fig.add_trace(go.Bar(x=df_GDP['Country'], y=df_GDP['net_imp_to_GDP'],name='dasdsa',marker_color='forestgreen'))
    # fig.add_trace(go.Bar(x=summary_df['Country'], y=summary_df['aviation_to_import'], name='Int. aviation bunkers',marker_color='lightsalmon'))

    a = df_GDP['Country']
    b = df_GDP['net_imp_to_GDP']


    fig.update_layout(#width=1500,
        # height=500,
        barmode='relative')
    fig.update_layout(legend = dict(bgcolor = 'rgba(0,0,0,0)',    yanchor="bottom",orientation="h",
        y=1.05,
        xanchor="center",
        x=0.5),
                      font=dict(
                          family="Calibri",
                          size=16,
                          color="white"
                      )
                      )
    fig.update_layout({
    'plot_bgcolor': 'rgba(0,0,0,0)',
    'paper_bgcolor': 'rgba(0,0,0,0)',
    })
    fig.update_yaxes(title_text="% of GDP",showline=True)
    fig.update_xaxes(showline=True,
                     title_text="<a href=\"https://oec.world/en/home-b\"><sub>Source: The Observatory of Economic Complexity (OEC)<sub></a>")

    fig.update_layout(
        title="% imported petroleum products in {} to the most recent reported GDP".format(year))
    # print(summary_df)
    fig.update_traces(marker_line_color='white',
                      marker_line_width=1.5, opacity=1)

    return fig







def import_export_figure(df_imp,df_exp,Interest_list,year):
    # fig = make_subplots(rows=1, cols=1,shared_xaxes=True,shared_yaxes=False,subplot_titles=("2019       Imports {}  Exports {} ($MM)".format(-int(df_imp['Trade Value'].sum()),int(df_exp['Trade Value'].sum()))
    #                                                                                         ),vertical_spacing =0.05)
    totalImports = int(-df_imp['Trade Value'].sum())
    totalExports = int(df_exp['Trade Value'].sum())


    fig = go.Figure()
    fig.add_trace(go.Bar(x=df_imp[df_imp['HS4'].isin(Interest_list)]['HS4'], y=df_imp[df_imp['HS4'].isin(Interest_list)]['Trade Value'],name='Imports',marker_color='red'))
    fig.add_trace(go.Bar(x=df_exp[df_exp['HS4'].isin(Interest_list)]['HS4'], y=df_exp[df_exp['HS4'].isin(Interest_list)]['Trade Value'], name='Exports',marker_color='green'))

    fig.update_layout(#width=1500,
        height=500,
        barmode='relative')
    fig.update_layout(legend = dict(bgcolor = 'rgba(0,0,0,0)',    yanchor="bottom",orientation="v",
        y=0.5,
        xanchor="center",
        x=1.07),
                      font=dict(
                          family="Calibri",
                          size=18,
                          color="white"
                      )
                      )
    fig.update_layout({
    'plot_bgcolor': 'rgba(0,0,0,0)',
    'paper_bgcolor': 'rgba(0,0,0,0)',
    })
    fig.update_yaxes(title_text="Value ($MM)",showline=True)
    fig.update_xaxes(showline=True,title_text = "<a href=\"https://oec.world/en/home-b\"><sub>Source: The Observatory of Economic Complexity (OEC)<sub></a>")

    fig.update_layout(
        title="{}, Total Imports = {}, Total Exports = {} ($million)".format(year,totalImports,totalExports))
    fig.update_traces(marker_line_color='white',
                      marker_line_width=1.5, opacity=1)
    return fig




def Generate_Sankey(year,country):
    import pandas as pd
    import plotly.graph_objects as go

    df = pd.read_csv("Data/Sankey/csv/{}/{}.csv".format(year,country))
    df_elec = df.loc[(df[' (from)']=='PowerStations')|(df[' (from)'] == 'Other Electricity & Heat')|(df[' (from)']=='Other Electricity & Heat3')
                     |(df[' (from)']=='Electricity & Heat: Supplied')
                     |(df[' (from)'] == 'Electricity & Heat: Final Consumption') | (df[' (to)']=='PowerStations')
                     |(df[' (to)']=='Other Electricity & Heat')
                     |(df[' (to)']=='Other Electricity & Heat3')|(df[' (to)']=='Electricity & Heat: Supplied')]



    color_dicts = {'Primary Oil: Production': 'grey', 'Primary Oil: Imports': 'grey', 'Oil Products: Imports': 'grey',
                   'Natural Gas: Primary Production': 'blue', 'Electricity: Primary Production': 'red',
                   'Heat: Primary Production': 'red', 'BioFuels: Primary Production': 'green', 'Primary Oil': 'grey',
                   'BioFuels': 'green', 'Oil Refineries': 'grey', 'Oil Products': 'grey',
                   'Natural Gas': 'blue', 'Oil: Supplied': 'grey', 'Natural Gas: Supplied': 'blue',
                   'Electricity & Heat: Supplied': 'red', 'Exports': 'yellow', 'Primary Oil': 'grey',
                   'Natural Gas': 'blue', 'Electricity & Heat: Supplied': 'red',
                   'PowerStations': 'red', 'Oil: Final Consumption': 'grey',
                   'Electricity & Heat: Final Consumption': 'red', 'BioFuels: Final Consumption': 'green',
                   'BioFuels: Supplied': 'green',
                   'Other Electricity & Heat': 'red', 'Other Electricity & Heat 3': 'red', }

    lst = df[' (from)'].to_list()
    lst2 = df[' (to)'].to_list()
    lst.extend(lst2)
    lst = list(dict.fromkeys(lst))

    d = {}
    for i in range(len(lst)):
        d[i] = lst[i]
    d = dict((y, x) for x, y in d.items())
    df['To'] = df[' (to)'].copy()
    df['From'] = df[' (from)'].copy()

    df.replace({" (from)": d}, inplace=True)
    df.replace({" (to)": d}, inplace=True)
    df.fillna('pink', inplace=True)
    for i in color_dicts.keys():
        df.loc[df['From'] == i, ' (color)'] = color_dicts[i]




    lst_e = df_elec[' (from)'].to_list()
    lst2_e = df_elec[' (to)'].to_list()
    lst_e.extend(lst2_e)
    lst_e = list(dict.fromkeys(lst_e))

    d = {}
    for i in range(len(lst_e)):
        d[i] = lst_e[i]
    d = dict((y, x) for x, y in d.items())
    df_elec['To'] = df_elec[' (to)'].copy()
    df_elec['From'] = df_elec[' (from)'].copy()

    df_elec.replace({" (from)": d}, inplace=True)
    df_elec.replace({" (to)": d}, inplace=True)
    df_elec.fillna('pink', inplace=True)
    for i in color_dicts.keys():
        df_elec.loc[df_elec['From'] == i, ' (color)'] = color_dicts[i]







    fig = go.Figure(data=[go.Sankey(
        valuesuffix="TJ",
        node=dict(
            pad=35,
            thickness=20,
            line=dict(color="black", width=0.5),
            label=lst,
            # color='brown'
        ),
        link=dict(
            source=df[' (from)'].to_list(),  # indices correspond to labels, eg A1, A2, A1, B1, ...
            target=df[' (to)'].to_list(),
            value=df[' (weight)'].to_list(),
            color=df[' (color)'].to_list()

        ))])

    fig2 = go.Figure(data=[go.Sankey(
        valuesuffix="TJ",
        node=dict(
            pad=35,
            thickness=20,
            line=dict(color="black", width=0.5),
            label=lst_e,
            # color='brown'
        ),
        link=dict(
            source=df_elec[' (from)'].to_list(),  # indices correspond to labels, eg A1, A2, A1, B1, ...
            target=df_elec[' (to)'].to_list(),
            value=df_elec[' (weight)'].to_list(),
            color=df_elec[' (color)'].to_list()

        ))])



    fig.update_layout(title_text="Sankey Plot for all sectors <br><a href=\"http://unstats.un.org/unsd/energystats/pubs/balance\"><sub>Source: Energy Balances, United Nations<sub></a>",
                      font_size=16)
    fig.update_layout(height=900,font=dict(
                          family="Calibri",
                          size=16,
                          color="white"
                      ))
    fig.update_layout({'plot_bgcolor': 'rgba(0,0,0,0)',
    'paper_bgcolor': 'rgba(0,0,0,0)'},)

    fig2.update_layout(height=350,font=dict(
                          family="Calibri",
                          size=16,
                          color="white"
                      ))
    fig2.update_layout({'plot_bgcolor': 'rgba(0,0,0,0)',
    'paper_bgcolor': 'rgba(0,0,0,0)'},)
    fig2.update_layout(title_text="Sankey Plot for the electricity sector <br><a href=\"http://unstats.un.org/unsd/energystats/pubs/balance\"><sub>Source: Energy Balances, United Nations<sub></a>",
                       font_size=16)

    return [fig,fig2]






def oil_to_RE(PV,PV_batt,wind,wind_bat,max_range,year):
    import plotly.graph_objs as go
    names = ['PV', 'PV+Battery','Wind','Wind+Battery']
    values = [PV,PV_batt,wind,wind_bat]
    data = [go.Bar(
        x=names,
        y=values,

    )]
    fig = go.Figure(data=data)
    fig.update_layout(
        title="Potential RE installation with the money paid for diesel transformation in {}".format(year))
    fig.update_yaxes(title_text="MW",showline=True)
    fig.update_xaxes(showline=True)

    fig.update_layout(yaxis_range=[0, max_range])

    fig.update_layout({'plot_bgcolor': 'rgba(0,0,0,0)',
    'paper_bgcolor': 'rgba(0,0,0,0)'})

    fig.update_layout(height=350,font=dict(
                          family="Calibri",
                          size=16,
                          color="white"
                      ))
    fig.update_traces(marker_color='lightsalmon', marker_line_color='white',
                      marker_line_width=2.5, opacity=1)


    return fig


def annual_demand(demand,growth_rate,decarb_rate):
    demand_list = []
    demand_list.append(demand)
    year_list = []
    year = 2019
    year_list.append(year)
    for i in range(0,31):
        demand += demand * growth_rate/100
        demand_list.append(demand)

        year += 1
        year_list.append(year)

    data = [go.Scatter(
        x=year_list,
        y=demand_list,
    )]
    fig = go.Figure(data=data)
    fig.update_layout(
        title="Current and future non-RE electricity demand with {}% annual growth".format(growth_rate))

    fig.update_yaxes(title_text="GWh")
    # fig.update_layout(yaxis_range=[0, max_range])

    fig.update_layout({'plot_bgcolor': 'rgba(0,0,0,0)',
                       'paper_bgcolor': 'rgba(0,0,0,0)'})

    fig.update_layout(#height=500,
                      font=dict(
        family="Calibri",
        size=16,
        color="white"
    ))
    fig.update_traces(marker_color='lightsalmon', marker_line_color='white',
                      marker_line_width=2.5, opacity=1)
    fig.update_xaxes(showgrid=False,showline=True)
    fig.update_yaxes(showgrid=True,showline=True)
    return fig


def decarbonization_scenarios(Efficiency,oil_imports_2019,demand,growth_rate,PV_cost,PVBatt_cost,WindBatt_cost,Wind_cost,decarb_year,
                              total_wind_share,small_PV_share,small_wind_share,
                              PV_pot,Wind_pot,diesel_HHV,diesel_price,
                              geothermal_switch,geothermal_completion_year,geothermal_MW,geothermal_CF,geothermal_CAPEX,
                              discount_rate,inflation_rate,
                              emission_tonneperMWh,
                              CommBattery_size,CommBatery_cost,CommBattery_year,switch_battery,
                              emission_dollarpertonne):

    if geothermal_switch != [1]:
        geothermal_MW = 0
        geothermal_CF = 0
    if switch_battery != [1]:
        CommBatery_cost = 0
        CommBattery_size = 0

    geothermal_GWh = geothermal_MW * (geothermal_CF/100) * 8760/1000

    total_wind_share = total_wind_share/100
    small_PV_share = small_PV_share/100
    small_wind_share = small_wind_share/100
    total_PV_share = 1-total_wind_share
    large_wind_share = 1-small_wind_share
    large_PV_share = 1-small_PV_share

    demand_df = pd.DataFrame()
    demand_list = []

    demand_list.append(demand)
    year_list = []
    year = 2019
    year_list.append(year)
    for i in range(0, 31):
        demand += demand * growth_rate / 100
        demand_list.append(demand)
        year += 1
        year_list.append(year)

    demand_list=demand_list[3:]
    year_list=year_list[3:]
    demand_df['Year']=year_list
    demand_df['Demand'] = demand_list #GWh
    demand_df['RE_cumulative'] = 0
    demand_df['Geothermal_inst'] = 0
    demand_df['Geothermal_GWh'] = 0
    demand_df['Geothermal_inst_cost'] = 0
    demand_df['Battery_inst_cost'] = 0

    demand_df['Battery_inst_cost'][demand_df['Year'] == CommBattery_year] = CommBatery_cost*CommBattery_size #Million Dollar



    demand_df['RE_cumulative'][demand_df['Year']==decarb_year] = demand_df['Demand'][demand_df['Year']==decarb_year] #GWh
    demand_df['Geothermal_inst'][demand_df['Year'] == geothermal_completion_year] = geothermal_MW #MW
    demand_df['Geothermal_GWh'][demand_df['Year'] >= geothermal_completion_year] = geothermal_GWh #GWh
    demand_df['Geothermal_inst_cost'][demand_df['Year'] <= geothermal_completion_year] = \
        (geothermal_MW * geothermal_CAPEX*1000000)/(geothermal_completion_year-2022+1)#$Dollar


    years= decarb_year - 2022
    if geothermal_completion_year <= decarb_year:
        step = (demand_df['Demand'][demand_df['Year'] == decarb_year]- geothermal_GWh) / (years+1) #GWh

        if step.values[0] < 0:
            step = 0
    else:
        step = (demand_df['Demand'][demand_df['Year'] == decarb_year]) / (years + 1)  # GWh

    demand_df.at[0, 'RE_cumulative'] = step
    for i, row in demand_df.iterrows():
        if (i>0) :
            demand_df.at[i,'RE_cumulative'] = demand_df.at[i-1,'RE_cumulative'] + step #GWh

    demand_df['RE_cumulative'][demand_df['Year'] > decarb_year] = demand_df['Demand'] - demand_df['Geothermal_GWh']
    demand_df['RE_cumulative'][demand_df['RE_cumulative'] < 0] = 0

    demand_df['Annual_RE'] = demand_df['RE_cumulative'].shift(-1) - demand_df['RE_cumulative']
    demand_df['Annual_RE'] = demand_df['Annual_RE'].mask(demand_df['Annual_RE'] < 0, 0)
    demand_df['PV_inst'] = (demand_df['Annual_RE'] * total_PV_share)/PV_pot #MW
    demand_df['wind_inst'] = (demand_df['Annual_RE'] * total_wind_share)/Wind_pot #MW

    demand_df['Small PV+B'] = demand_df['PV_inst'] * small_PV_share #MW
    demand_df['Large PV'] = demand_df['PV_inst'] * large_PV_share #MW
    demand_df['Small Wind+B'] = demand_df['wind_inst'] * small_wind_share #MW
    demand_df['Large Wind'] = demand_df['wind_inst'] * large_wind_share #MW

    demand_df['RE_inst_cost'] = (1000000 * demand_df['PV_inst'] * (small_PV_share*PVBatt_cost+large_PV_share*PV_cost) +\
                                1000000 * demand_df['wind_inst'] * (small_wind_share*WindBatt_cost+large_wind_share*Wind_cost)+ \
                                demand_df['Geothermal_inst_cost']+
                                 demand_df['Battery_inst_cost']*1000000)/1000000 #M$



    demand_df["non_RE_demand_TJ"] = (demand_df['Demand'] - demand_df['RE_cumulative']-demand_df['Geothermal_GWh'])/0.2777
    demand_df['non_RE_demand_TJ'][demand_df['non_RE_demand_TJ'] < 0] = 0

    demand_df["diesel_litre_dec"] = demand_df["non_RE_demand_TJ"] / (diesel_HHV*Efficiency) # L
    demand_df["diesel_cost_dec"] = demand_df["diesel_litre_dec"] * diesel_price / 1000000  # $MM

    demand_df["diesel_litre_bs"] = (demand_df["Demand"]/0.2777) / (diesel_HHV * Efficiency)
    demand_df["diesel_cost_bs"] = demand_df["diesel_litre_bs"] * diesel_price / 1000000  # $MM

    demand_df['Diesel_cost_saving'] = demand_df["diesel_cost_bs"] - demand_df["diesel_cost_dec"] # $MM


    demand_df['Net_saving'] = demand_df['Diesel_cost_saving'] - demand_df['RE_inst_cost']  # $MM









    diesel_emission_intensity = emission_tonneperMWh * 1000 # t CO2-e/GWh
    demand_df['Emission_bs_ton'] = demand_df['Demand'] * diesel_emission_intensity
    demand_df['Emission_dec_ton'] = (demand_df['Demand'] - demand_df['RE_cumulative'] -demand_df['Geothermal_GWh']) * diesel_emission_intensity
    demand_df['Emission_dec_ton'][demand_df['Emission_dec_ton'] < 0] = 0

    demand_df['Emission_red'] = demand_df['Emission_bs_ton'] - demand_df['Emission_dec_ton']
    demand_df['Emission_red_cum'] = demand_df['Emission_red'].cumsum()
    # add carbon price
    demand_df['Emission_red_saving'] = demand_df['Emission_red'] * emission_dollarpertonne/1000000 #million dolar
    demand_df['Diesel_import_reduction'] = (demand_df["diesel_litre_bs"] - demand_df["diesel_litre_dec"])/1000000 #Million Litre

    demand_df['Net_saving_discounted'] = 0
    demand_df['Emission_red_saving_discounted'] = 0
    inflation_rate = inflation_rate/100
    discount_rate = discount_rate/100

    for i, row in demand_df.iterrows():
        # if (i>0) :
        demand_df.at[i,'Net_saving_discounted'] = demand_df.at[i,'Net_saving'] * ((1+inflation_rate)/(1+discount_rate))**i
        demand_df.at[i,'Emission_red_saving_discounted'] = demand_df.at[i,'Emission_red_saving'] * ((1+inflation_rate)/(1+discount_rate))**i


    demand_df['Net_saving_cumsum'] = demand_df['Net_saving_discounted'].cumsum()
    demand_df['Net_saving_emission_cumsum'] = demand_df['Emission_red_saving_discounted'].cumsum()



    # fig = make_subplots(specs=[[{"secondary_y": False}]])
    fig=go.Figure()
    fig.add_trace(
        go.Bar(x=demand_df['Year'], y=demand_df['Net_saving_discounted'], name="Annual net saving",marker_color='forestgreen'),
    )
    fig.add_trace(
        go.Bar(x=demand_df['Year'], y=demand_df['Emission_red_saving_discounted'], name="Annual savings from emissions",marker_color='lightsalmon'),
    )



    fig.update_yaxes(title_text="Annual Saving ($m)",  showline=True, showgrid=False)

    fig.update_xaxes(showgrid=False, showline=True)

    fig.update_layout(height=350, font=dict(
        family="Calibri",
        size=16,
        color="white"
    ))
    fig.update_layout({'plot_bgcolor': 'rgba(0,0,0,0)',
                       'paper_bgcolor': 'rgba(0,0,0,0)'},
                      legend=dict(bgcolor='rgba(0,0,0,0)', yanchor="bottom", orientation="h",
                                  y=1.05,
                                  xanchor="center",
                                  x=0.5,
                                  ),
                      hovermode="x"
                      )
    fig.update_traces(marker_line_color='white',
                      marker_line_width=1.5, opacity=1)

    # fig.update_layout(yaxis_range=[0, max_range])

    fig.update_layout(
        title="Annual savings by achieving 100% RE in {}".format(decarb_year))
    fig.update_layout(barmode='relative')

############################################################################################
    ########################################################################################



    # fig2 = make_subplots(specs=[[{"secondary_y": False}]])
    fig2 = go.Figure()
    fig2.add_trace(
        go.Bar(x=year_list, y=demand_df['Net_saving_cumsum'], name="Cumulative net saving"
               ,marker_color='forestgreen'),
    )
    fig2.add_trace(
        go.Bar(x=year_list, y=demand_df['Net_saving_emission_cumsum'], name="Cumulative saving from emissions",
               marker_color='lightsalmon'),
    )

    fig2.update_yaxes(title_text="Cumulative Saving ($m)", showline=True, showgrid=False)
    fig2.update_xaxes(showgrid=False, showline=True)

    fig2.update_layout(height=350, font=dict(
        family="Calibri",
        size=16,
        color="white"
    ))
    fig2.update_layout({'plot_bgcolor': 'rgba(0,0,0,0)',
                       'paper_bgcolor': 'rgba(0,0,0,0)'},
                      legend=dict(bgcolor='rgba(0,0,0,0)', yanchor="bottom", orientation="h",
                                  y=1.05,
                                  xanchor="center",
                                  x=0.5,
                                  ),
                       hovermode="x"
                       )
    fig2.update_traces(marker_line_color='white',
                      marker_line_width=1.5, opacity=1)

    # fig.update_layout(yaxis_range=[0, max_range])

    fig2.update_layout(
        title="Cumulative Savings by achieving 100% RE in {}".format(decarb_year))
    fig2.update_layout(barmode='relative')

    fig3 = go.Figure()
    fig3.add_trace(go.Bar(x=demand_df['Year'], y=demand_df['Small PV+B'], name='Small PV+B',
                          marker_color='forestgreen'))
    fig3.add_trace(go.Bar(x=demand_df['Year'], y=demand_df['Large PV'], name='Large PV',
                          marker_color='lightsalmon'))
    fig3.add_trace(go.Bar(x=demand_df['Year'], y=demand_df['Small Wind+B'], name='Small Wind+B',
                          marker_color='greenyellow'))
    fig3.add_trace(go.Bar(x=demand_df['Year'], y=demand_df['Large Wind'], name='Large Wind',
                          marker_color='orangered'))
    # fig3.add_trace(go.Bar(x=summary_df['Country'], y=summary_df['Pipeline transport'], name='Pipeline transport',
    #                       marker_color='mediumvioletred'))
    # fig3.add_trace(go.Bar(x=summary_df['Country'], y=summary_df['transport n.e.s'], name='Transport n.e.s',
    #                       marker_color='darkturquoise'))

    fig3.update_layout(  # width=1500,
        # height=500,
        barmode='relative')
    fig3.update_layout(legend=dict(bgcolor='rgba(0,0,0,0)', yanchor="bottom", orientation="h",
                                   y=0.98,
                                   xanchor="center",
                                   x=0.5),
                       font=dict(
                           family="Calibri",
                           size=16,
                           color="white"
                       )
                       )
    fig3.update_layout({
        'plot_bgcolor': 'rgba(0,0,0,0)',
        'paper_bgcolor': 'rgba(0,0,0,0)',
    })
    fig3.update_yaxes(title_text="Installed Capacity (MW)", showline=True)
    fig3.update_xaxes(showline=True)

    fig3.update_layout(
        title="Breakdown of annual RE installation for 100% RE in {}".format(decarb_year))
    fig3.update_traces(marker_line_color='white',
                       marker_line_width=1.5, opacity=1)


    fig4 = make_subplots(specs=[[{"secondary_y": True}]])

    # fig4 = go.Figure()
    fig4.add_trace(go.Bar(x=demand_df['Year'], y=demand_df['Emission_red'], name='Annual emission reduction',
                          marker_color='forestgreen'))
    fig4.add_trace(go.Scatter(x=demand_df['Year'], y=demand_df['Emission_red_cum'], name='Cumulative emission reduction',
                          marker_color='lightsalmon',),secondary_y=True)
    fig4.update_layout(  # width=1500,
        # height=500,
        barmode='relative')
    fig4.update_layout(legend=dict(bgcolor='rgba(0,0,0,0)', yanchor="bottom", orientation="h",
                                   y=0.98,
                                   xanchor="center",
                                   x=0.5),
                       font=dict(
                           family="Calibri",
                           size=16,
                           color="white"
                       )
                       )
    fig4.update_layout({
        'plot_bgcolor': 'rgba(0,0,0,0)',
        'paper_bgcolor': 'rgba(0,0,0,0)',
    })
    fig4.update_yaxes(title_text="Annual (t CO2-e)", showline=True)
    fig4.update_yaxes(title_text="Cumulative (t CO2-e)", secondary_y=True, showline=True, showgrid=False)

    fig4.update_xaxes(showline=True)

    fig4.update_layout(
        title="Annaul CO2-e emission reduction by achieving 100% RE in {}".format(decarb_year))
    # print(summary_df)
    fig4.update_traces(marker_line_color='white',
                       marker_line_width=1.5, opacity=1)


    fig5 = make_subplots(specs=[[{"secondary_y": True}]])

    # fig4 = go.Figure()
    fig5.add_trace(go.Bar(x=demand_df['Year'], y=demand_df['Diesel_import_reduction'], name='Annual',
                          marker_color='forestgreen'))
    fig5.add_trace(go.Scatter(x=demand_df['Year'], y=demand_df['Diesel_import_reduction'].cumsum(), name='Cumulative',
                          marker_color='lightsalmon',),secondary_y=True)
    fig5.add_trace(go.Scatter(x=demand_df['Year'], y=[oil_imports_2019]*len(demand_df['Year']), name='Net oil products import in 2019',
                          marker_color='red'),secondary_y=False)
    # fig5.add_hline(y=oil_imports_2019, line_dash="dot",line=dict(color='Red',),
    #               annotation_text="2019 oil product imports",
    #               annotation_position="bottom left")
    # [z0] * len(seconds)

    fig5.update_layout(  # width=1500,
        # height=500,
        barmode='relative')
    fig5.update_layout(legend=dict(bgcolor='rgba(0,0,0,0)', yanchor="bottom", orientation="h",
                                   y=0.98,
                                   xanchor="center",
                                   x=0.5),
                       font=dict(
                           family="Calibri",
                           size=16,
                           color="white"
                       )
                       )
    fig5.update_layout({
        'plot_bgcolor': 'rgba(0,0,0,0)',
        'paper_bgcolor': 'rgba(0,0,0,0)',
    })
    fig5.update_yaxes(title_text="Annual (million Litre)", showline=True)
    fig5.update_yaxes(title_text="Cumulative (million Litre)", secondary_y=True, showline=True, showgrid=False)
    fig5.update_yaxes(title_text="Cumulative (million Litre)", secondary_y=True, showline=True, showgrid=False)

    fig5.update_xaxes(showline=True)

    fig5.update_layout(
        title="Diesel import reduction by achieving 100% RE in {}".format(decarb_year))
    # print(summary_df)
    fig5.update_traces(marker_line_color='white',
                       marker_line_width=1.5, opacity=1)

    return [fig,fig2,fig3,fig4,fig5]


def rooftop_PV_plot(available_buildings,PV_size):
    import pandas as pd
    df = pd.read_csv('Data/Rooftop Potential.csv')
    Countries = df['Country']
    Population = df['Population']
    Household_size = df['Household size']
    solar_radiation = df['Potential of Av.PV gen (GWh/MW/year)']

    number_of_homes = available_buildings*Population/Household_size # only those homes with rooftop PV potential

    rooftop_capacity_MW = number_of_homes * PV_size/1000

    rooftop_PV_generation_GWh = rooftop_capacity_MW * solar_radiation

    fig = make_subplots(specs=[[{"secondary_y": True}]])

    fig.add_trace(
        go.Bar(x=Countries, y=Population, name="Population",marker_color='forestgreen'),
        secondary_y=False,
    )

    fig.add_trace(
        go.Scatter(x=Countries, y=Household_size, name="Average household size",marker_color='red'),
        secondary_y=True,
    )
    fig.update_yaxes(title_text="Population", secondary_y=False,showline=True,showgrid=True)
    fig.update_yaxes(title_text="Average household size", secondary_y=True,showline=True, showgrid=True)
    fig.update_xaxes(showgrid=False,showline=True)
    fig.update_layout(#height=350,
                      font=dict(
                          family="Calibri",
                          size=16,
                          color="white"
                      ),
        hovermode="x"
    )
    fig.update_layout({'plot_bgcolor': 'rgba(0,0,0,0)',
                       'paper_bgcolor': 'rgba(0,0,0,0)'},
                      legend=dict(bgcolor='rgba(0,0,0,0)', yanchor="bottom", orientation="h",
                                  y=1.05,
                                  xanchor="center",
                                  x=0.5,
                      ))
    fig.update_traces(marker_line_color='white',
                      marker_line_width=1.5, opacity=1)

    fig.update_layout(
        title="Population and average households size")
    fig.update_xaxes(showline=True,title_text="<a href=\"http://purl.org/spc/digilib/doc/z8n4m\"><sub>Source: 2020 Pacific Populations, SPC<sub></a>")



    fig2 = make_subplots(specs=[[{"secondary_y": True}]])
    fig2.add_trace(
        go.Bar(x=Countries, y=number_of_homes, name="Number of homes available for rooftop PV",marker_color='forestgreen'),
        secondary_y=False,
    )
    fig2.add_trace(
        go.Scatter(x=Countries, y=rooftop_capacity_MW, name="Potential rooftop PV generation",marker_color='red'),
        secondary_y=True,
    )
    fig2.update_yaxes(title_text="Number of homes available for rooftop PV", secondary_y=False,showline=True,showgrid=True)
    fig2.update_yaxes(title_text="Potential rooftop PV capacity (MW)", secondary_y=True,showline=True, showgrid=False,rangemode='tozero')
    fig2.update_xaxes(showgrid=False,showline=True)

    fig2.update_layout(#height=350,
                      font=dict(
                          family="Calibri",
                          size=16,
                          color="white"
                      ),
        hovermode="x"
    )
    fig2.update_layout({'plot_bgcolor': 'rgba(0,0,0,0)',
                       'paper_bgcolor': 'rgba(0,0,0,0)'},
                      legend=dict(bgcolor='rgba(0,0,0,0)', yanchor="bottom", orientation="h",
                                  y=1.05,
                                  xanchor="center",
                                  x=0.5,
                      ))
    fig2.update_traces(marker_line_color='white',
                      marker_line_width=1.5, opacity=1)
    fig2.update_layout(
        title="Number of homes available for rooftop PV and potential rooftop PV capacity")



    fig3 = make_subplots(specs=[[{"secondary_y": False}]])
    fig3.add_trace(
        go.Bar(x=Countries, y=rooftop_PV_generation_GWh, name="Potential rooftop PV generation (GWh)",marker_color='forestgreen'),
    )
    fig3.update_yaxes(title_text="Rooftop PV generation (GWh/year)", showline=True, showgrid=True)
    fig3.update_xaxes(showgrid=False,showline=True)

    fig3.update_layout(#height=350,
                      font=dict(
                          family="Calibri",
                          size=16,
                          color="white"
                      ),
        hovermode="x"
    )
    fig3.update_layout({'plot_bgcolor': 'rgba(0,0,0,0)',
                       'paper_bgcolor': 'rgba(0,0,0,0)'},
                      legend=dict(bgcolor='rgba(0,0,0,0)', yanchor="bottom", orientation="h",
                                  y=1.05,
                                  xanchor="center",
                                  x=0.5,
                      ))
    fig3.update_traces(marker_line_color='white',
                      marker_line_width=1.5, opacity=1)
    fig3.update_layout(
        title="Potential rooftop PV generation")
    return [fig,fig2,fig3]


def Update_UNstats_database(year):
    Country_List = ['Samoa', 'Nauru', 'Vanuatu', 'Palau', 'Kiribati', 'Cook Islands', 'Solomon Islands', 'Tonga',
                    'New Caledonia', 'French Polynesia', 'Micronesia', 'Niue', 'Tuvalu', 'PNG', 'Fiji']
    all_countries_df = pd.DataFrame()

    for country in Country_List:
        df = pd.read_csv("Data/EnergyBalance/{}/{}.csv".format(year,country))
        if country == Country_List[0]:
            all_countries_df = df
        elif country != Country_List[0]:
            # pd.concat([all_countries_df,df],inplace=True)
            # pass
            all_countries_df = all_countries_df.append(df,ignore_index=True)

    all_countries_df.replace({"---": 0}, inplace=True)
    all_countries_df = all_countries_df.replace({'\*': ''},regex=True)

    c_list = all_countries_df.columns
    for i in c_list[2:]:
        all_countries_df[i] = all_countries_df[i].astype(float)

    all_countries_df['All Coal'] = all_countries_df['Primary Coal and Peat'] + all_countries_df['Coal and Peat Products']

    all_countries_df['All Oil'] = all_countries_df['Primary Oil'] + all_countries_df['Oil Products']


    all_countries_df['All Inputs'] = all_countries_df['All Coal'] + all_countries_df['All Oil'] + all_countries_df['Natural Gas'] +\
                                     all_countries_df['Biofuels and Waste'] + all_countries_df['Nuclear'] +all_countries_df['Heat']
    # all_countries_df.applymap(lambda x: 'Micronesia' if "Micronesia" in str(x) else x)
    all_countries_df.replace('Micronesia (Federated States of)', 'Micronesia',inplace=True)
    all_countries_df.replace('Papua New Guinea', 'PNG',inplace=True)

    all_countries_df.to_csv("Data/EnergyBalance/{}/all_countries_df.csv".format(year))

def UNstats_plots(year):
    summary_df = pd.DataFrame()
    df = pd.read_csv("Data/EnergyBalance/{}/all_countries_df.csv".format(year))
    imports = df[df['Transactions(down)/Commodity(right)']=='Imports']['All Oil'].values
    Int_marine = df[df['Transactions(down)/Commodity(right)']=='International marine bunkers']['All Oil'].values
    Int_avi = df[df['Transactions(down)/Commodity(right)']=='International aviation bunkers']['All Oil'].values
    transformation = -df[df['Transactions(down)/Commodity(right)']=='Transformation']['All Oil'].values
    transformation_losses = - df[df['Transactions(down)/Commodity(right)']=='Transformation']['Total Energy'].values

    summary_df['Country'] = df. iloc[:, 1].unique()
    summary_df['Oil imports'] = imports
    summary_df['Transformation'] = transformation
    summary_df['transformation_losses'] = transformation_losses


    summary_df['int marine'] = -Int_marine
    summary_df['int aviation'] = -Int_avi
    summary_df['marine_to_import'] = 100 * summary_df['int marine']/summary_df['Oil imports']
    summary_df['aviation_to_import'] = 100 * summary_df['int aviation']/summary_df['Oil imports']
    summary_df['transformation_to_import'] = 100 * summary_df['Transformation']/summary_df['Oil imports']
    summary_df['transformation_losses_to_import'] = 100 * summary_df['transformation_losses']/summary_df['Oil imports']
    summary_df['road'] = 100 * df[df['Transactions(down)/Commodity(right)']=='Road']['All Oil'].values/summary_df['Oil imports']
    summary_df['rail'] = 100 * df[df['Transactions(down)/Commodity(right)']=='Rail']['All Oil'].values/summary_df['Oil imports']
    summary_df['Domestic aviation'] = 100 * df[df['Transactions(down)/Commodity(right)']=='Domestic aviation']['All Oil'].values/summary_df['Oil imports']
    summary_df['Domestic navigation'] = 100 * df[df['Transactions(down)/Commodity(right)']=='Domestic navigation']['All Oil'].values/summary_df['Oil imports']
    summary_df['Pipeline transport'] = 100 * df[df['Transactions(down)/Commodity(right)']=='Pipeline transport']['All Oil'].values/summary_df['Oil imports']
    summary_df['transport n.e.s'] = 100 * df[df['Transactions(down)/Commodity(right)']=='Transport n.e.s']['All Oil'].values/summary_df['Oil imports']







    fig = go.Figure()
    fig.add_trace(go.Bar(x=summary_df['Country'], y=summary_df['marine_to_import'],name='Int. marine bunkers',marker_color='forestgreen'))
    fig.add_trace(go.Bar(x=summary_df['Country'], y=summary_df['aviation_to_import'], name='Int. aviation bunkers',marker_color='lightsalmon'))



    fig.update_layout(#width=1500,
        # height=500,
        barmode='relative')
    fig.update_layout(legend = dict(bgcolor = 'rgba(0,0,0,0)',    yanchor="bottom",orientation="h",
        y=1.05,
        xanchor="center",
        x=0.5),
                      font=dict(
                          family="Calibri",
                          size=16,
                          color="white"
                      ),
                        hovermode = "x"
                      )
    fig.update_layout({
    'plot_bgcolor': 'rgba(0,0,0,0)',
    'paper_bgcolor': 'rgba(0,0,0,0)',
    })
    fig.update_yaxes(title_text="% of imported oil",showline=True)
    fig.update_xaxes(showline=True,title_text="<a href=\"http://unstats.un.org/unsd/energystats/pubs/balance\"><sub>Source: Energy Balances, United Nations<sub></a>")

    fig.update_layout(
        title="% of imported oil consumed for international transit in {}".format(year))
    # print(summary_df)
    fig.update_traces(marker_line_color='white',
                      marker_line_width=1.5, opacity=1)

    fig2 = go.Figure()
    fig2.add_trace(go.Bar(x=summary_df['Country'], y=summary_df['transformation_to_import'], name='Transformation',
                         marker_color='forestgreen'))
    fig2.add_trace(go.Bar(x=summary_df['Country'], y=summary_df['transformation_losses_to_import'], name='Transformation losses',
                         marker_color='lightsalmon'))

    # fig2.update_layout(  # width=1500,
    #     # height=500,
    # )barmode='relative')
    fig2.update_layout(legend=dict(bgcolor='rgba(0,0,0,0)', yanchor="bottom", orientation="h",
                                  y=1.05,
                                  xanchor="center",
                                  x=0.5),
                      font=dict(
                          family="Calibri",
                          size=16,
                          color="white"
                      )
                      )
    fig2.update_layout({
        'plot_bgcolor': 'rgba(0,0,0,0)',
        'paper_bgcolor': 'rgba(0,0,0,0)',
    })
    fig2.update_yaxes(title_text="% of imported oil", showline=True)
    fig2.update_xaxes(showline=True,title_text="<a href=\"http://unstats.un.org/unsd/energystats/pubs/balance\"><sub>Source: Energy Balances, United Nations<sub></a>")

    fig2.update_layout(
        title="% of imported oil transformed into electricity and transformation losses in {}".format(year))
    # title="Plot Title <br><sub>Plot Subtitle</sub>",)
    # print(summary_df)
    fig2.update_traces(marker_line_color='white',
                      marker_line_width=1.5, opacity=1)


    fig3 = go.Figure()
    fig3.add_trace(go.Bar(x=summary_df['Country'], y=summary_df['road'], name='Road',
                         marker_color='forestgreen'))
    fig3.add_trace(go.Bar(x=summary_df['Country'], y=summary_df['rail'], name='Rail',
                         marker_color='lightsalmon'))
    fig3.add_trace(go.Bar(x=summary_df['Country'], y=summary_df['Domestic aviation'], name='Domestic aviation',
                         marker_color='greenyellow'))
    fig3.add_trace(go.Bar(x=summary_df['Country'], y=summary_df['Domestic navigation'], name='Domestic navigation',
                         marker_color='orangered'))
    fig3.add_trace(go.Bar(x=summary_df['Country'], y=summary_df['Pipeline transport'], name='Pipeline transport',
                         marker_color='mediumvioletred'))
    fig3.add_trace(go.Bar(x=summary_df['Country'], y=summary_df['transport n.e.s'], name='Transport n.e.s',
                         marker_color='darkturquoise'))

    fig3.update_layout(  # width=1500,
        # height=500,
        barmode='relative')
    fig3.update_layout(legend=dict(bgcolor='rgba(0,0,0,0)', yanchor="bottom", orientation="h",
                                  y=0.98,
                                  xanchor="center",
                                  x=0.5),
                      font=dict(
                          family="Calibri",
                          size=16,
                          color="white"
                      )
                      )
    fig3.update_layout({
        'plot_bgcolor': 'rgba(0,0,0,0)',
        'paper_bgcolor': 'rgba(0,0,0,0)',
    })
    fig3.update_yaxes(title_text="% of imported oil", showline=True)
    fig3.update_xaxes(showline=True,title_text="<a href=\"http://unstats.un.org/unsd/energystats/pubs/balance\"><sub>Source: Energy Balances, United Nations<sub></a>")

    fig3.update_layout(
        title="Breakdown of imported oil consumed for domestic transport in {}".format(year))
    # print(summary_df)
    fig3.update_traces(marker_line_color='white',
                      marker_line_width=1.5, opacity=1)


    return [fig,fig2,fig3]

def land_use_plot():
    df = pd.read_excel('Data/Potentials.xlsx')
    countries = df.columns[2:]
    PV_pot = df.iloc[0, 2:] #GWh/MW/year
    Wind_CF =df.iloc[1, 2:]
    Wind_pot =df.iloc[2, 2:] #GWh/MW/year

    arable = df.iloc[4,2:]
    crops = df.iloc[5, 2:]
    pasture = df.iloc[6, 2:]
    forested = df.iloc[7, 2:]
    other =df.iloc[8, 2:]
    non_RE_demand = df.iloc[10,2:]
    final_demand = df.iloc[12,2:]
    coastline = df.iloc[13,2:]
    area = df.iloc[14,2:]



    Wind_MW_non_RE = 1.2 * non_RE_demand/Wind_pot
    Wind_MW_final = 1.2 * final_demand/Wind_pot

    percentage_of_coastline_final = ((Wind_MW_final * 100/1.5)*0.25)/coastline
    percentage_of_coastline_non_RE = ((Wind_MW_non_RE * 100/1.5)*0.25)/coastline

    PV_non_RE = 1.2 * non_RE_demand/PV_pot #MW
    PV_final_demand = 1.2 * final_demand/PV_pot #MW

    PV_area_non_RE = PV_non_RE/(100) #0.1kw/m2 # Converted to km2
    PV_area_non_RE_per = 100 * PV_area_non_RE/area
    PV_area_final_demand = PV_final_demand/(100) #0.1kw/m2
    PV_area_final_demand_per = 100 * PV_area_final_demand/area
    fig = make_subplots(specs=[[{"secondary_y": False}]])

    fig.add_trace(go.Scatter(x=countries, y=Wind_MW_non_RE, name='Decarbonizing the electricity sector',
                          marker_color='red', text = Wind_MW_non_RE,
                      ))
    fig.add_trace(go.Scatter(x=countries, y=Wind_MW_final, name='Meeting the final demand',
                          marker_color='black', text = Wind_MW_final,
                      ))
    fig.update_layout(  # width=1500,
        # height=500,
        barmode='group')
    fig.update_layout(legend=dict(bgcolor='rgba(0,0,0,0)', yanchor="bottom", orientation="h",
                                   y=0.98,
                                   xanchor="center",
                                   x=0.5),
                       font=dict(
                           family="Calibri",
                           size=16,
                           color="white"
                       ),
                      hovermode="x"
                      )
    fig.update_layout({
        'plot_bgcolor': 'rgba(0,0,0,0)',
        'paper_bgcolor': 'rgba(0,0,0,0)',
    })
    fig.update_yaxes(title_text="Wind capacity (MW)", showline=True,rangemode='tozero')
    fig.update_xaxes(showline=True,showgrid=False)
    fig.update_layout(
        title="Required wind capacity")
    # print(summary_df)
    fig.update_traces(marker_line_color='white',
                       marker_line_width=1.5, opacity=1)
    fig.update_traces(texttemplate='%{text:.1s}',)



    fig1 = make_subplots(specs=[[{"secondary_y": False}]])


    fig1.add_trace(go.Scatter(x=countries, y=percentage_of_coastline_final, name='% coastline for final demand',
                          marker_color='black'))
    fig1.add_trace(
        go.Scatter(x=countries, y=percentage_of_coastline_non_RE, name='% coastline for decarbonizing the electricity sector',
                   marker_color='red'))
    fig1.update_layout(legend=dict(bgcolor='rgba(0,0,0,0)', yanchor="bottom", orientation="h",
                                   y=0.98,
                                   xanchor="center",
                                   x=0.5),
                       font=dict(
                           family="Calibri",
                           size=16,
                           color="white"
                       ),
                       hovermode="x",


                       )
    fig1.update_layout({
        'plot_bgcolor': 'rgba(0,0,0,0)',
        'paper_bgcolor': 'rgba(0,0,0,0)',
    })
    fig1.update_yaxes(title_text="% of coastline", showline=True, showgrid=True)

    fig1.update_xaxes(showline=True,showgrid=False)

    fig1.update_layout(
        title="Coastline required for wind turbine installation")
    fig1.update_traces(marker_line_color='white',
                       marker_line_width=1.5, opacity=1)
    fig1.update_yaxes(rangemode='tozero')


    fig2 = make_subplots(specs=[[{"secondary_y": False}]])

    fig2.add_trace(go.Scatter(x=countries, y=PV_non_RE, name='Decarbonizing the electricity sector',
                          marker_color='red',text = PV_non_RE,
                      ))
    fig2.add_trace(go.Scatter(x=countries, y=PV_final_demand, name='Meeting the final demand',
                          marker_color='black',text = PV_final_demand,
                      ))

    fig2.update_layout(  # width=1500,
        # height=500,
        barmode='relative')
    fig2.update_layout(legend=dict(bgcolor='rgba(0,0,0,0)', yanchor="bottom", orientation="h",
                                   y=0.98,
                                   xanchor="center",
                                   x=0.5),
                       font=dict(
                           family="Calibri",
                           size=16,
                           color="white"
                       ),
                       hovermode="x"

                       )
    fig2.update_layout({
        'plot_bgcolor': 'rgba(0,0,0,0)',
        'paper_bgcolor': 'rgba(0,0,0,0)',
    })
    fig2.update_yaxes(title_text="PV capacity (MW)", showline=True,rangemode='tozero')
    # fig2.update_yaxes(title_text="Capacity Factor (%)", secondary_y=True, showline=True, showgrid=False)

    fig2.update_xaxes(showline=True,showgrid=False)

    fig2.update_layout(
        title="Required PV capacity")
    # print(summary_df)
    fig2.update_traces(marker_line_color='white',
                       marker_line_width=1.5, opacity=1)
    fig2.update_yaxes(rangemode='tozero')
    fig2.update_traces(texttemplate='%{text:.1s}')



    fig3 = go.Figure()
    fig3.add_trace(go.Bar(x=countries, y=arable, name='Arable',
                         marker_color='orangered'))
    fig3.add_trace(go.Bar(x=countries, y=crops, name='Crops',
                         marker_color='lightsalmon'))
    fig3.add_trace(go.Bar(x=countries, y=pasture, name='Pasture',
                         marker_color='mediumvioletred'))
    fig3.add_trace(go.Bar(x=countries, y=forested, name='Forested',
                         marker_color='green'))
    fig3.add_trace(go.Bar(x=countries, y=other, name='Other',
                         marker_color='darkturquoise'))
    fig3.add_trace(go.Scatter(x=countries, y=PV_area_non_RE_per, name='% of land for decarbonizing the electricity sector',
                         marker_color='red'))
    fig3.add_trace(go.Scatter(x=countries, y=PV_area_final_demand_per, name='% of land for final demand',
                         marker_color='black'))

    fig3.update_layout(  # width=1500,
        # height=600,
        # autosize = True,
        barmode='relative')

    fig3.update_layout(legend=dict(bgcolor='rgba(0,0,0,0)', yanchor="bottom", orientation="h",
                                  y=0.94,
                                  xanchor="left",
                                  x=0),
                      font=dict(
                          family="Calibri",
                          size=14,
                          color="white"
                      ),
                      )
    fig3.update_layout({
        'plot_bgcolor': 'rgba(0,0,0,0)',
        'paper_bgcolor': 'rgba(0,0,0,0)',
    })
    fig3.update_yaxes(title_text="% land", showline=True,rangemode='tozero')
    fig3.update_xaxes(showline=True,title_text="<a href=\"https://www.cia.gov/the-world-factbook/countries\"><sub>Source: The World Factbook, CIA<sub></a>")

    fig3.update_traces(marker_line_color='white',
                      marker_line_width=1.5, opacity=1)
    fig3.update_layout(margin=dict(t=130))
    fig3.update_layout(
        title={
            'text': "Breakdown of  and area required for PV installation to meet the demand",
            'y': 0.95,
            # 'x': 0,
            'xanchor': 'left',
            'yanchor': 'top'})








    return fig, fig1,fig2,fig3


def mapboxplot(Country):
    import math
    df = pd.read_excel('Data/Potentials.xlsx')
    countries = df.columns[2:]
    # PV_pot = df.iloc[0, 2:] #GWh/MW/year
    PV_pot = df.iloc[0][Country] #GWh/MW/year

    Wind_CF = df.iloc[1][Country]
    Wind_pot = df.iloc[2][Country]#GWh/MW/year

    non_RE_demand = df.iloc[10][Country]
    final_demand = df.iloc[12][Country]
    coastline = df.iloc[13][Country]
    area = df.iloc[14][Country] #km2



    Wind_MW_non_RE = 1.2 * non_RE_demand/Wind_pot
    Wind_MW_final = 1.2 * final_demand/Wind_pot

    percentage_of_coastline_final = ((Wind_MW_final * 100/1.5)*0.25)/coastline
    percentage_of_coastline_non_RE = ((Wind_MW_non_RE * 100/1.5)*0.25)/coastline

    PV_non_RE = 1.2 * non_RE_demand/PV_pot #MW
    PV_final_demand = 1.2 * final_demand/PV_pot #MW

    PV_area_non_RE = PV_non_RE/(100) #0.1kw/m2 # Converted to km2
    PV_area_non_RE_per = 100 * PV_area_non_RE/area
    PV_area_final_demand = PV_final_demand/(100) #0.1kw/m2
    PV_area_final_demand_per = 100 * PV_area_final_demand/area

    width_decarb = math.sqrt(PV_area_non_RE) * 1000/2
    width_final_demand = math.sqrt(PV_area_final_demand) * 1000/2

    import plotly.graph_objects as go
    from math import sqrt, atan, pi
    import pyproj
    geod = pyproj.Geod(ellps='WGS84')
    # Country = "Samoa"

    Coordinates = {"Samoa": [-13.597336, -172.457458], "Nauru": [-0.5228, 166.9315], "Vanuatu": [-15.3767, 166.9592],
                   "Palau": [7.5150, 134.5825], "Kiribati": [1.780915, -157.304505],
                   "Cook Islands": [-21.2367, -159.7777],
                   "Solomon Islands": [-9.6457, 160.1562], "Tonga": [-21.1790, -175.1982],
                   "New Caledonia": [-21.222232, 165.251540],
                   "French Polynesia": [-17.622779, -149.457556], "Micronesia": [6.881990, 158.220540],
                   "Niue": [-19.0544, -169.8672],
                   "Tuvalu": [-8.519814, 179.19750], "PNG": [-6.3150, 143.9555], "Fiji": [-17.7134, 178.0650]}

    width = width_decarb  # m
    height = width_decarb  # m

    rect_diag = sqrt(width ** 2 + height ** 2)

    center_lon = Coordinates[Country][1]
    center_lat = Coordinates[Country][0]
    azimuth1 = atan(width / height)
    azimuth2 = atan(-width / height)
    azimuth3 = atan(width / height) + pi  # first point + 180 degrees
    azimuth4 = atan(-width / height) + pi  # second point + 180 degrees
    pt1_lon, pt1_lat, _ = geod.fwd(center_lon, center_lat, azimuth1 * 180 / pi, rect_diag)
    pt2_lon, pt2_lat, _ = geod.fwd(center_lon, center_lat, azimuth2 * 180 / pi, rect_diag)
    pt3_lon, pt3_lat, _ = geod.fwd(center_lon, center_lat, azimuth3 * 180 / pi, rect_diag)
    pt4_lon, pt4_lat, _ = geod.fwd(center_lon, center_lat, azimuth4 * 180 / pi, rect_diag)




    fig = go.Figure(go.Scattermapbox(
        mode="lines+text", fill="toself",
        marker=dict(size=16, color='red'),
        textposition='top right',
        # name = "asdsadad"
        textfont=dict(size=16, color='red'),
        hovertemplate="<b>{}</b><br><br>".format(Country) +
                      "PV area for decarbonizing the electricity sector: {} km2</b><br>".format(round(PV_area_non_RE,2)) +
                      "% of land: {}<extra></extra>".format(round(PV_area_non_RE_per,2)),
        lon=[pt1_lon, pt2_lon, pt3_lon, pt4_lon, pt1_lon, ],
        lat=[pt1_lat, pt2_lat, pt3_lat, pt4_lat, pt1_lat],
    ))
    width = width_final_demand  # m
    height = width_final_demand  # m
    rect_diag = sqrt(width ** 2 + height ** 2)
    center_lon = Coordinates[Country][1]
    center_lat = Coordinates[Country][0]
    azimuth1 = atan(width / height)
    azimuth2 = atan(-width / height)
    azimuth3 = atan(width / height) + pi  # first point + 180 degrees
    azimuth4 = atan(-width / height) + pi  # second point + 180 degrees
    pt1_lon, pt1_lat, _ = geod.fwd(center_lon, center_lat, azimuth1 * 180 / pi, rect_diag)
    pt2_lon, pt2_lat, _ = geod.fwd(center_lon, center_lat, azimuth2 * 180 / pi, rect_diag)
    pt3_lon, pt3_lat, _ = geod.fwd(center_lon, center_lat, azimuth3 * 180 / pi, rect_diag)
    pt4_lon, pt4_lat, _ = geod.fwd(center_lon, center_lat, azimuth4 * 180 / pi, rect_diag)

    fig.add_trace(go.Scattermapbox(
        mode="lines+text", fill="toself",
        marker=dict(size=16, color='grey'),
        textposition='top left',
        # name = "asdsadad"
        textfont=dict(size=16, color='black'),
        hovertemplate="<b>{}</b><br><br>".format(Country) +
                      "PV area for final demand: {} km2</b><br>".format(round(PV_area_final_demand,2)) +
                      "% of land: {}<extra></extra>".format(round(PV_area_final_demand_per,2)),
        lon=[pt1_lon, pt2_lon, pt3_lon, pt4_lon, pt1_lon, ],
        lat=[pt1_lat, pt2_lat, pt3_lat, pt4_lat, pt1_lat],
    ))


    styles = ["open-street-map", "carto-positron", "carto-darkmatter", "stamen-terrain", "stamen-toner",
              "stamen-watercolor"]
    fig.update_layout(
        mapbox={'style': styles[3], 'center': {'lon': center_lon, 'lat': center_lat}, 'zoom': 6},
        # add zoom as a slider
        showlegend=False,
        margin={'l': 0, 'r': 0, 'b': 0, 't': 0},
    )
    print(width_decarb , width_final_demand)
    return fig

def generation_mix_plot():
    df = pd.read_csv('Data/Energy Pofiles.csv')
    Generation_df = df[['Country','Total_GWh_2019','Rebewable_GWh_2019','Non-Renewable_GWh_2019','Hydro_GWh_2019','Solar_GWh_2019','Wind_GWh_2019','Bio_GWh_2019','Geothermal_GWh_2020']]
    Capacity_df = df[['Country','Total_MW_2020','Rebewable_MW_2020','Non-Renewable_MW_2020','Hydro_MW_2020','Solar_MW_2020','Wind_MW_2020','Bio_MW_2020','Geothermal_MW_2020']]
    fig = go.Figure()
    fig.add_trace(go.Bar(x=Generation_df['Country'], y=100*Generation_df['Non-Renewable_GWh_2019']/Generation_df['Total_GWh_2019'], name='non-Renewable',
                         marker_color='black'))
    fig.add_trace(go.Bar(x=Generation_df['Country'], y=100*Generation_df['Hydro_GWh_2019']/Generation_df['Total_GWh_2019'], name='Hydro and Marine',
                         marker_color='lightblue'))
    fig.add_trace(go.Bar(x=Generation_df['Country'], y=100*Generation_df['Solar_GWh_2019']/Generation_df['Total_GWh_2019'], name='Solar',
                         marker_color='yellow'))
    fig.add_trace(go.Bar(x=Generation_df['Country'], y=100*Generation_df['Wind_GWh_2019']/Generation_df['Total_GWh_2019'], name='Wind',
                         marker_color='darkturquoise'))
    fig.add_trace(go.Bar(x=Generation_df['Country'], y=100*Generation_df['Bio_GWh_2019']/Generation_df['Total_GWh_2019'], name='Bio',
                         marker_color='green'))
    fig.add_trace(go.Bar(x=Generation_df['Country'], y=100*Generation_df['Geothermal_GWh_2020']/Generation_df['Total_GWh_2019'], name='Geothermal',
                         marker_color='red'))

    fig.update_layout(  # width=1500,
        # height=500,
        barmode='relative')
    fig.update_layout(legend=dict(bgcolor='rgba(0,0,0,0)', yanchor="bottom", orientation="h",
                                  y=1.05,
                                  xanchor="center",
                                  x=0.5),
                      font=dict(
                          family="Calibri",
                          size=16,
                          color="white"
                      )
                      )
    fig.update_layout({
        'plot_bgcolor': 'rgba(0,0,0,0)',
        'paper_bgcolor': 'rgba(0,0,0,0)',
    })
    fig.update_yaxes(title_text="% of total GWh generation", showline=True)
    fig.update_xaxes(showline=True,title_text="<a href=\"https://www.irena.org/Statistics/Statistical-Profiles\"><sub>Source: Country Profiles, IRENA<sub></a>")

    fig.update_layout(
        title="Generation mix in 2019")
    # print(summary_df)
    fig.update_traces(marker_line_color='white',
                      marker_line_width=1.5, opacity=1)

    fig2 = go.Figure()
    fig2.add_trace(go.Bar(x=Generation_df['Country'], y=100*Capacity_df['Non-Renewable_MW_2020']/Capacity_df['Total_MW_2020'], name='non-Renewable',
                         marker_color='black'))
    fig2.add_trace(go.Bar(x=Generation_df['Country'], y=100*Capacity_df['Hydro_MW_2020']/Capacity_df['Total_MW_2020'], name='Hydro and Marine',
                         marker_color='lightblue'))
    fig2.add_trace(go.Bar(x=Generation_df['Country'], y=100*Capacity_df['Solar_MW_2020']/Capacity_df['Total_MW_2020'], name='Solar',
                         marker_color='yellow'))
    fig2.add_trace(go.Bar(x=Generation_df['Country'], y=100*Capacity_df['Wind_MW_2020']/Capacity_df['Total_MW_2020'], name='Wind',
                         marker_color='darkturquoise'))
    fig2.add_trace(go.Bar(x=Generation_df['Country'], y=100*Capacity_df['Bio_MW_2020']/Capacity_df['Total_MW_2020'], name='Bio',
                         marker_color='green'))
    fig2.add_trace(go.Bar(x=Generation_df['Country'], y=100*Capacity_df['Geothermal_MW_2020']/Capacity_df['Total_MW_2020'], name='Geothermal',
                         marker_color='red'))

    fig2.update_layout(  # width=1500,
        # height=500,
        barmode='relative')
    fig2.update_layout(legend=dict(bgcolor='rgba(0,0,0,0)', yanchor="bottom", orientation="h",
                                  y=1.05,
                                  xanchor="center",
                                  x=0.5),
                      font=dict(
                          family="Calibri",
                          size=16,
                          color="white"
                      )
                      )
    fig2.update_layout({
        'plot_bgcolor': 'rgba(0,0,0,0)',
        'paper_bgcolor': 'rgba(0,0,0,0)',
    })
    fig2.update_yaxes(title_text="% of total MW capacity", showline=True)
    fig2.update_xaxes(showline=True,title_text="<a href=\"https://www.irena.org/Statistics/Statistical-Profiles\"><sub>Source: Country Profiles, IRENA<sub></a>")

    fig2.update_layout(
        title="Installed capacity mix in 2020")
    # print(summary_df)
    fig2.update_traces(marker_line_color='white',
                      marker_line_width=1.5, opacity=1)



    return [fig,fig2]

def validation():
    # from page1FarmView import Country_List
    Country_List = ['Samoa', 'Nauru', 'Vanuatu', 'Palau', 'Kiribati', 'Cook Islands', 'Solomon Islands', 'Tonga',
                    'New Caledonia', 'French Polynesia', 'Micronesia', 'Niue', 'Tuvalu', 'PNG', 'Fiji']

    import numpy as np
    file = pd.read_csv('Data/Validation.csv')
    for c in Country_List:
        df = pd.read_csv("Data/Sankey/csv/{}/{}.csv".format('2019',c))
        if c == 'PNG':
            oil_import_TJ = df[df[' (from)'] == 'Oil Products: Imports'][' (weight)'].values[0]  # Tj-
            oil_import_GWh = oil_import_TJ * 0.2777
            power_generated_GWh = oil_import_GWh * 0.2 # Imported oil * efficiency of non-RE power plants
        else:
            power_generated_TJ = df[(df[' (from)'] == 'PowerStations') & (df[' (to)'] == 'Electricity & Heat: Supplied')][' (weight)'] #TJ
            power_generated_GWh = int(power_generated_TJ * 0.2777)
        file.loc[file.Country == c, 'This Work'] = power_generated_GWh

    # file.to_csv('Data/Validation.csv')




def cross_country_sankey(df,from_,to_):
    fig = go.Figure()
    fig.add_trace(go.Bar(x=df['Country'], y=df['Values'],name='dasdsa',marker_color='forestgreen',text = df['Values']))
    # fig.add_trace(go.Bar(x=summary_df['Country'], y=summary_df['aviation_to_import'], name='Int. aviation bunkers',marker_color='lightsalmon'))




    fig.update_layout(width=800,
        # height=500,
        barmode='relative')
    fig.update_layout(legend = dict(bgcolor = 'rgba(0,0,0,0)',    yanchor="bottom",orientation="h",
        y=1.05,
        xanchor="center",
        x=0.5),
                      font=dict(
                          family="Calibri",
                          size=16,
                          color="white"
                      )
                      )
    fig.update_layout({
    'plot_bgcolor': 'rgba(0,0,0,0)',
    'paper_bgcolor': 'rgba(0,0,0,0)',

    })
    fig.update_yaxes(title_text="TJ",showline=True)
    fig.update_xaxes(showline=True,
                     title_text="<a href=\"http://unstats.un.org/unsd/energystats/pubs/balance\"><sub>Source: Energy Balances, United Nations<sub></a>"),

    fig.update_layout(
        title="From {} to {}".format(from_,to_))
    # print(summary_df)
    fig.update_traces(marker_line_color='white',
                      marker_line_width=1.5, opacity=1)
    fig.update_traces(texttemplate='%{text:.1s}')


    return fig



def import_export_figure_dynamic(df,product):

    fig = go.Figure()
    min = df['import_values'].min()
    min = min + 0.2 * min
    max = df['export_values'].max()
    max = max + 0.2 * max

    print(df)
    fig.add_trace(go.Bar(x=df['Country'], y=df['import_values'], name='Imports', marker_color='red',text = df['import_values'].round(decimals=2)))
    fig.add_trace(go.Bar(x=df['Country'], y=df['export_values'], name='Exports', marker_color='green',text = df['export_values'].round(decimals=2)))
    fig.update_layout(width=800,
        # height=500,
        barmode='relative')
    fig.update_layout(legend = dict(bgcolor = 'rgba(0,0,0,0)',    yanchor="bottom",orientation="v",
        y=0.5,
        xanchor="center",
        x=1.07),
                      font=dict(
                          family="Calibri",
                          size=16,
                          color="white"
                      )
                      )
    fig.update_layout({
    'plot_bgcolor': 'rgba(0,0,0,0)',
    'paper_bgcolor': 'rgba(0,0,0,0)',
    })
    fig.update_yaxes(title_text="Value ($MM)",showline=True)
    fig.update_xaxes(showline=True,title_text = "<a href=\"https://oec.world/en/home-b\"><sub>Source: The Observatory of Economic Complexity (OEC)<sub></a>")

    fig.update_layout(
        title="{}".format(product))
    fig.update_traces(marker_line_color='white',
                      marker_line_width=1.5, opacity=1)
    # fig.update_traces(texttemplate='%{text:.1s}')
    fig.update_layout(
        yaxis_range=[min-5, max+5]
    )

    return fig


def Solar_physical_resources():
    import plotly.graph_objs as go
    names = ['Wind', 'PV']
    df = pd.read_excel('Data/Potentials.xlsx')

    countries = Country_List
    Wind_pot = df.iloc[2, 2:]  # GWh/MW/year
    PV_pot = df.iloc[0, 2:]  # GWh/MW/year
    fig = go.Figure(data=[go.Bar(
        x=countries,
        y=PV_pot,

    )])
    fig.update_layout(
        title="Available solar resources")
    fig.update_yaxes(title_text="GWh/MW/year",showline=True)
    fig.update_xaxes(showline=True)

    fig.update_layout({'plot_bgcolor': 'rgba(0,0,0,0)',
    'paper_bgcolor': 'rgba(0,0,0,0)'})
    # fig.update_layout(yaxis_range=[0, max_range])

    fig.update_layout(#height=350,
                      font=dict(
                          family="Calibri",
                          size=15,
                          color="white"
                      ))
    fig.update_traces(marker_color='Yellow', marker_line_color='white',
                      marker_line_width=2, opacity=1)


    fig2 = go.Figure(data=[go.Bar(
        x=countries,
        y=Wind_pot,

    )])
    fig2.update_layout(
        title="Available wind resources")
    fig2.update_yaxes(title_text="GWh/MW/year",showline=True)
    fig2.update_xaxes(showline=True)

    fig2.update_layout({'plot_bgcolor': 'rgba(0,0,0,0)',
    'paper_bgcolor': 'rgba(0,0,0,0)'})
    # fig.update_layout(yaxis_range=[0, max_range])

    fig2.update_layout(#height=350,
                       font=dict(
                          family="Calibri",
                          size=15,
                          color="white"
                      ))
    fig2.update_traces(marker_color='lightblue', marker_line_color='white',
                      marker_line_width=2, opacity=1)

    return fig,fig2



def diesel_petrol_price(Fuel):
    import plotly.graph_objs as go
    df = pd.read_csv("Data/{}.csv".format(Fuel)) #USD c/Litre



    fig = go.Figure()
    fig.add_trace(go.Bar(x=df['Country'], y=df['Tax excluded'],name='Tax excluded',marker_color='forestgreen'))
    fig.add_trace(go.Bar(x=df['Country'], y=df['Tax'],name='Tax',marker_color='red'))


    fig.update_layout(
        title="Regional {} retail price for quarter 1, 2022 ".format(Fuel))
    fig.update_yaxes(title_text="US cents/Litre",showline=True)
    # fig.update_xaxes(showline=True)

    fig.update_layout({'plot_bgcolor': 'rgba(0,0,0,0)',
    'paper_bgcolor': 'rgba(0,0,0,0)'})
    # fig.update_layout(yaxis_range=[0, max_range])

    fig.update_layout(#height=350,
                      font=dict(
                          family="Calibri",
                          size=15,
                          color="white"
                      ),
                        barmode='relative')
    fig.update_traces(marker_line_color='white',
                      marker_line_width=2, opacity=1)
    fig.update_layout(legend = dict(bgcolor = 'rgba(0,0,0,0)',    yanchor="bottom",orientation="h",
        y=1.05,
        xanchor="center",
        x=0.5))
    fig.update_xaxes(showline=True,title_text = "<a href=\"https://www.haletwomey.co.nz/\"><sub>Source: Pacific Islands fuel supply, demand and comparison of regional prices 2022, Hale&Twomey <sub></a>")

    return fig


def elec_price_plot():
    import plotly.graph_objs as go
    df = pd.read_csv("Data/elec Price and subsidies.csv") #USD c/Litre



    fig = go.Figure()
    fig.add_trace(go.Bar(x=df['Country'], y=df['small res'],name='Residential consumer, 1.1 kVA, 60 kWh/month',marker_color='forestgreen'))
    fig.add_trace(go.Bar(x=df['Country'], y=df['res'],name='Residential consumer, 3.3 kVA, 300 kWh/month',marker_color='yellow'))
    fig.add_trace(go.Bar(x=df['Country'], y=df['res'],name='Business consumer, 100 kVA, 10,000 kWh/month',marker_color='red'))



    fig.update_layout(
        title="Regional electricity retail price in 2019")
    fig.update_yaxes(title_text="USD/kWh",showline=True)
    fig.update_xaxes(showline=True)

    fig.update_layout({'plot_bgcolor': 'rgba(0,0,0,0)',
    'paper_bgcolor': 'rgba(0,0,0,0)'})
    fig.update_layout(#height=350,
                      font=dict(
                          family="Calibri",
                          size=15,
                          color="white"
                      ),
                        )
    fig.update_traces(marker_line_color='white',
                      marker_line_width=2, opacity=1)
    fig.update_layout(legend = dict(bgcolor = 'rgba(0,0,0,0)',    yanchor="bottom",orientation="h",
        y=1.05,
        xanchor="center",
        x=0.5))
    fig.update_xaxes(showline=True,title_text = "<a href=\"chrome-extension://efaidnbmnnnibpcajpcglclefindmkaj/http://ura.gov.vu/attachments/article/67/Comparative%20Report%20-%20Pacific%20Region%20Electricity%20Bills%20June%202016.pdf\"><sub>Source: Pacific Region Electricity Bills 2019, Utilities Regulatory Authority (URA) <sub></a>")

    return fig
