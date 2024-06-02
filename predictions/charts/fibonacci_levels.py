import plotly.graph_objs as go

def plot_fibonacci_levels(df, levels, predicted_close=None):
    trace_close = go.Scatter(
        x=df.index,
        y=df['Close'],
        name='Close',
        line=dict(color='blue')
    )

    # Add a marker for the predicted close, if available
    traces = [trace_close]
    if predicted_close:
        trace_predicted = go.Scatter(
            x=[df.index.max()],  # Assume the predicted close is the next point
            y=[predicted_close],
            name='Predicted Close',
            mode='markers',
            marker=dict(color='purple', size=10),
            text=f"Predicted Close: {predicted_close:.2f}"
        )
        traces.append(trace_predicted)

    # Create the shapes for the Fibonacci levels
    shapes = []
    for key, value in levels.items():
        shapes.append({
            'type': 'line',
            'x0': df.index.min(),
            'y0': value,
            'x1': df.index.max(),
            'y1': value,
            'line': {
                'color': 'orange',
                'width': 2,
                'dash': 'dash'
            },
            'name': key
        })

    layout = go.Layout(
        title='Fibonacci Retracement Levels',
        xaxis=dict(title='Date'),
        yaxis=dict(title='Price'),
        shapes=shapes
    )

    fig = go.Figure(data=traces, layout=layout)
    return fig.to_html(full_html=False, include_plotlyjs='cdn')
