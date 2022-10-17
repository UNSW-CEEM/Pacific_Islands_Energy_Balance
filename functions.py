import pandas as pd
import numpy as np
from EnergyFlows import Country_List

def fetch_wind_PV_potential(Country):
    df_p = pd.read_excel('Data/Potentials.xlsx')
    # print(df_p.loc[2, country],power_generated_GWh)
    Wind_pot = df_p.loc[2, Country]  # GWh/MW/year
    PV_pot = df_p.loc[0, Country]  # GWh/MW/year
    area = df_p.iloc[14][Country]  # km2
    coastline = df_p.iloc[13][Country]


    return PV_pot,Wind_pot,area,coastline
def fetch_single_country_demand(Country,Year,Unit='GWh'):
    """This function calculates the final demand and non-RE transformation"""
    df = pd.read_csv("Data/EnergyBalance/{}/all_countries_df.csv".format(Year))
    df = df[df["Country ({})".format(Year)] == Country]
    ElectricitySupply = df[df['Transactions(down)/Commodity(right)']=='Transformation']['Electricity'].values[0] #TJ
    ofWhichRenewable_transformation = -df[df['Transactions(down)/Commodity(right)']=='Transformation']['memo: Of which Renewables'].values[0] #TJ # This is the input to power plants
    renewable_transformation_efficiency = 0.35
    non_RE_demand =  ElectricitySupply - ofWhichRenewable_transformation * renewable_transformation_efficiency #TJ

    electrification_efficiency_improvement = 0.4
    final_consumption = df[df['Transactions(down)/Commodity(right)']=='Final consumption']['Total Energy'].values[0] #TJ#Does not include fuel for transformation. Only output of power plants and energy delivered to users
    ofWhichRenewable_final_consumption = df[df['Transactions(down)/Commodity(right)']=='Final consumption']['memo: Of which Renewables'].values[0] #TJ # This is the input to power plants
    final_consumption_electricity = df[df['Transactions(down)/Commodity(right)']=='Final consumption']['Electricity'].values[0]
    """
    final demand is the non renewable part of the demand, assuming that all sectors are electrified
    """
    final_demand = non_RE_demand + (final_consumption-final_consumption_electricity-ofWhichRenewable_final_consumption) * (1-electrification_efficiency_improvement)


    df_world_per_capita_demand = pd.read_csv("Data/worldinData/per-capita-energy-use.csv")
    per_capita_average = df_world_per_capita_demand['Primary energy consumption per capita (kWh/person)'].mean() #kWh/person
    df_pop = pd.read_csv('Data/Economic Indicators.csv')
    population = df_pop[df_pop.Country == Country]['Population'].values[0]
    print(population)
    wolrd_average_demand = per_capita_average * population/1000000 # GWh/year
    if Unit =='GWh':
        final_demand = final_demand * 0.277778
        non_RE_demand = non_RE_demand * 0.277778
        wolrd_average_demand = wolrd_average_demand * 0.277778
    return non_RE_demand,final_demand


def PV_area_single_country(Country,Year):
    PV_pot, Wind_pot, area, coastline = fetch_wind_PV_potential(Country)
    non_RE_demand,final_demand = fetch_single_country_demand(Country,Year)
    PV_non_RE = 1.2 * non_RE_demand / PV_pot  # MW
    PV_final_demand = 1.2 * final_demand / PV_pot  # MW
    PV_area_non_RE = PV_non_RE / (100)  # 0.1kw/m2 # Converted to km2
    PV_area_non_RE_per = 100 * PV_area_non_RE / area
    PV_area_final_demand = PV_final_demand / (100)  # 0.1kw/m2
    PV_area_final_demand_per = 100 * PV_area_final_demand / area

    return PV_area_non_RE,PV_area_final_demand,PV_area_non_RE_per,PV_area_final_demand_per


def Wind_area_single_country(Country,Year):
    PV_pot, Wind_pot, area, coastline = fetch_wind_PV_potential(Country)

    non_RE_demand,final_demand = fetch_single_country_demand(Country,Year)
    Wind_MW_non_RE = 1.2 * non_RE_demand / Wind_pot
    Wind_MW_final = 1.2 * final_demand / Wind_pot
    percentage_of_coastline_final = ((Wind_MW_final * 100/1.5)*0.25)/coastline
    percentage_of_coastline_non_RE = ((Wind_MW_non_RE * 100/1.5)*0.25)/coastline

    return percentage_of_coastline_final,percentage_of_coastline_non_RE


