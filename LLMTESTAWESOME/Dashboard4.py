from dash import dcc, html, Dash, callback, Input, Output
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np

css = ["https://cdn.jsdelivr.net/npm/bootstrap@5.3.1/dist/css/bootstrap.min.css"]
app = Dash(name="Supply Chain Dashboard", external_stylesheets=css)

# Mock dataset
data = {
    "Product": ["Product A", "Product B", "Product C"],
    "Ingredients": [["Ingredient 1", "Ingredient 2"], ["Ingredient 3", "Ingredient 4"], ["Ingredient 1", "Ingredient 5"]],
    "Businesses": ["Business 1", "Business 2", "Business 1"],
    "Suppliers": ["Supplier 1", "Supplier 2", "Supplier 3"],
    "Environmental Impact": [0.3, 0.5, 0.2]
}

df = pd.DataFrame(data)

# Dropdown options
products = df["Product"].unique()
businesses = df["Businesses"].unique()
suppliers = df["Suppliers"].unique()

# Sample data for the scatter plot
np.random.seed(0)
scatter_df = pd.DataFrame({"Col " + str(i + 1): np.random.rand(30) for i in range(6)})

# Define layout
app.layout = html.Div([
    html.Div([
        html.H1("Supply Chain Dashboard", className="text-center fw-bold m-2"),
        html.Br(),
        dcc.Tabs([
            dcc.Tab([
                html.Br(),
                dcc.Dropdown(id="ingredient_search", options=[{'label': i, 'value': i} for i in products], value=products[0], clearable=False),
                html.Br(),
                dcc.Graph(id="ingredient_graph")
            ], label="Ingredient Search"),
            dcc.Tab([
                html.Br(),
                dcc.Dropdown(id="product_reverse_search", options=[{'label': i, 'value': i} for i in products], value=products[0], clearable=False),
                html.Br(),
                dcc.Graph(id="reverse_search_graph")
            ], label="Product Reverse Search"),
            dcc.Tab([
                html.Br(),
                dcc.Dropdown(id="business_to_product", options=[{'label': i, 'value': i} for i in businesses], value=businesses[0], clearable=False),
                html.Br(),
                dcc.Graph(id="business_product_graph")
            ], label="Business-to-Product Mapping"),
            dcc.Tab([
                html.Br(),
                dcc.Dropdown(id="supply_chain_mapping", options=[{'label': i, 'value': i} for i in products], value=products[0], clearable=False),
                html.Br(),
                dcc.Graph(id="supply_chain_graph")
            ], label="Supply Chain Mapping"),
            dcc.Tab([
                html.Br(),
                html.Div(dcc.Graph(id="g1", config={"displayModeBar": False}), className="four columns"),
                html.Div(dcc.Graph(id="g2", config={"displayModeBar": False}), className="four columns"),
                html.Div(dcc.Graph(id="g3", config={"displayModeBar": False}), className="four columns")
            ], label="Power Dynamics Mapping"),
            dcc.Tab([
                html.Br(),
                dcc.Dropdown(id="comparison_feature", options=[{'label': i, 'value': i} for i in products], value=products[0], clearable=False),
                html.Br(),
                dcc.Graph(id="comparison_graph")
            ], label="Comparison Feature"),
            dcc.Tab([
                html.Br(),
                dcc.Dropdown(id="environmental_impact", options=[{'label': i, 'value': i} for i in products], value=products[0], clearable=False),
                html.Br(),
                dcc.Graph(id="environmental_impact_graph")
            ], label="Environmental Impact Analysis"),
            dcc.Tab([
                html.Br(),
                dcc.Dropdown(id="stakeholder_info", options=[{'label': i, 'value': i} for i in products], value=products[0], clearable=False),
                html.Br(),
                dcc.Graph(id="stakeholder_graph")
            ], label="Stakeholder Information")
        ])
    ], className="col-8 mx-auto"),
], style={"background-color": "#e5ecf6", "height": "100vh"})

# Define callback for scatter plot interactions
def get_figure(df, x_col, y_col, selectedpoints, selectedpoints_local):
    if selectedpoints_local and selectedpoints_local["range"]:
        ranges = selectedpoints_local["range"]
        selection_bounds = {
            "x0": ranges["x"][0],
            "x1": ranges["x"][1],
            "y0": ranges["y"][0],
            "y1": ranges["y"][1],
        }
    else:
        selection_bounds = {
            "x0": np.min(df[x_col]),
            "x1": np.max(df[x_col]),
            "y0": np.min(df[y_col]),
            "y1": np.max(df[y_col]),
        }

    fig = px.scatter(df, x=df[x_col], y=df[y_col], text=df.index)
    fig.update_traces(
        selectedpoints=selectedpoints,
        customdata=df.index,
        mode="markers+text",
        marker={"color": "rgba(0, 116, 217, 0.7)", "size": 20},
        unselected={"marker": {"opacity": 0.3}, "textfont": {"color": "rgba(0, 0, 0, 0)"}}
    )
    fig.update_layout(
        margin={"l": 20, "r": 0, "b": 15, "t": 5},
        dragmode="select",
        hovermode=False,
        newselection_mode="gradual",
    )
    fig.add_shape(
        dict(
            {"type": "rect", "line": {"width": 1, "dash": "dot", "color": "darkgrey"}},
            **selection_bounds
        )
    )
    return fig

