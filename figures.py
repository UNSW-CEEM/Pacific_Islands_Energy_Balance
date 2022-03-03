import pandas as pd
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import plotly.express as px






def import_export_figure(df_imp,df_exp,Interest_list,year):
    # fig = make_subplots(rows=1, cols=1,shared_xaxes=True,shared_yaxes=False,subplot_titles=("2019       Imports {}  Exports {} ($MM)".format(-int(df_imp['Trade Value'].sum()),int(df_exp['Trade Value'].sum()))
    #                                                                                         ),vertical_spacing =0.05)
    totalImports = int(-df_imp['Trade Value'].sum())
    totalExports = int(df_exp['Trade Value'].sum())


    fig = go.Figure()
    fig.add_trace(go.Bar(x=df_imp[df_imp['HS4'].isin(Interest_list)]['HS4'], y=df_imp[df_imp['HS4'].isin(Interest_list)]['Trade Value'],marker_pattern_shape=".",name='Imports',marker_color='red'))
    fig.add_trace(go.Bar(x=df_exp[df_exp['HS4'].isin(Interest_list)]['HS4'], y=df_exp[df_exp['HS4'].isin(Interest_list)]['Trade Value'], marker_pattern_shape="+",name='Exports',marker_color='green'))

    fig.update_layout(#width=1500,
        height=500,
        barmode='relative')
    fig.update_layout(legend = dict(bgcolor = 'rgba(0,0,0,0)',    yanchor="bottom",orientation="v",
        y=0.5,
        xanchor="center",
        x=1.07),
                      font=dict(
                          family="Palatino Linotype",
                          size=18,
                          color="white"
                      )
                      )
    fig.update_layout({
    'plot_bgcolor': 'rgba(0,0,0,0)',
    'paper_bgcolor': 'rgba(0,0,0,0)',
    })
    fig.update_yaxes(title_text="Value ($MM)",showline=True)
    fig.update_xaxes(showline=True)

    fig.update_layout(
        title="{}, Total Imports = {}, Total Exports = {} ($million)".format(year,totalImports,totalExports))

    return fig




def Generate_Sankey(year,country):
    import pandas as pd
    import plotly.graph_objects as go

    df = pd.read_csv("Data/Sankey/csv/{}/{}.csv".format(year,country))
    df_elec = df.loc[(df[' (from)']=='PowerStations')|(df[' (from)']=='Other Electricity & Heat')|(df[' (from)']=='Other Electricity & Heat3')|(df[' (from)']=='Electricity & Heat: Supplied')
                     | (df[' (to)']=='PowerStations')|(df[' (to)']=='Other Electricity & Heat')|(df[' (to)']=='Other Electricity & Heat3')|(df[' (to)']=='Electricity & Heat: Supplied')]



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



    fig.update_layout(title_text="Sankey Plot for all sectors", font_size=16)
    fig.update_layout(height=900,font=dict(
                          family="Palatino Linotype",
                          size=16,
                          color="white"
                      ))
    fig.update_layout({'plot_bgcolor': 'rgba(0,0,0,0)',
    'paper_bgcolor': 'rgba(0,0,0,0)'},)



    fig2.update_layout(height=350,font=dict(
                          family="Palatino Linotype",
                          size=16,
                          color="white"
                      ))
    fig2.update_layout({'plot_bgcolor': 'rgba(0,0,0,0)',
    'paper_bgcolor': 'rgba(0,0,0,0)'},)
    fig2.update_layout(title_text="Sankey Plot for the electricity sector", font_size=16)

    return [fig,fig2]




def potentials_bar(wind_pot,PV_pot,max_range,year):
    import plotly.graph_objs as go
    names = ['Wind', 'PV']
    values = [wind_pot,PV_pot]
    data = [go.Bar(
        x=names,
        y=values,

    )]
    fig = go.Figure(data=data)
    fig.update_layout(
        title="RE for Decarbonization with 20% losses")
    fig.update_yaxes(title_text="MW",showline=True)
    fig.update_xaxes(showline=True)

    fig.update_layout({'plot_bgcolor': 'rgba(0,0,0,0)',
    'paper_bgcolor': 'rgba(0,0,0,0)'})
    fig.update_layout(yaxis_range=[0, max_range])

    fig.update_layout(height=350,font=dict(
                          family="Palatino Linotype",
                          size=15,
                          color="white"
                      ))
    fig.update_traces(marker_color='lightsalmon', marker_line_color='white',
                      marker_line_width=2.5, opacity=1)

    return fig

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
                          family="Palatino Linotype",
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
    for i in range(0,11):
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
        title="Current and future non-RE electricity demand with {}% growth rate".format(growth_rate))

    fig.update_yaxes(title_text="GWh")
    # fig.update_layout(yaxis_range=[0, max_range])

    fig.update_layout({'plot_bgcolor': 'rgba(0,0,0,0)',
                       'paper_bgcolor': 'rgba(0,0,0,0)'})

    fig.update_layout(height=350, font=dict(
        family="Palatino Linotype",
        size=16,
        color="white"
    ))
    fig.update_traces(marker_color='lightsalmon', marker_line_color='white',
                      marker_line_width=2.5, opacity=1)
    fig.update_xaxes(showgrid=False,showline=True)
    fig.update_yaxes(showgrid=True,showline=True)


    return fig


