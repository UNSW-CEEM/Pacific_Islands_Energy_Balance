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
    fig.update_yaxes(title_text="Value ($MM)")
    fig.update_layout(
        title="{}, Total Imports = {}, Total Exports = {} ($million)".format(year,totalImports,totalExports))

    return fig




def Generate_Sankey(year,country):
    import pandas as pd
    import plotly.graph_objects as go

    df = pd.read_csv("Data/Sankey/csv/{}/{}.csv".format(year,country))
    # print(df.columns)
    lst = df[' (from)'].to_list()
    lst2 = df[' (to)'].to_list()
    lst.extend(lst2)
    # lst = set(lst)
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

    # print(df.columns)

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

    for i in color_dicts.keys():
        df.loc[df['From'] == i, ' (color)'] = color_dicts[i]

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
    df.to_csv('sank.csv')
    # fig.update_layout(title_text="Basic Sankey Diagram", font_size=15)
    fig.update_layout(height=900,font=dict(
                          family="Palatino Linotype",
                          size=16,
                          color="white"
                      ))
    fig.update_layout({'plot_bgcolor': 'rgba(0,0,0,0)',
    'paper_bgcolor': 'rgba(0,0,0,0)'},)
    return fig




def potentials_bar(wind_pot,PV_pot,max_range):
    import plotly.graph_objs as go
    names = ['Wind', 'PV']
    values = [wind_pot,PV_pot]
    data = [go.Bar(
        x=names,
        y=values
    )]
    fig = go.Figure(data=data)
    fig.update_layout(
        title='Renewable Energy Required to Decarbonize Electricity sector with 20% losses')
    fig.update_yaxes(title_text="MW")
    fig.update_layout({'plot_bgcolor': 'rgba(0,0,0,0)',
    'paper_bgcolor': 'rgba(0,0,0,0)'})
    fig.update_layout(yaxis_range=[0, max_range])

    fig.update_layout(height=350,font=dict(
                          family="Palatino Linotype",
                          size=16,
                          color="white"
                      ))


    return fig

def oil_to_RE(PV,PV_batt,max_range):
    import plotly.graph_objs as go
    names = ['PV', 'PV+Battery']
    values = [PV,PV_batt]
    data = [go.Bar(
        x=names,
        y=values
    )]
    fig = go.Figure(data=data)
    fig.update_layout(
        title='Potential RE installation with the money paid for diesel transformation')
    fig.update_yaxes(title_text="MW")
    fig.update_layout(yaxis_range=[0, max_range])

    fig.update_layout({'plot_bgcolor': 'rgba(0,0,0,0)',
    'paper_bgcolor': 'rgba(0,0,0,0)'})

    fig.update_layout(height=350,font=dict(
                          family="Palatino Linotype",
                          size=16,
                          color="white"
                      ))


    return fig