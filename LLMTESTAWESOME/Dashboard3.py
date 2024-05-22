from dash import dcc, html, Dash, callback, Input, Output
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import networkx as nx

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
                dcc.Graph(id="power_dynamics_graph")
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

# Data for power dynamics
nodes = [
    {"id": "Business 1", "group": 1},
    {"id": "Business 2", "group": 1},
    {"id": "Supplier 1", "group": 2},
    {"id": "Supplier 2", "group": 2},
    {"id": "Supplier 3", "group": 2},
    {"id": "Product A", "group": 3},
    {"id": "Product B", "group": 3},
    {"id": "Product C", "group": 3}
]

links = [
    {"source": "Business 1", "target": "Product A", "value": 1},
    {"source": "Business 1", "target": "Product C", "value": 1},
    {"source": "Business 2", "target": "Product B", "value": 1},
    {"source": "Supplier 1", "target": "Business 1", "value": 1},
    {"source": "Supplier 2", "target": "Business 2", "value": 1},
    {"source": "Supplier 3", "target": "Business 1", "value": 1}
]

def create_force_directed_graph():
    G = nx.Graph()
    
    for node in nodes:
        G.add_node(node["id"], group=node["group"])
        
    for link in links:
        G.add_edge(link["source"], link["target"], value=link["value"])
    
    pos = nx.spring_layout(G, seed=42)  # positions for all nodes
    
    edge_trace = go.Scatter(
        x=[],
        y=[],
        line=dict(width=0.5, color='#888'),
        hoverinfo='none',
        mode='lines')

    for edge in G.edges():
        x0, y0 = pos[edge[0]]
        x1, y1 = pos[edge[1]]
        edge_trace['x'] += [x0, x1, None]
        edge_trace['y'] += [y0, y1, None]

    node_trace = go.Scatter(
        x=[],
        y=[],
        text=[],
        mode='markers+text',
        textposition='top center',
        hoverinfo='text',
        marker=dict(
            showscale=True,
            colorscale='YlGnBu',
            size=10,
            colorbar=dict(
                thickness=15,
                title='Node Connections',
                xanchor='left',
                titleside='right'
            ),
            line_width=2))

    for node in G.nodes():
        x, y = pos[node]
        node_trace['x'] += [x]
        node_trace['y'] += [y]
        node_trace['text'] += [node]

    fig = go.Figure(data=[edge_trace, node_trace],
                 layout=go.Layout(
                    title='Power Dynamics Mapping',
                    titlefont_size=16,
                    showlegend=False,
                    hovermode='closest',
                    margin=dict(b=20,l=5,r=5,t=40),
                    annotations=[ dict(
                        text="",
                        showarrow=False,
                        xref="paper", yref="paper") ],
                    xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                    yaxis=dict(showgrid=False, zeroline=False, showticklabels=False))
                    )
    
    return fig

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

# Callback to update power dynamics graph
@app.callback(
    Output("power_dynamics_graph", "figure"),
    [Input("ingredient_search", "value")]  # Placeholder input
)
def update_power_dynamics_mapping(_):
    return create_force_directed_graph()

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
