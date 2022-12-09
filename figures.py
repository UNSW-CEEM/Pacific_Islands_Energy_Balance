import pandas as pd
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import plotly.express as px
import functions
from EnergyFlows import Country_List
import warnings

warnings.filterwarnings("ignore")

mode = "app"
color_dict = {"app": "white", "report": "black"}
font_color = color_dict[mode]
line_color = color_dict[mode]
size_dict = {"app": 17, "report": 19}
font_size = size_dict[mode]
simple_template = dict(
    layout=go.Layout(
        title=dict(font=dict(family="Calibri", size=22), y=0.98),
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Calibri", size=font_size, color=font_color),
        legend=dict(
            bgcolor="rgba(0,0,0,0)",
            yanchor="bottom",
            orientation="h",
            y=1.05,
            xanchor="center",
            x=0.5,
        ),
        yaxis=dict(showline=True, linecolor=line_color, gridcolor=line_color),
        xaxis=dict(
            showgrid=False,
            gridcolor="grey",
            showline=True,
            linecolor=line_color,
            automargin=True,
            tickangle=35,
        ),
    )
)


def single_barplot(title, x_axis, y_axis, x_title, y_title, color="forestgreen"):

    x_axis_title_dict = {
        "OEC": '<a href="https://oec.world/en/home-b"><sub>Source: The Observatory of Economic Complexity (OEC)<sub></a>',
        "UNSTATS": '<a href="http://unstats.un.org/unsd/energystats/pubs/balance"><sub>Source: Energy Balances, United Nations<sub></a>',
        "WID": '<a href="https://ourworldindata.org/grapher/per-capita-energy-use"><sub>Source: Our world in data <sub></a>',
    }
    if x_title in x_axis_title_dict.keys():
        x_title = x_axis_title_dict[x_title]

    fig = go.Figure()
    fig.add_trace(go.Bar(x=x_axis, y=y_axis, text=y_axis, name="", marker_color=color))

    fig.update_layout(template=simple_template, title=title)
    fig.update_yaxes(title_text=y_title)
    fig.update_xaxes(title_text=x_title)

    return fig


def multiple_barplot(
    title,
    x_axis,
    y_axis_list,
    x_title,
    y_title,
    name_list,
    color_list,
    barmode,
):
    x_axis_title_dict = {
        "OEC": '<a href="https://oec.world/en/home-b"><sub>Source: The Observatory of Economic Complexity (OEC)<sub></a>',
        "UNSTATS": '<a href="http://unstats.un.org/unsd/energystats/pubs/balance"><sub>Source: Energy Balances, United Nations<sub></a>',
        "WID": '<a href="https://ourworldindata.org/grapher/per-capita-energy-use"><sub>Source: Our world in data <sub></a>',
    }
    if x_title in x_axis_title_dict.keys():
        x_title = x_axis_title_dict[x_title]

    fig = go.Figure()
    for y in range(len(y_axis_list)):
        fig.add_trace(
            go.Bar(
                x=x_axis,
                y=y_axis_list[y],
                text=y_axis_list[y],
                name=name_list[y],
                marker_color=color_list[y],
            )
        )

    fig.update_layout(template=simple_template, title=title, barmode=barmode)
    fig.update_yaxes(title_text=y_title)
    fig.update_xaxes(title_text=x_title)
    return fig


def imports_to_GDP(year):
    net_imp_list = []
    interest_list = ["Refined Petroleum"]
    for c in Country_List:
        df_exp = pd.read_csv(
            "Data/{}/Exports-{}---Click-to-Select-a-Product.csv".format(c, year)
        )
        df_imp = pd.read_csv(
            "Data/{}/Imports-{}---Click-to-Select-a-Product.csv".format(c, year)
        )

        df_imp["Trade Value"] = df_imp["Trade Value"] / 1000000  # to million $
        df_exp["Trade Value"] = df_exp["Trade Value"] / 1000000  # to million $

        df_GDP = pd.read_csv("Data/Economic Indicators.csv")
        imp = df_imp[df_imp["HS4"].isin(interest_list)]["Trade Value"]
        exp = df_exp[df_exp["HS4"].isin(interest_list)]["Trade Value"]

        net_imp = imp.values[0]
        if len(exp) > 0:
            net_imp = imp.values[0] - exp.values[0]

        net_imp_list.append(net_imp)
    df_GDP["Imp"] = net_imp_list
    df_GDP["net_imp_to_GDP"] = 100 * df_GDP["Imp"] / df_GDP["GDP(million$)2019"]
    df_GDP["net_imp_to_GDP"] = df_GDP["net_imp_to_GDP"].round(1)
    df_GDP["net_imp_per_capita"] = (
        df_GDP["Imp"] * 1000000 / df_GDP["Population"]
    )  # $ per capita
    df_GDP["net_imp_per_capita"] = df_GDP["net_imp_per_capita"].round(0)

    fig = single_barplot(
        x_axis=df_GDP["Country"],
        y_axis=df_GDP["net_imp_to_GDP"],
        title="Ratio of net imported petroleum products to GDP",
        x_title="OEC",
        y_title="% of GDP",
    )
    fig2 = single_barplot(
        x_axis=df_GDP["Country"],
        y_axis=df_GDP["net_imp_per_capita"],
        title="Imported petroleum products per capita",
        x_title="OEC",
        y_title="$ per capita",
    )
    return [fig, fig2]


def import_export_figure(df_imp, df_exp, Interest_list, year):
    totalImports = int(-df_imp["Trade Value"].sum())
    totalExports = int(df_exp["Trade Value"].sum())
    fig = go.Figure()
    fig.add_trace(
        go.Bar(
            x=df_imp[df_imp["HS4"].isin(Interest_list)]["HS4"],
            y=df_imp[df_imp["HS4"].isin(Interest_list)]["Trade Value"],
            name="Imports",
            marker_color="red",
        )
    )
    fig.add_trace(
        go.Bar(
            x=df_exp[df_exp["HS4"].isin(Interest_list)]["HS4"],
            y=df_exp[df_exp["HS4"].isin(Interest_list)]["Trade Value"],
            name="Exports",
            marker_color="green",
        )
    )

    fig.update_layout(height=500, barmode="relative")  # width=1500,
    fig.update_layout(
        legend=dict(
            bgcolor="rgba(0,0,0,0)",
            yanchor="bottom",
            orientation="v",
            y=0.5,
            xanchor="center",
            x=1.07,
        ),
        font=dict(family="Calibri", size=18, color=font_color),
    )
    fig.update_layout(
        {
            "plot_bgcolor": "rgba(0,0,0,0)",
            "paper_bgcolor": "rgba(0,0,0,0)",
        }
    )
    fig.update_yaxes(
        title_text="Value (millions of $)",
        showline=True,
        linecolor=line_color,
        gridcolor=line_color,
    )
    fig.update_xaxes(
        showline=True,
        linecolor=line_color,
        title_text='<a href="https://oec.world/en/home-b"><sub>Source: The Observatory of Economic Complexity (OEC)<sub></a>',
    )

    fig.update_layout(
        title="{}, Total Imports = {}, Total Exports = {} (millions of $)".format(
            year, totalImports, totalExports
        )
    )
    fig.update_traces(marker_line_color=font_color, marker_line_width=1.5, opacity=1)
    return fig


def Generate_Sankey(year, country):
    import pandas as pd
    import plotly.graph_objects as go

    df = pd.read_csv("Data/Sankey/csv/{}/{}.csv".format(year, country))
    df_elec = df.loc[
        (df[" (from)"] == "PowerStations")
        | (df[" (from)"] == "Other Electricity & Heat")
        | (df[" (from)"] == "Other Electricity & Heat3")
        | (df[" (from)"] == "Electricity & Heat: Supplied")
        | (df[" (from)"] == "Electricity & Heat: Final Consumption")
        | (df[" (to)"] == "PowerStations")
        | (df[" (to)"] == "Other Electricity & Heat")
        | (df[" (to)"] == "Other Electricity & Heat3")
        | (df[" (to)"] == "Electricity & Heat: Supplied")
    ]

    color_dicts = {
        "Primary Oil: Production": "grey",
        "Primary Oil: Imports": "grey",
        "Oil Products: Imports": "grey",
        "Natural Gas: Primary Production": "blue",
        "Electricity: Primary Production": "forestgreen",
        "Heat: Primary Production": "forestgreen",
        "BioFuels: Primary Production": "green",
        "Primary Oil": "grey",
        "BioFuels": "green",
        "Oil Refineries": "grey",
        "Oil Products": "grey",
        "Natural Gas": "blue",
        "Oil: Supplied": "grey",
        "Natural Gas: Supplied": "blue",
        "Electricity & Heat: Supplied": "red",
        "Exports": "yellow",
        "Primary Oil": "grey",
        "Natural Gas": "blue",
        "Electricity & Heat: Supplied": "red",
        "PowerStations": "purple",
        "Oil: Final Consumption": "grey",
        "Electricity & Heat: Final Consumption": "red",
        "BioFuels: Final Consumption": "green",
        "BioFuels: Supplied": "green",
        "Other Electricity & Heat": "forestgreen",
        "Other Electricity & Heat 3": "forestgreen",
    }

    lst = df[" (from)"].to_list()
    lst2 = df[" (to)"].to_list()
    lst.extend(lst2)
    lst = list(dict.fromkeys(lst))

    d = {}
    for i in range(len(lst)):
        d[i] = lst[i]
    d = dict((y, x) for x, y in d.items())
    df["To"] = df[" (to)"].copy()
    df["From"] = df[" (from)"].copy()

    df.replace({" (from)": d}, inplace=True)
    df.replace({" (to)": d}, inplace=True)
    df.fillna("pink", inplace=True)
    for i in color_dicts.keys():
        df.loc[df["From"] == i, " (color)"] = color_dicts[i]
        df.loc[
            (df["From"] == i) & (df["To"] == "Transformation Losses"), " (color)"
        ] = "brown"
    lst_e = df_elec[" (from)"].to_list()
    lst2_e = df_elec[" (to)"].to_list()
    lst_e.extend(lst2_e)
    lst_e = list(dict.fromkeys(lst_e))

    d = {}
    for i in range(len(lst_e)):
        d[i] = lst_e[i]
    d = dict((y, x) for x, y in d.items())
    df_elec["To"] = df_elec[" (to)"].copy()
    df_elec["From"] = df_elec[" (from)"].copy()

    df_elec.replace({" (from)": d}, inplace=True)
    df_elec.replace({" (to)": d}, inplace=True)
    df_elec.fillna("pink", inplace=True)
    for i in color_dicts.keys():
        df_elec.loc[df_elec["From"] == i, " (color)"] = color_dicts[i]

    fig = go.Figure(
        data=[
            go.Sankey(
                valuesuffix="TJ",
                node=dict(
                    pad=35,
                    thickness=20,
                    line=dict(color="black", width=0.5),
                    label=lst,
                    # color='brown'
                ),
                link=dict(
                    source=df[
                        " (from)"
                    ].to_list(),  # indices correspond to labels, eg A1, A2, A1, B1, ...
                    target=df[" (to)"].to_list(),
                    value=df[" (weight)"].to_list(),
                    color=df[" (color)"].to_list(),
                ),
            )
        ]
    )

    fig2 = go.Figure(
        data=[
            go.Sankey(
                valuesuffix="TJ",
                node=dict(
                    pad=35,
                    thickness=20,
                    line=dict(color="black", width=0.5),
                    label=lst_e,
                    # color='brown'
                ),
                link=dict(
                    source=df_elec[
                        " (from)"
                    ].to_list(),  # indices correspond to labels, eg A1, A2, A1, B1, ...
                    target=df_elec[" (to)"].to_list(),
                    value=df_elec[" (weight)"].to_list(),
                    color=df_elec[" (color)"].to_list(),
                ),
            )
        ]
    )

    fig.update_layout(
        title_text='Sankey Plot for all sectors <br><a href="http://unstats.un.org/unsd/energystats/pubs/balance"><sub>Source: Energy Balances, United Nations<sub></a>',
    )
    fig.update_layout(
        height=1100, font=dict(family="Calibri", size=22, color=font_color)
    )
    fig.update_layout(
        {"plot_bgcolor": "rgba(0,0,0,0)", "paper_bgcolor": "rgba(0,0,0,0)"},
    )

    fig2.update_layout(
        height=400, font=dict(family="Calibri", size=22, color=font_color)
    )
    fig2.update_layout(
        {"plot_bgcolor": "rgba(0,0,0,0)", "paper_bgcolor": "rgba(0,0,0,0)"},
    )
    fig2.update_layout(
        title_text='Sankey Plot for the electricity sector <br><a href="http://unstats.un.org/unsd/energystats/pubs/balance"><sub>Source: Energy Balances, United Nations<sub></a>',
    )

    return [fig, fig2]