def fetch_all_countries_demand(Year,Unit='GWh',Use="Analysis"):
    df = pd.read_csv("Data/EnergyBalance/{}/all_countries_df.csv".format(Year))
    # final_demand = df[df['Transactions(down)/Commodity(right)']=='Total energy supply']['Total Energy'].values
    Countries = df. iloc[:, 1].unique()

    ElectricitySupply = df[df['Transactions(down)/Commodity(right)']=='Electricity Plants']['Electricity'].values #TJ
    ofWhichRenewable_transformation = -df[df['Transactions(down)/Commodity(right)']=='Electricity Plants']['memo: Of which Renewables'].values #TJ # This is the input to power plants
    renewable_transformation_efficiency = 0.35
    transformed_elec_from_renewables = ofWhichRenewable_transformation * renewable_transformation_efficiency
    non_RE_elec =  ElectricitySupply - transformed_elec_from_renewables #TJ

    if Use == 'Analysis':
        electrification_efficiency_improvement = 0.4
        final_consumption = df[df['Transactions(down)/Commodity(right)']=='Final consumption']['Total Energy'].values #TJ#Does not include fuel for transformation. Only output of power plants and energy delivered to users
        ofWhichRenewable_final_consumption = df[df['Transactions(down)/Commodity(right)']=='Final consumption']['memo: Of which Renewables'].values #TJ # This is the input to power plants
        final_consumption_electricity = df[df['Transactions(down)/Commodity(right)']=='Final consumption']['Electricity'].values
        total_demand = non_RE_elec + (final_consumption-final_consumption_electricity-ofWhichRenewable_final_consumption) * (1-electrification_efficiency_improvement)



    #previously
    if Use == 'SummaryPlot':
        total_demand = df[df['Transactions(down)/Commodity(right)']=='Total energy supply']['Total Energy'].values #TJ#Total energy entering the country(oil and renewables)

    renewables_in_total = df[df['Transactions(down)/Commodity(right)']=='Total energy supply']['memo: Of which Renewables'].values #TJ
    renewable_electricity_primary = df[df['Transactions(down)/Commodity(right)']=='Primary production']['Electricity'].values #TJ
    renewable_electricity = renewable_electricity_primary + transformed_elec_from_renewables


    imports_oil = df[df['Transactions(down)/Commodity(right)']=='Imports']['All Oil'].values
    all_imports = df[df['Transactions(down)/Commodity(right)']=='Imports']['Total Energy'].values

    Int_marine_oil = df[df['Transactions(down)/Commodity(right)']=='International marine bunkers']['All Oil'].values
    Int_avi_oil = df[df['Transactions(down)/Commodity(right)']=='International aviation bunkers']['All Oil'].values

    Int_marine_total = df[df['Transactions(down)/Commodity(right)'] == 'International marine bunkers']['Total Energy'].values
    Int_avi_total = df[df['Transactions(down)/Commodity(right)'] == 'International aviation bunkers']['Total Energy'].values
    exports_total = df[df['Transactions(down)/Commodity(right)'] == 'Exports']['Total Energy'].values
    net_imports_total = all_imports + Int_marine_total + Int_avi_total + exports_total



    transformation = -df[df['Transactions(down)/Commodity(right)']=='Electricity  CHP & Heat Plants']['All Oil'].values
    transformation_losses = - df[df['Transactions(down)/Commodity(right)']=='Electricity  CHP & Heat Plants']['Total Energy'].values

    wolrd_per_capita_use = pd.read_csv('Data/worldinData/per-capita-energy-use.csv')
    wolrd_per_capita_use = wolrd_per_capita_use.sort_values('Year', ascending=False).drop_duplicates(['Entity'])

    wolrd_average_per_capita_use = wolrd_per_capita_use['Primary energy consumption per capita (kWh/person)'].mean()
    wolrd_median_per_capita_use = wolrd_per_capita_use['Primary energy consumption per capita (kWh/person)'].median()
    df_pop = pd.read_csv('Data/Economic Indicators.csv')
    df_pop.rename(columns={'Country': 'Entity'}, inplace=True)

    df_pop['average_scenario_demand_GWh'] = 0.8 * df_pop[
        "Population"] * wolrd_average_per_capita_use / 1000000  # GWh/year

    world_average_demand = df_pop['average_scenario_demand_GWh']/0.277778 # it is calculated on GWh > convert to TJ

    if Unit == "GWh":
        non_RE_elec = non_RE_elec * 0.277778
        total_demand = total_demand * 0.277778
        imports_oil = imports_oil * 0.277778
        Int_marine_oil = Int_marine_oil * 0.277778
        Int_avi_oil = Int_avi_oil * 0.277778
        transformation = transformation * 0.277778
        transformation_losses = transformation_losses * 0.277778
        renewables_in_total = renewables_in_total * 0.277778
        renewable_electricity = renewable_electricity * 0.277778
        all_imports = all_imports * 0.277778
        world_average_demand = world_average_demand * 0.277778
        exports_total = exports_total * 0.277778
        Int_avi_total = Int_avi_total * 0.277778
        Int_marine_total = Int_marine_total * 0.277778
        net_imports_total = net_imports_total * 0.277778
        df_demand = pd.DataFrame()
        df_demand['Country'] = Countries
        df_demand['Non-RE'] = non_RE_elec
        df_demand['Total'] = total_demand
        df_demand['World_average_demand'] = world_average_demand.round(0)
        df_demand.to_csv("demand_df_{}.csv".format(Unit))
    return [Countries,total_demand,imports_oil,Int_marine_oil,Int_avi_oil,transformation,
            transformation_losses,renewables_in_total,
            renewable_electricity,non_RE_elec,all_imports,world_average_demand,
            Int_marine_total,Int_avi_total,exports_total,net_imports_total]

