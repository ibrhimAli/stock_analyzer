import pandas as pd
import plotly.graph_objs as go
import numpy as np

def plot_bollinger_bands(df, predicted_close):
    trace_close = go.Scatter(
        x=df.index,
        y=df['Close'],
        name='Close',
        line=dict(color='blue')
    )
    
    trace_sma = go.Scatter(
        x=df.index,
        y=df['SMA'],
        name='SMA',
        line=dict(color='orange')
    )
    
    trace_upper_band = go.Scatter(
        x=df.index,
        y=df['Upper Band'],
        name='Upper Band',
        line=dict(color='green')
    )
    
    trace_lower_band = go.Scatter(
        x=df.index,
        y=df['Lower Band'],
        name='Lower Band',
        line=dict(color='red')
    )
    
    trace_predicted = go.Scatter(
        x=[df.index[-1] + pd.Timedelta(days=1)],  # This plots the predicted point on the next day
        y=[predicted_close],
        name='Predicted Close',
        mode='markers+text',  # Adds text label
        text=['Predicted Close'],
        textposition="top center",
        marker=dict(color='purple', size=10)
    )
    
    trace_band_fill = go.Scatter(
        x=np.concatenate([df.index, df.index[::-1]]),  # Concatenate index for x-axis using numpy
        y=np.concatenate([df['Upper Band'], df['Lower Band'][::-1]]),  # Concatenate upper and lower bands for y-axis using numpy
        fill='toself',
        fillcolor='rgba(68, 68, 68, 0.3)',  # semi-transparent fill
        line=dict(color='rgba(255,255,255,0)'),  # hide the line
        showlegend=False,
        name='Band Fill'
    )
    
    # Calculate width of bands as a new column
    df['Band Width'] = df['Upper Band'] - df['Lower Band']

    # Identify narrow band points (customize the threshold as needed)
    narrow_band = df['Band Width'] < (df['Band Width'].mean() * 0.5)  # Example threshold: 50% of the average width

    trace_squeeze = go.Scatter(
        x=df.index[narrow_band],
        y=df['SMA'][narrow_band],
        name='Squeeze Points',
        mode='markers',
        marker=dict(color='black', size=5),
        text='Squeeze'
    )
    
    data = [trace_close, trace_sma, trace_band_fill, trace_upper_band, trace_lower_band, trace_predicted, trace_squeeze]
    
    trace_buy_signals = go.Scatter(
        x=df.index[df['Buy'].notna()],
        y=df['Buy'][df['Buy'].notna()],
        mode='markers',
        marker=dict(color='green', size=10),
        name='Buy Signal'
    )

    trace_sell_signals = go.Scatter(
        x=df.index[df['Sell'].notna()],
        y=df['Sell'][df['Sell'].notna()],
        mode='markers',
        marker=dict(color='red', size=10),
        name='Sell Signal'
    )

    data.extend([trace_buy_signals, trace_sell_signals])

    layout = go.Layout(
        title='Bollinger Bands and Predicted Close',
        xaxis=dict(title='Date'),
        yaxis=dict(title='Price')
    )
    
    fig = go.Figure(data=data, layout=layout)
    return fig.to_html(full_html=False, include_plotlyjs='cdn')