def oil_to_RE(PV, PV_batt, wind, wind_bat, max_range, year):
    import plotly.graph_objs as go

    names = ["PV", "PV+Battery", "Wind", "Wind+Battery"]
    values = [PV, PV_batt, wind, wind_bat]
    data = [
        go.Bar(
            x=names,
            y=values,
        )
    ]
    fig = go.Figure(data=data)
    fig.update_layout(
        title="Potential RE installation with the money paid for diesel transformation in {}".format(
            year
        )
    )
    fig.update_yaxes(
        title_text="MW", showline=True, linecolor=line_color, gridcolor=line_color
    )
    fig.update_xaxes(showline=True, linecolor=line_color)

    fig.update_layout(yaxis_range=[0, max_range])

    fig.update_layout(
        {"plot_bgcolor": "rgba(0,0,0,0)", "paper_bgcolor": "rgba(0,0,0,0)"}
    )

    fig.update_layout(
        height=350, font=dict(family="Calibri", size=16, color=font_color)
    )
    fig.update_traces(
        marker_color="lightsalmon",
        marker_line_color=font_color,
        marker_line_width=2.5,
        opacity=1,
    )

    return fig


def annual_demand(demand, growth_rate, decarb_rate):
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

    data = [
        go.Scatter(
            x=year_list,
            y=demand_list,
        )
    ]
    fig = go.Figure(data=data)
    fig.update_layout(
        title="Current and future non-RE electricity demand with {}% annual growth".format(
            growth_rate
        )
    )
    fig.update_layout(
        {"plot_bgcolor": "rgba(0,0,0,0)", "paper_bgcolor": "rgba(0,0,0,0)"}
    )
    fig.update_layout(  # height=500,
        font=dict(family="Calibri", size=16, color=font_color)
    )
    fig.update_traces(
        marker_color="lightsalmon",
        marker_line_color=font_color,
        marker_line_width=2.5,
        opacity=1,
    )
    fig.update_xaxes(showgrid=False, showline=True, linecolor=line_color)
    fig.update_yaxes(
        title_text="GWh",
        showgrid=True,
        showline=True,
        linecolor=line_color,
        gridcolor=line_color,
    )
    return fig



def rooftop_PV_plot(available_buildings, PV_size):
    rooftop_df = functions.calculate_rooftop_PV_potential(
        available_buildings=available_buildings, PV_size=PV_size
    )

    fig = make_subplots(specs=[[{"secondary_y": True}]])
    fig.add_trace(
        go.Bar(
            x=rooftop_df["Country"],
            y=rooftop_df["Population"],
            name="Population",
            marker_color="forestgreen",
        ),
        secondary_y=False,
    )
    fig.add_trace(
        go.Scatter(
            x=rooftop_df["Country"],
            y=rooftop_df["Household_size"],
            name="Average household size",
            marker_color="red",
            mode="markers",
        ),
        secondary_y=True,
    )
    fig.update_yaxes(
        title_text="Population",
        secondary_y=False,
    )
    fig.update_yaxes(
        title_text="Average household size",
        secondary_y=True,
    )

    fig.update_layout(
        title="Population and average households size", template=simple_template
    )
    fig.update_xaxes(
        showline=True,
        linecolor=line_color,
        title_text='<a href="http://purl.org/spc/digilib/doc/z8n4m"><sub>Source: 2020 Pacific Populations, SPC<sub></a>',
    )

    fig2 = single_barplot(
        title="Number of homes available for rooftop PV ",
        x_axis=rooftop_df["Country"],
        y_axis=rooftop_df["avaialble_homes"],
        y_title="Number of homes",
        x_title="",
    )

    fig3 = single_barplot(
        title="Potential rooftop PV generation",
        x_axis=rooftop_df["Country"],
        y_axis=rooftop_df["Generation_GWh"],
        y_title="Generation (GWh/year)",
        x_title="",
    )
    fig4 = single_barplot(
        title="Potential rooftop PV capacity",
        x_axis=rooftop_df["Country"],
        y_axis=rooftop_df["Capacity_MW"],
        y_title="Capacity (MW)",
        x_title="",
    )
    return [fig, fig2, fig3, fig4]


def UNstats_plots(year):
    summary_df = functions.all_countries_cross_comparison_unstats(
        2019, Unit="TJ", Use="SummaryPlot"
    )

    fig = multiple_barplot(
        x_axis=summary_df["Country"],
        y_axis_list=[
            summary_df["marine_to_import"].round(0),
            summary_df["aviation_to_import"].round(0),
        ],
        title="% of imported oil consumed for international transit in {}".format(year),
        x_title="UNSTATS",
        y_title="% of imported oil",
        name_list=["Int. marine bunkers", "Int. aviation bunkers"],
        color_list=["forestgreen", "lightsalmon"],
        barmode="relative",
    )

    fig2 = multiple_barplot(
        x_axis=summary_df["Country"],
        y_axis_list=[
            summary_df["transformation_to_import"].round(0),
            summary_df["transformation_losses_to_import"].round(0),
        ],
        title="% of imported oil transformed into electricity and transformation losses in {}".format(
            year
        ),
        x_title="UNSTATS",
        y_title="% of imported oil",
        name_list=["Transformation", "Transformation losses"],
        color_list=["forestgreen", "lightsalmon"],
        barmode="group",
    )

    fig3 = go.Figure()
    fig3.add_trace(
        go.Bar(
            x=summary_df["Country"],
            y=summary_df["road"],
            name="Road",
            marker_color="forestgreen",
        )
    )
    fig3.add_trace(
        go.Bar(
            x=summary_df["Country"],
            y=summary_df["rail"],
            name="Rail",
            marker_color="lightsalmon",
        )
    )
    fig3.add_trace(
        go.Bar(
            x=summary_df["Country"],
            y=summary_df["Domestic aviation"],
            name="Domestic aviation",
            marker_color="greenyellow",
        )
    )
    fig3.add_trace(
        go.Bar(
            x=summary_df["Country"],
            y=summary_df["Domestic navigation"],
            name="Domestic navigation",
            marker_color="orangered",
        )
    )
    fig3.add_trace(
        go.Bar(
            x=summary_df["Country"],
            y=summary_df["Pipeline transport"],
            name="Pipeline transport",
            marker_color="mediumvioletred",
        )
    )
    fig3.add_trace(
        go.Bar(
            x=summary_df["Country"],
            y=summary_df["transport n.e.s"],
            name="Transport n.e.s",
            marker_color="darkturquoise",
        )
    )
    fig3.update_yaxes(
        title_text="% of imported oil",
    )
    fig3.update_xaxes(
        title_text='<a href="http://unstats.un.org/unsd/energystats/pubs/balance"><sub>Source: Energy Balances, United Nations<sub></a>',
    )

    fig3.update_layout(
        template=simple_template,
        title=dict(
            text="Breakdown of imported oil consumed for domestic transport in {}".format(
                year
            ),
            y=0.98,
        ),
        barmode="relative",
    )

    fig4 = single_barplot(
        x_axis=summary_df["Country"],
        y_axis=summary_df["Oil imports"],
        title="Imported oil in {}".format(year),
        x_title="UNSTATS",
        y_title="TJ",
    )

    fig5 = single_barplot(
        x_axis=summary_df["Country"],
        y_axis=summary_df["Total_demand"],
        title="Total demand (excluding int transit) in {}".format(year),
        x_title="UNSTATS",
        y_title="TJ",
    )
    fig6 = single_barplot(
        x_axis=summary_df["Country"],
        y_axis=summary_df["renewables_in_total"],
        title="Total renewable energy (electricity and final consumption) used in {}".format(
            year
        ),
        x_title="UNSTATS",
        y_title="TJ",
    )

    fig7 = single_barplot(
        x_axis=summary_df["Country"],
        y_axis=summary_df["renewable_electricity"],
        title="Primary electricity production (wind, PV, hydro, geothermal) in {}".format(
            year
        ),
        x_title="UNSTATS",
        y_title="TJ",
    )

    fig8 = single_barplot(
        x_axis=summary_df["Country"],
        y_axis=summary_df["Renewables/Total_demand"],
        title="Contribution of renewables in total demand (excluding int transit) in {}".format(
            year
        ),
        x_title="UNSTATS",
        y_title="% of total demand",
    )

    fig_re_imp = single_barplot(
        x_axis=summary_df["Country"],
        y_axis=summary_df["Renewables/Total_imports"],
        title="Proportion of renewable  consumption to total energy imports in {}".format(
            year
        ),
        x_title="UNSTATS",
        y_title="% of total energy imports",
    )
    fig_re_imp.write_image("renewables_to_total_imports.png")

    fig9 = single_barplot(
        x_axis=summary_df["Country"],
        y_axis=summary_df["Renewables/capita"],
        title="Renewable energy consumption per capita in {}".format(year),
        x_title="UNSTATS",
        y_title="MJ per capita",
    )

    return [fig, fig2, fig3, fig4, fig5, fig6, fig7, fig8, fig9]


