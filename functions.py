import pandas as pd
import numpy as np


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
    #previously
    # final_demand = df[df['Transactions(down)/Commodity(right)']=='Total energy supply']['Total Energy'].values[0] #TJ

    if Unit =='GWh':
        final_demand = final_demand * 0.277778
        non_RE_demand = non_RE_demand * 0.277778
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

    ElectricitySupply = df[df['Transactions(down)/Commodity(right)']=='Transformation']['Electricity'].values #TJ
    ofWhichRenewable_transformation = -df[df['Transactions(down)/Commodity(right)']=='Transformation']['memo: Of which Renewables'].values #TJ # This is the input to power plants
    renewable_transformation_efficiency = 0.35
    non_RE_demand =  ElectricitySupply - ofWhichRenewable_transformation * renewable_transformation_efficiency #TJ

    if Use == 'Analysis':
        electrification_efficiency_improvement = 0.4
        final_consumption = df[df['Transactions(down)/Commodity(right)']=='Final consumption']['Total Energy'].values #TJ#Does not include fuel for transformation. Only output of power plants and energy delivered to users
        ofWhichRenewable_final_consumption = df[df['Transactions(down)/Commodity(right)']=='Final consumption']['memo: Of which Renewables'].values #TJ # This is the input to power plants
        final_consumption_electricity = df[df['Transactions(down)/Commodity(right)']=='Final consumption']['Electricity'].values
        total_demand = non_RE_demand + (final_consumption-final_consumption_electricity-ofWhichRenewable_final_consumption) * (1-electrification_efficiency_improvement)



    #previously
    if Use == 'SummaryPlot':
        total_demand = df[df['Transactions(down)/Commodity(right)']=='Total energy supply']['Total Energy'].values #TJ#Total energy entering the country(oil and renewables)

    renewables_in_total = df[df['Transactions(down)/Commodity(right)']=='Total energy supply']['memo: Of which Renewables'].values #TJ
    renewable_electricity = df[df['Transactions(down)/Commodity(right)']=='Primary production']['Electricity'].values #TJ
    imports = df[df['Transactions(down)/Commodity(right)']=='Imports']['All Oil'].values
    all_imports = df[df['Transactions(down)/Commodity(right)']=='Imports']['Total Energy'].values

    Int_marine = df[df['Transactions(down)/Commodity(right)']=='International marine bunkers']['All Oil'].values
    Int_avi = df[df['Transactions(down)/Commodity(right)']=='International aviation bunkers']['All Oil'].values
    transformation = -df[df['Transactions(down)/Commodity(right)']=='Electricity  CHP & Heat Plants']['All Oil'].values
    transformation_losses = - df[df['Transactions(down)/Commodity(right)']=='Electricity  CHP & Heat Plants']['Total Energy'].values
    if Unit == "GWh":
        non_RE_demand = non_RE_demand * 0.277778
        total_demand = total_demand * 0.277778
        imports = imports * 0.277778
        Int_marine = Int_marine * 0.277778
        Int_avi = Int_avi * 0.277778
        transformation = transformation * 0.277778
        transformation_losses = transformation_losses * 0.277778
        renewables_in_total = renewables_in_total * 0.277778
        renewable_electricity = renewable_electricity * 0.277778
        all_imports = all_imports * 0.277778
        df_demand = pd.DataFrame()
        df_demand['Country'] = Countries
        df_demand['Non-RE'] = non_RE_demand
        df_demand['Total'] = total_demand
        df_demand.to_csv('demand_df.csv')

    return [Countries,total_demand,imports,Int_marine,Int_avi,transformation,
            transformation_losses,renewables_in_total,
            renewable_electricity,non_RE_demand,all_imports]

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

    summary_df['Renewables/Total_demand'] = 100 * summary_df['renewables_in_total']/summary_df['Total_demand']
    summary_df['Renewables/Total_demand']=summary_df['Renewables/Total_demand'].round(1)

    summary_df['Renewables/Total_imports'] = 100 * summary_df['renewables_in_total']/summary_df['total imports']
    summary_df['Renewables/Total_imports']=summary_df['Renewables/Total_imports'].round(1)

    summary_df['Renewables/capita'] = (summary_df['renewables_in_total']/population['Population']) * 1000000 #MJ
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
