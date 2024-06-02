import plotly.graph_objs as go

def plot_stochastic_signals(df):
    buy_signals = df[(df['%K'] < 20) & (df['%K'].shift(-1) > df['%D'].shift(-1))]
    sell_signals = df[(df['%K'] > 80) & (df['%K'].shift(-1) < df['%D'].shift(-1))]
    
    trace_k = go.Scatter(x=df.index, y=df['%K'], name='%K', line=dict(color='blue'))
    trace_d = go.Scatter(x=df.index, y=df['%D'], name='%D', line=dict(color='orange'))
    trace_buy = go.Scatter(x=buy_signals.index, y=buy_signals['%K'], mode='markers', name='Buy Signal', marker=dict(color='green', size=10))
    trace_sell = go.Scatter(x=sell_signals.index, y=sell_signals['%K'], mode='markers', name='Sell Signal', marker=dict(color='red', size=10))

    layout = go.Layout(
        title='Stochastic Oscillator with Signals',
        xaxis=dict(title='Date'),
        yaxis=dict(title='Percentage'),
        shapes=[
            {'type': 'line', 'x0': df.index.min(), 'y0': 80, 'x1': df.index.max(), 'y1': 80, 'line': {'color': 'red', 'dash': 'dash'}},
            {'type': 'line', 'x0': df.index.min(), 'y0': 20, 'x1': df.index.max(), 'y1': 20, 'line': {'color': 'green', 'dash': 'dash'}}
        ]
    )

    fig = go.Figure(data=[trace_k, trace_d, trace_buy, trace_sell], layout=layout)
    return fig.to_html(full_html=False, include_plotlyjs='cdn')

