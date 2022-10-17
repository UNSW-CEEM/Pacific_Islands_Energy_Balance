import pandas as pd
import functions
def calculate_community_battery_size(country,residential_battery_capacity,demand_scenario="Decarbonization", total_storage_days = 5):
    demand = functions.fetch_single_country_demand(Country=country,Year=2019)
    if demand_scenario == "World average":
        demand = demand * 0.8
    daily_average_demand = demand/365
    total_storage_capacity_GWh = total_storage_days * daily_average_demand
    community_storage_capacity = total_storage_capacity_GWh - residential_battery_capacity

    return community_storage_capacity



def run_decarbonization_scenario():
    pass

calculate_community_battery_size("PNG",5)