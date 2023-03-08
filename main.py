from flask import Flask
import dash
import dash_bootstrap_components as dbc

# Import the layout from the dash_layout module
from dash_layout import layout

# Initialize Flask app
server = Flask(__name__)

# Initialize Dash app
app = dash.Dash(__name__, server=server, external_stylesheets=[dbc.themes.BOOTSTRAP, {'href': 'dash_custom_style.css', 'rel': 'stylesheet'}
], )

# Set the layout of the Dash app to the imported layout
app.layout = layout


# Define Flask route that returns the Dash app layout
@server.route('/')
def index():
    return app.layout


# Run the app
if __name__ == '__main__':
    server.run(debug=True)
