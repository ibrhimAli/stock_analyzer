import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error
import numpy as np
import pickle

def prepare_data_random_forest(df):
    # Use lagged values of features as inputs
    df['Prev Close'] = df['Close'].shift(1)
    df['Prev Open'] = df['Open'].shift(1)
    df['Prev High'] = df['High'].shift(1)
    df['Prev Low'] = df['Low'].shift(1)
    df['Prev Volume'] = df['Volume'].shift(1)

    # Drop rows with missing values
    df.dropna(inplace=True)

    # Define features and target
    features = ['Prev Close', 'Prev Open', 'Prev High', 'Prev Low', 'Prev Volume']
    X = df[features]
    y = df['Close']
    return X, y



def train_random_forest(X, y):
    # Split the data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Initialize and train the model
    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)

    # Evaluate the model
    y_pred = model.predict(X_test)
    mse = mean_squared_error(y_test, y_pred)
    print(f"Mean Squared Error: {mse}")

    return model

def predicted_price_random_forest(stock_symbol, timeframe, X, y):

    model_path = f"models/{stock_symbol}_{timeframe}_random_forest.pkl"
    try:
        with open(model_path, 'rb') as f:
            model = pickle.load(f)
    except FileNotFoundError:
        model = train_random_forest(X, y)
        with open(model_path, 'wb') as f:
            pickle.dump(model, f)

    # Make predictions for the latest data
    latest_prediction = model.predict([X.iloc[-1].tolist()])

    return latest_prediction