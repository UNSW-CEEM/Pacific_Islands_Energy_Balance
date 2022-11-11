import pandas as pd
import functions
from EnergyFlows import Country_List
def calculate_community_battery_size(demand,residential_battery_capacity,technical_pot,total_storage_days = 5):
    average_daily_demand = demand/365 #GWH/day
    if demand <= technical_pot:
        total_storage_capacity_GWh = average_daily_demand * total_storage_days
    elif demand > technical_pot:
        total_storage_capacity_GWh = (average_daily_demand * total_storage_days)*(technical_pot/demand)
    community_battery = max(total_storage_capacity_GWh - residential_battery_capacity,0)

    return community_battery

def calculate_demand(country,demand_scenario):
    if demand_scenario == "Decarbonization":
        demand = functions.fetch_single_country_demand(Country=country,Year=2019)[0]
    elif demand_scenario == "Electrification":
        demand = functions.fetch_single_country_demand(Country=country, Year=2019)[1]
    elif demand_scenario == "Net_zero":
        demand = functions.fetch_single_country_demand(Country=country, Year=2019)[2]

    return demand

def calculate_renewable_technical_potential(country,available_land,avaialble_coastline,avaialble_buildings=0.3,PV_size=2.5):
    technical_potential_df  = functions.calculate_PV_Wind_potential(available_land=available_land, available_coastline=avaialble_coastline)
    PV_technical_potential = technical_potential_df[technical_potential_df['Country'] == country]['PV_technical_GWh'].values[0]
    Wind_technical_potential = technical_potential_df[technical_potential_df['Country'] == country]['Wind_technical_GWh'].values[0]

    rooftop_df = functions.calculate_rooftop_PV_potential(available_buildings=avaialble_buildings,PV_size=PV_size)
    rooftop_potential = rooftop_df[rooftop_df['Country'] == country]['Generation_GWh'].values[0]
    # print(PV_technical_potential,Wind_technical_potential,rooftop_potential)

    total = PV_technical_potential + Wind_technical_potential + rooftop_potential
    return {"PV_tech_GWh":PV_technical_potential,"Wind_tech_GWh":Wind_technical_potential,"Rooftop_GWh":rooftop_potential,"Total":total}

def calculate_capacity_of_each_technology(country,dic_potential,demand):

    rooftop_PV_GWh = min(dic_potential["Rooftop_GWh"],demand)
    rooftop_PV_GWh = max(0,rooftop_PV_GWh)

    large_PV_GWh = min(dic_potential["PV_tech_GWh"],demand-rooftop_PV_GWh)
    large_PV_GWh = max(0,large_PV_GWh)

    wind_GWh = min(dic_potential["Wind_tech_GWh"],demand-rooftop_PV_GWh-large_PV_GWh)
    wind_GWh = max(0,wind_GWh)

    df_potentials = pd.read_excel('Data/Potentials.xlsx')
    PV_pot = df_potentials.iloc[0, 2:] #GWh/MW/year
    Wind_pot =df_potentials.iloc[2, 2:] #GWh/MW/year

    PV_pot = PV_pot[country]
    Wind_pot = Wind_pot[country]
    # print(PV_pot[country])

    rooftop_MW = rooftop_PV_GWh/PV_pot #MW
    large_PV_MW = large_PV_GWh/PV_pot #MW

    wind_MW = wind_GWh/Wind_pot

    total_GWh = wind_GWh + large_PV_GWh + rooftop_PV_GWh

    community_battery = calculate_community_battery_size(demand=demand,residential_battery_capacity = rooftop_MW*2/1000,technical_pot=total_GWh,total_storage_days=5 )

    return {"Rooftop_MW":rooftop_MW,"Large_PV_MW":large_PV_MW,"Wind_MW":wind_MW,"residential_battery_MWh":rooftop_MW*2,"total_GWh":total_GWh,"Community_battery_GWh":community_battery}