def land_use_plot():
    summary_demand_df = pd.DataFrame()
    final_demand = functions.fetch_all_countries_demand(
        2019, Unit="GWh", Use="Analysis"
    )[1]
    non_RE_demand = functions.fetch_all_countries_demand(
        2019, Unit="GWh", Use="Analysis"
    )[9]
    countries = functions.fetch_all_countries_demand(2019, Unit="GWh", Use="Analysis")[
        0
    ]
    non_RE_demand = non_RE_demand.round(0)
    final_demand = final_demand.round(0)
    net_zero_demand = functions.fetch_all_countries_demand(
        2019, Unit="GWh", Use="Analysis"
    )[16]

    summary_demand_df["countries"] = countries
    summary_demand_df["non-RE-GWh"] = non_RE_demand
    summary_demand_df["final-GWh"] = final_demand
    df_pop = pd.read_csv("Data/Economic Indicators.csv")

    df = pd.read_excel("Data/Potentials.xlsx")
    PV_pot = df.iloc[0, 2:]  # GWh/MW/year
    Wind_CF = df.iloc[1, 2:]
    Wind_pot = df.iloc[2, 2:]  # GWh/MW/year

    arable = df.iloc[4, 2:]
    crops = df.iloc[5, 2:]
    pasture = df.iloc[6, 2:]
    forested = df.iloc[7, 2:]
    other = df.iloc[8, 2:]
    coastline = df.iloc[13, 2:]
    area = df.iloc[14, 2:]

    Wind_MW_non_RE = 1.2 * non_RE_demand / Wind_pot
    Wind_MW_final = 1.2 * final_demand / Wind_pot

    percentage_of_coastline_final = ((Wind_MW_final * 100 / 1.5) * 0.25) / coastline
    percentage_of_coastline_non_RE = ((Wind_MW_non_RE * 100 / 1.5) * 0.25) / coastline

    PV_non_RE = 1.2 * non_RE_demand / PV_pot  # MW
    PV_final_demand = 1.2 * final_demand / PV_pot  # MW
    PV_net_zero = 1.2 * net_zero_demand / PV_pot
    import numpy as np

    PV_area_non_RE = PV_non_RE / (100)  # 0.1kw/m2 # Converted to km2
    PV_area_non_RE_per = 100 * PV_area_non_RE / area
    PV_area_final_demand = PV_final_demand / (100)  # 0.1kw/m2
    PV_area_final_demand_per = 100 * PV_area_final_demand / area
    PV_area_net_zero = PV_net_zero / 100
    PV_area_net_zero_per = 100 * PV_area_net_zero / area

    final_demand_per_capita = (
        1000 * final_demand / df_pop["Population"]
    )  # MWh/year.person
    non_RE_demand_per_capita = (
        1000 * non_RE_demand / df_pop["Population"]
    )  # MWh/year.person
    final_demand_per_capita = final_demand_per_capita.round(1)
    non_RE_demand_per_capita = non_RE_demand_per_capita.round(1)

    fig = make_subplots(specs=[[{"secondary_y": False}]])

    fig.add_trace(
        go.Scatter(
            x=countries,
            y=Wind_MW_non_RE,
            name="Decarbonizing the electricity sector",
            marker_color="red",
            text=Wind_MW_non_RE,
            mode="markers",
        )
    )
    fig.add_trace(
        go.Bar(
            x=countries,
            y=Wind_MW_final,
            name="Final electrified demand",
            marker_color="forestgreen",
            text=Wind_MW_final,
        )
    )
    fig.update_layout(  # width=1500,
        # height=500,
        barmode="group"
    )
    fig.update_layout(
        legend=dict(
            bgcolor="rgba(0,0,0,0)",
            yanchor="bottom",
            orientation="h",
            y=0.98,
            xanchor="center",
            x=0.5,
        ),
        font=dict(family="Calibri", size=16, color=font_color),
        hovermode="x",
    )
    fig.update_layout(
        {
            "plot_bgcolor": "rgba(0,0,0,0)",
            "paper_bgcolor": "rgba(0,0,0,0)",
        }
    )
    fig.update_yaxes(
        title_text="Wind capacity (MW)",
        showline=True,
        rangemode="tozero",
        linecolor=line_color,
        gridcolor=line_color,
    )
    fig.update_xaxes(showline=True, showgrid=False, linecolor=line_color)
    fig.update_layout(title="Required wind capacity")
    fig.update_traces(marker_line_color=font_color, marker_line_width=1.5, opacity=1)
    fig.update_traces(
        texttemplate="%{text:.1s}",
    )

    fig1 = make_subplots(specs=[[{"secondary_y": False}]])
    fig1.add_trace(
        go.Bar(
            x=countries,
            y=percentage_of_coastline_final,
            name="Final electrified demand",
            marker_color="forestgreen",
        )
    )
    fig1.add_trace(
        go.Scatter(
            x=countries,
            y=percentage_of_coastline_non_RE,
            name="Decarbonizing of the electricity sector",
            marker_color="red",
            mode="markers",
        )
    )
    fig1.update_layout(
        legend=dict(
            bgcolor="rgba(0,0,0,0)",
            yanchor="bottom",
            orientation="h",
            y=0.98,
            xanchor="center",
            x=0.5,
        ),
        font=dict(family="Calibri", size=16, color=font_color),
        hovermode="x",
    )
    fig1.update_layout(
        {
            "plot_bgcolor": "rgba(0,0,0,0)",
            "paper_bgcolor": "rgba(0,0,0,0)",
        }
    )
    fig1.update_xaxes(showline=True, showgrid=False, linecolor=line_color)
    fig1.update_layout(title="Coastline required for wind turbine installation")
    fig1.update_traces(marker_line_color=font_color, marker_line_width=1.5, opacity=1)
    fig1.update_yaxes(
        title_text="% of coastline",
        showline=True,
        showgrid=True,
        rangemode="tozero",
        linecolor=line_color,
        gridcolor=line_color,
    )
    fig2 = make_subplots(specs=[[{"secondary_y": False}]])
    fig2.add_trace(
        go.Scatter(
            x=countries,
            y=PV_non_RE,
            name="Decarbonizing the electricity sector",
            marker_color="red",
            text=PV_non_RE,
            mode="markers",
        )
    )
    fig2.add_trace(
        go.Bar(
            x=countries,
            y=PV_final_demand,
            name="Final electrified demand",
            marker_color="forestgreen",
            text=PV_final_demand,
        )
    )
    fig2.update_layout(
        barmode="relative"
    )
    fig2.update_layout(
        legend=dict(
            bgcolor="rgba(0,0,0,0)",
            yanchor="bottom",
            orientation="h",
            y=0.98,
            xanchor="center",
            x=0.5,
        ),
        font=dict(family="Calibri", size=16, color=font_color),
        hovermode="x",
    )
    fig2.update_layout(
        {
            "plot_bgcolor": "rgba(0,0,0,0)",
            "paper_bgcolor": "rgba(0,0,0,0)",
        }
    )
    fig2.update_yaxes(
        title_text="PV capacity (MW)",
        showline=True,
        rangemode="tozero",
        linecolor=line_color,
        gridcolor=line_color,
    )
    fig2.update_xaxes(
        showline=True,
        showgrid=False,
        linecolor=line_color,
    )
    fig2.update_layout(title="Required PV capacity")
    fig2.update_traces(marker_line_color=font_color, marker_line_width=1.5, opacity=1)
    fig2.update_yaxes(rangemode="tozero", linecolor=line_color, gridcolor=line_color)
    fig2.update_traces(texttemplate="%{text:.1s}")

    fig3 = go.Figure()
    fig3.add_trace(
        go.Bar(x=countries, y=arable, name="Arable", marker_color="orangered")
    )
    fig3.add_trace(
        go.Bar(x=countries, y=crops, name="Crops", marker_color="lightsalmon")
    )
    fig3.add_trace(
        go.Bar(x=countries, y=pasture, name="Pasture", marker_color="mediumvioletred")
    )
    fig3.add_trace(
        go.Bar(x=countries, y=forested, name="Forested", marker_color="green")
    )
    fig3.add_trace(
        go.Bar(x=countries, y=other, name="Other", marker_color="darkturquoise")
    )

    fig3.update_layout(barmode="relative")  # width=1500,
    fig3.update_layout(
        legend=dict(
            bgcolor="rgba(0,0,0,0)",
            yanchor="bottom",
            orientation="h",
            y=1,
            xanchor="left",
            x=0,
        ),
        font=dict(family="Calibri", size=font_size, color=font_color),
        hovermode="x",
    )
    fig3.update_layout(
        {
            "plot_bgcolor": "rgba(0,0,0,0)",
            "paper_bgcolor": "rgba(0,0,0,0)",
        }
    )
    fig3.update_yaxes(
        title_text="% land",
        showline=True,
        rangemode="tozero",
        linecolor=line_color,
        gridcolor=line_color,
    )
    fig3.update_xaxes(
        showline=True,
        linecolor=line_color,
        title_text='<a href="https://www.cia.gov/the-world-factbook/countries"><sub>Source: The World Factbook, CIA<sub></a>',
    )
    fig3.update_traces(marker_line_color=font_color, marker_line_width=1.5, opacity=1)
    fig3.update_layout(margin=dict(t=110))
    fig3.update_layout(
        title={
            "text": "Breakdown of  land area",
            "y": 0.95,
            # 'x': 0,
            "xanchor": "left",
            "yanchor": "top",
        }
    )

    fig4 = multiple_barplot(
        title="Demand per capita",
        x_axis=countries,
        y_axis_list=[non_RE_demand_per_capita, final_demand_per_capita],
        color_list=["forestgreen", "lightsalmon"],
        name_list=["Decarbonizing the electricity sector", "Meeting the final demand"],
        x_title="UNSTATS",
        y_title="Demand (MWh/year/person)",
        barmode="group",
    )

    fig5 = multiple_barplot(
        title="Demand",
        x_axis=countries,
        y_axis_list=[non_RE_demand, final_demand],
        color_list=["forestgreen", "lightsalmon"],
        name_list=["Decarbonizing the electricity sector", "Meeting the final demand"],
        x_title="UNSTATS",
        y_title="Demand (MWh/year)",
        barmode="group",
    )
    fig6 = multiple_barplot(
        title="Proportion of land required for PV installation for three demand scenarios",
        x_axis=countries,
        y_axis_list=[
            PV_area_non_RE_per,
            PV_area_final_demand_per,
            PV_area_net_zero_per,
        ],
        color_list=["forestgreen", "lightsalmon", "blue"],
        name_list=[
            "Decarbonizing the electricity sector",
            "Electrification of the final demand",
            "Net zero emission scenario",
        ],
        x_title="UNSTATS",
        y_title="% of land",
        barmode="group",
    )

    return fig, fig1, fig2, fig3, fig4, fig5, fig6


