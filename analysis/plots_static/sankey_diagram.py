import pandas as pd
import plotly.graph_objects as go
from dash import Dash, dcc, html, Input, Output

# Read direction estimates
df = pd.read_csv("data/line_outputs/Crosstown/direction_estimates.csv")

# Read station mapping
station_mapping = (
    pd.read_csv("data/line_outputs/Crosstown/line_metadata.csv")
      .set_index("sortorder")["stop_name"]
      .to_dict()
)

# Unique months and days of the week for dropdown options
months = df['Month'].unique()
days_of_week = df['day_of_week'].unique()

def create_sankey_diagram(data: pd.DataFrame, station_mapping: dict, hour: int):
    """
    Create a Sankey diagram for one hour of data.
    """
    # Map IDs → names
    data = data.copy()
    data['origin_name'] = data['origin'].map(station_mapping)
    data['destination_name'] = data['destination'].map(station_mapping)

    # All station names used as node labels
    unique_labels = list(station_mapping.values())
    label_to_index = {lab: idx for idx, lab in enumerate(unique_labels)}

    # Build source / target index arrays
    source_indices = data['origin_name'].map(label_to_index)
    target_indices = data['destination_name'].map(label_to_index)

    # Make the figure
    fig = go.Figure(go.Sankey(
        node=dict(
            pad=15,
            thickness=20,
            line=dict(color="black", width=0.5),
            label=unique_labels,
        ),
        link=dict(
            source=source_indices,
            target=target_indices,
            value=data['estimated_ridership'],
        )
    ))

    fig.update_layout(
        title_text=f"Sankey Diagram of Subway Ridership — Hour {hour}",
        font_size=10
    )
    return fig

# Initialize the Dash app
app = Dash(__name__)

# Layout of the app
app.layout = html.Div([
    html.H1("Subway Ridership Sankey Diagram"),
    dcc.Dropdown(
        id='month-dropdown',
        options=[{'label': f'Month {int(month)}', 'value': int(month)} for month in months],
        value=1,  # Default value
        clearable=False
    ),
    dcc.Dropdown(
        id='day-dropdown',
        options=[{'label': day, 'value': day} for day in days_of_week],
        value='Monday',  # Default value
        clearable=False
    ),
    dcc.Dropdown(
        id='hour-dropdown',
        options=[{'label': f'Hour {hour}', 'value': hour} for hour in range(1, 25)],  # Assuming 24 hours
        value=1,  # Default value
        clearable=False
    ),
    dcc.Graph(id='sankey-graph')
])

# Callback to update the Sankey diagram based on selected month, day, and hour
@app.callback(
    Output('sankey-graph', 'figure'),
    Input('month-dropdown', 'value'),
    Input('day-dropdown', 'value'),
    Input('hour-dropdown', 'value')
)
def update_sankey(selected_month, selected_day, selected_hour):
    # Filter for the selected month, day of the week, and hour
    subset = df[
        (df.Month == selected_month) &
        (df.day_of_week == selected_day) &
        (df.hour_of_day == selected_hour)
    ]

    subset = subset.groupby(["origin","destination","hour_of_day"]).sum().reset_index()
    return create_sankey_diagram(subset, station_mapping, selected_hour)

# Run the app
if __name__ == '__main__':
    app.run(debug=False)