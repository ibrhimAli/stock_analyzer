import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split

def prepare_features(df):
    """

    Prepares features for the model. This includes shifting the 'Close' price by one day to predict the next day's close.
    """
    df['Prev Close'] = df['Close'].shift(1)  # Previous day's close
    df['Prev Open'] = df['Open'].shift(1)  # Previous day's open
    df['Prev High'] = df['High'].shift(1)  # Previous day's high
    df['Prev Low'] = df['Low'].shift(1)  # Previous day's low
    df['Prev Volume'] = df['Volume'].shift(1)  # Previous day's volume

    df.dropna(inplace=True)  # Remove any rows with NaN values
    return df

def predict_next_day_close_linear_regression(df):
    df = prepare_features(df)
    
    # Assuming the last row is the most recent day
    X = df[['Prev Close']]  # More features can be added
    y = df['Close']
    
    # Use all data except the last day for training
    X_train, y_train = X[:-1], y[:-1]
    X_last = X[-1:].values.reshape(1, -1)  # Reshape for single prediction
    
    # Initialize and train the Linear Regression model
    model = LinearRegression()
    model.fit(X_train, y_train)
    
    # Predict the next day's close using the most recent data point
    predicted_close = model.predict(X_last)[0]
    return predicted_close

