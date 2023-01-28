import dash
import pathlib
import dash_bootstrap_components as dbc

external_stylesheets = [dbc.themes.DARKLY]
app = dash.Dash(__name__, external_stylesheets=external_stylesheets,
                suppress_callback_exceptions=True,
                meta_tags=[
                    {
                        "name": "viewport",
                        "content": "width=device-width, initial-scale=1, maximum-scale=1",
                    }
                ],
                )
application  = app.server
APP_PATH = str(pathlib.Path(__file__).parent.resolve())