def create_yearly_df(country,decarb_year,capacity_dic,cost_dic,diesel_price,inflation_rate, discount_rate):
    from datetime import datetime
    now = datetime.now().year
    number_of_years = decarb_year - 2022
    year_list = []
    installation_df = pd.DataFrame()

    for i in range(0, 31):
        now += 1
        year_list.append(now)

    # community_battery = calculate_community_battery_size(demand=)
    installation_df['Year'] = year_list
    installation_df['rooftop_MW'] = capacity_dic["Rooftop_MW"]/number_of_years
    installation_df['resid_battery_MW'] = installation_df['rooftop_MW'] * 2
    installation_df['PV_MW'] = capacity_dic["Large_PV_MW"]/number_of_years
    installation_df['wind_MW'] = capacity_dic["Wind_MW"]/number_of_years
    installation_df["Community_battery_GWh"] = capacity_dic['Community_battery_GWh']/number_of_years

    installation_df.loc[number_of_years:,'rooftop_MW'] = 0
    installation_df.loc[number_of_years:,'resid_battery_MW'] = 0
    installation_df.loc[number_of_years:,'PV_MW'] = 0
    installation_df.loc[number_of_years:,'wind_MW'] = 0
    installation_df.loc[number_of_years:,"Community_battery_GWh"] = 0

    # costs are $/W - 1000000/MW
    # The output is #$
    installation_df['installation_Cost'] = (installation_df['rooftop_MW'] * cost_dic['rooftop'] +
                                            installation_df['resid_battery_MW'] *cost_dic['resid_battery'] +
                                            installation_df['Community_battery_GWh']*1000 *cost_dic['resid_battery'] +
                                            installation_df['PV_MW'] * cost_dic['large_PV'] +\
                                           installation_df['wind_MW'] * cost_dic['wind'])*1000000#Convert to $/MW #in the cost dic, are costs are $/W


    installation_df['avoided_demand_GWh'] = capacity_dic["total_GWh"]/number_of_years
    installation_df.loc[number_of_years:,'avoided_demand_GWh'] = 0

    diesel_efficiency = 0.4

    diesel_generatio = 2.5 #kWh/Liter
    installation_df["avoided_diesel_liter"] = installation_df["avoided_demand_GWh"] / (2.5/1000000)
    installation_df["cumulative_avoided_diesel_liter"] = installation_df["avoided_diesel_liter"].cumsum(axis=0)
    installation_df["avoided_diesel_savings"] = installation_df["cumulative_avoided_diesel_liter"] * diesel_price

    if country =="New Caledonia":
        #coal price is 400 USD/Tonne
        # 47% demand is met by diesel, and 53% by coal
        # 0.00814 GWh energy in one tonne coal.
        installation_df["avoided_diesel_liter"] = installation_df["avoided_diesel_liter"]*0.47
        installation_df["avoided_coal_tonne"] = (installation_df["avoided_demand_GWh"]*0.53)/(0.00814 * 0.35)

        installation_df["cumulative_avoided_diesel_liter"] = installation_df["avoided_diesel_liter"].cumsum(axis=0)
        installation_df["cumulative_avoided_coal_tonne"] = installation_df["avoided_coal_tonne"].cumsum(axis=0)

        installation_df["avoided_diesel_savings"] = installation_df["cumulative_avoided_diesel_liter"] * diesel_price
        installation_df["avoided_coal_savings"] = installation_df["cumulative_avoided_coal_tonne"] * 400
        installation_df["avoided_diesel_savings"] = installation_df["avoided_diesel_savings"] + installation_df["avoided_coal_savings"]

    installation_df['Cumulative_avoided_cost'] = installation_df['avoided_diesel_savings'].cumsum(axis=0)

    inflation_rate = inflation_rate/100
    discount_rate = discount_rate/100

    for i, row in installation_df.iterrows():
        installation_df.at[i, 'Cumulative_avoided_cost'] = installation_df.at[i, 'Cumulative_avoided_cost'] * ((1+inflation_rate)/(1+discount_rate))**i
        installation_df.at[i, 'installation_Cost'] = installation_df.at[i, 'installation_Cost'] * ((1+inflation_rate)/(1+discount_rate))**i

    installation_df['Annual_Net_saving'] = installation_df['Cumulative_avoided_cost'] - installation_df['installation_Cost']  # $MM
    installation_df["Cumulative_net_saving"] = installation_df['Annual_Net_saving'].cumsum(axis=0)

    return installation_df
    # demand_df['Net_saving_discounted'] = 0
    # demand_df['Emission_red_saving_discounted'] = 0
    # inflation_rate = inflation_rate/100
    # discount_rate = discount_rate/100