def all_countries_cross_comparison_unstats(Year,Unit,Use):
    summary_df = pd.DataFrame()
    population= pd.read_csv('Data/Economic Indicators.csv')




    df = pd.read_csv("Data/EnergyBalance/{}/all_countries_df.csv".format(Year))
    summary_list = fetch_all_countries_demand(2019,Unit=Unit,Use=Use)
    summary_df['Country'] = summary_list[0]
    summary_df['Total_demand'] = summary_list[1]
    summary_df['Oil imports'] = summary_list[2]
    summary_df['int marine'] = -summary_list[3]
    summary_df['int aviation'] = -summary_list[4]
    summary_df['Transformation'] = summary_list[5]
    summary_df['transformation_losses'] = summary_list[6]
    summary_df['renewables_in_total'] = summary_list[7]
    summary_df['renewable_electricity'] = summary_list[8]
    summary_df['total imports'] = summary_list[10]
    summary_df['World_average_demand'] = summary_list[11].round(0)

    summary_df['Renewables/Total_demand'] = 100 * summary_df['renewables_in_total']/summary_df['Total_demand']
    summary_df['Renewables/Total_demand']=summary_df['Renewables/Total_demand'].round(1)

    summary_df['Renewables/Total_imports'] = 100 * summary_df['renewables_in_total']/summary_df['total imports']
    summary_df['Renewables/Total_imports']=summary_df['Renewables/Total_imports'].round(1)

    summary_df['Renewables/capita'] = (summary_df['renewables_in_total']/population['Population'])  #Tj or GWh
    summary_df['Renewables/capita'] = summary_df['Renewables/capita'].round(0)

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

    summary_df['road_real'] = df[df['Transactions(down)/Commodity(right)'] == 'Road']['All Oil'].values
    summary_df['rail_real'] = df[df['Transactions(down)/Commodity(right)'] == 'Rail']['All Oil'].values
    summary_df['Domestic aviation_real'] = df[df['Transactions(down)/Commodity(right)'] == 'Domestic aviation'][
        'All Oil'].values
    summary_df['Domestic navigation_real'] = df[df['Transactions(down)/Commodity(right)'] == 'Domestic navigation'][
        'All Oil'].values
    summary_df['Pipeline transport_real'] = df[df['Transactions(down)/Commodity(right)'] == 'Pipeline transport'][
        'All Oil'].values
    summary_df['transport n.e.s_real'] = df[df['Transactions(down)/Commodity(right)'] == 'Transport n.e.s'][
        'All Oil'].values

    summary_df.to_csv("Summary_df.csv")
    return summary_df




def Update_UNstats_database(year):
    Country_List = ['Samoa', 'Nauru', 'Vanuatu', 'Palau', 'Kiribati', 'Cook Islands', 'Solomon Islands', 'Tonga',
                    'New Caledonia', 'French Polynesia', 'Micronesia', 'Niue', 'Tuvalu', 'PNG', 'Fiji']
    all_countries_df = pd.DataFrame()
    for country in Country_List:
        df = pd.read_csv("Data/EnergyBalance/{}/{}.csv".format(year,country))
        if country == Country_List[0]:
            all_countries_df = df
        elif country != Country_List[0]:
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
    all_countries_df.replace('Micronesia (Federated States of)', 'Micronesia',inplace=True)
    all_countries_df.replace('Papua New Guinea', 'PNG',inplace=True)

    all_countries_df.to_csv("Data/EnergyBalance/{}/all_countries_df.csv".format(year))




