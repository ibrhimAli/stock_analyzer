import plotly.graph_objs as go
from plotly.subplots import make_subplots

def plot_stl_decomposition(trend, seasonal, resid, dates):
    # Create a subplot with 3 rows
    fig = make_subplots(rows=3, cols=1, shared_xaxes=True, vertical_spacing=0.02)

    fig.add_trace(go.Scatter(x=dates, y=trend, name='Trend', line=dict(color='blue', width=2)), row=1, col=1)
    fig.add_trace(go.Scatter(x=dates, y=seasonal, name='Seasonal', line=dict(color='green', dash='dot')), row=2, col=1)
    fig.add_trace(go.Scatter(x=dates, y=resid, name='Residual', line=dict(color='red', width=1)), row=3, col=1)

    # Set titles and axis properties
    fig.update_layout(height=600, width=800, title_text="STL Decomposition: Trend, Seasonal, and Residual Components")
    fig.update_xaxes(title_text="Date")
    fig.update_yaxes(title_text="Value", row=1, col=1)
    fig.update_yaxes(title_text="Value", row=2, col=1)
    fig.update_yaxes(title_text="Value", row=3, col=1)

    # Interactive features
    fig.update_layout(hovermode='closest')

    return fig.to_html(full_html=False, include_plotlyjs='cdn')
