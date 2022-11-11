import pandas as pd
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import plotly.express as px
import functions
from EnergyFlows import Country_List
import warnings
warnings.filterwarnings('ignore')
font_color = 'black'
line_color = 'black'

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
    df_GDP['net_imp_to_GDP'] = df_GDP['net_imp_to_GDP'].round(1)
    df_GDP['net_imp_per_capita'] = df_GDP['Imp']*1000000/df_GDP['Population'] #$ per capita
    df_GDP['net_imp_per_capita'] = df_GDP['net_imp_per_capita'].round(0)
    # df_GDP['net_imp_per_capita'] = df_GDP['net_imp_per_capita']
    fig = go.Figure()
    fig.add_trace(go.Bar(x=df_GDP['Country'], y=df_GDP['net_imp_to_GDP'],text=df_GDP['net_imp_to_GDP'],name='',marker_color='forestgreen'))
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
                          color=font_color
                      )
                      )
    fig.update_layout({
    'plot_bgcolor': 'rgba(0,0,0,0)',
    'paper_bgcolor': 'rgba(0,0,0,0)',
    })
    fig.update_yaxes(title_text="% of GDP",showline=True,linecolor=line_color,gridcolor=line_color)
    fig.update_xaxes(showline=True,linecolor=line_color,
                     title_text="<a href=\"https://oec.world/en/home-b\"><sub>Source: The Observatory of Economic Complexity (OEC)<sub></a>")

    fig.update_layout(
        title="Ratio of net imported petroleum products to GDP")
    # print(summary_df)
    fig.update_traces(marker_line_color=font_color,
                      marker_line_width=1.5, opacity=1)



    fig2 = go.Figure()
    fig2.add_trace(go.Bar(x=df_GDP['Country'], y=df_GDP['net_imp_per_capita'],text=df_GDP['net_imp_per_capita'],name='dasdsa',marker_color='forestgreen'))
    fig2.update_layout(#width=1500,
        # height=500,
        barmode='relative')
    fig2.update_layout(legend = dict(bgcolor = 'rgba(0,0,0,0)',    yanchor="bottom",orientation="h",
        y=1.05,
        xanchor="center",
        x=0.5),
                      font=dict(
                          family="Calibri",
                          size=16,
                          color=font_color
                      )
                      )
    fig2.update_layout({
    'plot_bgcolor': 'rgba(0,0,0,0)',
    'paper_bgcolor': 'rgba(0,0,0,0)',
    })
    fig2.update_yaxes(title_text="$ per capita",showline=True,linecolor=line_color,gridcolor=line_color)
    fig2.update_xaxes(showline=True,linecolor=line_color,
                     title_text="<a href=\"https://oec.world/en/home-b\"><sub>Source: The Observatory of Economic Complexity (OEC)<sub></a>")

    fig2.update_layout(
        title="Imported petroleum products per capita")
    # print(summary_df)
    fig2.update_traces(marker_line_color=font_color,
                      marker_line_width=1.5, opacity=1)

    return [fig,fig2]


