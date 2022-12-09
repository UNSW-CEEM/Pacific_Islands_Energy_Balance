from dash.dependencies import Input, Output, ALL, State, MATCH, ALLSMALLER

import functions
from app import app
from dash import html
import numpy as np
import pandas as pd
import figures
import Summary
import EnergyFlows
import Decarbonization
import WindSolar
import FinancialFlows
import BioEnergy
import Geothermal

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


@app.callback(Output("Visible-content", "children"), Input("tabs", "active_tab"))
def switch_tab(tab):
    if tab == "summary-tab":
        return Summary.content
    elif tab == "energy-flows-tab":
        return EnergyFlows.content
    elif tab == "decrb-tab":
        return Decarbonization.content
    elif tab == "windSolar-tab":
        return WindSolar.content
    elif tab == "geothermal-tab":
        return Geothermal.content
    elif tab == "financial-flows-tab":
        return FinancialFlows.content
    elif tab == "bioenergy-tab":
        return BioEnergy.content


@app.callback(
    [
        Output("transit_figure1", "figure"),
        Output("transit_figure2", "figure"),
        Output("transit_figure3", "figure"),
        Output("transit_figure4", "figure"),
        Output("generation_mix_GWh", "figure"),
        Output("generation_mix_MW", "figure"),
    ],
    [Input("select-year", "value")],
)
def update_update_database(year):
    # functions.Update_UNstats_database(year)
    # figures.validation()
    return (
        figures.UNstats_plots(year)[0],
        figures.UNstats_plots(year)[1],
        figures.UNstats_plots(year)[2],
        figures.imports_to_GDP(year),
        figures.generation_mix_plot()[0],
        figures.generation_mix_plot()[1],
    )


@app.callback(
    Output("PV-map", "figure"),
    [
        Input("select-justcountry", "value"),
        Input("select-map-style", "value"),
    ],
)
def update_options(Country, style):
    return figures.mapboxplot(Country, style)