def mapboxplot(Country, style):
    import math
    import plotly.graph_objects as go
    from math import sqrt, atan, pi
    import pyproj

    (
        PV_area_non_RE,
        PV_area_final_demand,
        PV_area_net_zero,
        PV_area_non_RE_per,
        PV_area_final_demand_per,
        PV_area_net_zero_per,
    ) = functions.PV_area_single_country(Country, 2019)
    width_decarb = math.sqrt(PV_area_non_RE) * 1000 / 2
    width_final_demand = math.sqrt(PV_area_final_demand) * 1000 / 2
    width_net_zero = math.sqrt(PV_area_net_zero) * 1000 / 2
    geod = pyproj.Geod(ellps="WGS84")
    Coordinates = {
        "Samoa": [-13.597336, -172.457458],
        "Nauru": [-0.5228, 166.9315],
        "Vanuatu": [-15.245988, 167.008684],
        "Palau": [7.5150, 134.5825],
        "Kiribati": [1.780915, -157.304505],
        "Cook Islands": [-21.2367, -159.7777],
        "Solomon Islands": [-9.6457, 160.1562],
        "Tonga": [-21.1790, -175.1982],
        "New Caledonia": [-21.222232, 165.251540],
        "French Polynesia": [-17.622779, -149.457556],
        "Micronesia": [6.881990, 158.220540],
        "Niue": [-19.0544, -169.8672],
        "Tuvalu": [-8.519814, 179.19750],
        "PNG": [-6.3150, 143.9555],
        "Fiji": [-17.7134, 178.0650],
    }

    width = width_decarb  # m
    height = width_decarb  # m
    rect_diag = sqrt(width**2 + height**2)
    center_lon = Coordinates[Country][1]
    center_lat = Coordinates[Country][0]
    azimuth1 = atan(width / height)
    azimuth2 = atan(-width / height)
    azimuth3 = atan(width / height) + pi  # first point + 180 degrees
    azimuth4 = atan(-width / height) + pi  # second point + 180 degrees
    pt1_lon, pt1_lat, _ = geod.fwd(
        center_lon, center_lat, azimuth1 * 180 / pi, rect_diag
    )
    pt2_lon, pt2_lat, _ = geod.fwd(
        center_lon, center_lat, azimuth2 * 180 / pi, rect_diag
    )
    pt3_lon, pt3_lat, _ = geod.fwd(
        center_lon, center_lat, azimuth3 * 180 / pi, rect_diag
    )
    pt4_lon, pt4_lat, _ = geod.fwd(
        center_lon, center_lat, azimuth4 * 180 / pi, rect_diag
    )

    fig = go.Figure(
        go.Scattermapbox(
            mode="lines+text",
            fill="toself",
            marker=dict(size=16, color="red"),
            textposition="top right",
            # name = "asdsadad"
            textfont=dict(size=16, color="red"),
            hovertemplate="<b>{}</b><br><br>".format(Country)
            + "PV area for decarbonizing the electricity sector: {} km2</b><br>".format(
                round(PV_area_non_RE, 3)
            )
            + "% of land: {}<extra></extra>".format(round(PV_area_non_RE_per, 3)),
            lon=[
                pt1_lon,
                pt2_lon,
                pt3_lon,
                pt4_lon,
                pt1_lon,
            ],
            lat=[pt1_lat, pt2_lat, pt3_lat, pt4_lat, pt1_lat],
        )
    )
    width = width_final_demand  # m
    height = width_final_demand  # m
    rect_diag = sqrt(width**2 + height**2)
    center_lon = Coordinates[Country][1]
    center_lat = Coordinates[Country][0]
    azimuth1 = atan(width / height)
    azimuth2 = atan(-width / height)
    azimuth3 = atan(width / height) + pi  # first point + 180 degrees
    azimuth4 = atan(-width / height) + pi  # second point + 180 degrees
    pt1_lon, pt1_lat, _ = geod.fwd(
        center_lon, center_lat, azimuth1 * 180 / pi, rect_diag
    )
    pt2_lon, pt2_lat, _ = geod.fwd(
        center_lon, center_lat, azimuth2 * 180 / pi, rect_diag
    )
    pt3_lon, pt3_lat, _ = geod.fwd(
        center_lon, center_lat, azimuth3 * 180 / pi, rect_diag
    )
    pt4_lon, pt4_lat, _ = geod.fwd(
        center_lon, center_lat, azimuth4 * 180 / pi, rect_diag
    )

    fig.add_trace(
        go.Scattermapbox(
            mode="lines+text",
            fill="toself",
            marker=dict(size=16, color="black"),
            textposition="top left",
            # name = "asdsadad"
            textfont=dict(size=16, color="black"),
            hovertemplate="<b>{}</b><br><br>".format(Country)
            + "PV area for final demand: {} km2</b><br>".format(
                round(PV_area_final_demand, 3)
            )
            + "% of land: {}<extra></extra>".format(round(PV_area_final_demand_per, 3)),
            lon=[
                pt1_lon,
                pt2_lon,
                pt3_lon,
                pt4_lon,
                pt1_lon,
            ],
            lat=[pt1_lat, pt2_lat, pt3_lat, pt4_lat, pt1_lat],
        )
    )

    fig.update_layout(
        mapbox={
            "style": style,
            "center": {"lon": center_lon, "lat": center_lat},
            "zoom": 9,
        },
        # add zoom as a slider
        showlegend=False,
        margin={"l": 0, "r": 0, "b": 0, "t": 0},
    )

    width = width_net_zero  # m
    height = width_net_zero  # m
    rect_diag = sqrt(width**2 + height**2)
    center_lon = Coordinates[Country][1]
    center_lat = Coordinates[Country][0]
    azimuth1 = atan(width / height)
    azimuth2 = atan(-width / height)
    azimuth3 = atan(width / height) + pi  # first point + 180 degrees
    azimuth4 = atan(-width / height) + pi  # second point + 180 degrees
    pt1_lon, pt1_lat, _ = geod.fwd(
        center_lon, center_lat, azimuth1 * 180 / pi, rect_diag
    )
    pt2_lon, pt2_lat, _ = geod.fwd(
        center_lon, center_lat, azimuth2 * 180 / pi, rect_diag
    )
    pt3_lon, pt3_lat, _ = geod.fwd(
        center_lon, center_lat, azimuth3 * 180 / pi, rect_diag
    )
    pt4_lon, pt4_lat, _ = geod.fwd(
        center_lon, center_lat, azimuth4 * 180 / pi, rect_diag
    )

    fig.add_trace(
        go.Scattermapbox(
            mode="lines+text",
            fill="toself",
            marker=dict(size=16, color="lightblue"),
            textposition="top left",
            # name = "asdsadad"
            textfont=dict(size=16, color="black"),
            hovertemplate="<b>{}</b><br><br>".format(Country)
            + "PV area for net zero demand scenario: {} km2</b><br>".format(
                round(PV_area_net_zero, 3)
            )
            + "% of land: {}<extra></extra>".format(round(PV_area_net_zero_per, 3)),
            lon=[
                pt1_lon,
                pt2_lon,
                pt3_lon,
                pt4_lon,
                pt1_lon,
            ],
            lat=[pt1_lat, pt2_lat, pt3_lat, pt4_lat, pt1_lat],
        )
    )

    fig.update_layout(
        mapbox={
            "style": style,
            "center": {"lon": center_lon, "lat": center_lat},
            "zoom": 9,
        },
        # add zoom as a slider
        showlegend=False,
        margin={"l": 0, "r": 0, "b": 0, "t": 0},
    )

    return fig


def generation_mix_plot():
    df = pd.read_csv("Data/Energy Pofiles.csv")
    Generation_df = df[
        [
            "Country",
            "Total_GWh_2019",
            "Rebewable_GWh_2019",
            "Non-Renewable_GWh_2019",
            "Hydro_GWh_2019",
            "Solar_GWh_2019",
            "Wind_GWh_2019",
            "Bio_GWh_2019",
            "Geothermal_GWh_2020",
        ]
    ]
    Capacity_df = df[
        [
            "Country",
            "Total_MW_2020",
            "Rebewable_MW_2020",
            "Non-Renewable_MW_2020",
            "Hydro_MW_2020",
            "Solar_MW_2020",
            "Wind_MW_2020",
            "Bio_MW_2020",
            "Geothermal_MW_2020",
        ]
    ]
    fig = go.Figure()
    fig.add_trace(
        go.Bar(
            x=Generation_df["Country"],
            y=100
            * Generation_df["Non-Renewable_GWh_2019"]
            / Generation_df["Total_GWh_2019"],
            name="non-Renewable",
            marker_color="black",
        )
    )
    fig.add_trace(
        go.Bar(
            x=Generation_df["Country"],
            y=100 * Generation_df["Hydro_GWh_2019"] / Generation_df["Total_GWh_2019"],
            name="Hydro and Marine",
            marker_color="lightblue",
        )
    )
    fig.add_trace(
        go.Bar(
            x=Generation_df["Country"],
            y=100 * Generation_df["Solar_GWh_2019"] / Generation_df["Total_GWh_2019"],
            name="Solar",
            marker_color="yellow",
        )
    )
    fig.add_trace(
        go.Bar(
            x=Generation_df["Country"],
            y=100 * Generation_df["Wind_GWh_2019"] / Generation_df["Total_GWh_2019"],
            name="Wind",
            marker_color="darkturquoise",
        )
    )
    fig.add_trace(
        go.Bar(
            x=Generation_df["Country"],
            y=100 * Generation_df["Bio_GWh_2019"] / Generation_df["Total_GWh_2019"],
            name="Bio",
            marker_color="green",
        )
    )
    fig.add_trace(
        go.Bar(
            x=Generation_df["Country"],
            y=100
            * Generation_df["Geothermal_GWh_2020"]
            / Generation_df["Total_GWh_2019"],
            name="Geothermal",
            marker_color="red",
        )
    )

    fig.update_layout(
        title="Generation mix in 2019", template=simple_template, barmode="relative"
    )

    fig.update_yaxes(
        title_text="% of total GWh generation",
    )
    fig.update_xaxes(
        title_text='<a href="https://www.irena.org/Statistics/Statistical-Profiles"><sub>Source: Country Profiles, IRENA<sub></a>',
    )

    fig2 = go.Figure()
    fig2.add_trace(
        go.Bar(
            x=Generation_df["Country"],
            y=100 * Capacity_df["Non-Renewable_MW_2020"] / Capacity_df["Total_MW_2020"],
            name="non-Renewable",
            marker_color="black",
        )
    )
    fig2.add_trace(
        go.Bar(
            x=Generation_df["Country"],
            y=100 * Capacity_df["Hydro_MW_2020"] / Capacity_df["Total_MW_2020"],
            name="Hydro and Marine",
            marker_color="lightblue",
        )
    )
    fig2.add_trace(
        go.Bar(
            x=Generation_df["Country"],
            y=100 * Capacity_df["Solar_MW_2020"] / Capacity_df["Total_MW_2020"],
            name="Solar",
            marker_color="yellow",
        )
    )
    fig2.add_trace(
        go.Bar(
            x=Generation_df["Country"],
            y=100 * Capacity_df["Wind_MW_2020"] / Capacity_df["Total_MW_2020"],
            name="Wind",
            marker_color="darkturquoise",
        )
    )
    fig2.add_trace(
        go.Bar(
            x=Generation_df["Country"],
            y=100 * Capacity_df["Bio_MW_2020"] / Capacity_df["Total_MW_2020"],
            name="Bio",
            marker_color="green",
        )
    )
    fig2.add_trace(
        go.Bar(
            x=Generation_df["Country"],
            y=100 * Capacity_df["Geothermal_MW_2020"] / Capacity_df["Total_MW_2020"],
            name="Geothermal",
            marker_color="red",
        )
    )

    fig2.update_layout(
        template=simple_template,
        title="Installed capacity mix in 2020",
        barmode="relative",
    )

    fig2.update_yaxes(
        title_text="% of total MW capacity",
    )
    fig2.update_xaxes(
        title_text='<a href="https://www.irena.org/Statistics/Statistical-Profiles"><sub>Source: Country Profiles, IRENA<sub></a>',
    )
    return [fig, fig2]


