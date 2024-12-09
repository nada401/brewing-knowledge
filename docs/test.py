import numpy as np
import plotly.graph_objects as go

# Function to generate data
def generate_graph_data(weight1, weight2):
    x = np.linspace(0, 10, 100)
    y = np.sin(x * weight1) * np.cos(x * weight2)
    return x, y

# Initial data
initial_weight1 = 1
initial_weight2 = 1
x, y = generate_graph_data(initial_weight1, initial_weight2)

# Define weight ranges
weight1_range = np.linspace(0.5, 2, 10)
weight2_range = np.linspace(0.5, 2, 10)

# Create figure
fig = go.Figure()

# Add initial trace
fig.add_trace(go.Scatter(x=x, y=y, mode='lines', name='Graph'))

# Create dropdown options for weight1 and weight2
dropdown_weight1 = [
    {"label": f"Weight 1: {w1:.1f}", "method": "update", 
     "args": [{"visible": [i == idx for i in range(len(weight1_range))]},
              {"title": f"Weight 1: {w1:.1f}"}]}
    for idx, w1 in enumerate(weight1_range)
]

dropdown_weight2 = [
    {"label": f"Weight 2: {w2:.1f}", "method": "update", 
     "args": [{"visible": [i == idx for i in range(len(weight2_range))]},
              {"title": f"Weight 2: {w2:.1f}"}]}
    for idx, w2 in enumerate(weight2_range)
]

# Add buttons to layout
fig.update_layout(
    updatemenus=[
        {"buttons": dropdown_weight1, "direction": "down", "x": 0.1, "y": 1.2, "showactive": True},
        {"buttons": dropdown_weight2, "direction": "down", "x": 0.3, "y": 1.2, "showactive": True},
    ],
    title="Interactive Graph with Dropdown Menus",
    xaxis_title="X",
    yaxis_title="Y",
)

fig.show()
