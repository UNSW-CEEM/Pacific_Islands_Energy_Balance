from dash.dependencies import Input, Output, State

from app import app
from EnergyFlows import Country_List
from DecarbonizationFunctions import run_decarbonization_scenario
from figures import single_barplot, multiple_barplot


@app.callback(
    [
        Output("payback-periods", "figure"),
        Output("installed-storage", "figure"),
        Output("installed-MW", "figure"),
    ],
    Input("update-button", "n_clicks"),
    [
        State("radio-demand-scenario", "value"),
        State("year-for-decarbonization", "value"),
        State("genset-cost", "value"),
        State("diesel-price", "value"),
        State("coal-price", "value"),
        State("carbon-price", "value"),
        State("available-land", "value"),
        State("available-coastline", "value"),
        State("available-buildings", "value"),
        State("large-PV-cost", "value"),
        State("rooftop-PV-cost", "value"),
        State("res-battery-cost", "value"),
        State("wind-large-cost", "value"),
        State("storage-days", "value"),
        State("rooftop-size", "value"),
        State("res-battery-size", "value"),
        State("ComBattery-cost", "value"),
        State("decarb-year", "value"),
        State("discount-rate", "value"),
        State("inflation-rate", "value"),
    ],
)
def sensor_checklist(
    n_clicks,
    demand_scenario,
    dataset_year,
    genset_cap,
    diesel_price,
    coal_price,
    carbon_price,
    avail_land,
    avail_coast,
    avail_buildings,
    lg_PV_cost,
    rooftop_PV_cost,
    sm_batt_cost,
    wind_cost,
    storage_days,
    rooftop_size,
    res_bat_size,
    comm_bat_cost,
    decarb_year,
    disc_rate,
    infl_rate,
):
    if n_clicks:

        Dict = {
            "diesel_cap": genset_cap,
            "rooftop": rooftop_PV_cost,
            "resid_battery": sm_batt_cost,
            "comm_battery": comm_bat_cost,
            "large_PV": lg_PV_cost,
            "wind": wind_cost,
            "coal": coal_price,
            "discount_rate": disc_rate,
            "inflation_rate": infl_rate,
            "diesel_price": diesel_price,
            "storage_days": storage_days,
            "gas$/m3": "Nan",
            "emissiont/GWh_diesel": 1100,  # AEMO:0.7-1.5
            "emissiont/GWh_blackCoal": 900,  # AEMO:0.7-1.5
            "emissiont/GWh_brownCoal": 1200,  # AEMO:1.1-1.3
            "carbon_price": carbon_price,  # $/tonne
            "rooftop_size": rooftop_size,
            "res_battery_size": res_bat_size,
        }

        final_df, all_countries_result = run_decarbonization_scenario(
            cost_scenario=None,
            country_list=Country_List,
            demand_scenario=demand_scenario,
            available_land=avail_land / 100,
            avaialble_coastline=avail_coast / 100,
            avaialble_buildings=avail_buildings / 100,
            PV_size=rooftop_size,
            decarb_year=decarb_year,
            input_dicts=Dict,
        )

        fig = single_barplot(
            title="Payback Period",
            x_axis=Country_List,
            y_axis=all_countries_result.iloc[6, 1:].values.tolist(),
            x_title="",
            y_title="Years",
        )
        fig2 = multiple_barplot(
            title="Storage capacity",
            x_axis=Country_List,
            y_axis_list=[
                all_countries_result.iloc[3, 1:].values.tolist(),
                all_countries_result.iloc[4, 1:].values.tolist(),
            ],
            x_title="",
            y_title="GWh",
            name_list=["Residential battery", "Community battery"],
            color_list=["#0033CC", "#33CCFF"],
            barmode="group",
        )
        fig3 = multiple_barplot(
            title="Capacity",
            x_axis=Country_List,
            y_axis_list=[
                all_countries_result.iloc[0, 1:].values.tolist(),
                all_countries_result.iloc[1, 1:].values.tolist(),
                all_countries_result.iloc[2, 1:].values.tolist(),
            ],
            x_title="",
            y_title="MW",
            name_list=["Rooftop PV", "Utility PV", "Wind"],
            color_list=["#0033CC", "#33CCFF", "blue"],
            barmode="group",
        )
        fig3.update_layout(legend=dict(y=0.9,yanchor="bottom"))

        return fig, fig2, fig3