def validation():
    # from page1FarmView import Country_List
    Country_List = [
        "Samoa",
        "Nauru",
        "Vanuatu",
        "Palau",
        "Kiribati",
        "Cook Islands",
        "Solomon Islands",
        "Tonga",
        "New Caledonia",
        "French Polynesia",
        "Micronesia",
        "Niue",
        "Tuvalu",
        "PNG",
        "Fiji",
    ]

    import numpy as np

    file = pd.read_csv("Data/Validation.csv")
    for c in Country_List:
        df = pd.read_csv("Data/Sankey/csv/{}/{}.csv".format("2019", c))
        if c == "PNG":
            oil_import_TJ = df[df[" (from)"] == "Oil Products: Imports"][
                " (weight)"
            ].values[
                0
            ]  # Tj-
            oil_import_GWh = oil_import_TJ * 0.2777
            power_generated_GWh = (
                oil_import_GWh * 0.2
            )  # Imported oil * efficiency of non-RE power plants
        else:
            power_generated_TJ = df[
                (df[" (from)"] == "PowerStations")
                & (df[" (to)"] == "Electricity & Heat: Supplied")
            ][
                " (weight)"
            ]  # TJ
            power_generated_GWh = int(power_generated_TJ * 0.2777)
        file.loc[file.Country == c, "This Work"] = power_generated_GWh

    # file.to_csv('Data/Validation.csv')


def cross_country_sankey(df, from_, to_, normalization):
    from_plain_text = change_case(from_).replace("_", " ")
    to_plain_text = change_case(to_).replace("_", " ")
    if normalization == 1:
        Unit = "TJ"
        tail = "real values"

    elif normalization == " (from)":
        Unit = "% {}".format(from_plain_text)
        tail = "normalized with origin"
    elif normalization == " (to)":
        Unit = "% {}".format(to_plain_text)
        tail = "normalized with destination"
    fig = go.Figure()
    fig.add_trace(
        go.Bar(
            x=df["Country"],
            y=df["Values"],
            name="dasdsa",
            marker_color="forestgreen",
            text=df["Values"],
        )
    )
    fig.update_layout(
        width=800,
        barmode="relative",
    )

    fig.update_yaxes(
        title_text=Unit,
    )
    fig.update_xaxes(
        tickangle=35,
        # showline=True,
        # linecolor=line_color,
        title_text='<a href="http://unstats.un.org/unsd/energystats/pubs/balance"><sub>Source: Energy Balances, United Nations<sub></a>',
    ),

    fig.update_layout(
        title="From {} to {} ({})".format(from_plain_text, to_plain_text, tail)
    )
    # print(summary_df)
    # fig.update_traces(marker_line_color=font_color, marker_line_width=1.5, opacity=1)
    # fig.update_traces(texttemplate='%{text:.1s}')
    fig.update_layout(template=simple_template)
    return fig


def import_export_figure_dynamic(df, product):

    fig = go.Figure()
    min = df["import_values"].min()
    min = min + 0.2 * min
    max = df["export_values"].max()
    max = max + 0.2 * max
    fig.add_trace(
        go.Bar(
            x=df["Country"],
            y=df["import_values"],
            name="Imports",
            marker_color="red",
            text=df["import_values"].round(decimals=2),
        )
    )
    fig.add_trace(
        go.Bar(
            x=df["Country"],
            y=df["export_values"],
            name="Exports",
            marker_color="green",
            text=df["export_values"].round(decimals=2),
        )
    )
    fig.update_layout(
        width=800,
        # height=500,
        barmode="relative",
    )
    fig.update_layout(
        legend=dict(
            bgcolor="rgba(0,0,0,0)",
            yanchor="bottom",
            orientation="v",
            y=0.5,
            xanchor="center",
            x=1.07,
        ),
        font=dict(family="Calibri", size=16, color=font_color),
    )
    fig.update_layout(
        {
            "plot_bgcolor": "rgba(0,0,0,0)",
            "paper_bgcolor": "rgba(0,0,0,0)",
        }
    )
    fig.update_yaxes(
        title_text="Value (millions of $)",
        showline=True,
        linecolor=line_color,
        gridcolor=line_color,
    )
    fig.update_xaxes(
        showline=True,
        linecolor=line_color,
        title_text='<a href="https://oec.world/en/home-b"><sub>Source: The Observatory of Economic Complexity (OEC)<sub></a>',
    )

    fig.update_layout(title="{}".format(product))
    fig.update_traces(marker_line_color=font_color, marker_line_width=1.5, opacity=1)
    # fig.update_traces(texttemplate='%{text:.1s}')
    fig.update_layout(yaxis_range=[min - 10, max + 5])

    return fig


def Solar_physical_resources():
    import plotly.graph_objs as go

    df_avg = pd.read_excel("Data/World_average_potentials.xlsx")
    average_world_PV = df_avg["World"][0]
    average_world_wind = df_avg["World"][2]
    df_technical_potential = functions.calculate_PV_Wind_potential(
        available_land=0.02, available_coastline=0.1
    )
    fig = single_barplot(
        x_axis=df_technical_potential["Country"],
        y_axis=df_technical_potential["PV_pot"],
        title="Available solar resources",
        x_title="",
        y_title="GWh/MW/year",
    )
    fig.add_shape(
        type="line",
        line=dict(dash="dot", color="red"),
        x0=0,
        x1=len(df_technical_potential["Country"]) - 1,
        y0=average_world_PV,
        y1=average_world_PV,
    )
    fig.add_annotation(
        x=12,
        y=average_world_PV + 0.1,
        text="World average = {}".format(average_world_PV.round(1)),
        showarrow=False,
        font=dict(color=font_color, size=18),
    )

    fig2 = single_barplot(
        x_axis=df_technical_potential["Country"],
        y_axis=df_technical_potential["Wind_pot"],
        title="Available wind resources",
        x_title="",
        y_title="GWh/MW/year",
    )
    fig2.add_shape(
        type="line",
        line=dict(dash="dot", color="red"),
        x0=0,
        x1=len(df_technical_potential["Country"]) - 1,
        y0=average_world_wind,
        y1=average_world_wind,
    )
    fig2.add_annotation(
        x=4,
        y=average_world_wind + 0.3,
        text="World average = {}".format(average_world_wind.round(1)),
        showarrow=False,
        font=dict(color=font_color, size=18),
    )

    fig3 = single_barplot(
        x_axis=df_technical_potential["Country"],
        y_axis=df_technical_potential["Wind_technical_GWh"],
        title="Technical wind generation",
        x_title="",
        y_title="GWh/year",
    )

    fig4 = single_barplot(
        x_axis=df_technical_potential["Country"],
        y_axis=df_technical_potential["Theoretical_PV_GWh"],
        title="Theoretical PV generation",
        x_title="",
        y_title="GWh/year",
    )

    fig5 = single_barplot(
        x_axis=df_technical_potential["Country"],
        y_axis=df_technical_potential["Theoretical_PV_GW"],
        title="Theoretical PV capacity",
        x_title="",
        y_title="GW",
    )

    fig6 = single_barplot(
        x_axis=df_technical_potential["Country"],
        y_axis=df_technical_potential["Wind_technical_GW"],
        title="Technical wind capacity",
        x_title="",
        y_title="GW",
    )

    fig7 = single_barplot(
        x_axis=df_technical_potential["Country"],
        y_axis=df_technical_potential["PV_technical_GW"],
        title="Technical PV capacity",
        x_title="",
        y_title="GW",
    )

    fig8 = single_barplot(
        x_axis=df_technical_potential["Country"],
        y_axis=df_technical_potential["PV_technical_GWh"],
        title="Technical PV generation",
        x_title="",
        y_title="GWh/year",
    )
    fig9 = single_barplot(
        x_axis=df_technical_potential["Country"],
        y_axis=df_technical_potential["Theoretical_wind_GW"],
        title="Theoretical wind capacity",
        x_title="",
        y_title="GW",
    )

    return fig, fig2, fig3, fig4, fig5, fig6, fig7, fig8, fig9


