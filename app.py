import dash
import pathlib
import dash_bootstrap_components as dbc

external_stylesheets = [dbc.themes.DARKLY]
app = dash.Dash(__name__, external_stylesheets=external_stylesheets,suppress_callback_exceptions=True)
application  = app.server
APP_PATH = str(pathlib.Path(__file__).parent.resolve())