def import_export_figure(df_imp,df_exp,Interest_list,year):
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
                          color=font_color
                      )
                      )
    fig.update_layout({
    'plot_bgcolor': 'rgba(0,0,0,0)',
    'paper_bgcolor': 'rgba(0,0,0,0)',
    })
    fig.update_yaxes(title_text="Value ($MM)",showline=True,linecolor=line_color,gridcolor=line_color)
    fig.update_xaxes(showline=True,linecolor=line_color,
                     title_text = "<a href=\"https://oec.world/en/home-b\"><sub>Source: The Observatory of Economic Complexity (OEC)<sub></a>")

    fig.update_layout(
        title="{}, Total Imports = {}, Total Exports = {} ($million)".format(year,totalImports,totalExports))
    fig.update_traces(marker_line_color=font_color,
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
                      )
    fig.update_layout(height=900,font=dict(
                          family="Calibri",
                          size=22,
                          color=font_color
                      ))
    fig.update_layout({'plot_bgcolor': 'rgba(0,0,0,0)',
    'paper_bgcolor': 'rgba(0,0,0,0)'},)

    fig2.update_layout(height=400,font=dict(
                          family="Calibri",
                          size=22,
                          color=font_color
                      ))
    fig2.update_layout({'plot_bgcolor': 'rgba(0,0,0,0)',
    'paper_bgcolor': 'rgba(0,0,0,0)'},)
    fig2.update_layout(title_text="Sankey Plot for the electricity sector <br><a href=\"http://unstats.un.org/unsd/energystats/pubs/balance\"><sub>Source: Energy Balances, United Nations<sub></a>",
                       )

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
    fig.update_yaxes(title_text="MW",showline=True,linecolor=line_color,gridcolor=line_color)
    fig.update_xaxes(showline=True,linecolor=line_color)

    fig.update_layout(yaxis_range=[0, max_range])

    fig.update_layout({'plot_bgcolor': 'rgba(0,0,0,0)',
    'paper_bgcolor': 'rgba(0,0,0,0)'})

    fig.update_layout(height=350,font=dict(
                          family="Calibri",
                          size=16,
                          color=font_color
                      ))
    fig.update_traces(marker_color='lightsalmon', marker_line_color=font_color,
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
    fig.update_layout({'plot_bgcolor': 'rgba(0,0,0,0)',
                       'paper_bgcolor': 'rgba(0,0,0,0)'})
    fig.update_layout(#height=500,
                      font=dict(
        family="Calibri",
        size=16,
        color=font_color
    ))
    fig.update_traces(marker_color='lightsalmon', marker_line_color=font_color,
                      marker_line_width=2.5, opacity=1)
    fig.update_xaxes(showgrid=False,showline=True,linecolor=line_color)
    fig.update_yaxes(title_text="GWh",showgrid=True,showline=True,linecolor=line_color,gridcolor=line_color)
    return fig


def decarbonization_scenarios(Country,Efficiency,oil_imports_2019,demand,growth_rate,PV_cost,rooftop_PV_cost,res_batt_cost,WindBatt_cost,Wind_cost,decarb_year,
                              total_wind_share,small_PV_share,small_wind_share,
                              PV_pot,Wind_pot,diesel_HHV,diesel_price,
                              geothermal_switch,geothermal_completion_year,geothermal_MW,geothermal_CF,geothermal_CAPEX,
                              discount_rate,inflation_rate,
                              emission_tonneperMWh,
                              CommBattery_size,CommBatery_cost,switch_battery,
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
    years= decarb_year - 2022

    total_battery_cost =  CommBatery_cost * CommBattery_size
    installment_comm_battery = total_battery_cost/(years+1)
    # demand_df['Battery_inst_cost'][demand_df['Year'] == CommBattery_year] = CommBatery_cost*CommBattery_size #Million Dollar
    demand_df['Battery_inst_cost'][demand_df['Year'] <= decarb_year] = installment_comm_battery #Million Dollar per year

    demand_df['RE_cumulative'][demand_df['Year']==decarb_year] = demand_df['Demand'][demand_df['Year']==decarb_year] #GWh
    demand_df['Geothermal_inst'][demand_df['Year'] == geothermal_completion_year] = geothermal_MW #MW
    demand_df['Geothermal_GWh'][demand_df['Year'] >= geothermal_completion_year] = geothermal_GWh #GWh
    demand_df['Geothermal_inst_cost'][demand_df['Year'] <= geothermal_completion_year] = \
        (geothermal_MW * geothermal_CAPEX*1000000)/(geothermal_completion_year-2022+1)#$Dollar


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
    demand_df['PV_inst'] = ((demand_df['Annual_RE'] * total_PV_share)/PV_pot) #MW
    demand_df['wind_inst'] = (demand_df['Annual_RE'] * total_wind_share)/Wind_pot #MW

    demand_df['Small PV+B'] = (demand_df['PV_inst'] * small_PV_share)/0.7 #MW #30% less performance for rooftop
    demand_df['Large PV'] = demand_df['PV_inst'] * large_PV_share #MW
    demand_df['Small Wind+B'] = demand_df['wind_inst'] * small_wind_share #MW
    demand_df['Large Wind'] = demand_df['wind_inst'] * large_wind_share #MW

    # demand_df['RE_inst_cost'] = (1000000 * (demand_df['PV_inst'] * (small_PV_share*rooftop_PV_cost+large_PV_share*PV_cost) )+\
    #                             1000000 * demand_df['wind_inst'] * (small_wind_share*WindBatt_cost+large_wind_share*Wind_cost)+ \
    #                             demand_df['Geothermal_inst_cost']+
    #                              demand_df['Battery_inst_cost']*1000000)/1000000 #M$
    demand_df['RE_inst_cost'] = (1000000 * (demand_df['Small PV+B'] *rooftop_PV_cost + demand_df['Small PV+B'] * 2 * res_batt_cost + demand_df['Large PV'] *PV_cost)+\
                                1000000 * demand_df['wind_inst'] * (small_wind_share*WindBatt_cost+large_wind_share*Wind_cost)+ \
                                demand_df['Geothermal_inst_cost']+
                                 demand_df['Battery_inst_cost']*1000000)/1000000 #M$


    demand_df["non_RE_demand_TJ"] = (demand_df['Demand'] - demand_df['RE_cumulative']-demand_df['Geothermal_GWh'])/0.2777
    demand_df['non_RE_demand_TJ'][demand_df['non_RE_demand_TJ'] < 0] = 0
    demand_df["diesel_litre_dec"] = demand_df["non_RE_demand_TJ"] / (diesel_HHV*Efficiency) # L
    demand_df["diesel_cost_dec"] = demand_df["diesel_litre_dec"] * diesel_price / 1000000  # $MM
    demand_df["diesel_litre_bs"] = (demand_df["Demand"]/0.2777) / (diesel_HHV * Efficiency)
    demand_df["diesel_cost_bs"] = demand_df["diesel_litre_bs"] * diesel_price / 1000000  # $MM

    if Country =="New Caledonia":
        #coal price is 400 USD/Tonne
        demand_df["diesel_cost_dec"] = demand_df["diesel_cost_dec"]/2
        demand_df['Coal_dec_tonne'] = demand_df["non_RE_demand_TJ"] / 0.02931  # 0.02931TJ = 1 tonne of coal
        demand_df['Coal_dec_tonne'] = demand_df['Coal_dec_tonne']/2
        demand_df["coal_dec_mdollar"] = demand_df["Coal_dec_tonne"] * 400 /1000000
        demand_df["diesel_cost_bs"] = demand_df["diesel_cost_bs"]/2
        demand_df["coal_bs_tonne"] = (demand_df["Demand"]/0.2777)/0.02931  # 0.02931TJ = 1 tonne of coal
        demand_df["coal_bs_tonne"]= demand_df["coal_bs_tonne"] / 2 #0.5 total demand is met by coal
        demand_df["coal_bs_mdollar"] = demand_df["coal_bs_tonne"] * 400 /1000000

        demand_df["diesel_cost_bs"] = demand_df["diesel_cost_bs"] + demand_df["coal_bs_mdollar"]
        demand_df["diesel_cost_dec"] = demand_df["diesel_cost_dec"] + demand_df["coal_dec_mdollar"]

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
        demand_df.at[i,'Net_saving_discounted'] = demand_df.at[i,'Net_saving'] * ((1+inflation_rate)/(1+discount_rate))**i
        demand_df.at[i,'Emission_red_saving_discounted'] = demand_df.at[i,'Emission_red_saving'] * ((1+inflation_rate)/(1+discount_rate))**i
    demand_df['Net_saving_cumsum'] = demand_df['Net_saving_discounted'].cumsum()
    demand_df['Net_saving_emission_cumsum'] = demand_df['Emission_red_saving_discounted'].cumsum()

    fig=go.Figure()
    fig.add_trace(
        go.Bar(x=demand_df['Year'], y=demand_df['Net_saving_discounted'], name="Annual net saving",marker_color='forestgreen'),
    )
    # fig.add_trace(
    #     go.Bar(x=demand_df['Year'], y=demand_df['Emission_red_saving_discounted'], name="Annual savings from emissions",marker_color='lightsalmon'),
    # )

    fig.update_yaxes(title_text="Annual Saving ($m)",  showline=True, showgrid=False,linecolor=line_color,gridcolor=line_color,rangemode='tozero')
    fig.update_xaxes(showgrid=False, showline=True,linecolor=line_color)
    fig.update_layout(height=350, font=dict(
        family="Calibri",
        size=16,
        color=font_color
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
    fig.update_traces(marker_line_color=font_color,
                      marker_line_width=1.5, opacity=1)
    fig.update_layout(
        title="Annual savings by achieving 100% RE in {}".format(decarb_year))
    fig.update_layout(barmode='relative')

############################################################################################
    ########################################################################################

    fig2 = go.Figure()
    fig2.add_trace(
        go.Bar(x=year_list, y=demand_df['Net_saving_cumsum'], name="Cumulative net saving"
               ,marker_color='forestgreen'),
    )
    # fig2.add_trace(
    #     go.Bar(x=year_list, y=demand_df['Net_saving_emission_cumsum'], name="Cumulative saving from emissions",
    #            marker_color='lightsalmon'),
    # )

    fig2.update_yaxes(title_text="Cumulative Saving ($m)", showline=True, showgrid=False,linecolor=line_color,gridcolor=line_color)
    fig2.update_xaxes(showgrid=False, showline=True,linecolor=line_color)

    fig2.update_layout(height=350, font=dict(
        family="Calibri",
        size=16,
        color=font_color
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
    fig2.update_traces(marker_line_color=font_color,
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
                           color=font_color
                       )
                       )
    fig3.update_layout({
        'plot_bgcolor': 'rgba(0,0,0,0)',
        'paper_bgcolor': 'rgba(0,0,0,0)',
    })
    fig3.update_yaxes(title_text="Installed Capacity (MW)", showline=True,linecolor=line_color,gridcolor=line_color)
    fig3.update_xaxes(showline=True,linecolor=line_color)

    fig3.update_layout(
        title="Breakdown of annual RE installation for 100% RE in {}".format(decarb_year))
    fig3.update_traces(marker_line_color=font_color,
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
                           color=font_color
                       )
                       )
    fig4.update_layout({
        'plot_bgcolor': 'rgba(0,0,0,0)',
        'paper_bgcolor': 'rgba(0,0,0,0)',
    })
    fig4.update_yaxes(title_text="Annual (t CO2-e)", showline=True,linecolor=line_color,gridcolor=line_color)
    fig4.update_yaxes(title_text="Cumulative (t CO2-e)", secondary_y=True, showline=True, showgrid=False,linecolor=line_color,gridcolor=line_color)

    fig4.update_xaxes(showline=True,linecolor=line_color)

    fig4.update_layout(
        title="Annaul CO2-e emission reduction by achieving 100% RE in {}".format(decarb_year))
    # print(summary_df)
    fig4.update_traces(marker_line_color=font_color,
                       marker_line_width=1.5, opacity=1)


    fig5 = make_subplots(specs=[[{"secondary_y": True}]])

    # fig4 = go.Figure()
    fig5.add_trace(go.Bar(x=demand_df['Year'], y=demand_df['Diesel_import_reduction'], name='Annual',
                          marker_color='forestgreen'))
    fig5.add_trace(go.Scatter(x=demand_df['Year'], y=demand_df['Diesel_import_reduction'].cumsum(), name='Cumulative',
                          marker_color='lightsalmon',),secondary_y=True)
    fig5.add_trace(go.Scatter(x=demand_df['Year'], y=[oil_imports_2019]*len(demand_df['Year']), name='Net oil products import in 2019',
                          marker_color='red'),secondary_y=False)

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
                           color=font_color
                       )
                       )
    fig5.update_layout({
        'plot_bgcolor': 'rgba(0,0,0,0)',
        'paper_bgcolor': 'rgba(0,0,0,0)',
    })
    fig5.update_yaxes(title_text="Annual (million Litre)", showline=True,linecolor=line_color,gridcolor=line_color)
    fig5.update_yaxes(title_text="Cumulative (million Litre)", secondary_y=True, showline=True, showgrid=False,linecolor=line_color,gridcolor=line_color)
    fig5.update_xaxes(showline=True,linecolor=line_color)

    fig5.update_layout(
        title="Diesel import reduction by achieving 100% RE in {}".format(decarb_year))
    # print(summary_df)
    fig5.update_traces(marker_line_color=font_color,
                       marker_line_width=1.5, opacity=1)

    return [fig,fig2,fig3,fig4,fig5]


def rooftop_PV_plot(available_buildings,PV_size):
    # import pandas as pd
    # rooftop_df = pd.DataFrame()
    # df = pd.read_csv('Data/Rooftop Potential.csv')
    # Countries = df['Country']
    # Population = df['Population']
    # Household_size = df['Household size']
    # solar_radiation = df['Potential of Av.PV gen (GWh/MW/year)']
    # number_of_homes = available_buildings*Population/Household_size # only those homes with rooftop PV potential
    # number_of_homes = number_of_homes.round(0)
    # rooftop_capacity_MW = number_of_homes * PV_size/1000
    # rooftop_capacity_MW = rooftop_capacity_MW.round(1)
    # rooftop_PV_generation_GWh = rooftop_capacity_MW * solar_radiation
    # rooftop_PV_generation_GWh = rooftop_PV_generation_GWh.astype(float)
    # rooftop_PV_generation_GWh = rooftop_PV_generation_GWh.round(decimals=1)
    # 
    # rooftop_df['Generation_GWh'] = rooftop_PV_generation_GWh
    # rooftop_df['Country'] = Countries
    # 
    # rooftop_df.to_csv('rooftop_Pv_potential.csv')

    rooftop_df = functions.calculate_rooftop_PV_potential(available_buildings=available_buildings,PV_size=PV_size)

    fig = make_subplots(specs=[[{"secondary_y": True}]])
    fig.add_trace(
        go.Bar(x=rooftop_df['Country'], y=rooftop_df['Population'], name="Population",marker_color='forestgreen'),
        secondary_y=False,
    )
    fig.add_trace(
        go.Scatter(x=rooftop_df['Country'], y=rooftop_df['Household_size'], name="Average household size",marker_color='red',mode='markers'),
        secondary_y=True,)
    fig.update_yaxes(title_text="Population", secondary_y=False,showline=True,showgrid=True,linecolor=line_color,gridcolor=line_color)
    fig.update_yaxes(title_text="Average household size", secondary_y=True,showline=True, showgrid=True,linecolor=line_color,gridcolor=line_color)
    fig.update_xaxes(showgrid=False,showline=True,linecolor=line_color)
    fig.update_layout(
                      font=dict(
                          family="Calibri",
                          size=16,
                          color=font_color
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
    fig.update_traces(marker_line_color=font_color,
                      marker_line_width=1.5, opacity=1)
    fig.update_layout(
        title="Population and average households size")
    fig.update_xaxes(showline=True,linecolor=line_color,
                     title_text="<a href=\"http://purl.org/spc/digilib/doc/z8n4m\"><sub>Source: 2020 Pacific Populations, SPC<sub></a>")
    fig.update_layout(#width=1500,
        # height=500,
        barmode='group')
    fig2 = make_subplots(specs=[[{"secondary_y": True}]])
    fig2.add_trace(
        go.Bar(x=rooftop_df['Country'], y=rooftop_df['avaialble_homes'],text=rooftop_df['avaialble_homes'], name="Number of homes available for rooftop PV",marker_color='forestgreen'),
        secondary_y=False,
    )
    fig2.update_yaxes(title_text="Number of homes available for rooftop PV", secondary_y=False,showline=True,showgrid=True,linecolor=line_color,gridcolor=line_color)
    fig2.update_xaxes(showgrid=False,showline=True,linecolor=line_color)

    fig2.update_layout(#height=350,
                      font=dict(
                          family="Calibri",
                          size=16,
                          color=font_color
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
    fig2.update_traces(marker_line_color=font_color,
                      marker_line_width=1.5, opacity=1)
    fig2.update_layout(
        title="Number of homes available for rooftop PV ")



    fig3 = make_subplots(specs=[[{"secondary_y": False}]])
    fig3.add_trace(
        go.Bar(x=rooftop_df['Country'], y=rooftop_df['Generation_GWh'],text=rooftop_df['Generation_GWh'], name="Potential rooftop PV generation (GWh)",marker_color='forestgreen'),
    )
    fig3.update_yaxes(title_text="Rooftop PV generation (GWh/year)", showline=True, showgrid=True,linecolor=line_color,gridcolor=line_color)
    fig3.update_xaxes(showgrid=False,showline=True,linecolor=line_color)

    fig3.update_layout(#height=350,
                      font=dict(
                          family="Calibri",
                          size=16,
                          color=font_color
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
    fig3.update_traces(marker_line_color=font_color,
                      marker_line_width=1.5, opacity=1)
    fig3.update_layout(
        title="Potential rooftop PV generation")


    fig4 = make_subplots(specs=[[{"secondary_y": False}]])
    fig4.add_trace(
        go.Bar(x=rooftop_df['Country'], y=rooftop_df['Capacity_MW'], text=rooftop_df['Capacity_MW'],name="Rooftop PV capacity",marker_color='forestgreen'),
    )

    fig4.update_yaxes(title_text="Potential rooftop PV capacity (MW)", secondary_y=False,showline=True,showgrid=True,linecolor=line_color,gridcolor=line_color)
    fig4.update_xaxes(showgrid=False,showline=True,linecolor=line_color)

    fig4.update_layout(#height=350,
                      font=dict(
                          family="Calibri",
                          size=16,
                          color=font_color
                      ),
        hovermode="x"
    )
    fig4.update_layout({'plot_bgcolor': 'rgba(0,0,0,0)',
                       'paper_bgcolor': 'rgba(0,0,0,0)'},
                      legend=dict(bgcolor='rgba(0,0,0,0)', yanchor="bottom", orientation="h",
                                  y=1.05,
                                  xanchor="center",
                                  x=0.5,
                      ))
    fig4.update_traces(marker_line_color=font_color,
                      marker_line_width=1.5, opacity=1)
    fig4.update_layout(
        title="Potential rooftop PV capacity")

    return [fig,fig2,fig3,fig4]




def UNstats_plots(year):
    summary_df = functions.all_countries_cross_comparison_unstats(2019,Unit='TJ',Use="SummaryPlot")
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
                          color=font_color
                      ),
                        hovermode = "x"
                      )
    fig.update_layout({
    'plot_bgcolor': 'rgba(0,0,0,0)',
    'paper_bgcolor': 'rgba(0,0,0,0)',
    })
    fig.update_yaxes(title_text="% of imported oil",showline=True,linecolor=line_color,gridcolor=line_color)
    fig.update_xaxes(showline=True,linecolor=line_color,
                     title_text="<a href=\"http://unstats.un.org/unsd/energystats/pubs/balance\"><sub>Source: Energy Balances, United Nations<sub></a>")

    fig.update_layout(
        title="% of imported oil consumed for international transit in {}".format(year))
    # print(summary_df)
    fig.update_traces(marker_line_color=font_color,
                      marker_line_width=1.5, opacity=1)

    fig2 = go.Figure()
    fig2.add_trace(go.Bar(x=summary_df['Country'], y=summary_df['transformation_to_import'], name='Transformation',
                         marker_color='forestgreen'))
    fig2.add_trace(go.Bar(x=summary_df['Country'], y=summary_df['transformation_losses_to_import'], name='Transformation losses',
                         marker_color='lightsalmon'))
    fig2.update_layout(legend=dict(bgcolor='rgba(0,0,0,0)', yanchor="bottom", orientation="h",
                                  y=1.05,
                                  xanchor="center",
                                  x=0.5),
                      font=dict(
                          family="Calibri",
                          size=16,
                          color=font_color
                      ),
                       hovermode="x"

                       )
    fig2.update_layout({
        'plot_bgcolor': 'rgba(0,0,0,0)',
        'paper_bgcolor': 'rgba(0,0,0,0)',
    })
    fig2.update_yaxes(title_text="% of imported oil", showline=True,linecolor=line_color,gridcolor=line_color)
    fig2.update_xaxes(showline=True, linecolor=line_color,
                      title_text="<a href=\"http://unstats.un.org/unsd/energystats/pubs/balance\"><sub>Source: Energy Balances, United Nations<sub></a>")

    fig2.update_layout(
        title="% of imported oil transformed into electricity and transformation losses in {}".format(year))
    fig2.update_traces(marker_line_color=font_color,
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
        barmode='relative')
    fig3.update_layout(legend=dict(bgcolor='rgba(0,0,0,0)', yanchor="bottom", orientation="h",
                                  y=0.98,
                                  xanchor="center",
                                  x=0.5),
                      font=dict(
                          family="Calibri",
                          size=16,
                          color=font_color
                      ),
                       hovermode="x"

                       )
    fig3.update_layout({
        'plot_bgcolor': 'rgba(0,0,0,0)',
        'paper_bgcolor': 'rgba(0,0,0,0)',
    })
    fig3.update_yaxes(title_text="% of imported oil", showline=True,linecolor=line_color,gridcolor=line_color)
    fig3.update_xaxes(showline=True,linecolor=line_color,
                      title_text="<a href=\"http://unstats.un.org/unsd/energystats/pubs/balance\"><sub>Source: Energy Balances, United Nations<sub></a>")

    fig3.update_layout(
        title="Breakdown of imported oil consumed for domestic transport in {}".format(year))
    fig3.update_traces(marker_line_color=font_color,
                      marker_line_width=1.5, opacity=1)

    fig4 = go.Figure()
    fig4.add_trace(go.Bar(x=summary_df['Country'], y=summary_df['Oil imports'], name='Oil imports',text=summary_df['Oil imports'],
                          marker_color='forestgreen'))

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
                           color=font_color
                       ),
                       hovermode="x"
                       )
    fig4.update_layout({
        'plot_bgcolor': 'rgba(0,0,0,0)',
        'paper_bgcolor': 'rgba(0,0,0,0)',
    })
    fig4.update_yaxes(title_text="TJ", showline=True, linecolor=line_color, gridcolor=line_color)
    fig4.update_xaxes(showline=True, linecolor=line_color,
                      title_text="<a href=\"http://unstats.un.org/unsd/energystats/pubs/balance\"><sub>Source: Energy Balances, United Nations<sub></a>")
    fig4.update_layout(
        title="Imported oil in {}".format(year))
    fig4.update_traces(marker_line_color=font_color,
                       marker_line_width=1.5, opacity=1)
    # fig4.update_traces(texttemplate='%{text:.1s}')

    fig5 = go.Figure()
    fig5.add_trace(go.Bar(x=summary_df['Country'], y=summary_df['Total_demand'], name='Total demand',text=summary_df['Total_demand'],
                          marker_color='forestgreen'))

    fig5.update_layout(legend=dict(bgcolor='rgba(0,0,0,0)', yanchor="bottom", orientation="h",
                                   y=0.98,
                                   xanchor="center",
                                   x=0.5),
                       font=dict(
                           family="Calibri",
                           size=16,
                           color=font_color
                       ),
                       hovermode="x"
                       )
    fig5.update_layout({
        'plot_bgcolor': 'rgba(0,0,0,0)',
        'paper_bgcolor': 'rgba(0,0,0,0)',
    })
    fig5.update_yaxes(title_text="TJ", showline=True, linecolor=line_color, gridcolor=line_color)
    fig5.update_xaxes(showline=True, linecolor=line_color,
                      title_text="<a href=\"http://unstats.un.org/unsd/energystats/pubs/balance\"><sub>Source: Energy Balances, United Nations<sub></a>")

    fig5.update_layout(
        title="Total demand (excluding int transit) in {}".format(year))
    # print(summary_df)
    fig5.update_traces(marker_line_color=font_color,
                       marker_line_width=1.5, opacity=1)
    fig5.update_traces(hovertemplate=None)



    fig6 = go.Figure()
    fig6.add_trace(go.Bar(x=summary_df['Country'], y=summary_df['renewables_in_total'], name='Total energy from renewables',text=summary_df['renewables_in_total'],
                          marker_color='forestgreen'))

    fig6.update_layout(legend=dict(bgcolor='rgba(0,0,0,0)', yanchor="bottom", orientation="h",
                                   y=0.98,
                                   xanchor="center",
                                   x=0.5),
                       font=dict(
                           family="Calibri",
                           size=16,
                           color=font_color
                       ),
                       hovermode="x"
                       )
    fig6.update_layout({
        'plot_bgcolor': 'rgba(0,0,0,0)',
        'paper_bgcolor': 'rgba(0,0,0,0)',
    })
    fig6.update_yaxes(title_text="TJ", showline=True, linecolor=line_color, gridcolor=line_color)
    fig6.update_xaxes(showline=True, linecolor=line_color,
                      title_text="<a href=\"http://unstats.un.org/unsd/energystats/pubs/balance\"><sub>Source: Energy Balances, United Nations<sub></a>")
    fig6.update_layout(
        title="Total renewable energy (electricity and final consumption) used in {}".format(year))
    # print(summary_df)
    fig6.update_traces(marker_line_color=font_color,
                       marker_line_width=1.5, opacity=1)
    fig6.update_traces(hovertemplate=None)

    fig7 = go.Figure()
    fig7.add_trace(go.Bar(x=summary_df['Country'], y=summary_df['renewable_electricity'], name='Total energy from renewables',text=summary_df['renewable_electricity'],
                          marker_color='forestgreen'))

    fig7.update_layout(legend=dict(bgcolor='rgba(0,0,0,0)', yanchor="bottom", orientation="h",
                                   y=0.98,
                                   xanchor="center",
                                   x=0.5),
                       font=dict(
                           family="Calibri",
                           size=16,
                           color=font_color
                       ),
                       hovermode="x"
                       )
    fig7.update_layout({
        'plot_bgcolor': 'rgba(0,0,0,0)',
        'paper_bgcolor': 'rgba(0,0,0,0)',
    })
    fig7.update_yaxes(title_text="TJ", showline=True, linecolor=line_color, gridcolor=line_color)
    fig7.update_xaxes(showline=True, linecolor=line_color,
                      title_text="<a href=\"http://unstats.un.org/unsd/energystats/pubs/balance\"><sub>Source: Energy Balances, United Nations<sub></a>")
    fig7.update_layout(
        title="Primary electricity production (wind, PV, hydro, geothermal) in {}".format(year))
    # print(summary_df)
    fig7.update_traces(marker_line_color=font_color,
                       marker_line_width=1.5, opacity=1)
    fig7.update_traces(hovertemplate=None)

    fig8 = go.Figure()
    fig8.add_trace(go.Bar(x=summary_df['Country'], y=summary_df['Renewables/Total_demand'], name='Total energy from renewables',text=summary_df['Renewables/Total_demand'],
                          marker_color='forestgreen'))

    fig8.update_layout(legend=dict(bgcolor='rgba(0,0,0,0)', yanchor="bottom", orientation="h",
                                   y=0.98,
                                   xanchor="center",
                                   x=0.5),
                       font=dict(
                           family="Calibri",
                           size=16,
                           color=font_color
                       ),
                       hovermode="x"
                       )
    fig8.update_layout({
        'plot_bgcolor': 'rgba(0,0,0,0)',
        'paper_bgcolor': 'rgba(0,0,0,0)',
    })
    fig8.update_yaxes(title_text="% of total demand", showline=True, linecolor=line_color, gridcolor=line_color)
    fig8.update_xaxes(showline=True, linecolor=line_color,
                      title_text="<a href=\"http://unstats.un.org/unsd/energystats/pubs/balance\"><sub>Source: Energy Balances, United Nations<sub></a>")
    fig8.update_layout(
        title="Contribution of renewables in total demand (excluding int transit) in {}".format(year))
    fig8.update_traces(marker_line_color=font_color,
                       marker_line_width=1.5, opacity=1)
    fig8.update_traces(hovertemplate=None)

    fig_re_imp = go.Figure()
    fig_re_imp.add_trace(go.Bar(x=summary_df['Country'], y=summary_df['Renewables/Total_imports'], name='Total energy from renewables',text=summary_df['Renewables/Total_imports'],
                          marker_color='forestgreen'))

    fig_re_imp.update_layout(legend=dict(bgcolor='rgba(0,0,0,0)', yanchor="bottom", orientation="h",
                                   y=0.98,
                                   xanchor="center",
                                   x=0.5),
                       font=dict(
                           family="Calibri",
                           size=16,
                           color=font_color
                       ),
                       hovermode="x"
                       )
    fig_re_imp.update_layout({
        'plot_bgcolor': 'rgba(0,0,0,0)',
        'paper_bgcolor': 'rgba(0,0,0,0)',
    })
    fig_re_imp.update_yaxes(title_text="% of total energy imports", showline=True, linecolor=line_color, gridcolor=line_color)
    fig_re_imp.update_xaxes(showline=True, linecolor=line_color,
                      title_text="<a href=\"http://unstats.un.org/unsd/energystats/pubs/balance\"><sub>Source: Energy Balances, United Nations<sub></a>")
    fig_re_imp.update_layout(
        title="Proportion of renewable  consumption to total energy imports in {}".format(year))
    fig_re_imp.update_traces(marker_line_color=font_color,
                       marker_line_width=1.5, opacity=1)
    fig_re_imp.update_traces(hovertemplate=None)
    fig_re_imp.write_image("renewables_to_total_imports.png")

    fig9 = go.Figure()
    fig9.add_trace(go.Bar(x=summary_df['Country'], y=summary_df['Renewables/capita'], name='Total energy from renewables',text=summary_df['Renewables/capita'],
                          marker_color='forestgreen'))

    fig9.update_layout(legend=dict(bgcolor='rgba(0,0,0,0)', yanchor="bottom", orientation="h",
                                   y=0.98,
                                   xanchor="center",
                                   x=0.5),
                       font=dict(
                           family="Calibri",
                           size=16,
                           color=font_color
                       ),
                       hovermode="x"
                       )
    fig9.update_layout({
        'plot_bgcolor': 'rgba(0,0,0,0)',
        'paper_bgcolor': 'rgba(0,0,0,0)',
    })
    fig9.update_yaxes(title_text="MJ per capita", showline=True, linecolor=line_color, gridcolor=line_color)
    fig9.update_xaxes(showline=True, linecolor=line_color,
                      title_text="<a href=\"http://unstats.un.org/unsd/energystats/pubs/balance\"><sub>Source: Energy Balances, United Nations<sub></a>")
    fig9.update_layout(
        title="Renewable energy consumption per capita in {}".format(year))
    fig9.update_traces(marker_line_color=font_color,
                       marker_line_width=1.5, opacity=1)
    fig9.update_traces(hovertemplate=None)

    return [fig,fig2,fig3,fig4,fig5,fig6,fig7,fig8,fig9]

def land_use_plot():
    summary_demand_df= pd.DataFrame()
    final_demand = functions.fetch_all_countries_demand(2019,Unit='GWh',Use='Analysis')[1]
    non_RE_demand = functions.fetch_all_countries_demand(2019,Unit='GWh',Use='Analysis')[9]
    countries = functions.fetch_all_countries_demand(2019,Unit='GWh',Use='Analysis')[0]
    non_RE_demand = non_RE_demand.round(0)
    final_demand=final_demand.round(0)
    world_average_demand = functions.fetch_all_countries_demand(2019,Unit='GWh',Use='Analysis')[11].round(0)

    summary_demand_df['countries'] = countries
    summary_demand_df['non-RE-GWh'] = non_RE_demand
    summary_demand_df['final-GWh'] = final_demand
    df_pop = pd.read_csv('Data/Economic Indicators.csv')

    df = pd.read_excel('Data/Potentials.xlsx')
    PV_pot = df.iloc[0, 2:] #GWh/MW/year
    Wind_CF =df.iloc[1, 2:]
    Wind_pot =df.iloc[2, 2:] #GWh/MW/year

    arable = df.iloc[4,2:]
    crops = df.iloc[5, 2:]
    pasture = df.iloc[6, 2:]
    forested = df.iloc[7, 2:]
    other =df.iloc[8, 2:]
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



    final_demand_per_capita = 1000 * final_demand/df_pop['Population']#MWh/year.person
    non_RE_demand_per_capita = 1000 * non_RE_demand/df_pop['Population']#MWh/year.person
    final_demand_per_capita = final_demand_per_capita.round(1)
    non_RE_demand_per_capita = non_RE_demand_per_capita.round(1)

    fig = make_subplots(specs=[[{"secondary_y": False}]])

    fig.add_trace(go.Scatter(x=countries, y=Wind_MW_non_RE, name='Decarbonizing the electricity sector',
                          marker_color='red', text = Wind_MW_non_RE,mode='markers',
                      ))
    fig.add_trace(go.Bar(x=countries, y=Wind_MW_final, name='Meeting the final demand',
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
                           color=font_color
                       ),
                      hovermode="x"
                      )
    fig.update_layout({
        'plot_bgcolor': 'rgba(0,0,0,0)',
        'paper_bgcolor': 'rgba(0,0,0,0)',
    })
    fig.update_yaxes(title_text="Wind capacity (MW)", showline=True,rangemode='tozero',linecolor=line_color,gridcolor=line_color)
    fig.update_xaxes(showline=True,showgrid=False,linecolor=line_color)
    fig.update_layout(
        title="Required wind capacity")
    # print(summary_df)
    fig.update_traces(marker_line_color=font_color,
                       marker_line_width=1.5, opacity=1)
    fig.update_traces(texttemplate='%{text:.1s}',)

    fig1 = make_subplots(specs=[[{"secondary_y": False}]])
    fig1.add_trace(go.Bar(x=countries, y=percentage_of_coastline_final, name='% coastline for final demand',
                          marker_color='black'))
    fig1.add_trace(
        go.Scatter(x=countries, y=percentage_of_coastline_non_RE, name='% coastline for decarbonizing the electricity sector',
                   marker_color='red',mode='markers'))
    fig1.update_layout(legend=dict(bgcolor='rgba(0,0,0,0)', yanchor="bottom", orientation="h",
                                   y=0.98,
                                   xanchor="center",
                                   x=0.5),
                       font=dict(
                           family="Calibri",
                           size=16,
                           color=font_color
                       ),
                       hovermode="x",
                       )
    fig1.update_layout({
        'plot_bgcolor': 'rgba(0,0,0,0)',
        'paper_bgcolor': 'rgba(0,0,0,0)',
    })
    fig1.update_xaxes(showline=True,showgrid=False,linecolor=line_color)
    fig1.update_layout(
        title="Coastline required for wind turbine installation")
    fig1.update_traces(marker_line_color=font_color,
                       marker_line_width=1.5, opacity=1)
    fig1.update_yaxes(title_text="% of coastline", showline=True, showgrid=True,rangemode='tozero',linecolor=line_color,gridcolor=line_color)
    fig2 = make_subplots(specs=[[{"secondary_y": False}]])
    fig2.add_trace(go.Scatter(x=countries, y=PV_non_RE, name='Decarbonizing the electricity sector',
                          marker_color='red',text = PV_non_RE,mode='markers',
                      ))
    fig2.add_trace(go.Bar(x=countries, y=PV_final_demand, name='Meeting the final demand',
                          marker_color='black',text = PV_final_demand,
                      ))
    fig2.update_layout(
        # height=500,
        barmode='relative')
    fig2.update_layout(legend=dict(bgcolor='rgba(0,0,0,0)', yanchor="bottom", orientation="h",
                                   y=0.98,
                                   xanchor="center",
                                   x=0.5),
                       font=dict(
                           family="Calibri",
                           size=16,
                           color=font_color
                       ),
                       hovermode="x"

                       )
    fig2.update_layout({
        'plot_bgcolor': 'rgba(0,0,0,0)',
        'paper_bgcolor': 'rgba(0,0,0,0)',
    })
    fig2.update_yaxes(title_text="PV capacity (MW)", showline=True,rangemode='tozero',linecolor=line_color,gridcolor=line_color)
    fig2.update_xaxes(showline=True,showgrid=False,linecolor=line_color,)
    fig2.update_layout(
        title="Required PV capacity")
    fig2.update_traces(marker_line_color=font_color,
                       marker_line_width=1.5, opacity=1)
    fig2.update_yaxes(rangemode='tozero',linecolor=line_color,gridcolor=line_color)
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
        barmode='relative')
    fig3.update_layout(legend=dict(bgcolor='rgba(0,0,0,0)', yanchor="bottom", orientation="h",
                                  y=0.94,
                                  xanchor="left",
                                  x=0),
                      font=dict(
                          family="Calibri",
                          size=14,
                          color=font_color
                      ),
                       hovermode="x"
                       )
    fig3.update_layout({
        'plot_bgcolor': 'rgba(0,0,0,0)',
        'paper_bgcolor': 'rgba(0,0,0,0)',
    })
    fig3.update_yaxes(title_text="% land", showline=True,rangemode='tozero',linecolor=line_color,gridcolor=line_color)
    fig3.update_xaxes(showline=True,linecolor=line_color,
                      title_text="<a href=\"https://www.cia.gov/the-world-factbook/countries\"><sub>Source: The World Factbook, CIA<sub></a>")
    fig3.update_traces(marker_line_color=font_color,
                      marker_line_width=1.5, opacity=1)
    fig3.update_layout(margin=dict(t=130))
    fig3.update_layout(
        title={
            'text': "Breakdown of  and area required for PV installation to meet the demand",
            'y': 0.95,
            # 'x': 0,
            'xanchor': 'left',
            'yanchor': 'top'})
    fig4 = make_subplots(specs=[[{"secondary_y": False}]])
    fig4.add_trace(go.Bar(x=countries, y=non_RE_demand,text=non_RE_demand, name='Decarbonizing the electricity sector',
                          marker_color='red',
                      ))
    fig4.add_trace(go.Bar(x=countries, y=final_demand,text=final_demand, name='Meeting the final demand',
                          marker_color='darkgrey',
                      ))
    fig4.add_trace(go.Bar(x=countries, y=world_average_demand,text=world_average_demand, name='World average per capita demand',
                          marker_color='green',
                      ))
    fig4.update_layout(legend=dict(bgcolor='rgba(0,0,0,0)', yanchor="bottom", orientation="h",
                                   y=0.98,
                                   xanchor="center",
                                   x=0.5),
                       font=dict(
                           family="Calibri",
                           size=16,
                           color=font_color
                       ),
                       hovermode="x"

                       )
    fig4.update_layout({
        'plot_bgcolor': 'rgba(0,0,0,0)',
        'paper_bgcolor': 'rgba(0,0,0,0)',
    })
    fig4.update_yaxes(title_text="Demand (GWh/year)", showline=True,rangemode='tozero',linecolor=line_color,gridcolor=line_color)
    fig4.update_xaxes(showline=True,showgrid=False,linecolor=line_color,)
    fig4.update_layout(
        title="Demand for decarbonization")
    fig4.update_traces(marker_line_color=font_color,
                       marker_line_width=0, opacity=1)
    fig4.update_yaxes(rangemode='tozero',linecolor=line_color,gridcolor=line_color)
    # fig4.update_traces(texttemplate='%{text:.1s}')


    fig5 = make_subplots(specs=[[{"secondary_y": False}]])
    fig5.add_trace(go.Bar(x=countries, y=non_RE_demand_per_capita,text=non_RE_demand_per_capita, name='Decarbonizing the electricity sector',
                          marker_color='red',
                      ))
    fig5.add_trace(go.Bar(x=countries, y=final_demand_per_capita,text=final_demand_per_capita, name='Meeting the final demand',
                          marker_color='darkgrey',
                      ))
    fig5.update_layout(legend=dict(bgcolor='rgba(0,0,0,0)', yanchor="bottom", orientation="h",
                                   y=0.98,
                                   xanchor="center",
                                   x=0.5),
                       font=dict(
                           family="Calibri",
                           size=16,
                           color=font_color
                       ),
                       hovermode="x"

                       )
    fig5.update_layout({
        'plot_bgcolor': 'rgba(0,0,0,0)',
        'paper_bgcolor': 'rgba(0,0,0,0)',
    })
    fig5.update_yaxes(title_text="Demand (MWh/year/person)", showline=True,rangemode='tozero',linecolor=line_color,gridcolor=line_color)
    fig5.update_xaxes(showline=True,showgrid=False,linecolor=line_color,)
    fig5.update_layout(
        title="Demand per capita")
    fig5.update_traces(marker_line_color=font_color,
                       marker_line_width=0, opacity=1)
    fig5.update_yaxes(rangemode='tozero',linecolor=line_color,gridcolor=line_color)

    return fig, fig1,fig2,fig3,fig4,fig5


def mapboxplot(Country,style):
    import math
    import plotly.graph_objects as go
    from math import sqrt, atan, pi
    import pyproj

    PV_area_non_RE, PV_area_final_demand,PV_area_net_zero,\
    PV_area_non_RE_per, PV_area_final_demand_per, PV_area_net_zero_per = functions.PV_area_single_country(Country,2019)
    width_decarb = math.sqrt(PV_area_non_RE) * 1000/2
    width_final_demand = math.sqrt(PV_area_final_demand) * 1000/2
    width_net_zero = math.sqrt(PV_area_net_zero) * 1000/2
    geod = pyproj.Geod(ellps='WGS84')
    Coordinates = {"Samoa": [-13.597336, -172.457458], "Nauru": [-0.5228, 166.9315], "Vanuatu": [-15.245988, 167.008684],
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
                      "PV area for decarbonizing the electricity sector: {} km2</b><br>".format(round(PV_area_non_RE,3)) +
                      "% of land: {}<extra></extra>".format(round(PV_area_non_RE_per,3)),
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
        marker=dict(size=16, color='black'),
        textposition='top left',
        # name = "asdsadad"
        textfont=dict(size=16, color='black'),
        hovertemplate="<b>{}</b><br><br>".format(Country) +
                      "PV area for final demand: {} km2</b><br>".format(round(PV_area_final_demand,3)) +
                      "% of land: {}<extra></extra>".format(round(PV_area_final_demand_per,3)),
        lon=[pt1_lon, pt2_lon, pt3_lon, pt4_lon, pt1_lon, ],
        lat=[pt1_lat, pt2_lat, pt3_lat, pt4_lat, pt1_lat],
    ))

    fig.update_layout(
        mapbox={'style': style, 'center': {'lon': center_lon, 'lat': center_lat}, 'zoom': 9},
        # add zoom as a slider
        showlegend=False,
        margin={'l': 0, 'r': 0, 'b': 0, 't': 0},
    )



    width = width_net_zero  # m
    height = width_net_zero  # m
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
        marker=dict(size=16, color='lightblue'),
        textposition='top left',
        # name = "asdsadad"
        textfont=dict(size=16, color='black'),
        hovertemplate="<b>{}</b><br><br>".format(Country) +
                      "PV area for final demand: {} km2</b><br>".format(round(PV_area_net_zero,3)) +
                      "% of land: {}<extra></extra>".format(round(PV_area_net_zero_per,3)),
        lon=[pt1_lon, pt2_lon, pt3_lon, pt4_lon, pt1_lon, ],
        lat=[pt1_lat, pt2_lat, pt3_lat, pt4_lat, pt1_lat],
    ))

    fig.update_layout(
        mapbox={'style': style, 'center': {'lon': center_lon, 'lat': center_lat}, 'zoom': 9},
        # add zoom as a slider
        showlegend=False,
        margin={'l': 0, 'r': 0, 'b': 0, 't': 0},
    )

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
                          color=font_color
                      )
                      )
    fig.update_layout({
        'plot_bgcolor': 'rgba(0,0,0,0)',
        'paper_bgcolor': 'rgba(0,0,0,0)',
    })
    fig.update_yaxes(title_text="% of total GWh generation", showline=True,linecolor=line_color,gridcolor=line_color)
    fig.update_xaxes(showline=True,linecolor=line_color,
                     title_text="<a href=\"https://www.irena.org/Statistics/Statistical-Profiles\"><sub>Source: Country Profiles, IRENA<sub></a>")

    fig.update_layout(
        title="Generation mix in 2019")
    # print(summary_df)
    fig.update_traces(marker_line_color=font_color,
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
                          color=font_color
                      )
                      )
    fig2.update_layout({
        'plot_bgcolor': 'rgba(0,0,0,0)',
        'paper_bgcolor': 'rgba(0,0,0,0)',
    })
    fig2.update_yaxes(title_text="% of total MW capacity", showline=True,linecolor=line_color,gridcolor=line_color)
    fig2.update_xaxes(showline=True,linecolor=line_color,
                      title_text="<a href=\"https://www.irena.org/Statistics/Statistical-Profiles\"><sub>Source: Country Profiles, IRENA<sub></a>")

    fig2.update_layout(
        title="Installed capacity mix in 2020")
    # print(summary_df)
    fig2.update_traces(marker_line_color=font_color,
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




def cross_country_sankey(df,from_,to_,normalization):
    if normalization ==1:
        Unit = "TJ"
        tail = "real values"

    elif normalization == ' (from)':
        Unit = "%"
        tail = 'normalized with origin'
    elif normalization == ' (to)':
        Unit = "%"
        tail = 'normalized with destination'
    fig = go.Figure()
    fig.add_trace(go.Bar(x=df['Country'], y=df['Values'],name='dasdsa',marker_color='forestgreen',text = df['Values']))
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
                          color=font_color
                      )
                      )
    fig.update_layout({
    'plot_bgcolor': 'rgba(0,0,0,0)',
    'paper_bgcolor': 'rgba(0,0,0,0)',

    })
    fig.update_yaxes(title_text=Unit,showline=True,linecolor=line_color,gridcolor=line_color)
    fig.update_xaxes(showline=True,linecolor=line_color,
                     title_text="<a href=\"http://unstats.un.org/unsd/energystats/pubs/balance\"><sub>Source: Energy Balances, United Nations<sub></a>"),

    fig.update_layout(
        title="From {} to {} ({})".format(from_,to_,tail))
    # print(summary_df)
    fig.update_traces(marker_line_color=font_color,
                      marker_line_width=1.5, opacity=1)
    # fig.update_traces(texttemplate='%{text:.1s}')


    return fig



