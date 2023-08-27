import pandas as pd
import functions
from EnergyFlows import Country_List


def calculate_community_battery_size(
    demand,
    total_rooftop_PV_capacity_MW,
    technical_pot,
    rooftop_size,
    res_battery_size,
    total_storage_days=5,
):

    number_of_homes = total_rooftop_PV_capacity_MW * 1000 / rooftop_size
    total_res_storage_capacity_GWh = number_of_homes * res_battery_size / 1000000

    average_daily_demand = demand / 365  # GWH/day
    if demand <= technical_pot:
        total_storage_capacity_GWh = average_daily_demand * total_storage_days
    elif demand > technical_pot:
        total_storage_capacity_GWh = (average_daily_demand * total_storage_days) * (
            technical_pot / demand
        )
    community_battery = max(
        total_storage_capacity_GWh - total_res_storage_capacity_GWh, 0
    )

    return community_battery, total_res_storage_capacity_GWh


def calculate_demand(country, demand_scenario):
    if demand_scenario == "Decarbonization":
        demand = functions.fetch_single_country_demand(Country=country, Year=2019)[0]
    elif demand_scenario == "Electrification":
        demand = functions.fetch_single_country_demand(Country=country, Year=2019)[1]
    elif demand_scenario == "Net_zero":
        demand = functions.fetch_single_country_demand(Country=country, Year=2019)[2]

    return demand


def calculate_renewable_technical_potential(
    country, available_land, avaialble_coastline, avaialble_buildings=0.3, PV_size=2.5
):
    technical_potential_df = functions.calculate_PV_Wind_potential(
        available_land=available_land, available_coastline=avaialble_coastline
    )
    PV_technical_potential = technical_potential_df[
        technical_potential_df["Country"] == country
    ]["PV_technical_GWh"].values[0]
    Wind_technical_potential = technical_potential_df[
        technical_potential_df["Country"] == country
    ]["Wind_technical_GWh"].values[0]

    rooftop_df = functions.calculate_rooftop_PV_potential(
        available_buildings=avaialble_buildings, PV_size=PV_size
    )
    rooftop_potential = rooftop_df[rooftop_df["Country"] == country][
        "Generation_GWh"
    ].values[0]

    total = PV_technical_potential + Wind_technical_potential + rooftop_potential
    return {
        "PV_tech_GWh": PV_technical_potential,
        "Wind_tech_GWh": Wind_technical_potential,
        "Rooftop_GWh": rooftop_potential,
        "Total": total,
    }


def calculate_capacity_of_each_technology(
    country, dic_potential, demand, demand_scenario, cost_dic
):

    rooftop_PV_GWh = min(dic_potential["Rooftop_GWh"], demand)
    rooftop_PV_GWh = max(0, rooftop_PV_GWh)

    large_PV_GWh = min(dic_potential["PV_tech_GWh"], demand - rooftop_PV_GWh)
    large_PV_GWh = max(0, large_PV_GWh)

    wind_GWh = min(
        dic_potential["Wind_tech_GWh"], demand - rooftop_PV_GWh - large_PV_GWh
    )
    wind_GWh = max(0, wind_GWh)

    diesel_GWh = calculate_demand(country, demand_scenario) - calculate_demand(
        country, "Decarbonization"
    )

    df_potentials = pd.read_excel("Data/Potentials.xlsx")
    PV_pot = df_potentials.iloc[0, 2:]  # GWh/MW/year
    Wind_pot = df_potentials.iloc[2, 2:]  # GWh/MW/year

    PV_pot = PV_pot[country]
    Wind_pot = Wind_pot[country]

    rooftop_MW = rooftop_PV_GWh / PV_pot  # MW
    large_PV_MW = large_PV_GWh / PV_pot  # MW

    wind_MW = wind_GWh / Wind_pot

    total_GWh = wind_GWh + large_PV_GWh + rooftop_PV_GWh

    community_battery_GWh, res_battery_GWh = calculate_community_battery_size(
        demand=demand,
        total_rooftop_PV_capacity_MW=rooftop_MW,
        technical_pot=total_GWh,
        total_storage_days=cost_dic["storage_days"],
        rooftop_size=cost_dic["rooftop_size"],
        res_battery_size=cost_dic["res_battery_size"],
    )

    return {
        "Rooftop_MW": round(rooftop_MW, 2),
        "Large_PV_MW": round(large_PV_MW,2),
        "Wind_MW": round(wind_MW,2),
        "residential_battery_GWh": res_battery_GWh,
        "total_GWh": total_GWh,
        "Community_battery_GWh": community_battery_GWh,
        "diesel_GWh": diesel_GWh,
    }


