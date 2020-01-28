import dash
import pandas as pd
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
from dash.dependencies import Input, Output

# For Full length map, see notes here: https://github.com/facultyai/dash-bootstrap-components/issues/286
px.set_mapbox_access_token(open(".mapbox_token").read())

# Read in feature data
int_df = pd.read_csv('data/featurescombined.csv')

# Transform for intersection choices dropdown
int_choices = (int_df.filter(items=['location', 'cl_node_id'])
                     .rename(columns={'location': 'label', 'cl_node_id': 'value'})
                     .to_dict('records'))

fig = px.scatter_mapbox(int_df, lat='LAT', lon='LON', size='volume', zoom=10)

# Intersection selection dropdown
int_dropdown = dbc.FormGroup(
    [
        dbc.Label('Find Intersection', html_for='dropdown'),
        dcc.Dropdown(
            id='dropdown',
            options=int_choices,
        ),
    ]
)

# Checkbox for volume type shown in map
# TODO: udpate this checkbox w/ disabled actual volume
#       if actual is not available
output_type_checkbox = dbc.FormGroup(
[
    dbc.Label('Output Volume Type', html_for='output_type'),
    dbc.Checklist(
        id='output_type',
        options=[
            {'label': 'Projected', 'value': 'projected', 'disabled': True},
            {'label': 'Actual (if available)', 'value': 'volume'}
        ]
        )
]
    )


navbar = dbc.NavbarSimple(
    brand="Pedestrian Volume Modeling Project",
    brand_href="#",
    sticky="top",
)

body = dbc.Container(
    [
        dbc.Row(
            [
                dbc.Col(
                    [
                        html.H2("Intersection Viewer"),
                        html.P(
                            """Use the dropdown to find an intersection and the associated projected traffic volume."""
                        ),
                        dbc.Form(int_dropdown),
                        dbc.Form(output_type_checkbox),
                        dbc.Button("View details", color="secondary"),
                    ],
                    md=4,
                ),
                dbc.Col(
                    [
                        dcc.Graph(id="map-graph", style={"height":"100%"}),#, figure=fig),
                    ]
                ),
            ],
            className="h-100",
            no_gutters=True
        )
    ],
    className="mt-4",
    style={"height": "100vh"},
)

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

app.layout = html.Div([navbar, body])

@app.callback(
    Output('map-graph', 'figure'), 
    [Input('dropdown', 'value')],
)
def update_map(int_select):
    filtered_df = int_df.query("cl_node_id == @int_select")
    filtered_fig = px.scatter_mapbox(filtered_df, lat='LAT', lon='LON', size='volume', zoom=10)
    return filtered_fig

if __name__ == "__main__":

    import os

    debug = False if os.environ.get('DASH_DEBUG_MODE') == 'False' else True

    app.run_server(
        host='0.0.0.0', 
        port=8050,
        debug=debug
    )
