import pandas as pd
from statsmodels.tsa.seasonal import STL

def decompose_time_series(df, seasonal):
    series = df['Close']
    stl = STL(series, seasonal)  
    result = stl.fit()
    return result.trend, result.seasonal, result.resid