def import_export_figure_dynamic(df,product):

    fig = go.Figure()
    min = df['import_values'].min()
    min = min + 0.2 * min
    max = df['export_values'].max()
    max = max + 0.2 * max
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
                          color=font_color
                      )
                      )
    fig.update_layout({
    'plot_bgcolor': 'rgba(0,0,0,0)',
    'paper_bgcolor': 'rgba(0,0,0,0)',
    })
    fig.update_yaxes(title_text="Value ($MM)",showline=True,linecolor=line_color,gridcolor=line_color)
    fig.update_xaxes(showline=True,linecolor=line_color,
                     title_text = "<a href=\"https://oec.world/en/home-b\"><sub>Source: The Observatory of Economic Complexity (OEC)<sub></a>")

    fig.update_layout(
        title="{}".format(product))
    fig.update_traces(marker_line_color=font_color,
                      marker_line_width=1.5, opacity=1)
    # fig.update_traces(texttemplate='%{text:.1s}')
    fig.update_layout(
        yaxis_range=[min-10, max+5]
    )

    return fig


def Solar_physical_resources():
    import plotly.graph_objs as go
    df_technical_potential = functions.calculate_PV_Wind_potential(available_land=0.02,available_coastline=0.1)



    fig = go.Figure(data=[go.Bar(
        x=df_technical_potential['Country'],
        y=df_technical_potential['PV_pot'],

    )])
    fig.update_layout(
        title="Available solar resources")
    fig.update_yaxes(title_text="GWh/MW/year",showline=True,linecolor=line_color,gridcolor=line_color)
    fig.update_xaxes(showline=True,linecolor=line_color,)

    fig.update_layout({'plot_bgcolor': 'rgba(0,0,0,0)',
    'paper_bgcolor': 'rgba(0,0,0,0)'})
    # fig.update_layout(yaxis_range=[0, max_range])

    fig.update_layout(#height=350,
                      font=dict(
                          family="Calibri",
                          size=15,
                          color=font_color
                      ))
    fig.update_traces(marker_color='Yellow', marker_line_color=font_color,
                      marker_line_width=2, opacity=1)


    fig2 = go.Figure(data=[go.Bar(
        x=df_technical_potential['Country'],
        y=df_technical_potential['Wind_pot'],

    )])
    fig2.update_layout(
        title="Available wind resources")
    fig2.update_yaxes(title_text="GWh/MW/year",showline=True,linecolor=line_color,gridcolor=line_color)
    fig2.update_xaxes(showline=True,linecolor=line_color)

    fig2.update_layout({'plot_bgcolor': 'rgba(0,0,0,0)',
    'paper_bgcolor': 'rgba(0,0,0,0)'})
    fig2.update_layout(#height=350,
                       font=dict(
                          family="Calibri",
                          size=15,
                          color=font_color
                      ))
    fig2.update_traces(marker_color='lightblue', marker_line_color=font_color,
                      marker_line_width=2, opacity=1)

    fig3 = go.Figure(data=[go.Bar(
        x=df_technical_potential['Country'],
        y=df_technical_potential['Wind_technical_GWh'],
        text=df_technical_potential['Wind_technical_GWh']
    )])
    fig3.update_layout(
        title="Technical wind generation")
    fig3.update_yaxes(title_text="GWh/year",showline=True,linecolor=line_color,gridcolor=line_color)
    fig3.update_xaxes(showline=True,linecolor=line_color)

    fig3.update_layout({'plot_bgcolor': 'rgba(0,0,0,0)',
    'paper_bgcolor': 'rgba(0,0,0,0)'})
    fig3.update_layout(#height=350,
                       font=dict(
                          family="Calibri",
                          size=15,
                          color=font_color
                      ))
    fig3.update_traces(marker_color='lightblue', marker_line_color=font_color,
                      marker_line_width=2, opacity=1)
    # fig3.update_traces(texttemplate='%{text:.1s}')

    fig4 = go.Figure(data=[go.Bar(
        x=df_technical_potential['Country'],
        y=df_technical_potential['Theoretical_PV_GWh'],
        text=df_technical_potential['Theoretical_PV_GWh']
    )])
    fig4.update_layout(
        title="Theoretical PV generation")
    fig4.update_yaxes(title_text="GWh/year",showline=True,linecolor=line_color,gridcolor=line_color)
    fig4.update_xaxes(showline=True,linecolor=line_color)
    fig4.update_layout({'plot_bgcolor': 'rgba(0,0,0,0)',
    'paper_bgcolor': 'rgba(0,0,0,0)'})
    fig4.update_layout(#height=350,
                       font=dict(
                          family="Calibri",
                          size=15,
                          color=font_color
                      ))
    fig4.update_traces(marker_color='yellow', marker_line_color=font_color,
                      marker_line_width=2, opacity=1)
    fig4.update_traces(texttemplate='%{text:.1s}')

    fig5 = go.Figure(data=[go.Bar(
        x=df_technical_potential['Country'],
        y=df_technical_potential['Theoretical_PV_GW'],
        text=df_technical_potential['Theoretical_PV_GW']
    )])
    fig5.update_layout(
        title="Theoretical PV capacity")
    fig5.update_yaxes(title_text="GW",showline=True,linecolor=line_color,gridcolor=line_color)
    fig5.update_xaxes(showline=True,linecolor=line_color)
    fig5.update_layout({'plot_bgcolor': 'rgba(0,0,0,0)',
    'paper_bgcolor': 'rgba(0,0,0,0)'})
    fig5.update_layout(#height=350,
                       font=dict(
                          family="Calibri",
                          size=15,
                          color=font_color
                      ))
    fig5.update_traces(marker_color='yellow', marker_line_color=font_color,
                      marker_line_width=2, opacity=1)

    fig6 = go.Figure(data=[go.Bar(
        x=df_technical_potential['Country'],
        y=df_technical_potential['Wind_technical_GW'],
        text=df_technical_potential['Wind_technical_GW']
    )])
    fig6.update_layout(
        title="Technical wind capacity")
    fig6.update_yaxes(title_text="GW",showline=True,linecolor=line_color,gridcolor=line_color)
    fig6.update_xaxes(showline=True,linecolor=line_color)
    fig6.update_layout({'plot_bgcolor': 'rgba(0,0,0,0)',
    'paper_bgcolor': 'rgba(0,0,0,0)'})
    fig6.update_layout(#height=350,
                       font=dict(
                          family="Calibri",
                          size=15,
                          color=font_color
                      ))
    fig6.update_traces(marker_color='lightblue', marker_line_color=font_color,
                      marker_line_width=2, opacity=1)

    fig7 = go.Figure(data=[go.Bar(
        x=df_technical_potential['Country'],
        y=df_technical_potential['PV_technical_GW'],
        text=df_technical_potential['PV_technical_GW']
    )])
    fig7.update_layout(
        title="Technical PV capacity")
    fig7.update_yaxes(title_text="GW", showline=True, linecolor=line_color, gridcolor=line_color)
    fig7.update_xaxes(showline=True, linecolor=line_color)
    fig7.update_layout({'plot_bgcolor': 'rgba(0,0,0,0)',
                        'paper_bgcolor': 'rgba(0,0,0,0)'})
    fig7.update_layout(  # height=350,
        font=dict(
            family="Calibri",
            size=15,
            color=font_color
        ))
    fig7.update_traces(marker_color='yellow', marker_line_color=font_color,
                       marker_line_width=2, opacity=1)
    # fig7.update_traces(texttemplate='%{text:.1s}')

    fig8 = go.Figure(data=[go.Bar(
        x=df_technical_potential['Country'],
        y=df_technical_potential['PV_technical_GWh'],
        text=df_technical_potential['PV_technical_GWh']
    )])
    fig8.update_layout(
        title="Technical PV generation")
    fig8.update_yaxes(title_text="GWh/year", showline=True, linecolor=line_color, gridcolor=line_color)
    fig8.update_xaxes(showline=True, linecolor=line_color)
    fig8.update_layout({'plot_bgcolor': 'rgba(0,0,0,0)',
                        'paper_bgcolor': 'rgba(0,0,0,0)'})
    fig8.update_layout(  # height=350,
        font=dict(
            family="Calibri",
            size=15,
            color=font_color
        ))
    fig8.update_traces(marker_color='yellow', marker_line_color=font_color,
                       marker_line_width=2, opacity=1)
    # fig8.update_traces(texttemplate='%{text:.1s}')

    return fig,fig2,fig3,fig4,fig5,fig6,fig7,fig8