def create_yearly_df(
    country,
    decarb_year,
    capacity_dic,
    cost_dic,
    diesel_price,
):
    from datetime import datetime

    now = datetime.now().year
    number_of_years = decarb_year - 2022
    year_list = []
    installation_df = pd.DataFrame()

    for i in range(0, 31):
        now += 1
        year_list.append(now)

    installation_df["Year"] = year_list
    installation_df["rooftop_MW"] = capacity_dic["Rooftop_MW"] / number_of_years
    installation_df["resid_battery_GWh"] = (
        capacity_dic["residential_battery_GWh"] / number_of_years
    )
    installation_df["PV_MW"] = capacity_dic["Large_PV_MW"] / number_of_years
    installation_df["wind_MW"] = capacity_dic["Wind_MW"] / number_of_years
    installation_df["Community_battery_GWh"] = (
        capacity_dic["Community_battery_GWh"] / number_of_years
    )
    installation_df["Diesel_GWh"] = capacity_dic["diesel_GWh"] / number_of_years
    installation_df["Diesel_MW"] = (installation_df["Diesel_GWh"] / (0.7 * 8760)) * 1000

    installation_df.loc[number_of_years:, "rooftop_MW"] = 0
    installation_df.loc[number_of_years:, "resid_battery_GWh"] = 0
    installation_df.loc[number_of_years:, "PV_MW"] = 0
    installation_df.loc[number_of_years:, "wind_MW"] = 0
    installation_df.loc[number_of_years:, "Community_battery_GWh"] = 0
    installation_df.loc[number_of_years:, "Diesel_MW"] = 0

    # costs are $/W - 1000000/MW
    # The output is #$
    installation_df["installation_Cost"] = (
        installation_df["rooftop_MW"] * cost_dic["rooftop"]
        + installation_df["resid_battery_GWh"] * cost_dic["resid_battery"] * 1000
        + installation_df["Community_battery_GWh"] * 1000 * cost_dic["comm_battery"]
        + installation_df["PV_MW"] * cost_dic["large_PV"]
        + installation_df["wind_MW"] * cost_dic["wind"]
        - installation_df["Diesel_MW"] * cost_dic["diesel_cap"]
    ) * 1000000  # Convert to $/MW #in the cost dic, are costs are $/W
    installation_df["installation_Cost_original"] = installation_df["installation_Cost"]
    installation_df["avoided_demand_GWh"] = capacity_dic["total_GWh"] / number_of_years
    installation_df.loc[number_of_years:, "avoided_demand_GWh"] = 0

    installation_df["avoided_emissions_tonne"] = (
        installation_df["avoided_demand_GWh"] * cost_dic["emissiont/GWh_diesel"]
    )
    installation_df["cumulative_avoided_emissions_tonne"] = installation_df[
        "avoided_emissions_tonne"
    ].cumsum(axis=0)
    installation_df["emission_cost_$"] = (
        installation_df["cumulative_avoided_emissions_tonne"] * cost_dic["carbon_price"]
    )

    diesel_generation = 2.5  # kWh/Liter
    installation_df["avoided_diesel_liter"] = installation_df["avoided_demand_GWh"] / (
        diesel_generation / 1000000
    )
    installation_df["cumulative_avoided_diesel_liter"] = installation_df[
        "avoided_diesel_liter"
    ].cumsum(axis=0)
    installation_df["avoided_diesel_savings"] = (
        installation_df["cumulative_avoided_diesel_liter"] * diesel_price
    )

    if country == "New Caledonia":
        # coal price is 400 USD/Tonne
        # 47% demand is met by diesel, and 53% by coal
        # 0.00814 GWh energy in one tonne coal.

        df = pd.read_csv("Data/Sankey/csv/{}/{}.csv".format(2019, country))
        to_power_stations = df[df[" (to)"] == "PowerStations"][" (weight)"].values[0]
        coal = df[
            (df[" (to)"] == "PowerStations") & (df[" (from)"] == "Coal: Supplied")
        ][" (weight)"].values[0]
        oil = df[(df[" (to)"] == "PowerStations") & (df[" (from)"] == "Oil: Supplied")][
            " (weight)"
        ].values[0]

        installation_df["avoided_diesel_liter"] = installation_df[
            "avoided_diesel_liter"
        ] * (oil / to_power_stations)

        installation_df["avoided_emissions_tonne"] = installation_df[
            "avoided_demand_GWh"
        ] * (
            (oil / to_power_stations) * cost_dic["emissiont/GWh_diesel"]
            + (coal / to_power_stations) * cost_dic["emissiont/GWh_blackCoal"]
        )
        installation_df["cumulative_avoided_emissions_tonne"] = installation_df[
            "avoided_emissions_tonne"
        ].cumsum(axis=0)
        installation_df["emission_cost_$"] = (
            installation_df["cumulative_avoided_emissions_tonne"]
            * cost_dic["carbon_price"]
        )

        installation_df["avoided_coal_tonne"] = (
            installation_df["avoided_demand_GWh"] * (coal / to_power_stations)
        ) / (0.00814 * 0.35)

        installation_df["cumulative_avoided_diesel_liter"] = installation_df[
            "avoided_diesel_liter"
        ].cumsum(axis=0)
        installation_df["cumulative_avoided_coal_tonne"] = installation_df[
            "avoided_coal_tonne"
        ].cumsum(axis=0)

        installation_df["avoided_diesel_savings"] = (
            installation_df["cumulative_avoided_diesel_liter"] * diesel_price
        )
        installation_df["avoided_coal_savings"] = (
            installation_df["cumulative_avoided_coal_tonne"] * cost_dic["coal"]
        )
        installation_df["avoided_diesel_savings"] = (
            installation_df["avoided_diesel_savings"]
            + installation_df["avoided_coal_savings"]
        )
    if country == "PNG":
        df = pd.read_csv("Data/Sankey/csv/{}/{}.csv".format(2019, country))
        to_power_stations = df[df[" (to)"] == "PowerStations"][" (weight)"].values[0]
        oil = df[(df[" (to)"] == "PowerStations") & (df[" (from)"] == "Oil: Supplied")][
            " (weight)"
        ].values[0]
        natural_gas = df[
            (df[" (to)"] == "PowerStations")
            & (df[" (from)"] == "Natural Gas: Supplied")
        ][" (weight)"].values[0]

        perc_oil = oil / to_power_stations
        perc_gas = natural_gas / to_power_stations

        installation_df["avoided_diesel_liter"] = (
            (perc_oil + perc_gas)
            * installation_df["avoided_demand_GWh"]
            / (diesel_generation / 1000000)
        )
        # site for natural gass generation
        # https: // www.eia.gov / tools / faqs / faq.php?id = 667 & t = 8
        # Electricity generation from natural gas# 0.14 kWh/cf3 = 4.94 kWh/m3 = 4.94e-6 GWh/m3
        # NAtural gas thermal energy kWh to m3: 10kWh/m3
        # Natural gas price:
        # https: // www.globalpetrolprices.com / Papua - New - Guinea / natural_gas_prices /
        # installation_df["avoided_gas_m3"] = (
        #     perc_gas * (installation_df["avoided_demand_GWh"]) * 1000000 / 4.94
        # )
        installation_df["cumulative_avoided_diesel_liter"] = installation_df[
            "avoided_diesel_liter"
        ].cumsum(axis=0)
        # installation_df["cumulative_avoided_gas_m3"] = installation_df[
        #     "avoided_gas_m3"
        # ].cumsum(axis=0)
        #
        installation_df["avoided_emissions_tonne"] = installation_df[
            "avoided_demand_GWh"
        ] * ((perc_oil + perc_gas) * cost_dic["emissiont/GWh_diesel"])
        installation_df["cumulative_avoided_emissions_tonne"] = installation_df[
            "avoided_emissions_tonne"
        ].cumsum(axis=0)
        installation_df["emission_cost_$"] = (
            installation_df["cumulative_avoided_emissions_tonne"]
            * cost_dic["carbon_price"]
        )

        installation_df["avoided_diesel_savings"] = (
            installation_df["cumulative_avoided_diesel_liter"] * diesel_price
        )
        #
        # installation_df["avoided_gas_savings"] = (
        #     installation_df["cumulative_avoided_gas_m3"] * cost_dic["gas$/m3"]
        # )

    installation_df["avoided_diesel_savings"] = (
        installation_df["avoided_diesel_savings"] + installation_df["emission_cost_$"]
    )

    installation_df["Cumulative_avoided_cost"] = installation_df[
        "avoided_diesel_savings"
    ].cumsum(axis=0)

    inflation_rate = cost_dic["inflation_rate"] / 100
    discount_rate = cost_dic["discount_rate"] / 100

    for i, row in installation_df.iterrows():
        installation_df.at[i, "Cumulative_avoided_cost"] = (
            installation_df.at[i, "Cumulative_avoided_cost"]
            * ((1 + inflation_rate) / (1 + discount_rate)) ** i
        )
        installation_df.at[i, "installation_Cost"] = (
            installation_df.at[i, "installation_Cost"]
            * ((1 + inflation_rate) / (1 + discount_rate)) ** i
        )

    installation_df["Annual_Net_saving"] = (
        installation_df["Cumulative_avoided_cost"]
        - installation_df["installation_Cost"]
    )  # $MM
    installation_df["Cumulative_net_saving"] = installation_df[
        "Annual_Net_saving"
    ].cumsum(axis=0)

    return installation_df