def decarbonization_scenarios(demand,diesel_cost,growth_rate,decarb_rate,PV_cost,PVBatt_cost,WindBatt_cost,Wind_cost):
    demand_df = pd.DataFrame()
    demand_list = []
    diesel_cost_list=[]
    RE_installation = []
    demand_list.append(demand)
    diesel_cost_list.append(diesel_cost)
    year_list = []
    year = 2019
    year_list.append(year)
    for i in range(0, 21):
        demand += demand * growth_rate / 100
        diesel_cost += diesel_cost * growth_rate / 100
        demand_list.append(demand)
        diesel_cost_list.append(diesel_cost)
        year += 1
        year_list.append(year)

    demand_list=demand_list[3:]
    year_list=year_list[3:]
    diesel_cost_list = diesel_cost_list[3:]
    demand_df['Year']=year_list
    demand_df['Demand'] = demand_list
    demand_df['bs_diesel_cost'] = diesel_cost_list
    demand_df['2030-RE'] = 0

    for i in range(0,len(demand_list)):
        if i==0:
            RE_installation.append(demand_list[i]*decarb_rate/100)
            # non_RE_demand.append((1-decarb_rate/100)*demand_list[i])
        else:
            d = demand_list[i]-RE_installation[i-1]
            RE_installation.append(RE_installation[i-1] + d*decarb_rate/100)



    demand_df['2030-RE'][demand_df['Year']==2030] = demand_df['Demand'][demand_df['Year']==2030]
    year = 2030
    years= year-2022
    step = demand_df['Demand'][demand_df['Year']==2030]/(years+1)
    demand_df.at[0, '2030-RE'] = step
    for i, row in demand_df.iterrows():
        if (i>0) :
            demand_df.at[i,'2030-RE'] = demand_df.at[i-1,'2030-RE'] + step
    demand_df['2030-RE'][demand_df['Year'] > 2030] = demand_df['Demand'].copy()
    demand_df['Annual_RE'] = demand_df['2030-RE'].shift(-1) - demand_df['2030-RE']
    demand_df['Wind_cost'] = Wind_cost * demand_df['2030-RE']
    demand_df['PV_cost'] = PV_cost * demand_df['2030-RE']
    # demand_df['Non_RE_demand'] = demand_df['Demand'] -



    # print(demand_df.head(20), )

    data = [go.Bar(
        x=year_list,
        y=RE_installation,name='Step Change'
    )]

    fig = make_subplots(specs=[[{"secondary_y": True}]])
    fig.add_trace(
        go.Bar(x=year_list, y=RE_installation, name="RE-Step Change"),
        secondary_y=False,
    )
    fig.add_trace(
        go.Scatter(x=year_list, y=demand_list, name="Demand"),
        secondary_y=False,
    )

    fig.update_yaxes(title_text="Generation (GWh)", secondary_y=False, showline=True, showgrid=False)
    # fig.update_yaxes(title_text="Generation (GWh)", secondary_y=True, showline=True, showgrid=False)
    fig.update_xaxes(showgrid=False, showline=True)

    fig.update_layout(height=350, font=dict(
        family="Palatino Linotype",
        size=16,
        color="white"
    ))
    fig.update_layout({'plot_bgcolor': 'rgba(0,0,0,0)',
                       'paper_bgcolor': 'rgba(0,0,0,0)'},
                      legend=dict(bgcolor='rgba(0,0,0,0)', yanchor="bottom", orientation="h",
                                  y=1.05,
                                  xanchor="center",
                                  x=0.5,
                                  ))
    fig.update_traces(marker_color='lightsalmon', marker_line_color='white',
                      marker_line_width=2.5, opacity=1)

    # fig.update_layout(yaxis_range=[0, max_range])

    fig.update_layout(
        title="Replacing the non-RE demand by renewable generation with a constant rate of {}%".format(decarb_rate))
    return fig


