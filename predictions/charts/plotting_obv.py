import plotly.graph_objs as go

def plot_obv(df):
    trace_obv = go.Scatter(
        x=df.index,
        y=df['OBV'],
        name='On-Balance Volume',
        line=dict(color='blue')
    )

    layout = go.Layout(
        title='On-Balance Volume',
        xaxis=dict(title='Date'),
        yaxis=dict(title='OBV'),
    )

    fig = go.Figure(data=[trace_obv], layout=layout)
    return fig.to_html(full_html=False, include_plotlyjs='cdn')
