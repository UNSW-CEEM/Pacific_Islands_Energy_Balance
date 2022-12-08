from dash.dependencies import Input, Output, ALL, State, MATCH, ALLSMALLER

from app import app

@app.callback(
    [Output('payback-periods', 'children'),
     Output('installed-wind', 'children'),
     ],
    Input('update-button','n_clicks'),
    [State("year-for-decarbonization", "value"),
     State("diesel-price", "value"),
     State("coal-price", "value"),
     State("carbon-price", "value"),
     State("available-land", "value"),
     State("available-coastline", "value"),
     State("available-buildings", "value"),
     State("large-PV-cost", "value"),
     State("res-battery-cost", "value"),
     State('wind-large-cost', "value"),
     State('storage-days', "value"),
     State('rooftop-size', "value"),
     State('res-battery-size', "value"),
     State('ComBattery-cost', "value"),
     State('decarb-year', "value"),
     State('discount-rate', "value"),
     State('inflation-rate', "value"),
     ])
def sensor_checklist(n_clicks,dataset_year,diesel_price,coal_price,carbon_price,
                     avail_land,avail_coast,avail_buildings,
                     lg_PV_cost, sm_batt_cost,wind_cost,storage_days,rooftop_size,
                     res_bat_size,comm_bat_cost,decarb_year,disc_rate,infl_rate
                     ):
 input_dict = {
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
  "carbon_price": 100,  # $/tonne

 },  # $/W