def diesel_petrol_price(Fuel):
    import plotly.graph_objs as go
    df = pd.read_csv("Data/{}.csv".format(Fuel)) #USD c/Litre
    fig = go.Figure()
    fig.add_trace(go.Bar(x=df['Country'], y=df['Tax excluded'],name='Tax excluded',marker_color='forestgreen'))
    fig.add_trace(go.Bar(x=df['Country'], y=df['Tax'],name='Tax',marker_color='red'))


    fig.update_layout(
        title="Regional {} retail price for quarter 1, 2022 ".format(Fuel))
    fig.update_yaxes(title_text="US cents/Litre",showline=True,linecolor=line_color,gridcolor=line_color)
    fig.update_layout({'plot_bgcolor': 'rgba(0,0,0,0)',
    'paper_bgcolor': 'rgba(0,0,0,0)'})
    fig.update_layout(#height=350,
                      font=dict(
                          family="Calibri",
                          size=15,
                          color=font_color
                      ),
                        barmode='relative')
    fig.update_traces(marker_line_color=font_color,
                      marker_line_width=2, opacity=1)
    fig.update_layout(legend = dict(bgcolor = 'rgba(0,0,0,0)',    yanchor="bottom",orientation="h",
        y=1.05,
        xanchor="center",
        x=0.5))
    fig.update_xaxes(linecolor=line_color,showline=True,title_text = "<a href=\"https://www.haletwomey.co.nz/\"><sub>Source: Pacific Islands fuel supply, demand and comparison of regional prices 2022, Hale&Twomey <sub></a>")

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
    fig.update_yaxes(title_text="USD/kWh",showline=True,linecolor=line_color,gridcolor=line_color)

    fig.update_layout({'plot_bgcolor': 'rgba(0,0,0,0)',
    'paper_bgcolor': 'rgba(0,0,0,0)'})
    fig.update_layout(#height=350,
                      font=dict(
                          family="Calibri",
                          size=18,
                          color=font_color
                      ),
                        )
    fig.update_traces(marker_line_color=font_color,
                      marker_line_width=2, opacity=1)
    fig.update_layout(legend = dict(bgcolor = 'rgba(0,0,0,0)', yanchor="bottom",orientation="h",
        y=1.05,
        xanchor="center",
        x=0.5))
    fig.update_xaxes(showline=True,linecolor=line_color,
                     title_text = "<a href=\"chrome-extension://efaidnbmnnnibpcajpcglclefindmkaj/http://ura.gov.vu/attachments/article/67/Comparative%20Report%20-%20Pacific%20Region%20Electricity%20Bills%20June%202016.pdf\"><sub>Source: Pacific Region Electricity Bills 2019, Utilities Regulatory Authority (URA) <sub></a>")

    return fig