def diesel_petrol_price(Fuel):
    import plotly.graph_objs as go

    df = pd.read_csv("Data/{}.csv".format(Fuel))  # USD c/Litre
    Australia = df[(df["Country"] == "Australia")]["Tax included"].values[0]
    NZ = df[(df["Country"] == "New Zealand")]["Tax included"].values[0]
    df = df[(df["Country"] != "Australia") & (df["Country"] != "New Zealand")]
    fig = go.Figure()
    fig.add_trace(
        go.Bar(
            x=df["Country"],
            y=df["Tax excluded"],
            name="Tax excluded",
            marker_color="forestgreen",
        )
    )
    fig.add_trace(go.Bar(x=df["Country"], y=df["Tax"], name="Tax", marker_color="red"))
    fig.add_shape(
        type="line",
        line=dict(dash="dot", color="red"),
        x0=0,
        x1=len(df["Country"]) - 1,
        y0=Australia,
        y1=Australia,
    )
    fig.add_shape(
        type="line",
        line=dict(dash="dot", color="red"),
        x0=0,
        x1=len(df["Country"]) - 1,
        y0=NZ,
        y1=NZ,
    )
    fig.add_annotation(
        x=2.5,
        y=Australia + 7,
        text="Australia = {}".format(Australia.round(1)),
        showarrow=False,
        font=dict(color=font_color, size=16),
    )
    fig.add_annotation(
        x=0.8,
        y=NZ + 10,
        text="New Zealand = {}".format(NZ.round(1)),
        showarrow=False,
        font=dict(color=font_color, size=16),
    )
    fig.update_layout(
        title="Regional {} retail price for quarter 1, 2022 ".format(Fuel)
    )
    fig.update_yaxes(
        title_text="US cents/Litre",
        # showline=True,
        # linecolor=line_color,
        # gridcolor=line_color,
    )

    fig.update_layout(
        template=simple_template,  # height=350,
        # font=dict(family="Calibri", size=15, color=font_color),
        barmode="relative",
    )
    # fig.update_traces(marker_line_color=font_color, marker_line_width=2, opacity=1)
    # fig.update_layout(
    #     legend=dict(
    #         bgcolor="rgba(0,0,0,0)",
    #         yanchor="bottom",
    #         orientation="h",
    #         y=1.05,
    #         xanchor="center",
    #         x=0.5,
    #     )
    # )
    fig.update_xaxes(
        # linecolor=line_color,
        # showline=True,
        title_text='<a href="https://www.haletwomey.co.nz/"><sub>Source: Pacific Islands fuel supply, demand and comparison of regional prices 2022, Hale&Twomey <sub></a>',
    )

    return fig


def elec_price_plot():
    import plotly.graph_objs as go

    df = pd.read_csv("Data/elec Price and subsidies.csv")  # USD c/Litre

    fig = go.Figure()
    fig.add_trace(
        go.Bar(
            x=df["Country"],
            y=df["small res"],
            name="Residential consumer, 1.1 kVA, 60 kWh/month",
            marker_color="forestgreen",
        )
    )
    fig.add_trace(
        go.Bar(
            x=df["Country"],
            y=df["res"],
            name="Residential consumer, 3.3 kVA, 300 kWh/month",
            marker_color="yellow",
        )
    )
    fig.add_trace(
        go.Bar(
            x=df["Country"],
            y=df["res"],
            name="Business consumer, 100 kVA, 10,000 kWh/month",
            marker_color="red",
        )
    )

    fig.update_layout(title="Regional electricity retail price in 2019")
    fig.update_yaxes(
        title_text="USD/kWh", showline=True, linecolor=line_color, gridcolor=line_color
    )

    fig.update_layout(
        {"plot_bgcolor": "rgba(0,0,0,0)", "paper_bgcolor": "rgba(0,0,0,0)"}
    )
    fig.update_layout(  # height=350,
        font=dict(family="Calibri", size=18, color=font_color),
    )
    fig.update_traces(marker_line_color=font_color, marker_line_width=2, opacity=1)
    fig.update_layout(
        legend=dict(
            bgcolor="rgba(0,0,0,0)",
            yanchor="bottom",
            orientation="h",
            y=1.05,
            xanchor="center",
            x=0.5,
        )
    )
    fig.update_xaxes(
        showline=True,
        linecolor=line_color,
        title_text='<a href="chrome-extension://efaidnbmnnnibpcajpcglclefindmkaj/http://ura.gov.vu/attachments/article/67/Comparative%20Report%20-%20Pacific%20Region%20Electricity%20Bills%20June%202016.pdf"><sub>Source: Pacific Region Electricity Bills 2019, Utilities Regulatory Authority (URA) <sub></a>',
    )

    return fig


def per_capita_comparison():

    total_demand_electrified = functions.fetch_all_countries_demand(
        2019, Unit="GWh", Use="Analysis"
    )[1]
    total_demand = functions.fetch_all_countries_demand(
        2019, Unit="GWh", Use="SummaryPlot"
    )[1]

    non_RE_elec = functions.fetch_all_countries_demand(
        2019, Unit="GWh", Use="Analysis"
    )[
        9
    ]  # Decarbonizing the electricity sector

    countries = functions.fetch_all_countries_demand(2019, Unit="GWh", Use="Analysis")[
        0
    ]
    non_RE_elec = non_RE_elec.round(0)
    total_demand_electrified = total_demand_electrified.round(0)

    df_pop = pd.read_csv("Data/Economic Indicators.csv")

    total_demand_electrified_per_capita = (
        1000 * total_demand_electrified / df_pop["Population"]
    )  # MWh/year/person
    total_demand_per_capita = (
        1000 * total_demand / df_pop["Population"]
    )  # MWh/year/person
    non_RE_elec_per_capita = (
        1000 * non_RE_elec / df_pop["Population"]
    )  # MWh/year/person

    total_demand_electrified_per_capita = total_demand_electrified_per_capita.round(1)
    total_demand_per_capita = total_demand_per_capita.round(1)
    non_RE_elec_per_capita = non_RE_elec_per_capita.round(1)

    wolrd_per_capita_use = pd.read_csv("Data/worldinData/per-capita-energy-use.csv")
    wolrd_per_capita_use = wolrd_per_capita_use.sort_values(
        "Year", ascending=False
    ).drop_duplicates(["Entity"])
    wolrd_per_capita_use["Primary energy consumption per capita (kWh/person)"] = (
        wolrd_per_capita_use["Primary energy consumption per capita (kWh/person)"]
        / 1000
    )  # MWh/capita
    wolrd_average_per_capita_use = wolrd_per_capita_use[
        "Primary energy consumption per capita (kWh/person)"
    ].mean()
    wolrd_median_per_capita_use = wolrd_per_capita_use[
        "Primary energy consumption per capita (kWh/person)"
    ].median()

    wolrd_per_capita_use["Entity"] = wolrd_per_capita_use["Entity"].replace(
        "Micronesia (country)", "Micronesia"
    )
    wolrd_per_capita_use["Entity"] = wolrd_per_capita_use["Entity"].replace(
        "Papua New Guinea", "PNG"
    )

    wolrd_per_capita_use = wolrd_per_capita_use[
        wolrd_per_capita_use.Entity.isin(Country_List)
    ]
    wolrd_per_capita_use[
        "Primary energy consumption per capita (kWh/person)"
    ] = wolrd_per_capita_use[
        "Primary energy consumption per capita (kWh/person)"
    ].round(
        1
    )

    fig_use_cap = make_subplots(specs=[[{"secondary_y": False}]])
    fig_use_cap.add_trace(
        go.Bar(
            x=countries,
            y=non_RE_elec_per_capita,
            text=non_RE_elec_per_capita,
            name="Decarbonizing the electricity sector-this research",
            marker_color="red",
        )
    )
    fig_use_cap.add_trace(
        go.Bar(
            x=countries,
            y=total_demand_electrified_per_capita,
            text=total_demand_electrified_per_capita,
            name="Final electrified demand-this research",
            marker_color="green",
        )
    )
    fig_use_cap.add_trace(
        go.Bar(
            x=countries,
            y=total_demand_per_capita,
            text=total_demand_per_capita,
            name="Total demand-this research",
            marker_color="blue",
        )
    )
    fig_use_cap.add_trace(
        go.Bar(
            x=wolrd_per_capita_use["Entity"],
            y=wolrd_per_capita_use[
                "Primary energy consumption per capita (kWh/person)"
            ],
            text=wolrd_per_capita_use[
                "Primary energy consumption per capita (kWh/person)"
            ],
            name="Total demand-our world in data",
            marker_color="orange",
        )
    )
    fig_use_cap.add_shape(
        type="line",
        line=dict(dash="dot", color="red"),
        x0=0,
        x1=len(countries),
        y0=wolrd_average_per_capita_use,
        y1=wolrd_average_per_capita_use,
    )
    fig_use_cap.add_shape(
        type="line",
        line=dict(dash="dot", color="orange"),
        x0=0,
        x1=len(countries),
        y0=wolrd_median_per_capita_use,
        y1=wolrd_median_per_capita_use,
    )
    fig_use_cap.update_layout(
        legend=dict(
            bgcolor="rgba(0,0,0,0)",
            yanchor="bottom",
            orientation="h",
            y=0.98,
            xanchor="center",
            x=0.5,
        ),
        font=dict(family="Calibri", size=18, color=font_color),
        hovermode="x",
    )
    fig_use_cap.add_annotation(
        x=0.5,
        y=wolrd_average_per_capita_use + 4,
        text="World average = {}".format(wolrd_average_per_capita_use.round(1)),
        showarrow=False,
        font=dict(color=font_color, size=18),
    )
    fig_use_cap.add_annotation(
        x=0.5,
        y=wolrd_median_per_capita_use + 4,
        text="World median = {}".format(wolrd_median_per_capita_use.round(1)),
        showarrow=False,
        font=dict(color=font_color, size=18),
    )
    fig_use_cap.update_layout(
        {
            "plot_bgcolor": "rgba(0,0,0,0)",
            "paper_bgcolor": "rgba(0,0,0,0)",
        }
    )
    fig_use_cap.update_yaxes(
        title_text="Demand (MWh/year/person)",
        showline=True,
        rangemode="tozero",
        linecolor=line_color,
        gridcolor=line_color,
    )
    fig_use_cap.update_xaxes(
        showline=True,
        showgrid=False,
        linecolor=line_color,
    )
    fig_use_cap.update_layout(title="Demand per capita for different demand scenarios")
    fig_use_cap.update_traces(
        marker_line_color=font_color, marker_line_width=0, opacity=1
    )
    fig_use_cap.update_yaxes(
        rangemode="tozero", linecolor=line_color, gridcolor=line_color
    )
    fig_use_cap.update_xaxes(
        showline=True,
        linecolor=line_color,
        title_text='<a href="http://unstats.un.org/unsd/energystats/pubs/balance"><sub>Source: Energy Balances, United Nations<sub></a>',
    )

    return fig_use_cap


