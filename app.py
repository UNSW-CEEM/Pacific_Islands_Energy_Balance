import dash
import dash_bootstrap_components as dbc
import pathlib

# external_stylesheets = ['/assets/css/darkly/bootstrap.min.css']
import pandas as pd

external_stylesheets = [dbc.themes.DARKLY]


app = dash.Dash(__name__, external_stylesheets=external_stylesheets,suppress_callback_exceptions=True)

server = app.server

APP_PATH = str(pathlib.Path(__file__).parent.resolve())



