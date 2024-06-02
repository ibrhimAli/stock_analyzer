import plotly.express as px

def create_price_chart(df):
    fig = px.line(df, x=df.index, y='Close', title='Close Price Over Time')
    return fig