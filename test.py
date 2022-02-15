import pandas as pd
import plotly.graph_objects as go



df= pd.read_csv('Data/Sankey/csv/PNG.csv')
# print(df.columns)
lst = df[' (from)'].to_list()
lst2 = df[' (to)'].to_list()
lst.extend(lst2)
# lst = set(lst)
lst = list(dict.fromkeys(lst) )

print(len(lst))
d = {}
for i in range(len(lst)):
    d[i] = lst[i]
d = dict((y,x) for x,y in d.items())
df['To']= df[' (to)'].copy()
df['From']= df[' (from)'].copy()

df.replace({" (from)": d},inplace=True)
df.replace({" (to)": d},inplace=True)
df.fillna('pink', inplace=True)


# print(df.columns)

color_dicts = {'Primary Oil: Production':'grey','Primary Oil: Imports':'grey','Oil Products: Imports':'grey','Natural Gas: Primary Production':'blue','Electricity: Primary Production':'red',
 'Heat: Primary Production':'red','BioFuels: Primary Production':'green','Primary Oil':'grey','BioFuels':'green','Oil Refineries':'grey','Oil Products':'grey',
 'Natural Gas':'blue','Oil: Supplied':'grey','Natural Gas: Supplied':'blue','Electricity & Heat: Supplied':'red','Exports':'yellow','Primary Oil':'grey','Natural Gas':'blue','Electricity & Heat: Supplied':'red',
 'PowerStations':'red','Oil: Final Consumption':'grey','Electricity & Heat: Final Consumption':'red','BioFuels: Final Consumption':'green','BioFuels: Supplied':'green',
               'Other Electricity & Heat':'red','Other Electricity & Heat 3':'red',}

for i in color_dicts.keys():
    df.loc[df['From'] == i, ' (color)'] = color_dicts[i]


fig = go.Figure(data=[go.Sankey(
    valuesuffix = "TJ",
    node = dict(
      pad = 35,
      thickness = 20,
      line = dict(color = "black", width = 0.5),
      label = lst,
      color = 'brown'
    ),
    link = dict(
      source = df[' (from)'].to_list(), # indices correspond to labels, eg A1, A2, A1, B1, ...
      target = df[' (to)'].to_list(),
      value = df[' (weight)'].to_list(),
      color=df[' (color)'].to_list()

    ))])
df.to_csv('sank.csv')
fig.update_layout(title_text="Basic Sankey Diagram", font_size=15)
fig.show()