def calculate_diesel_price(country,cost_dic):
    diesel_df = pd.read_csv("Data/Diesel.csv")
    if country in diesel_df["Country"].to_list():
        diesel_price = diesel_df[diesel_df["Country"] == country][
            "Tax included"
        ].values[0]
    else:
        diesel_price = diesel_df["Tax included"].mean()

    diesel_price = diesel_price  # 20c less than retails price
    diesel_price = diesel_price / 100  # convert to $ from cents

    return diesel_price


def run_decarbonization_scenario(
    cost_scenario,
    country_list,
    demand_scenario="Decarbonization",
    available_land=0.02,
    avaialble_coastline=0.1,
    avaialble_buildings=0.3,
    PV_size=2.5,
    decarb_year=2030,
    input_dicts=None,
):
    df_GDP = pd.read_csv("Data/Economic Indicators.csv")

    costs = {
        "optimistic": {
            "diesel_cap": 3,
            "rooftop": 2.5,
            "resid_battery": 2.5,
            "comm_battery": 1.5,
            "large_PV": 2.5,
            "wind": 3,
            "coal": 400,
            "discount_rate": 6,
            "inflation_rate": 3,
            "diesel_dif": 0,
            "storage_days": 4,
            "gas$/m3": "Nan",
            "emissiont/GWh_diesel": 1100,  # AEMO:0.7-1.5
            "emissiont/GWh_blackCoal": 900,  # AEMO:0.7-1.5
            "emissiont/GWh_brownCoal": 1200,  # AEMO:1.1-1.3
            "carbon_price": 0,  # $/tonne
            "rooftop_size": 2.5,
            "res_battery_size": 5
        },  # $/W
        "pessimistic": {
            "diesel_cap": 2,
            "rooftop": 4.5,
            "resid_battery": 4,
            "comm_battery": 3,
            "large_PV": 4.5,
            "wind": 6,
            "coal": 400,
            "discount_rate": 6,
            "inflation_rate": 3,
            "diesel_dif": 20,
            "storage_days": 5,
            "gas$/m3": "Nan",
            "emissiont/GWh_diesel": 1100,  # AEMO:0.7-1.5
            "emissiont/GWh_blackCoal": 1000,  # AEMO:0.7-1.5
            "emissiont/GWh_brownCoal": 1200,  # AEMO:1.1-1.3
            "carbon_price": 0,  # $/tonne
            "rooftop_size": 2.5,
            "res_battery_size": 5
        },
    }
    all_countries_result = pd.DataFrame()
    all_countries_result["Technology"] = [
        "Rooftop_MW",
        "Large_PV_MW",
        "Wind_MW",
        "resid_battery_GWh",
        "Community_battery_GWh",
        "total_GWh",
        "Payback period (years)",
        "installation_cost ($)",
        "GDP ($)",
        "GDP/installation_cost",
        "Total_storage_GWh",
    ]

    if input_dicts is None:
        cost_dic = costs[
            cost_scenario
        ]  # Here I should create the cost dic after entering in the GUI
    else:
        cost_dic = input_dicts
    for country in country_list:
        GDP = df_GDP[df_GDP["Country"] == country]["GDP(million$)2019"].values[0]
        if input_dicts is None:
            diesel_price = calculate_diesel_price(country=country, cost_dic=cost_dic)
        else:
            diesel_price = cost_dic["diesel_price"]
        pot = calculate_renewable_technical_potential(
            country,
            available_land=available_land,
            avaialble_coastline=avaialble_coastline,
            avaialble_buildings=avaialble_buildings,
            PV_size=PV_size,
        )
        demand = calculate_demand(country, demand_scenario)
        capacity_dic = calculate_capacity_of_each_technology(
            country, pot, demand, demand_scenario, cost_dic
        )
        final_df = create_yearly_df(
            country=country,
            decarb_year=decarb_year,
            capacity_dic=capacity_dic,
            cost_dic=cost_dic,
            diesel_price=diesel_price,
        )
        if input_dicts is None:

            final_df.to_csv(
                "Results/{}/Simulation_result_{}.csv".format(demand_scenario, country)
            )
        total_cost = final_df["installation_Cost_original"].sum()
        try:
            payback_period = final_df[
                final_df.Cumulative_net_saving < 0
            ].index.values.max()
        except:
            payback_period = 0
        gdp_to_cost = int(100 * GDP / (total_cost / 1000000))
        all_countries_result[country] = [
            round(capacity_dic["Rooftop_MW"],2),
            round(capacity_dic["Large_PV_MW"],2),
            round(capacity_dic["Wind_MW"],1),
            round(capacity_dic["residential_battery_GWh"],5),
            round(capacity_dic["Community_battery_GWh"],5),
            capacity_dic["total_GWh"],
            int(payback_period),
            total_cost,
            GDP,
            gdp_to_cost,
            capacity_dic["residential_battery_GWh"]
            + capacity_dic["Community_battery_GWh"],
        ]

    all_countries_result.reset_index(drop=True, inplace=True)
    if input_dicts is None:
        all_countries_result.to_excel(
            "Results/{}/{}_simulation_result_{}_wind_{}_PV_{}_carbon_{}.xlsx".format(
                demand_scenario,
                cost_scenario,
                demand_scenario,
                avaialble_coastline,
                available_land,
                cost_dic["carbon_price"],
            )
        )
    if input_dicts is None:
        return final_df
    else:
        return final_df, all_countries_result


if __name__ == "__main__":

    for cost_scenario in ["optimistic", "pessimistic"]:
        for demand_sceanrio in ["Decarbonization", "Electrification", "Net_zero"]:
            run_decarbonization_scenario(
                cost_scenario=cost_scenario,
                country_list=Country_List,
                demand_scenario=demand_sceanrio,
                available_land=0.02,
                avaialble_coastline=0.1,
                avaialble_buildings=0.3,
                PV_size=2.5,
                decarb_year=2040,
                input_dicts=None
            )

    # check community battery