@app.callback(
    Output("g1", "figure"),
    Output("g2", "figure"),
    Output("g3", "figure"),
    Input("g1", "selectedData"),
    Input("g2", "selectedData"),
    Input("g3", "selectedData")
)
def update_graphs(selection1, selection2, selection3):
    selectedpoints = scatter_df.index
    for selected_data in [selection1, selection2, selection3]:
        if selected_data and selected_data["points"]:
            selectedpoints = np.intersect1d(
                selectedpoints, [p["customdata"] for p in selected_data["points"]]
            )

    return [
        get_figure(scatter_df, "Col 1", "Col 2", selectedpoints, selection1),
        get_figure(scatter_df, "Col 3", "Col 4", selectedpoints, selection2),
        get_figure(scatter_df, "Col 5", "Col 6", selectedpoints, selection3),
    ]

# Callback to update ingredient search graph
@app.callback(
    Output("ingredient_graph", "figure"),
    [Input("ingredient_search", "value")]
)
def update_ingredient_search(product):
    ingredients = df[df["Product"] == product]["Ingredients"].values[0]
    fig = go.Figure(data=[go.Table(
        header=dict(values=["Ingredient"], align='left'),
        cells=dict(values=[[ingredient for ingredient in ingredients]], align='left'))
    ])
    return fig

# Callback to update product reverse search graph
@app.callback(
    Output("reverse_search_graph", "figure"),
    [Input("product_reverse_search", "value")]
)
def update_product_reverse_search(product):
    suppliers = df[df["Product"] == product]["Suppliers"].values[0]
    fig = px.bar(x=[suppliers], y=[1], labels={"x": "Supplier", "y": "Count"}, title=f"Suppliers for {product}")
    return fig

# Callback to update business to product mapping graph
@app.callback(
    Output("business_product_graph", "figure"),
    [Input("business_to_product", "value")]
)
def update_business_to_product(business):
    products = df[df["Businesses"] == business]["Product"].values
    fig = px.bar(x=products, y=[1]*len(products), labels={"x": "Product", "y": "Count"}, title=f"Products by {business}")
    return fig

# Callback to update supply chain mapping graph
@app.callback(
    Output("supply_chain_graph", "figure"),
    [Input("supply_chain_mapping", "value")]
)
def update_supply_chain_mapping(product):
    business = df[df["Product"] == product]["Businesses"].values[0]
    suppliers = df[df["Product"] == product]["Suppliers"].values[0]
    fig = go.Figure(data=[go.Table(
        header=dict(values=["Business", "Supplier"], align='left'),
        cells=dict(values=[[business], [suppliers]], align='left'))
    ])
    return fig

# Callback to update comparison feature graph
@app.callback(
    Output("comparison_graph", "figure"),
    [Input("comparison_feature", "value")]
)
def update_comparison_feature(product):
    env_impact = df[df["Product"] == product]["Environmental Impact"].values[0]
    fig = px.bar(x=[product], y=[env_impact], labels={"x": "Product", "y": "Environmental Impact"}, title=f"Environmental Impact of {product}")
    return fig

# Callback to update environmental impact graph
@app.callback(
    Output("environmental_impact_graph", "figure"),
    [Input("environmental_impact", "value")]
)
def update_environmental_impact(product):
    env_impact = df[df["Product"] == product]["Environmental Impact"].values[0]
    fig = px.bar(x=[product], y=[env_impact], labels={"x": "Product", "y": "Environmental Impact"}, title=f"Environmental Impact of {product}")
    return fig

# Callback to update stakeholder info graph
@app.callback(
    Output("stakeholder_graph", "figure"),
    [Input("stakeholder_info", "value")]
)
def update_stakeholder_info(product):
    suppliers = df[df["Product"] == product]["Suppliers"].values[0]
    business = df[df["Product"] == product]["Businesses"].values[0]
    fig = go.Figure(data=[go.Table(
        header=dict(values=["Stakeholder", "Role"], align='left'),
        cells=dict(values=[[business, suppliers], ["Business", "Supplier"]], align='left'))
    ])
    return fig

if __name__ == "__main__":
    app.run(debug=True)