def per_capita_comparison():

    total_demand_electrified = functions.fetch_all_countries_demand(2019,Unit='GWh',Use='Analysis')[1]
    total_demand = functions.fetch_all_countries_demand(2019,Unit='GWh',Use='SummaryPlot')[1]

    non_RE_elec = functions.fetch_all_countries_demand(2019,Unit='GWh',Use='Analysis')[9] # Decarbonizing the electricity sector

    countries = functions.fetch_all_countries_demand(2019,Unit='GWh',Use='Analysis')[0]
    non_RE_elec = non_RE_elec.round(0)
    total_demand_electrified = total_demand_electrified.round(0)

    df_pop = pd.read_csv('Data/Economic Indicators.csv')

    total_demand_electrified_per_capita = 1000 * total_demand_electrified / df_pop['Population']  # MWh/year/person
    total_demand_per_capita = 1000 * total_demand / df_pop['Population'] # MWh/year/person
    non_RE_elec_per_capita = 1000 * non_RE_elec / df_pop['Population'] # MWh/year/person

    total_demand_electrified_per_capita = total_demand_electrified_per_capita.round(1)
    total_demand_per_capita = total_demand_per_capita.round(1)
    non_RE_elec_per_capita = non_RE_elec_per_capita.round(1)

    wolrd_per_capita_use = pd.read_csv('Data/worldinData/per-capita-energy-use.csv')
    wolrd_per_capita_use = wolrd_per_capita_use.sort_values('Year', ascending=False).drop_duplicates(['Entity'])
    wolrd_per_capita_use['Primary energy consumption per capita (kWh/person)'] = wolrd_per_capita_use['Primary energy consumption per capita (kWh/person)']/1000 #MWh/capita
    wolrd_average_per_capita_use = wolrd_per_capita_use['Primary energy consumption per capita (kWh/person)'].mean()
    wolrd_median_per_capita_use = wolrd_per_capita_use['Primary energy consumption per capita (kWh/person)'].median()

    wolrd_per_capita_use['Entity'] = wolrd_per_capita_use['Entity'].replace('Micronesia (country)','Micronesia')
    wolrd_per_capita_use['Entity'] = wolrd_per_capita_use['Entity'].replace('Papua New Guinea','PNG')

    wolrd_per_capita_use = wolrd_per_capita_use[wolrd_per_capita_use.Entity.isin(Country_List)]
    wolrd_per_capita_use['Primary energy consumption per capita (kWh/person)'] = wolrd_per_capita_use['Primary energy consumption per capita (kWh/person)'].round(1)

    fig_use_cap = make_subplots(specs=[[{"secondary_y": False}]])
    fig_use_cap.add_trace(go.Bar(x=countries, y=non_RE_elec_per_capita,text=non_RE_elec_per_capita, name='Decarbonizing the electricity sector-this research',
                          marker_color='red',
                      ))
    fig_use_cap.add_trace(go.Bar(x=countries, y=total_demand_electrified_per_capita,text=total_demand_electrified_per_capita, name='Final electrified demand-this research',
                          marker_color='green',
                      ))
    fig_use_cap.add_trace(go.Bar(x=countries, y=total_demand_per_capita,text=total_demand_per_capita, name='Total demand-this research',
                          marker_color='blue',
                      ))
    fig_use_cap.add_trace(go.Bar(x=wolrd_per_capita_use['Entity'], y=wolrd_per_capita_use['Primary energy consumption per capita (kWh/person)'],text=wolrd_per_capita_use['Primary energy consumption per capita (kWh/person)'], name='Total demand-our world in data',
                          marker_color='orange',
                      ))
    fig_use_cap.add_shape(
        type='line', line=dict(dash='dot', color='red'),
        x0=0, x1=len(countries), y0=wolrd_average_per_capita_use, y1=wolrd_average_per_capita_use
    )
    fig_use_cap.add_shape(
        type='line', line=dict(dash='dot', color='orange'),
        x0=0, x1=len(countries), y0=wolrd_median_per_capita_use, y1=wolrd_median_per_capita_use
    )
    fig_use_cap.update_layout(legend=dict(bgcolor='rgba(0,0,0,0)', yanchor="bottom", orientation="h",
                                   y=0.98,
                                   xanchor="center",
                                   x=0.5),
                       font=dict(
                           family="Calibri",
                           size=18,
                           color=font_color
                       ),
                       hovermode="x"

                       )
    fig_use_cap.add_annotation(x=0.5, y=wolrd_average_per_capita_use+4,
                       text="World average = {}".format(wolrd_average_per_capita_use.round(1)),
                       showarrow=False, font=dict(
                color=font_color,
                size=18
            ),
                       )
    fig_use_cap.add_annotation(x=0.5, y=wolrd_median_per_capita_use+4,
                       text="World median = {}".format(wolrd_median_per_capita_use.round(1)),
                       showarrow=False, font=dict(
                color=font_color,
                size=18
            ),
                       )
    fig_use_cap.update_layout({
        'plot_bgcolor': 'rgba(0,0,0,0)',
        'paper_bgcolor': 'rgba(0,0,0,0)',
    })
    fig_use_cap.update_yaxes(title_text="Demand (MWh/year/person)", showline=True,rangemode='tozero',linecolor=line_color,gridcolor=line_color)
    fig_use_cap.update_xaxes(showline=True,showgrid=False,linecolor=line_color,)
    fig_use_cap.update_layout(
        title="Demand per capita for different demand scenarios")
    fig_use_cap.update_traces(marker_line_color=font_color,
                       marker_line_width=0, opacity=1)
    fig_use_cap.update_yaxes(rangemode='tozero',linecolor=line_color,gridcolor=line_color)
    fig_use_cap.update_xaxes(showline=True, linecolor=line_color,
                     title_text="<a href=\"http://unstats.un.org/unsd/energystats/pubs/balance\"><sub>Source: Energy Balances, United Nations<sub></a>")





    return fig_use_cap