def calculate_PV_Wind_potential(available_land = 0.01,available_coastline = 0.1):
    df_technical_potential = pd.DataFrame()
    import plotly.graph_objs as go
    df = pd.read_excel('Data/Potentials.xlsx')
    countries = Country_List
    Wind_pot = df.iloc[2, 2:]  # GWh/MW/year
    PV_pot = df.iloc[0, 2:]  # GWh/MW/year
    coastline = df.iloc[13,2:]
    area = df.iloc[14,2:]

    arable = df.iloc[4, 2:]
    crops = df.iloc[5, 2:]
    pasture = df.iloc[6, 2:]
    forested = df.iloc[7, 2:]
    other = df.iloc[8, 2:]
    Technical_PV_area = (available_land * pasture/100 + available_land * arable/100) * area


    Theoretical_PV_GWh = PV_pot * area * 0.1 * 1000 * 0.8 #GWh
    Theoretical_wind_GWh = Wind_pot * coastline * (1.5/0.25) * 0.8 # GWh

    Technical_PV_GWh = PV_pot * Technical_PV_area * 0.1 * 1000 * 0.8 #GWh
    Technical_wind_GWh = Theoretical_wind_GWh * available_coastline

    Theoretical_PV_GW = area * 1000 * 0.1/1000
    Technical_PV_GW = Technical_PV_area * 1000 * 0.1 / 1000

    Theoretical_wind_GW = (1.5/0.25) * coastline/1000
    Technical_wind_GW = Theoretical_wind_GW * available_coastline
    Technical_wind_GW = Technical_wind_GW.astype(float)
    Technical_wind_GW = Technical_wind_GW.round(decimals=1)

    Theoretical_PV_GWh = Theoretical_PV_GWh.astype(int)
    Theoretical_wind_GWh = Theoretical_wind_GWh.astype(float)
    Theoretical_wind_GWh = Theoretical_wind_GWh.round(decimals= 1)

    Theoretical_PV_GW = Theoretical_PV_GW.astype(int)
    Theoretical_wind_GW = Theoretical_wind_GW.astype(float)
    Theoretical_wind_GW = Theoretical_wind_GW.round(decimals= 2)
    Technical_PV_GW = Technical_PV_GW.astype(float)
    Technical_PV_GW = Technical_PV_GW.round(decimals=2)

    Technical_PV_GWh = Technical_PV_GWh.astype(float)
    Technical_PV_GWh = Technical_PV_GWh.round(decimals=1)

    Technical_wind_GWh = Technical_wind_GWh.astype(float)
    Technical_wind_GWh = Technical_wind_GWh.round(decimals=1)

    df_technical_potential['Country'] = countries
    df_technical_potential['PV_pot'] = PV_pot.values
    df_technical_potential['Wind_pot'] = Wind_pot.values
    df_technical_potential['Theoretical_PV_GWh'] = Theoretical_PV_GWh.values
    df_technical_potential['Theoretical_wind_GWh'] = Theoretical_wind_GWh.values

    df_technical_potential['Theoretical_PV_GW'] = Theoretical_PV_GW.values
    df_technical_potential['Theoretical_wind_GW'] = Theoretical_wind_GW.values

    df_technical_potential['PV_technical_GWh'] = Technical_PV_GWh.values
    df_technical_potential['Wind_technical_GWh'] = Technical_wind_GWh.values

    df_technical_potential['PV_technical_GW'] = Technical_PV_GW.values
    df_technical_potential['Wind_technical_GW'] = Technical_wind_GW.values

    df_technical_potential['sum_of_wind_and_solar_GWh'] = df_technical_potential['PV_technical_GWh'] + df_technical_potential['Wind_technical_GWh']

    df_technical_potential.to_csv('Wind_and_solar_technical_potential.csv')

    return df_technical_potential

def calculate_rooftop_PV_potential(available_buildings = 0.3,PV_size = 2.5):
    import pandas as pd
    rooftop_df = pd.DataFrame()
    df = pd.read_csv('Data/Rooftop Potential.csv')
    Countries = df['Country']
    Population = df['Population']
    Household_size = df['Household size']
    solar_radiation = df['Potential of Av.PV gen (GWh/MW/year)']
    number_of_homes = available_buildings*Population/Household_size # only those homes with rooftop PV potential
    number_of_homes = number_of_homes.round(0)
    rooftop_capacity_MW = number_of_homes * PV_size/1000
    rooftop_capacity_MW = rooftop_capacity_MW.round(1)
    rooftop_PV_generation_GWh = rooftop_capacity_MW * solar_radiation
    rooftop_PV_generation_GWh = rooftop_PV_generation_GWh.astype(float)
    rooftop_PV_generation_GWh = rooftop_PV_generation_GWh.round(decimals=1)

    rooftop_df['Generation_GWh'] = rooftop_PV_generation_GWh
    rooftop_df['Country'] = Countries
    rooftop_df['Capacity_MW'] = rooftop_capacity_MW
    rooftop_df['avaialble_homes'] = number_of_homes
    rooftop_df['Household_size'] = Household_size
    rooftop_df['Population'] = Population


    rooftop_df.to_csv('rooftop_Pv_potential.csv')

    return rooftop_df