def calculate_diesel_price(country):
    diesel_df = pd.read_csv("Data/Diesel.csv")
    if country in diesel_df["Country"].to_list():
        print("Hi")
        diesel_price = diesel_df[diesel_df['Country'] == country]['Tax included'].values[0]
    else:
        diesel_price = diesel_df['Tax included'].mean()

    diesel_price = diesel_price-20 #20c less than retails price
    diesel_price = diesel_price/100 # convert to $ from cents

    print(diesel_price)
    return diesel_price


def run_decarbonization_scenario(cost_scenario,country_list,demand_scenario="Decarbonization",available_land=0.02, avaialble_coastline=0.1,avaialble_buildings=0.3,PV_size=2.5,decarb_year=2030):
    # demand_scenario = ["Decarbonization","Electrification","Net_zero"]
    costs= {"optimistic":{"rooftop":3,"resid_battery":4,"large_PV":3,"wind":3},"pessimistic":{"rooftop":4.5,"resid_battery":4,"large_PV":4.5,"wind":6}}
    all_countries_result = pd.DataFrame()
    all_countries_result['Technology'] =["Rooftop_MW", "Large_PV_MW","Wind_MW","Residential_battery_MWh","Community_battery_GWh","total_GWh",'Payback period (years)']
    # : rooftop_MW, : large_PV_MW, : wind_MW, : total_GWh, : community_battery
    # cost_dic = {"rooftop":4.5,"resid_battery":4,"large_PV":4.5,"wind":6}#Pessimistic
    # cost_dic = {"rooftop":3,"resid_battery":4,"large_PV":3,"wind":3}#Optimistic
    cost_dic = costs[cost_scenario]
    for country in country_list:
        diesel_price = calculate_diesel_price(country)
        pot = calculate_renewable_technical_potential(country, available_land=available_land, avaialble_coastline=avaialble_coastline,avaialble_buildings=avaialble_buildings,PV_size=PV_size)
        demand = calculate_demand(country, demand_scenario)
        capacity_dic = calculate_capacity_of_each_technology(country, pot, demand)
        final_df = create_yearly_df(country=country,decarb_year=decarb_year,capacity_dic=capacity_dic,cost_dic=cost_dic,diesel_price=diesel_price,inflation_rate=3,discount_rate=7)
        final_df.to_csv("Results/{}/Simulation_result_{}.csv".format(demand_scenario,country))

        payback_period = final_df[final_df.Cumulative_net_saving < 0].index.values.max()

        all_countries_result[country] = [capacity_dic["Rooftop_MW"],
                                         capacity_dic["Large_PV_MW"],
                                         capacity_dic["Wind_MW"],
                                         capacity_dic["residential_battery_MWh"],
                                         capacity_dic["Community_battery_GWh"],
                                         capacity_dic["total_GWh"],
                                         payback_period
                                         ]

    all_countries_result.reset_index(drop=True,inplace=True)
    # all_countries_result = all_countries_result.pivot(columns="Technology",index=all_countries_result.columns)[all_countries_result.columns]

    all_countries_result.to_excel("Results/{}/{}_simulation_result_{}_wind_{}_PV_{}.xlsx".format(demand_scenario,cost_scenario,demand_scenario,avaialble_coastline,available_land))
    # print(all_countries_result.head())
    return final_df

for cost_scenario in ["optimistic",'pessimistic']:
    for demand_sceanrio in ['Decarbonization',"Electrification","Net_zero"]:
        run_decarbonization_scenario(cost_scenario=cost_scenario,country_list=Country_List,
                             demand_scenario=demand_sceanrio,available_land=0.1,
                             avaialble_coastline=0,avaialble_buildings=0.3,
                             PV_size=2.5,decarb_year=2030)


#check community battery