def per_capita_renewables():
    countries = functions.fetch_all_countries_demand(2019,Unit='GWh',Use='Analysis')[0]

    renewable_electricity = functions.fetch_all_countries_demand(2019,Unit='GWh',Use='Analysis')[8]
    df_pop = pd.read_csv('Data/Economic Indicators.csv')

    renewable_electricity = 1000 * renewable_electricity / df_pop['Population'] #MWh/year/capita


    wolrd_per_capita_RE_elec = pd.read_csv('Data/worldinData/low-carbon-elec-per-capita.csv')

    wolrd_per_capita_RE_elec = wolrd_per_capita_RE_elec.sort_values('Year', ascending=False).drop_duplicates(['Entity'])
    wolrd_per_capita_RE_elec['Low-carbon electricity per capita (kWh)'] = wolrd_per_capita_RE_elec['Low-carbon electricity per capita (kWh)']/1000 #MWh/capita
    wolrd_per_capita_RE_elec['Low-carbon electricity per capita (kWh)'] = wolrd_per_capita_RE_elec['Low-carbon electricity per capita (kWh)']
    wolrd_average_per_capita_RE_elec = wolrd_per_capita_RE_elec['Low-carbon electricity per capita (kWh)'].mean()
    wolrd_median_per_capita_RE_elec = wolrd_per_capita_RE_elec['Low-carbon electricity per capita (kWh)'].median()

    wolrd_per_capita_RE_elec['Entity'] = wolrd_per_capita_RE_elec['Entity'].replace('Micronesia (country)','Micronesia')
    wolrd_per_capita_RE_elec['Entity'] = wolrd_per_capita_RE_elec['Entity'].replace('Papua New Guinea','PNG')


    wolrd_per_capita_RE_elec = wolrd_per_capita_RE_elec[wolrd_per_capita_RE_elec.Entity.isin(Country_List)]



    fig_use_cap = make_subplots(specs=[[{"secondary_y": False}]])
    fig_use_cap.add_trace(go.Bar(x=countries, y=renewable_electricity,text=renewable_electricity.round(2), name='This research',
                          marker_color='red',
                      ))
    # fig_use_cap.add_trace(go.Bar(x=wolrd_per_capita_RE_elec['Entity'], y=wolrd_per_capita_RE_elec['Low-carbon electricity per capita (kWh)'],text=wolrd_per_capita_RE_elec['Low-carbon electricity per capita (kWh)'].round(1), name='Our world in data',
    #                       marker_color='green',
    #                   ))
    fig_use_cap.add_shape(
        type='line', line=dict(dash='dot', color='red'),
        x0=0, x1=len(countries), y0=wolrd_average_per_capita_RE_elec, y1=wolrd_average_per_capita_RE_elec
    )
    fig_use_cap.add_shape(
        type='line', line=dict(dash='dot', color='orange'),
        x0=0, x1=len(countries), y0=wolrd_median_per_capita_RE_elec, y1 = wolrd_median_per_capita_RE_elec
    )
    fig_use_cap.update_layout(legend=dict(bgcolor='rgba(0,0,0,0)', yanchor="bottom", orientation="h",
                                   y=0.98,
                                   xanchor="center",
                                   x=0.5),
                       font=dict(
                           family="Calibri",
                           size=16,
                           color=font_color
                       ),
                       hovermode="x"

                       )
    fig_use_cap.add_annotation(x=0.8, y=wolrd_average_per_capita_RE_elec+0.1,
                       text="World average = {}".format(wolrd_average_per_capita_RE_elec.round(1)),
                       showarrow=False, font=dict(
                color=font_color,
                size=16
            ),
                       )
    fig_use_cap.add_annotation(x=0.8, y=wolrd_median_per_capita_RE_elec+0.1,
                       text="World median = {}".format(wolrd_median_per_capita_RE_elec.round(1)),
                       showarrow=False, font=dict(
                color=font_color,
                size=16
            ),
                       )
    fig_use_cap.update_layout({
        'plot_bgcolor': 'rgba(0,0,0,0)',
        'paper_bgcolor': 'rgba(0,0,0,0)',
    })
    fig_use_cap.update_yaxes(title_text="Renewable electricity (MWh/year/person)", showline=True,rangemode='tozero',linecolor=line_color,gridcolor=line_color)
    fig_use_cap.update_xaxes(showline=True,showgrid=False,linecolor=line_color,)
    fig_use_cap.update_layout(
        title="Renewable electricity generation per capita")
    fig_use_cap.update_traces(marker_line_color=font_color,
                       marker_line_width=0, opacity=1)
    fig_use_cap.update_yaxes(rangemode='tozero',linecolor=line_color,gridcolor=line_color)
    fig_use_cap.update_xaxes(showline=True, linecolor=line_color,
                     title_text="<a href=\"http://unstats.un.org/unsd/energystats/pubs/balance\"><sub>Source: Energy Balances, United Nations<sub></a>")

    return fig_use_cap


def per_capita_intensity():

    countries = functions.fetch_all_countries_demand(2019,Unit='GWh',Use='Analysis')[0]

    wolrd_per_capita_intensity = pd.read_csv('Data/worldinData/energy-intensity-of-economies.csv')
    wolrd_per_capita_intensity = wolrd_per_capita_intensity.sort_values('Year', ascending=False).drop_duplicates(['Entity'])
    wolrd_average_per_capita_intensity  = wolrd_per_capita_intensity['Energy intensity level of primary energy (MJ/$2017 PPP GDP)'].mean()
    wolrd_median_per_capita_intensity = wolrd_per_capita_intensity['Energy intensity level of primary energy (MJ/$2017 PPP GDP)'].median()

    wolrd_per_capita_intensity['Entity'] = wolrd_per_capita_intensity['Entity'].replace('Micronesia (country)','Micronesia')
    wolrd_per_capita_intensity['Entity'] = wolrd_per_capita_intensity['Entity'].replace('Papua New Guinea','PNG')
    wolrd_per_capita_intensity = wolrd_per_capita_intensity[wolrd_per_capita_intensity.Entity.isin(Country_List)]


    total_demand = functions.fetch_all_countries_demand(2019,Unit='GWh',Use='SummaryPlot')[1]
    df_GDP = pd.read_csv('Data/Economic Indicators.csv')
    df_GDP['Demand'] = total_demand
    df_GDP['Demand_per_gdp'] = (df_GDP['Demand']*1000000)/(df_GDP['GDP(million$)2019']*1000000)



    fig_use_cap = make_subplots(specs=[[{"secondary_y": False}]])
    fig_use_cap.add_trace(go.Bar(x=countries, y=df_GDP['Demand_per_gdp'].round(1),text=df_GDP['Demand_per_gdp'].round(1), name='This research',
                          marker_color='red',
                      ))
    # fig_use_cap.add_trace(go.Bar(x=wolrd_per_capita_intensity['Entity'], y=wolrd_per_capita_intensity['Energy intensity level of primary energy (MJ/$2017 PPP GDP)'],text=wolrd_per_capita_intensity['Energy intensity level of primary energy (MJ/$2017 PPP GDP)'].round(1), name='Our world in data',
    #                       marker_color='green',
    #                   ))
    fig_use_cap.add_shape(
        type='line', line=dict(dash='dot', color='red'),
        x0=0, x1=len(countries), y0=wolrd_average_per_capita_intensity, y1=wolrd_average_per_capita_intensity
    )
    fig_use_cap.add_shape(
        type='line', line=dict(dash='dot', color='orange'),
        x0=0, x1=len(countries), y0=wolrd_median_per_capita_intensity, y1 = wolrd_median_per_capita_intensity
    )
    fig_use_cap.update_layout(legend=dict(bgcolor='rgba(0,0,0,0)', yanchor="bottom", orientation="h",
                                   y=0.98,
                                   xanchor="center",
                                   x=0.5),
                       font=dict(
                           family="Calibri",
                           size=16,
                           color=font_color
                       ),
                       hovermode="x"

                       )
    fig_use_cap.add_annotation(x=15, y=wolrd_average_per_capita_intensity+0.12,
                       text="World average = {}".format(wolrd_average_per_capita_intensity.round(1)),
                       showarrow=False, font=dict(
                color=font_color,
                size=16
            ),
                       )
    fig_use_cap.add_annotation(x=15, y=wolrd_median_per_capita_intensity+0.12,
                       text="World median = {}".format(wolrd_median_per_capita_intensity.round(1)),
                       showarrow=False, font=dict(
                color=font_color,
                size=16
            ),
                       )
    fig_use_cap.update_layout({
        'plot_bgcolor': 'rgba(0,0,0,0)',
        'paper_bgcolor': 'rgba(0,0,0,0)',
    })
    fig_use_cap.update_yaxes(title_text="(kWh/$ PPP GDP)", showline=True,rangemode='tozero',linecolor=line_color,gridcolor=line_color)
    fig_use_cap.update_xaxes(showline=True,showgrid=False,linecolor=line_color,)
    fig_use_cap.update_layout(
        title="Energy (primary, total) intensity  of economies")
    fig_use_cap.update_traces(marker_line_color=font_color,
                       marker_line_width=0, opacity=1)
    fig_use_cap.update_yaxes(rangemode='tozero',linecolor=line_color,gridcolor=line_color)
    fig_use_cap.update_xaxes(showline=True, linecolor=line_color,
                     title_text="<a href=\"http://unstats.un.org/unsd/energystats/pubs/balance\"><sub>Source: Energy Balances, United Nations<sub></a>")
    return fig_use_cap

