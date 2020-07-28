import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.graph_objects as go

from get_data import *
from navbar import new_navbar
from total_stats import cards, cards_lower, make_card
from make_graph import make_graph, lower_graph, total_graph
from select_graph_att import state_dcc, district_dcc

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.DARKLY])
app.title = "Covid India Tracker"

top_row = dbc.Container([
    dbc.Row([cards, total_graph]),
])

second_row = dbc.Container([
    dbc.Row(html.H3(children = "State & District Status"), justify = "center"),
    dbc.Row(html.Br()),
    dbc.Row([state_dcc, district_dcc], justify='center'),
    dbc.Row([cards_lower, lower_graph])
])

app.layout = html.Div(
    children=[
        new_navbar,
        html.Br(),
        top_row,
        html.Br(),
        second_row,
        html.Br()
    ])

# @app.callback(
#     Output("registeration-toast", "is_open"),
#     [Input("sign-up-button", "n_clicks")],
# )
# def open_toast(n):
#     if n:
#         return True
#     return False


@app.callback(
    [Output("district-selected-dcc", "options"),
    Output("lower_card", "children")],
    [Input("state-selected-dcc", "value")]
)
def update_district(state_name):
    df_1 = state_data_daily(state_name)[-1:]
    return [{'label':district_name, 'value':district_name} for district_name in get_state_to_district_mapping(state_name)],[dbc.Row([
    dbc.Col([
        dbc.Row([make_card(df_1, "Confirmed", "info")], 
            justify="center", 
            no_gutters=False), html.Br(), 
        dbc.Row([make_card(df_1, "Active", "danger")], 
            justify="center", 
            no_gutters=False)]),
    dbc.Col([
        dbc.Row([make_card(df_1, "Recovered", "success")], 
            justify="center", 
            no_gutters=False), html.Br(), 
        dbc.Row([make_card(df_1, "Deceased", "light")], 
            justify="center", 
            no_gutters=False)])
    ])]

@app.callback(
    Output("district-selected-nav", "options"),
    [Input("state-selected-nav", "value")]
)
def update_district_nav(state_name_nav):
    return [{'label':district_name, 'value':district_name} for district_name in get_state_to_district_mapping(state_name_nav)]

# @app.callback(
#     ,
#     [Input("state-selected-dcc", "value")]
# )
# def update_district(state_name):
    
#     return 


@app.callback(
    Output("lower_graph", "figure"),
    [Input("state-selected-dcc", "value"),
    Input("district-selected-dcc", "value")]
)
def update_graph2(*args):
    triggered_name = dash.callback_context.triggered[0]['prop_id'].split('.')[0]
    triggered_value = dash.callback_context.triggered[0]['value']
    if not dash.callback_context.triggered:
        df = state_data_daily("Delhi")
        return make_graph(df, "Delhi")
    if triggered_name == 'state-selected-dcc':
        df = state_data_daily(triggered_value)
        return make_graph(df, triggered_value)
    else:
        df = district_data_daily(triggered_value)
        return make_graph(df, triggered_value)



if __name__ == '__main__':
    app.run_server(dev_tools_hot_reload=True, debug=True)
