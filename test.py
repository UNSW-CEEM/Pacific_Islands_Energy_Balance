import pandas as pd
from EnergyFlows import Country_List
wolrd_per_capita_use = pd.read_csv('Data/worldinData/per-capita-energy-use.csv')
wolrd_per_capita_use = wolrd_per_capita_use.sort_values('Year', ascending=False).drop_duplicates(['Entity'])
wolrd_per_capita_use['Primary energy consumption per capita (kWh/person)'] = wolrd_per_capita_use[
                                                                                 'Primary energy consumption per capita (kWh/person)']   # kWh/capita
wolrd_average_per_capita_use = wolrd_per_capita_use['Primary energy consumption per capita (kWh/person)'].mean()
wolrd_median_per_capita_use = wolrd_per_capita_use['Primary energy consumption per capita (kWh/person)'].median()
df_pop = pd.read_csv('Data/Economic Indicators.csv')
df_pop.rename(columns={'Country': 'Entity'}, inplace=True)

df_pop['average_scenario_demand_GWh'] = 0.8 * df_pop["Population"] * wolrd_average_per_capita_use/1000000 #GWh/year
print(df_pop[df_pop["Entity"]=="Samoa"]['Population'].values[0])