def percentage_of_imports():
    countries = functions.fetch_all_countries_demand(2019,Unit='GWh',Use='Analysis')[0]
    total_energy_supply = functions.fetch_all_countries_demand(2019,Unit='GWh',Use='SummaryPlot')[1]
    net_imports = functions.fetch_all_countries_demand(2019,Unit='GWh',Use='Analysis')[15]
    current_share_of_imports = 100 * net_imports/total_energy_supply


    world_average_demand = functions.fetch_all_countries_demand(2019,Unit='GWh',Use='Analysis')[11] *100/80 # convert to total instead of electricity
    renewables_in_total = functions.fetch_all_countries_demand(2019,Unit='GWh',Use='Analysis')[7]
    world_average_demand_non_RE = (world_average_demand - renewables_in_total) * 80/100 # convert to electricity
    rooftop_PV_df = functions.calculate_rooftop_PV_potential()
    wind_PV_df = functions.calculate_PV_Wind_potential(available_land=0.02,available_coastline=0.1)
    remaining_demand_world_average = world_average_demand_non_RE - rooftop_PV_df['Generation_GWh'] - wind_PV_df['PV_technical_GWh']
    imports_world_average = 100 * remaining_demand_world_average/world_average_demand_non_RE

    imports_df = pd.DataFrame()

    demand_for_decarb = functions.fetch_all_countries_demand(2019)[9]
    countries = functions.fetch_all_countries_demand(2019)[0]
    remaining_demand_for_decarb = demand_for_decarb - rooftop_PV_df['Generation_GWh'] - wind_PV_df['PV_technical_GWh']
    imports_decarbonization = 100 * remaining_demand_for_decarb/demand_for_decarb
    imports_df['countries'] = countries
    imports_df['imports_decarb_%'] = imports_decarbonization
    imports_df['imports_decarb_%'] = imports_df['imports_decarb_%'].clip(lower=0)
    imports_df['imports_decarb_GWh'] = remaining_demand_for_decarb
    imports_df['imports_decarb_GWh'] = imports_df['imports_decarb_GWh'].clip(lower=0)


    electrified_demand = functions.fetch_all_countries_demand(2019,Use="Analysis")[1]
    remaining_demand_electrified = electrified_demand - rooftop_PV_df['Generation_GWh'] - wind_PV_df['PV_technical_GWh']
    imports_electrified = 100 * remaining_demand_electrified/electrified_demand
    imports_df['imports_electrified_%'] = imports_electrified
    imports_df['imports_electrified_%'] = imports_df['imports_electrified_%'].clip(lower=0)
    imports_df['imports_electrified_GWh'] = remaining_demand_electrified
    imports_df['imports_electrified_GWh'] = imports_df['imports_electrified_GWh'].clip(lower=0)

    imports_df['imports_world_average_%'] = imports_world_average
    imports_df['imports_world_average_%'] = imports_df['imports_world_average_%'].clip(lower=0)
    imports_df['imports_world_average_GWh'] = remaining_demand_world_average
    imports_df['imports_world_average_GWh'] = imports_df['imports_world_average_GWh'].clip(lower=0)

    imports_df['Current_%'] = current_share_of_imports
    imports_df['Current_%'] = imports_df['Current_%'].clip(lower=0)
    imports_df['Current_GWh'] = net_imports
    imports_df['Current_GWh'] = imports_df['Current_GWh'].clip(lower=0)



    imports_df.to_csv("imports_for_scenarios.csv")



    fig_use_cap = make_subplots(specs=[[{"secondary_y": False}]])
    fig_use_cap.add_trace(go.Bar(x=imports_df['countries'], y=imports_df['Current_%'].round(1),text=imports_df['Current_%'].round(1), name='Current',
                          marker_color='red',
                      ))
    fig_use_cap.add_trace(go.Bar(x=imports_df['countries'], y=imports_df['imports_decarb_%'].round(1),text=imports_df['imports_decarb_%'].round(1), name='Decarbonization',
                          marker_color='blue',
                      ))
    fig_use_cap.add_trace(go.Bar(x=imports_df['countries'], y=imports_df['imports_electrified_%'].round(1),text=imports_df['imports_electrified_%'].round(1), name='Electrification',
                          marker_color='brown',
                      ))
    fig_use_cap.add_trace(go.Bar(x=imports_df['countries'], y=imports_df['imports_world_average_%'].round(1),text=imports_df['imports_world_average_%'].round(1), name="Wolrd average",
                          marker_color='green',
                      ))

    fig_use_cap.update_layout(legend=dict(bgcolor='rgba(0,0,0,0)', yanchor="bottom", orientation="h",
                                   y=0.98,
                                   xanchor="center",
                                   x=0.5),
                       font=dict(
                           family="Calibri",
                           size=16,
                           color=font_color
                       ),
                       hovermode="x"

                       )

    fig_use_cap.update_layout({
        'plot_bgcolor': 'rgba(0,0,0,0)',
        'paper_bgcolor': 'rgba(0,0,0,0)',
    })
    fig_use_cap.update_yaxes(title_text="% of total demand", showline=True,rangemode='tozero',linecolor=line_color,gridcolor=line_color)
    fig_use_cap.update_xaxes(showline=True,showgrid=False,linecolor=line_color,)
    fig_use_cap.update_layout(
        title="The share of total demand met by net energy imports")
    fig_use_cap.update_traces(marker_line_color=font_color,
                       marker_line_width=0, opacity=1)
    fig_use_cap.update_yaxes(rangemode='tozero',linecolor=line_color,gridcolor=line_color)
    fig_use_cap.update_xaxes(showline=True, linecolor=line_color,
                     title_text="<a href=\"http://unstats.un.org/unsd/energystats/pubs/balance\"><sub>Source: Energy Balances, United Nations<sub></a>")
    return fig_use_cap

def dependance_on_imports():
    countries = functions.fetch_all_countries_demand(2019,Unit='GWh',Use='Analysis')[0]
    total_energy_supply = functions.fetch_all_countries_demand(2019,Unit='GWh',Use='SummaryPlot')[1]
    net_imports = functions.fetch_all_countries_demand(2019,Unit='GWh',Use='Analysis')[15]
    current_share_of_imports = 100 * net_imports/total_energy_supply
    int_aviation = functions.fetch_all_countries_demand(2019,Unit='GWh',Use='Analysis')[13]
    int_marine = functions.fetch_all_countries_demand(2019,Unit='GWh',Use='Analysis')[12]
    total_supply_incl_int_transit = total_energy_supply + abs(int_marine) + abs(int_aviation)
    current_share_of_imports_inc_int_transit = 100 * net_imports/total_supply_incl_int_transit

    fig_use_cap = make_subplots(specs=[[{"secondary_y": False}]])
    fig_use_cap.add_trace(go.Bar(x=countries, y=current_share_of_imports_inc_int_transit,text=current_share_of_imports_inc_int_transit.round(0), name='This research',
                          marker_color='green',
                      ))

    fig_use_cap.update_layout(legend=dict(bgcolor='rgba(0,0,0,0)', yanchor="bottom", orientation="h",
                                   y=0.98,
                                   xanchor="center",
                                   x=0.5),
                       font=dict(
                           family="Calibri",
                           size=16,
                           color=font_color
                       ),
                       hovermode="x"

                       )

    fig_use_cap.update_layout({
        'plot_bgcolor': 'rgba(0,0,0,0)',
        'paper_bgcolor': 'rgba(0,0,0,0)',
    })
    fig_use_cap.update_yaxes(title_text="Dependance on net imports (%)", linecolor=line_color,gridcolor=line_color)
    fig_use_cap.update_xaxes(showline=True,showgrid=False,linecolor=line_color,)
    fig_use_cap.update_layout(
        title="Dependence on net imports (share of net imports in total demand)")
    fig_use_cap.update_traces(marker_line_color=font_color,
                       marker_line_width=0, opacity=1)
    fig_use_cap.update_yaxes(rangemode='tozero',linecolor=line_color,gridcolor=line_color,zeroline=False)
    fig_use_cap.update_xaxes(showline=True, linecolor=line_color,
                     title_text="<a href=\"http://unstats.un.org/unsd/energystats/pubs/balance\"><sub>Source: Energy Balances, United Nations<sub></a>")
    return fig_use_cap


def GDP_per_capita():
    summary_df = pd.read_csv('Data/SummaryTable.csv')

    summary_df = summary_df[summary_df['Country / Territory'].isin(Country_List)]

    world_GDP_capita = pd.read_csv("Data/worldinData/gdp-per-capita-worldbank.csv")
    world_GDP_capita = world_GDP_capita.sort_values('Year', ascending=False).drop_duplicates(['Entity'])

    wolrd_average_GDP_per_capita = world_GDP_capita['GDP per capita, PPP (constant 2017 international $)'].mean()
    wolrd_median_GDP_per_capita = world_GDP_capita['GDP per capita, PPP (constant 2017 international $)'].median()
    fig_use_cap = make_subplots(specs=[[{"secondary_y": False}]])
    fig_use_cap.add_trace(go.Bar(x=summary_df['Country / Territory'], y=summary_df['GDP Per Capita ($)'],text=summary_df['GDP Per Capita ($)'],name='This research',
                          marker_color='green',
                      ))


    fig_use_cap.update_layout(legend=dict(bgcolor='rgba(0,0,0,0)', yanchor="bottom", orientation="h",
                                   y=0.98,
                                   xanchor="center",
                                   x=0.5),
                       font=dict(
                           family="Calibri",
                           size=16,
                           color=font_color
                       ),
                       hovermode="x"

                       )

    fig_use_cap.add_shape(
        type='line', line=dict(dash='dot', color='red'),
        x0=0, x1=len(summary_df['Country / Territory']), y0=wolrd_average_GDP_per_capita, y1=wolrd_average_GDP_per_capita
    )
    fig_use_cap.add_shape(
        type='line', line=dict(dash='dot', color='orange'),
        x0=0, x1=len(summary_df['Country / Territory']), y0=wolrd_median_GDP_per_capita, y1 = wolrd_median_GDP_per_capita
    )
    fig_use_cap.add_annotation(x=15, y=wolrd_average_GDP_per_capita+1000,
                       text="World average = {}".format(wolrd_average_GDP_per_capita.round(0)),
                       showarrow=False, font=dict(
                color=font_color,
                size=16
            ),
                       )
    fig_use_cap.add_annotation(x=15, y=wolrd_median_GDP_per_capita+1000,
                       text="World median = {}".format(wolrd_median_GDP_per_capita.round(0)),
                       showarrow=False, font=dict(
                color=font_color,
                size=16
            ),
                       )

    fig_use_cap.update_layout({
        'plot_bgcolor': 'rgba(0,0,0,0)',
        'paper_bgcolor': 'rgba(0,0,0,0)',
    })
    fig_use_cap.update_yaxes(title_text="GDP per Capita ($)", showline=True,rangemode='tozero',linecolor=line_color,gridcolor=line_color)
    fig_use_cap.update_xaxes(showline=True,showgrid=False,linecolor=line_color,)
    fig_use_cap.update_layout(
        title="GDP per capita and comparison with world's average")
    fig_use_cap.update_traces(marker_line_color=font_color,
                       marker_line_width=0, opacity=1)
    fig_use_cap.update_yaxes(rangemode='tozero',linecolor=line_color,gridcolor=line_color)
    fig_use_cap.update_xaxes(showline=True, linecolor=line_color,
                     title_text="<a href=\"https://ourworldindata.org/grapher/per-capita-energy-use\"><sub>Source: Our world in data <sub></a>")
    return fig_use_cap


