
from tensorflow.keras.models import Sequential, load_model
from tensorflow.keras.layers import LSTM, Dense, Dropout
import numpy as np
import pandas as pd
import os
import datetime
import pickle
import re
from sklearn.preprocessing import MinMaxScaler

def predict_price_tensorflow(df, stock_symbol, timeframe, window_size=5):
    # if model is already trained 
    model_path = f"models/{stock_symbol}_{timeframe}_model.h5"
    metadata_path = f"models/{stock_symbol}_{timeframe}_metadata.pkl"

    if os.path.exists(model_path) and os.path.exists(metadata_path):
        model, scaler, last_trained_date = load_model_for_stock(stock_symbol, timeframe)
        if last_trained_date == datetime.datetime.now().date():
            predicted_price = predict_next_day_close(model, df, scaler, window_size)
            return predicted_price

    # Else train the model:
    # Select the relevant features
    features = ['Open', 'High', 'Low', 'Close', 'Volume']
    df_filtered = df[features]

    # Scale the data
    scaler = MinMaxScaler(feature_range=(0, 1))
    scaled_data = scaler.fit_transform(df_filtered)

    # Prepare features and target
    X, y = [], []
    for i in range(window_size, len(scaled_data)):
        X.append(scaled_data[i-window_size:i, :])
        y.append(scaled_data[i, 3])  # 3 corresponds to the 'Close' column
    X, y = np.array(X), np.array(y)

    # Build the LSTM model
    model = Sequential()
    model.add(LSTM(50, return_sequences=True, input_shape=(X.shape[1], X.shape[2])))
    model.add(LSTM(50))
    model.add(Dense(1))
    model.compile(optimizer='adam', loss='mean_squared_error')

    # Train the model
    model.fit(X, y, batch_size=1, epochs=20)
 

    # Save the trained model
    save_model_for_stock(model, scaler, stock_symbol, timeframe)
    # Convert the scaled prediction back to actual price
    predicted_price = predict_next_day_close(model, df_filtered, scaler, window_size)
    return predicted_price



def predict_next_day_close(model, df, scaler, window_size):
    features = ['Open', 'High', 'Low', 'Close', 'Volume']
    last_window = df[features][-window_size:].values

    # Ensure the correct number of features
    if last_window.shape[1] != scaler.n_features_in_:
        raise ValueError(f"Expected {scaler.n_features_in_} features, but got {last_window.shape[1]} features")

    last_window_scaled = scaler.transform(last_window)
    X_pred = last_window_scaled.reshape((1, window_size, last_window.shape[1]))

    predicted_scaled_price = model.predict(X_pred)

    # Directly inverse transform only the "Close" column, which is index 3
    predicted_price_scaled = np.zeros((1, scaler.n_features_in_))
    predicted_price_scaled[0, 3] = predicted_scaled_price
    predicted_price = scaler.inverse_transform(predicted_price_scaled)[0, 3]

    return predicted_price





def sanitize_filename(filename):
    if isinstance(filename, str):
        return re.sub(r'[\/:*?"<>|]', '_', filename)
    else:
        raise ValueError(f"Invalid filename type: {type(filename)}. Expected a string.")

def save_model_for_stock(model, scaler, stock_symbol, timeframe):
    # Ensure stock_symbol is a string
    if not isinstance(stock_symbol, str):
        raise ValueError(f"Invalid stock symbol type: {type(stock_symbol)}. Expected a string.")

    # Create directory if it doesn't exist
    directory = 'models'
    os.makedirs(directory, exist_ok=True)

    # Save the model
    sanitized_symbol = sanitize_filename(stock_symbol)
    file_path = f"{directory}/{sanitized_symbol}_{timeframe}_model.h5"
    model.save(file_path)

    # Save metadata
    save_data = {
        'scaler': scaler,
        'last_trained_date': datetime.datetime.now().date()
    }
    metadata_path = f"{directory}/{sanitized_symbol}_{timeframe}_metadata.pkl"
    with open(metadata_path, 'wb') as f:
        pickle.dump(save_data, f)

def load_model_for_stock(stock_symbol, timeframe):
    file_path = f"models/{stock_symbol}_{timeframe}_model.h5"
    metadata_path = f"models/{stock_symbol}_{timeframe}_metadata.pkl"
    model = load_model(file_path)
    with open(metadata_path, 'rb') as f:
        save_data = pickle.load(f)
    return model, save_data['scaler'], save_data['last_trained_date']
