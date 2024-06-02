import pandas as pd
from statsmodels.tsa.arima.model import ARIMA
from sklearn.metrics import mean_squared_error
import numpy as np
import pmdarima as pm


def train_arima_model(df):
    model = ARIMA(df['Close'], order=(5, 1, 0))  # Order should be determined based on ACF/PACF analysis
    model_fit = model.fit()
    return model_fit

def predict_next_day_close_arima(model):
    # Forecast the next value
    forecast = model.forecast(steps=1)
    next_day_close = 0
    for cast in forecast:
        next_day_close = cast
        print("ARIMA_ARIMA_ARIMA_ARIMA_ARIMA_ARIMA_ARIMA_ARIMA_", next_day_close)
    return next_day_close