def per_capita_renewables():
    countries = functions.fetch_all_countries_demand(2019, Unit="GWh", Use="Analysis")[
        0
    ]

    renewable_electricity = functions.fetch_all_countries_demand(
        2019, Unit="GWh", Use="Analysis"
    )[8]
    df_pop = pd.read_csv("Data/Economic Indicators.csv")

    renewable_electricity = (
        1000 * renewable_electricity / df_pop["Population"]
    )  # MWh/year/capita

    wolrd_per_capita_RE_elec = pd.read_csv(
        "Data/worldinData/low-carbon-elec-per-capita.csv"
    )

    wolrd_per_capita_RE_elec = wolrd_per_capita_RE_elec.sort_values(
        "Year", ascending=False
    ).drop_duplicates(["Entity"])
    wolrd_per_capita_RE_elec["Low-carbon electricity per capita (kWh)"] = (
        wolrd_per_capita_RE_elec["Low-carbon electricity per capita (kWh)"] / 1000
    )  # MWh/capita
    wolrd_per_capita_RE_elec[
        "Low-carbon electricity per capita (kWh)"
    ] = wolrd_per_capita_RE_elec["Low-carbon electricity per capita (kWh)"]
    wolrd_average_per_capita_RE_elec = wolrd_per_capita_RE_elec[
        "Low-carbon electricity per capita (kWh)"
    ].mean()
    wolrd_median_per_capita_RE_elec = wolrd_per_capita_RE_elec[
        "Low-carbon electricity per capita (kWh)"
    ].median()

    wolrd_per_capita_RE_elec["Entity"] = wolrd_per_capita_RE_elec["Entity"].replace(
        "Micronesia (country)", "Micronesia"
    )
    wolrd_per_capita_RE_elec["Entity"] = wolrd_per_capita_RE_elec["Entity"].replace(
        "Papua New Guinea", "PNG"
    )

    wolrd_per_capita_RE_elec = wolrd_per_capita_RE_elec[
        wolrd_per_capita_RE_elec.Entity.isin(Country_List)
    ]

    fig = single_barplot(
        title="Renewable electricity generation per capita",
        x_axis=countries,
        y_axis=renewable_electricity.round(2),
        x_title="UNSTATS",
        y_title="(MWh/year/person)",
    )

    fig.add_shape(
        type="line",
        line=dict(dash="dot", color="red"),
        x0=0,
        x1=14,
        y0=wolrd_average_per_capita_RE_elec,
        y1=wolrd_average_per_capita_RE_elec,
    )
    fig.add_shape(
        type="line",
        line=dict(dash="dot", color="orange"),
        x0=0,
        x1=14,
        y0=wolrd_median_per_capita_RE_elec,
        y1=wolrd_median_per_capita_RE_elec,
    )
    fig.update_layout(
        legend=dict(
            bgcolor="rgba(0,0,0,0)",
            yanchor="bottom",
            orientation="h",
            y=0.98,
            xanchor="center",
            x=0.5,
        ),
        font=dict(family="Calibri", size=font_size, color=font_color),
        hovermode="x",
    )
    fig.add_annotation(
        x=0.8,
        y=wolrd_average_per_capita_RE_elec + 0.1,
        text="World average = {}".format(wolrd_average_per_capita_RE_elec.round(1)),
        showarrow=False,
        font=dict(color=font_color, size=16),
    )
    fig.add_annotation(
        x=0.8,
        y=wolrd_median_per_capita_RE_elec + 0.1,
        text="World median = {}".format(wolrd_median_per_capita_RE_elec.round(1)),
        showarrow=False,
        font=dict(color=font_color, size=16),
    )
    fig.update_layout(template=simple_template)

    return fig


def per_capita_intensity():

    countries = functions.fetch_all_countries_demand(2019, Unit="GWh", Use="Analysis")[
        0
    ]

    wolrd_per_capita_intensity = pd.read_csv(
        "Data/worldinData/energy-intensity-of-economies.csv"
    )
    wolrd_per_capita_intensity = wolrd_per_capita_intensity.sort_values(
        "Year", ascending=False
    ).drop_duplicates(["Entity"])
    wolrd_average_per_capita_intensity = wolrd_per_capita_intensity[
        "Energy intensity level of primary energy (MJ/$2017 PPP GDP)"
    ].mean()
    wolrd_median_per_capita_intensity = wolrd_per_capita_intensity[
        "Energy intensity level of primary energy (MJ/$2017 PPP GDP)"
    ].median()

    wolrd_per_capita_intensity["Entity"] = wolrd_per_capita_intensity["Entity"].replace(
        "Micronesia (country)", "Micronesia"
    )
    wolrd_per_capita_intensity["Entity"] = wolrd_per_capita_intensity["Entity"].replace(
        "Papua New Guinea", "PNG"
    )
    wolrd_per_capita_intensity = wolrd_per_capita_intensity[
        wolrd_per_capita_intensity.Entity.isin(Country_List)
    ]

    total_demand = functions.fetch_all_countries_demand(
        2019, Unit="GWh", Use="SummaryPlot"
    )[1]
    df_GDP = pd.read_csv("Data/Economic Indicators.csv")
    df_GDP["Demand"] = total_demand
    df_GDP["Demand_per_gdp"] = (df_GDP["Demand"] * 1000000) / (
        df_GDP["GDP(million$)2019"] * 1000000
    )

    fig_use_cap = single_barplot(
        title="Energy (primary, total) intensity  of economies",
        x_axis=countries,
        y_axis=df_GDP["Demand_per_gdp"].round(1),
        x_title="UNSTATS",
        y_title="(kWh/$ PPP GDP)",
    )

    fig_use_cap.add_shape(
        type="line",
        line=dict(dash="dot", color="red"),
        x0=0,
        x1=len(countries) - 1,
        y0=wolrd_average_per_capita_intensity,
        y1=wolrd_average_per_capita_intensity,
    )
    fig_use_cap.add_shape(
        type="line",
        line=dict(dash="dot", color="orange"),
        x0=0,
        x1=len(countries) - 1,
        y0=wolrd_median_per_capita_intensity,
        y1=wolrd_median_per_capita_intensity,
    )

    fig_use_cap.add_annotation(
        x=6,
        y=wolrd_average_per_capita_intensity + 0.25,
        text="World average = {}".format(wolrd_average_per_capita_intensity.round(1)),
        showarrow=False,
        font=dict(color=font_color, size=15),
    )
    fig_use_cap.add_annotation(
        x=12,
        y=wolrd_median_per_capita_intensity - 0.2,
        text="World median = {}".format(wolrd_median_per_capita_intensity.round(1)),
        showarrow=False,
        font=dict(color=font_color, size=15),
    )

    return fig_use_cap


def percentage_of_imports():
    countries = functions.fetch_all_countries_demand(2019, Unit="GWh", Use="Analysis")[
        0
    ]
    total_energy_supply = functions.fetch_all_countries_demand(
        2019, Unit="GWh", Use="SummaryPlot"
    )[1]
    net_imports = functions.fetch_all_countries_demand(
        2019, Unit="GWh", Use="Analysis"
    )[15]
    current_share_of_imports = 100 * net_imports / total_energy_supply

    world_average_demand = (
        functions.fetch_all_countries_demand(2019, Unit="GWh", Use="Analysis")[11]
        * 100
        / 80
    )  # convert to total instead of electricity
    renewables_in_total = functions.fetch_all_countries_demand(
        2019, Unit="GWh", Use="Analysis"
    )[7]
    world_average_demand_non_RE = (
        (world_average_demand - renewables_in_total) * 80 / 100
    )  # convert to electricity
    rooftop_PV_df = functions.calculate_rooftop_PV_potential()
    wind_PV_df = functions.calculate_PV_Wind_potential(
        available_land=0.02, available_coastline=0.1
    )
    remaining_demand_world_average = (
        world_average_demand_non_RE
        - rooftop_PV_df["Generation_GWh"]
        - wind_PV_df["PV_technical_GWh"]
    )
    imports_world_average = (
        100 * remaining_demand_world_average / world_average_demand_non_RE
    )

    imports_df = pd.DataFrame()

    demand_for_decarb = functions.fetch_all_countries_demand(2019)[9]
    countries = functions.fetch_all_countries_demand(2019)[0]
    remaining_demand_for_decarb = (
        demand_for_decarb
        - rooftop_PV_df["Generation_GWh"]
        - wind_PV_df["PV_technical_GWh"]
    )
    imports_decarbonization = 100 * remaining_demand_for_decarb / demand_for_decarb
    imports_df["countries"] = countries
    imports_df["imports_decarb_%"] = imports_decarbonization
    imports_df["imports_decarb_%"] = imports_df["imports_decarb_%"].clip(lower=0)
    imports_df["imports_decarb_GWh"] = remaining_demand_for_decarb
    imports_df["imports_decarb_GWh"] = imports_df["imports_decarb_GWh"].clip(lower=0)

    electrified_demand = functions.fetch_all_countries_demand(2019, Use="Analysis")[1]
    remaining_demand_electrified = (
        electrified_demand
        - rooftop_PV_df["Generation_GWh"]
        - wind_PV_df["PV_technical_GWh"]
    )
    imports_electrified = 100 * remaining_demand_electrified / electrified_demand
    imports_df["imports_electrified_%"] = imports_electrified
    imports_df["imports_electrified_%"] = imports_df["imports_electrified_%"].clip(
        lower=0
    )
    imports_df["imports_electrified_GWh"] = remaining_demand_electrified
    imports_df["imports_electrified_GWh"] = imports_df["imports_electrified_GWh"].clip(
        lower=0
    )

    imports_df["imports_world_average_%"] = imports_world_average
    imports_df["imports_world_average_%"] = imports_df["imports_world_average_%"].clip(
        lower=0
    )
    imports_df["imports_world_average_GWh"] = remaining_demand_world_average
    imports_df["imports_world_average_GWh"] = imports_df[
        "imports_world_average_GWh"
    ].clip(lower=0)

    imports_df["Current_%"] = current_share_of_imports
    imports_df["Current_%"] = imports_df["Current_%"].clip(lower=0)
    imports_df["Current_GWh"] = net_imports
    imports_df["Current_GWh"] = imports_df["Current_GWh"].clip(lower=0)

    imports_df.to_csv("imports_for_scenarios.csv")

    fig_use_cap = make_subplots(specs=[[{"secondary_y": False}]])
    fig_use_cap.add_trace(
        go.Bar(
            x=imports_df["countries"],
            y=imports_df["Current_%"].round(1),
            text=imports_df["Current_%"].round(1),
            name="Current",
            marker_color="red",
        )
    )
    fig_use_cap.add_trace(
        go.Bar(
            x=imports_df["countries"],
            y=imports_df["imports_decarb_%"].round(1),
            text=imports_df["imports_decarb_%"].round(1),
            name="Decarbonization",
            marker_color="blue",
        )
    )
    fig_use_cap.add_trace(
        go.Bar(
            x=imports_df["countries"],
            y=imports_df["imports_electrified_%"].round(1),
            text=imports_df["imports_electrified_%"].round(1),
            name="Electrification",
            marker_color="brown",
        )
    )
    fig_use_cap.add_trace(
        go.Bar(
            x=imports_df["countries"],
            y=imports_df["imports_world_average_%"].round(1),
            text=imports_df["imports_world_average_%"].round(1),
            name="Wolrd average",
            marker_color="green",
        )
    )

    fig_use_cap.update_layout(
        legend=dict(
            bgcolor="rgba(0,0,0,0)",
            yanchor="bottom",
            orientation="h",
            y=0.98,
            xanchor="center",
            x=0.5,
        ),
        font=dict(family="Calibri", size=16, color=font_color),
        hovermode="x",
    )

    fig_use_cap.update_layout(
        {
            "plot_bgcolor": "rgba(0,0,0,0)",
            "paper_bgcolor": "rgba(0,0,0,0)",
        }
    )
    fig_use_cap.update_yaxes(
        title_text="% of total demand",
        showline=True,
        rangemode="tozero",
        linecolor=line_color,
        gridcolor=line_color,
    )
    fig_use_cap.update_xaxes(
        showline=True,
        showgrid=False,
        linecolor=line_color,
    )
    fig_use_cap.update_layout(
        title="The share of total demand met by net energy imports"
    )
    fig_use_cap.update_traces(
        marker_line_color=font_color, marker_line_width=0, opacity=1
    )
    fig_use_cap.update_yaxes(
        rangemode="tozero", linecolor=line_color, gridcolor=line_color
    )
    fig_use_cap.update_xaxes(
        showline=True,
        linecolor=line_color,
        title_text='<a href="http://unstats.un.org/unsd/energystats/pubs/balance"><sub>Source: Energy Balances, United Nations<sub></a>',
    )
    return fig_use_cap


