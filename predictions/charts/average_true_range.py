import plotly.graph_objs as go

def plot_atr(df):
    trace_atr = go.Scatter(
        x=df.index,
        y=df['ATR'],
        name='Average True Range',
        line=dict(color='blue')
    )

    layout = go.Layout(
        title='Average True Range',
        xaxis=dict(title='Date'),
        yaxis=dict(title='ATR'),
    )

    fig = go.Figure(data=[trace_atr], layout=layout)
    return fig.to_html(full_html=False, include_plotlyjs='cdn')