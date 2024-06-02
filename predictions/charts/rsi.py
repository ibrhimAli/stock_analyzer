import plotly.express as px

def create_rsi_chart(df):
    fig = px.line(df, x=df.index, y='RSI', title='Relative Strength Index (RSI)')
    fig.add_hline(y=70, line_dash="dash", line_color="red")
    fig.add_hline(y=30, line_dash="dash", line_color="green")
    return fig