def dependance_on_imports():
    countries = functions.fetch_all_countries_demand(2019, Unit="GWh", Use="Analysis")[
        0
    ]
    total_energy_supply = functions.fetch_all_countries_demand(
        2019, Unit="GWh", Use="SummaryPlot"
    )[1]
    net_imports = functions.fetch_all_countries_demand(
        2019, Unit="GWh", Use="Analysis"
    )[15]
    current_share_of_imports = 100 * net_imports / total_energy_supply
    int_aviation = functions.fetch_all_countries_demand(
        2019, Unit="GWh", Use="Analysis"
    )[13]
    int_marine = functions.fetch_all_countries_demand(2019, Unit="GWh", Use="Analysis")[
        12
    ]
    total_supply_incl_int_transit = (
        total_energy_supply + abs(int_marine) + abs(int_aviation)
    )
    current_share_of_imports_inc_int_transit = (
        100 * net_imports / total_supply_incl_int_transit
    )

    fig = single_barplot(
        title="Share of net imports in total demand (including int transit))",
        x_axis=countries,
        y_axis=current_share_of_imports_inc_int_transit.round(0),
        x_title="UNSTATS",
        y_title="% of net imports",
    )

    return fig


def GDP_per_capita():
    summary_df = pd.read_csv("Data/SummaryTable.csv")

    summary_df = summary_df[summary_df["Country / Territory"].isin(Country_List)]

    world_GDP_capita = pd.read_csv("Data/worldinData/gdp-per-capita-worldbank.csv")
    world_GDP_capita = world_GDP_capita.sort_values(
        "Year", ascending=False
    ).drop_duplicates(["Entity"])

    wolrd_average_GDP_per_capita = world_GDP_capita[
        "GDP per capita, PPP (constant 2017 international $)"
    ].mean()
    wolrd_median_GDP_per_capita = world_GDP_capita[
        "GDP per capita, PPP (constant 2017 international $)"
    ].median()

    fig = single_barplot(
        title="GDP per capita and comparison with world's average",
        x_axis=summary_df["Country / Territory"],
        y_axis=summary_df["GDP Per Capita ($)"],
        x_title="WID",
        y_title="GDP per capita ($)",
    )

    fig.add_shape(
        type="line",
        line=dict(dash="dot", color="red"),
        x0=0,
        x1=len(summary_df["Country / Territory"]),
        y0=wolrd_average_GDP_per_capita,
        y1=wolrd_average_GDP_per_capita,
    )
    fig.add_shape(
        type="line",
        line=dict(dash="dot", color="orange"),
        x0=0,
        x1=len(summary_df["Country / Territory"]),
        y0=wolrd_median_GDP_per_capita,
        y1=wolrd_median_GDP_per_capita,
    )
    fig.add_annotation(
        x=11,
        y=wolrd_average_GDP_per_capita + 1300,
        text="World average = {}".format(wolrd_average_GDP_per_capita.round(0)),
        showarrow=False,
        font=dict(color=font_color, size=16),
    )
    fig.add_annotation(
        x=11,
        y=wolrd_median_GDP_per_capita + 1200,
        text="World median = {}".format(wolrd_median_GDP_per_capita.round(0)),
        showarrow=False,
        font=dict(color=font_color, size=16),
    )
    return fig



def dynamic_breakdown_figure_generation(
    y_axis_title,
    from_="Primary production",
    list_of_consumers=["International marine bunkers", "Domestic navigation"],
    carrier="Total Energy",
    destination_carrier="Total Energy",
):
    import os
    import plotly.express as px

    path = "Data/EnergyBalance"
    files = os.listdir(path)

    df = pd.read_csv("Data/EnergyBalance/{}/all_countries_df.csv".format(files[-1]))
    if carrier == destination_carrier:
        df = df[
            [
                "Country ({})".format(files[-1]),
                "Transactions(down)/Commodity(right)",
                carrier,
            ]
        ]
        df_final = pd.DataFrame()
        for country in Country_List:
            df_1 = df[df["Country ({})".format(files[-1])] == country]
            total_source = 0
            for i in from_:
                total_source += df_1[df_1["Transactions(down)/Commodity(right)"] == i][
                    carrier
                ].values[0]
            df_1.loc[:, carrier] = 100 * abs(df_1.loc[:, carrier]) / total_source  #
            if df_final.shape[0] == 0:
                df_final = df_1
            else:
                df_final = pd.concat([df_final, df_1])
    else:
        df = df[
            [
                "Country ({})".format(files[-1]),
                "Transactions(down)/Commodity(right)",
                carrier,
                destination_carrier,
            ]
        ]
        df_final = pd.DataFrame()
        for country in Country_List:
            df_1 = df[df["Country ({})".format(files[-1])] == country]
            total_source = 0
            for i in from_:
                total_source += df_1[df_1["Transactions(down)/Commodity(right)"] == i][
                    carrier
                ].values[0]
            df_1.loc[:, destination_carrier] = (
                100 * abs(df_1.loc[:, destination_carrier]) / total_source
            )  #
            if df_final.shape[0] == 0:
                df_final = df_1
            else:
                df_final = pd.concat([df_final, df_1])
    df_final = df_final[
        df_final["Transactions(down)/Commodity(right)"].isin(list_of_consumers)
    ]
    if carrier == destination_carrier:
        y_axis = carrier
    else:
        y_axis = destination_carrier
    fig = px.bar(
        df_final,
        x="Country ({})".format(files[-1]),
        color_discrete_sequence=px.colors.qualitative.Alphabet,
        y=y_axis,
        color="Transactions(down)/Commodity(right)",
    )

    fig.update_layout(
        legend=dict(
            bgcolor="rgba(0,0,0,0)",
            orientation="h",
            # yanchor="bottom",
            y=1.2,
            # xanchor="right",
            # x=0
        ),
        font=dict(family="Calibri", size=20, color=font_color),
        # hovermode="x"
    )

    fig.update_layout(
        {
            "plot_bgcolor": "rgba(0,0,0,0)",
            "paper_bgcolor": "rgba(0,0,0,0)",
        }
    )
    fig.update_yaxes(
        title_text=y_axis_title,
        showline=True,
        rangemode="tozero",
        linecolor=line_color,
        gridcolor=line_color,
    )
    fig.update_xaxes(
        showline=True,
        showgrid=False,
        linecolor=line_color,
    )
    fig.update_layout(title="")
    fig.update_traces(marker_line_color=font_color, marker_line_width=0, opacity=1)
    fig.update_layout(legend={"title_text": ""})

    fig.update_yaxes(rangemode="tozero", linecolor=line_color, gridcolor=line_color)
    fig.update_xaxes(
        showline=True,
        linecolor=line_color,
        title_text='<a href="http://unstats.un.org/unsd/energystats/pubs/balance"><sub>Source: Energy Balances, United Nations<sub></a>',
    ),
    return fig


def dynamic_breakdown_of_one_row(row):
    import os

    path = "Data/EnergyBalance"
    files = os.listdir(path)
    df = pd.read_csv("Data/EnergyBalance/{}/all_countries_df.csv".format(files[-1]))
    # print(df.head())

    df = df[df["Transactions(down)/Commodity(right)"] == row]
    df = df.iloc[:, :13]  # = df.iloc[:,2:12]/df["Total Energy"]
    df.iloc[:, 3:] = 100 * df.iloc[:, 3:].div(df["Total Energy"], axis=0)
    df.drop(columns=["Total Energy"], inplace=True)
    df = df.melt(id_vars=df.columns[:3])

    fig = px.bar(
        df,
        x="Country ({})".format(files[-1]),
        y="value",
        color="variable",
        color_discrete_sequence=px.colors.qualitative.Alphabet,
    )
    fig.update_layout(
        legend=dict(
            bgcolor="rgba(0,0,0,0)",
            orientation="h",
            y=1.2,
        ),
    )
    fig.update_yaxes(
        title_text="% of {}".format(row.lower()),
    )
    fig.update_layout(
        legend={"title_text": ""},
        template=simple_template,
    )
    fig.update_xaxes(
        title_text='<a href="http://unstats.un.org/unsd/energystats/pubs/balance"><sub>Source: Energy Balances, United Nations<sub></a>',
    )

    return fig


def dynamic_one_column_multiple_source(column, provider, y_axis_title):
    import os
    import plotly.express as px

    path = "Data/EnergyBalance"
    files = os.listdir(path)

    df = pd.read_csv("Data/EnergyBalance/{}/all_countries_df.csv".format(files[-1]))
    df = df[
        [
            "Country ({})".format(files[-1]),
            "Transactions(down)/Commodity(right)",
            column,
        ]
    ]
    df = df[df["Transactions(down)/Commodity(right)"].isin(provider)]
    df[column] = df[column] * 0.277778
    df[column] = df[column].round(1)
    fig = px.bar(
        df,
        x="Country ({})".format(files[-1]),
        text=column,
        color_discrete_sequence=px.colors.qualitative.Alphabet,
        y=column,
        color="Transactions(down)/Commodity(right)",
    )
    fig.update_yaxes(
        title_text=y_axis_title,
    )

    fig.update_layout(legend={"title_text": ""}, template=simple_template)
    fig.update_xaxes(
        title_text='<a href="http://unstats.un.org/unsd/energystats/pubs/balance"><sub>Source: Energy Balances, United Nations<sub></a>',
    ),
    return fig


def change_case(str):
    res = [str[0].lower()]
    for c in str[1:]:
        if c in ("ABCDEFGHIJKLMNOPQRSTUVWXYZ"):
            res.append("_")
            res.append(c.lower())
        else:
            res.append(c)

    return "".join(res)


if __name__ == "__main__":

    df_avg = pd.read_excel("Data/World_average_potentials.xlsx")
    average_world_PV = df_avg["World"][0]
    average_world_wind = df_avg["World"][2]
    print(average_world_PV)