def rooftop_PV_plot(Country,PV_size,max_range):
    import pandas as pd
    df = pd.read_csv('Data/Rooftop Potential.csv')
    population = df[df['Country']==Country]['Population'].values[0]
    household_size = df[df['Country']==Country]['Household size'].values[0]
    number_of_homes = int(population/household_size) * 0.7 # only those homes with rooftop PV potential

    rooftop_capacity_MW = number_of_homes * PV_size/1000

    PV_generation_potential = df[df['Country']==Country]['Potential of Av.PV gen (GWh/MW/year)'].values[0]
    rooftop_PV_generation_GWh = rooftop_capacity_MW * PV_generation_potential

    fig = make_subplots(specs=[[{"secondary_y": True}]])

    # Add traces
    x = ['Rooftop PV']
    y1 = [rooftop_capacity_MW]
    y2 = [rooftop_PV_generation_GWh]

    fig.add_trace(
        go.Bar(x=x, y=y1, name="Capacity"),
        secondary_y=False,
    )

    fig.add_trace(
        go.Scatter(x=x, y=y2, name="Generation",marker_color='red'),
        secondary_y=True,
    )
    fig.update_yaxes(title_text="Capacity (MW)", secondary_y=False,showline=True,showgrid=False)
    fig.update_yaxes(title_text="Generation (GWh)", secondary_y=True,showline=True,showgrid=False)
    fig.update_xaxes(showgrid=False,showline=True)


    fig.update_layout(height=350,font=dict(
                          family="Palatino Linotype",
                          size=16,
                          color="white"
                      ))
    fig.update_layout({'plot_bgcolor': 'rgba(0,0,0,0)',
                       'paper_bgcolor': 'rgba(0,0,0,0)'},
                      legend=dict(bgcolor='rgba(0,0,0,0)', yanchor="bottom", orientation="h",
                                  y=1.05,
                                  xanchor="center",
                                  x=0.5,
                      ))
    fig.update_traces(marker_color='lightsalmon', marker_line_color='white',
                      marker_line_width=2.5, opacity=1)

    fig.update_layout(yaxis_range=[0, max_range])

    fig.update_layout(
        title="Rooftop PV potential")


    return fig


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
    summary_df['int marine'] = -Int_marine
    summary_df['int aviation'] = -Int_avi
    summary_df['marine_to_import'] = 100 * summary_df['int marine']/summary_df['Oil imports']
    summary_df['aviation_to_import'] = 100 * summary_df['int aviation']/summary_df['Oil imports']
    summary_df['transformation_to_import'] = 100 * transformation/summary_df['Oil imports']
    summary_df['transformation_losses_to_import'] = 100 * transformation_losses/summary_df['Oil imports']
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
                          family="Palatino Linotype",
                          size=16,
                          color="white"
                      )
                      )
    fig.update_layout({
    'plot_bgcolor': 'rgba(0,0,0,0)',
    'paper_bgcolor': 'rgba(0,0,0,0)',
    })
    fig.update_yaxes(title_text="% of imported oil",showline=True)
    fig.update_xaxes(showline=True)

    fig.update_layout(
        title="% of imported oil consumed for international transit in {}".format(year))
    # print(summary_df)
    fig.update_traces(marker_line_color='white',
                      marker_line_width=2, opacity=1)

    fig2 = go.Figure()
    fig2.add_trace(go.Bar(x=summary_df['Country'], y=summary_df['transformation_to_import'], name='Transformation',
                         marker_color='forestgreen'))
    fig2.add_trace(go.Bar(x=summary_df['Country'], y=summary_df['aviation_to_import'], name='Transformation losses',
                         marker_color='lightsalmon'))

    fig2.update_layout(  # width=1500,
        # height=500,
        barmode='relative')
    fig2.update_layout(legend=dict(bgcolor='rgba(0,0,0,0)', yanchor="bottom", orientation="h",
                                  y=1.05,
                                  xanchor="center",
                                  x=0.5),
                      font=dict(
                          family="Palatino Linotype",
                          size=16,
                          color="white"
                      )
                      )
    fig2.update_layout({
        'plot_bgcolor': 'rgba(0,0,0,0)',
        'paper_bgcolor': 'rgba(0,0,0,0)',
    })
    fig2.update_yaxes(title_text="% of imported oil", showline=True)
    fig2.update_xaxes(showline=True)

    fig2.update_layout(
        title="% of imported oil transformed into electricity and transformation losses in {}".format(year))
    # print(summary_df)
    fig2.update_traces(marker_line_color='white',
                      marker_line_width=2, opacity=1)


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
                          family="Palatino Linotype",
                          size=16,
                          color="white"
                      )
                      )
    fig3.update_layout({
        'plot_bgcolor': 'rgba(0,0,0,0)',
        'paper_bgcolor': 'rgba(0,0,0,0)',
    })
    fig3.update_yaxes(title_text="% of imported oil", showline=True)
    fig3.update_xaxes(showline=True)

    fig3.update_layout(
        title="Breakdown of imported oil consumed for domestic transport in {}".format(year))
    # print(summary_df)
    fig3.update_traces(marker_line_color='white',
                      marker_line_width=2, opacity=1)


    return [fig,fig2,fig3]