def biomass_consumption_breakdown():
    import os
    import plotly.express as px

    list_of_consumers = ['Electricity Plants',"Manufacturing  const. and mining",'Households','Commerce and public services',
                         'Agriculture  forestry and fishing','Other consumption n.e.s']
    path = 'Data/EnergyBalance'
    files = os.listdir(path)

    df = pd.read_csv("Data/EnergyBalance/{}/all_countries_df.csv".format(files[-1]))
    df = df[["Country ({})".format(files[-1]),"Transactions(down)/Commodity(right)",'Biofuels and Waste']]
    df_final = pd.DataFrame()
    for country in Country_List:
        df_1 = df[df["Country ({})".format(files[-1])]==country]
        primary_production = df_1.iloc[0, 2]
        # print(primary_production)
        # df_1.loc[:,'primary_production'] = primary_production
        df_1.loc[:,'Biofuels and Waste'] = 100 * abs(df_1.loc[:,'Biofuels and Waste'])/primary_production#/df_1.loc[:,'primary_production']
        if df_final.shape[0] ==0:
            df_final = df_1
        else:
            df_final = pd.concat([df_final,df_1])
    df_final = df_final[df_final["Transactions(down)/Commodity(right)"].isin(list_of_consumers)]

    fig = px.bar(df_final, x="Country ({})".format(files[-1]), y="Biofuels and Waste", color="Transactions(down)/Commodity(right)")


    fig.update_layout(legend=dict(bgcolor='rgba(0,0,0,0)', yanchor="bottom", orientation="v",
                                   # y=0.98,
                                   xanchor="center",
                                   # x=0.2
                                  ),
                       font=dict(
                           family="Calibri",
                           size=16,
                           color=font_color
                       ),
                       # hovermode="x"

                       )

    fig.update_layout({
        'plot_bgcolor': 'rgba(0,0,0,0)',
        'paper_bgcolor': 'rgba(0,0,0,0)',
    })
    fig.update_yaxes(title_text="% biofuel and waste primary production", showline=True,linecolor=line_color,gridcolor=line_color)
    fig.update_xaxes(showline=True,showgrid=False,linecolor=line_color,)
    fig.update_layout(
        title="Breakdown of biofuel and waste consumption")
    fig.update_traces(marker_line_color=font_color,
                       marker_line_width=0, opacity=1)
    fig.update_layout(legend={'title_text': ''})

    fig.update_yaxes(linecolor=line_color,gridcolor=line_color,zeroline=False,showline=True)
    fig.update_xaxes(showline=True,linecolor=line_color,zeroline = True,
                     title_text="<a href=\"http://unstats.un.org/unsd/energystats/pubs/balance\"><sub>Source: Energy Balances, United Nations<sub></a>"),
    return fig


def navigation_and_int_maritime():
    import os
    import plotly.express as px

    list_of_consumers = ['International marine bunkers',"Domestic navigation"]
    path = 'Data/EnergyBalance'
    path = 'Data/EnergyBalance'
    files = os.listdir(path)

    df = pd.read_csv("Data/EnergyBalance/{}/all_countries_df.csv".format(files[-1]))
    df = df[["Country ({})".format(files[-1]),"Transactions(down)/Commodity(right)",'Total Energy']]
    df_final = pd.DataFrame()
    for country in Country_List:
        df_1 = df[df["Country ({})".format(files[-1])]==country]
        total_primary_production = df_1.iloc[0, 2]
        # print(primary_production)
        # df_1.loc[:,'total_primary_production'] = total_primary_production
        df_1.loc[:,'Total Energy'] = 100 * abs(df_1.loc[:,'Total Energy'])/total_primary_production#df_1.loc[:,'total_primary_production']
        if df_final.shape[0] ==0:
            df_final = df_1
        else:
            df_final = pd.concat([df_final,df_1])
    df_final = df_final[df_final["Transactions(down)/Commodity(right)"].isin(list_of_consumers)]

    fig = px.bar(df_final, x="Country ({})".format(files[-1]), y="Total Energy", color="Transactions(down)/Commodity(right)")
    fig.update_layout(legend=dict(bgcolor='rgba(0,0,0,0)', yanchor="bottom", orientation="v",
                                   # y=0.98,
                                   xanchor="center",
                                   # x=0.2
                                  ),
                       font=dict(
                           family="Calibri",
                           size=16,
                           color=font_color
                       ),
                       # hovermode="x"

                       )

    fig.update_layout({
        'plot_bgcolor': 'rgba(0,0,0,0)',
        'paper_bgcolor': 'rgba(0,0,0,0)',
    })
    fig.update_yaxes(title_text="% of total primary production", showline=True,rangemode='tozero',linecolor=line_color,gridcolor=line_color)
    fig.update_xaxes(showline=True,showgrid=False,linecolor=line_color,)
    fig.update_layout(
        title="Primary production vs domestic and international marine transport")
    fig.update_traces(marker_line_color=font_color,
                       marker_line_width=0, opacity=1)
    fig.update_layout(legend={'title_text': ''})

    fig.update_yaxes(rangemode='tozero',linecolor=line_color,gridcolor=line_color)
    fig.update_xaxes(showline=True,linecolor=line_color,
                     title_text="<a href=\"http://unstats.un.org/unsd/energystats/pubs/balance\"><sub>Source: Energy Balances, United Nations<sub></a>"),
    return fig
# biomass_consumption_breakdown()



def dynamic_breakdown_figure_generation(y_axis_title,from_="Primary production",list_of_consumers = ['International marine bunkers',"Domestic navigation"],carrier = 'Total Energy',destination_carrier = 'Total Energy'):
    import os
    import plotly.express as px

    path = 'Data/EnergyBalance'
    files = os.listdir(path)

    df = pd.read_csv("Data/EnergyBalance/{}/all_countries_df.csv".format(files[-1]))
    if carrier == destination_carrier:
        df = df[["Country ({})".format(files[-1]),"Transactions(down)/Commodity(right)",carrier]]
        df_final = pd.DataFrame()
        for country in Country_List:
            df_1 = df[df["Country ({})".format(files[-1])]==country]
            total_source = 0
            for i in from_:
                total_source += df_1[df_1["Transactions(down)/Commodity(right)"]==i][carrier].values[0]
            df_1.loc[:,carrier] =  100 * abs(df_1.loc[:,carrier])/total_source#
            if df_final.shape[0] == 0:
                df_final = df_1
            else:
                df_final = pd.concat([df_final,df_1])
    else:
        df = df[["Country ({})".format(files[-1]),"Transactions(down)/Commodity(right)",carrier,destination_carrier]]
        df_final = pd.DataFrame()
        for country in Country_List:
            df_1 = df[df["Country ({})".format(files[-1])]==country]
            total_source = 0
            for i in from_:
                total_source += df_1[df_1["Transactions(down)/Commodity(right)"] == i][carrier].values[0]
            df_1.loc[:,destination_carrier] =  100 * abs(df_1.loc[:,destination_carrier])/total_source#
            if df_final.shape[0] == 0:
                df_final = df_1
            else:
                df_final = pd.concat([df_final,df_1])
    df_final = df_final[df_final["Transactions(down)/Commodity(right)"].isin(list_of_consumers)]
    if carrier == destination_carrier:
        y_axis = carrier
    else:
        y_axis = destination_carrier
    fig = px.bar(df_final, x="Country ({})".format(files[-1]),color_discrete_sequence = px.colors.qualitative.Alphabet, y=y_axis, color="Transactions(down)/Commodity(right)")

    fig.update_layout(
        legend=dict(bgcolor='rgba(0,0,0,0)',  orientation="h",
                    # yanchor="bottom",
                                   y=1.2,
                                   # xanchor="right",
                                   # x=0
                                  ),
                       font=dict(
                           family="Calibri",
                           size=16,
                           color=font_color
                       ),
                       # hovermode="x"

                       )

    fig.update_layout({
        'plot_bgcolor': 'rgba(0,0,0,0)',
        'paper_bgcolor': 'rgba(0,0,0,0)',
    })
    fig.update_yaxes(title_text=y_axis_title, showline=True,rangemode='tozero',linecolor=line_color,gridcolor=line_color)
    fig.update_xaxes(showline=True,showgrid=False,linecolor=line_color,)
    fig.update_layout(
        title="")
    fig.update_traces(marker_line_color=font_color,
                       marker_line_width=0, opacity=1)
    fig.update_layout(legend={'title_text': ''})

    fig.update_yaxes(rangemode='tozero',linecolor=line_color,gridcolor=line_color)
    fig.update_xaxes(showline=True,linecolor=line_color,
                     title_text="<a href=\"http://unstats.un.org/unsd/energystats/pubs/balance\"><sub>Source: Energy Balances, United Nations<sub></a>"),
    return fig


def dynamic_breakdown_of_sectors(sector):
    import os
    path = 'Data/EnergyBalance'
    files = os.listdir(path)
    df = pd.read_csv("Data/EnergyBalance/{}/all_countries_df.csv".format(files[-1]))

    df = df[df["Transactions(down)/Commodity(right)"] == sector]
    df= df.iloc[:,:13]# = df.iloc[:,2:12]/df["Total Energy"]
    df.iloc[:,3:]=100*df.iloc[:,3:].div(df['Total Energy'], axis=0)
    df.drop(columns=['Total Energy'],inplace=True)
    df = df.melt(id_vars=df.columns[:3])

    fig = px.bar(df, x="Country ({})".format(files[-1]), y='value', color="variable",color_discrete_sequence = px.colors.qualitative.Alphabet)
    fig.update_layout(
        legend=dict(bgcolor='rgba(0,0,0,0)', orientation="h",
                    # yanchor="bottom",
                    y=1.2,
                    # xanchor="right",
                    # x=0
                    ),
        font=dict(
            family="Calibri",
            size=16,
            color=font_color
        ),
        # hovermode="x"

    )

    fig.update_layout({
        'plot_bgcolor': 'rgba(0,0,0,0)',
        'paper_bgcolor': 'rgba(0,0,0,0)',
    })
    fig.update_yaxes(title_text="% of {}".format(sector), showline=True, rangemode='tozero', linecolor=line_color,
                     gridcolor=line_color)
    fig.update_xaxes(showline=True, showgrid=False, linecolor=line_color, )
    fig.update_layout(
        title="")
    fig.update_traces(marker_line_color=font_color,
                      marker_line_width=0, opacity=1)
    fig.update_layout(legend={'title_text': ''})

    fig.update_yaxes(rangemode='tozero', linecolor=line_color, gridcolor=line_color)
    fig.update_xaxes(showline=True, linecolor=line_color,
                     title_text="<a href=\"http://unstats.un.org/unsd/energystats/pubs/balance\"><sub>Source: Energy Balances, United Nations<sub></a>"),
    # print(df.head(20))

    return fig



def dynamic_one_column_multiple_source(column,provider,y_axis_title):
    import os
    import plotly.express as px

    path = 'Data/EnergyBalance'
    files = os.listdir(path)

    df = pd.read_csv("Data/EnergyBalance/{}/all_countries_df.csv".format(files[-1]))
    df = df[["Country ({})".format(files[-1]),"Transactions(down)/Commodity(right)",column]]
    # df_final = pd.DataFrame()

    df = df[df["Transactions(down)/Commodity(right)"].isin(provider)]
    df[column] = df[column] * 0.277778
    df[column] = df[column].round(1)
    fig = px.bar(df, x="Country ({})".format(files[-1]),text=column,color_discrete_sequence = px.colors.qualitative.Alphabet, y=column, color="Transactions(down)/Commodity(right)")
    fig.update_layout(
        legend=dict(bgcolor='rgba(0,0,0,0)', orientation="h",
                    # yanchor="bottom",
                    y=1.2,
                    # xanchor="right",
                    # x=0
                    ),
        font=dict(
            family="Calibri",
            size=16,
            color=font_color
        ),
        # hovermode="x"

    )

    fig.update_layout({
        'plot_bgcolor': 'rgba(0,0,0,0)',
        'paper_bgcolor': 'rgba(0,0,0,0)',
    })
    fig.update_yaxes(title_text=y_axis_title, showline=True, rangemode='tozero', linecolor=line_color,
                     gridcolor=line_color)
    fig.update_xaxes(showline=True, showgrid=False, linecolor=line_color, )
    fig.update_layout(
        title="")
    fig.update_traces(marker_line_color=font_color,
                      marker_line_width=0, opacity=1)
    fig.update_layout(legend={'title_text': ''})

    fig.update_yaxes(rangemode='tozero', linecolor=line_color, gridcolor=line_color)
    fig.update_xaxes(showline=True, linecolor=line_color,
                     title_text="<a href=\"http://unstats.un.org/unsd/energystats/pubs/balance\"><sub>Source: Energy Balances, United Nations<sub></a>"),
    return fig

# dynamic_breakdown_of_sectors("Primary production")