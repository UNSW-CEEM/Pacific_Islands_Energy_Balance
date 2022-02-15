from app import app
import dash_bootstrap_components as dbc
import page1FarmView as F
from dash import html
from dash.dependencies import Input, Output, State
import pandas as pd
import callbacks
# import page1FarmView
# import callbacksPage1FarmView
# import callbacksPage1TurbineView
# import callbacksDbManager
# import callbacksTrendmonitoring

app.layout = dbc.Container([

    F.generate_navbar(app),
    html.Br(),
    F.content,
    html.Br(),
], fluid=True)

app.title = "Pacific Island Countries"

if __name__ == '__main__':
    # app.run_server(host='0.0.0.0',debug=False,port=8080,dev_tools_ui=False,dev_tools_props_check=False)#MapnaMind
    app.run_server(debug=True,dev_tools_ui=False,dev_tools_props_check=False)#ShayanLaptop


