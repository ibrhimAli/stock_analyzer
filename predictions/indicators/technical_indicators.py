import pandas as pd
import pandas_ta as ta
import numpy as np

def add_technical_indicators(df, short_window=30, long_window=180):
    # Add moving averages directly using pandas_ta functions
    df['SMA_30'] = ta.sma(df['Close'], length=short_window)
    df['EMA_30'] = ta.ema(df['Close'], length=long_window)

    # Add RSI
    df['RSI'] = ta.rsi(df['Close'], length=14)

    # Add MACD
    macd = ta.macd(df['Close'], fast=12, slow=26, signal=9)
    if isinstance(macd, pd.DataFrame):  # Ensure macd is a DataFrame
        df = pd.concat([df, macd], axis=1)

    # Add Bollinger Bands
    bbands = ta.bbands(df['Close'], length=20, std=2)
    if isinstance(bbands, pd.DataFrame):  # Ensure bbands is a DataFrame
        df = pd.concat([df, bbands], axis=1)

    return df

#---------------
#   Bollinger
#---------------
def calculate_bollinger_bands(df, window=20, num_std_dev=2):
    df['SMA'] = df['Close'].rolling(window=window).mean()
    df['StdDev'] = df['Close'].rolling(window=window).std()
    df['Upper Band'] = df['SMA'] + num_std_dev * df['StdDev']
    df['Lower Band'] = df['SMA'] - num_std_dev * df['StdDev']
    buy_signals = []
    sell_signals = []
    for i in range(len(df)):
        if df['Close'].iloc[i] < df['Lower Band'].iloc[i]:  # Condition to buy
            buy_signals.append(df['Close'].iloc[i])
            sell_signals.append(np.nan)
        elif df['Close'].iloc[i] > df['Upper Band'].iloc[i]:  # Condition to sell
            sell_signals.append(df['Close'].iloc[i])
            buy_signals.append(np.nan)
        else:
            buy_signals.append(np.nan)
            sell_signals.append(np.nan)
    df['Buy'] = buy_signals
    df['Sell'] = sell_signals
    return df


def predict_next_day_bollinger(df, close):
    last_row = df.iloc[-1]
    ##sma = last_row['SMA']
    upper_band = last_row['Upper Band']
    lower_band = last_row['Lower Band']

    print("hellllllllllllllllllllllllllllooooooooooooooooooooooooo", close, upper_band)
    if close > upper_band:
        # Overbought - predict a lower price
        color = 'red'
        predicted_price = "Sell"
    elif close < lower_band:
        # Oversold - predict a higher price
        color = 'green'
        predicted_price = "Buy"
    else:
        # Within the bands - predict the average (neutral)
        color = 'gray'
        predicted_price = "Hold"

    return predicted_price, color

#---------------
#   Stochastic
#---------------
def calculate_stochastic_oscillator(df, period=14, d_period=3):
    if len(df) < max(period, d_period):
        raise ValueError("Not enough data to calculate the Stochastic Oscillator")
    
    df['Low'] = df['Low'].rolling(window=period).min()  # Adjust to use actual low prices
    df['High'] = df['High'].rolling(window=period).max()  # Adjust to use actual high prices
    df['%K'] = 100 * (df['Close'] - df['Low']) / (df['High'] - df['Low'])
    df['%D'] = df['%K'].rolling(window=d_period).mean()
    return df


def stochastic_signal(df):
    latest = df.iloc[-1]
    previous = df.iloc[-2]
    
    crossover_up = (latest['%K'] > latest['%D']) and (previous['%K'] <= previous['%D'])
    crossover_down = (latest['%K'] < latest['%D']) and (previous['%K'] >= previous['%D'])
    
    if latest['%K'] > 80 and crossover_down:
        color = 'red'
        sell_buy = "Sell"
    elif latest['%K'] < 20 and crossover_up:
        color = 'green'
        sell_buy = "Buy"
    else:
        color = 'gray'
        sell_buy = "Hold"
    
    percent_k = df['%K'].iloc[-1]
    percent_d = df['%D'].iloc[-1]    
    return sell_buy, color, percent_k, percent_d


#---------------
#   ATR
#---------------
def calculate_atr(df, window=14):
    df['High-Low'] = df['High'] - df['Low']
    df['High-Close'] = np.abs(df['High'] - df['Close'].shift(1))
    df['Low-Close'] = np.abs(df['Low'] - df['Close'].shift(1))

    df['True Range'] = df[['High-Low', 'High-Close', 'Low-Close']].max(axis=1)
    df['ATR'] = df['True Range'].rolling(window=window).mean()

    df.drop(['High-Low', 'High-Close', 'Low-Close'], axis=1, inplace=True)
    return df

def determine_stop_loss(entry_price, atr_value, atr_multiple=2):
    stop_loss = entry_price - atr_multiple * atr_value
    return stop_loss

def make_trading_decision(df, current_price, atr_multiple=2):
    latest_atr = df['ATR'].iloc[-1]
    entry_price = current_price

    # Set stop-loss
    stop_loss = determine_stop_loss(entry_price, latest_atr, atr_multiple)

    # Simple example decision: buy if the current price is within a certain range of the entry price
    # You can customize this logic based on your strategy
    if current_price <= entry_price + latest_atr and current_price >= entry_price - latest_atr:
        color = 'green'
        decision = "Buy"
    else:
        color = 'gray'
        decision = "Hold"

    return decision, stop_loss, color

#---------------
#   OBV
#---------------
def calculate_obv(df):
    df['OBV'] = np.nan
    df['OBV'] = df['Volume'].where(df['Close'] > df['Close'].shift(1), -df['Volume']).cumsum()
    df['OBV'].fillna(method='ffill', inplace=True)
    return df


def identify_obv_divergence(df, window=5):
    recent_close = df['Close'].iloc[-window:]
    recent_obv = df['OBV'].iloc[-window:]

    close_trend = np.polyfit(range(len(recent_close)), recent_close, 1)[0]
    obv_trend = np.polyfit(range(len(recent_obv)), recent_obv, 1)[0]

    if close_trend > 0 and obv_trend < 0:
        return "Bearish Divergence"
    elif close_trend < 0 and obv_trend > 0:
        return "Bullish Divergence"
    else:
        return "No Divergence"


def make_obv_decision(df):
    divergence = identify_obv_divergence(df)
    if divergence == "Bullish Divergence":
        sell_buy = "Buy"
        color = 'green'
    elif divergence == "Bearish Divergence":
        sell_buy = "Sell"
        color = 'red'
    else:
        sell_buy = "Hold"
        color = 'gray'
    return sell_buy, color


#---------------
#   Fibonacci
#---------------
def calculate_fibonacci_levels(df, predicted_close=None):
    max_price = df['Close'].max()
    min_price = df['Close'].min()

    if predicted_close is not None:
        max_price = max(max_price, predicted_close)
        min_price = min(min_price, predicted_close)

    diff = max_price - min_price

    levels = {
        '23.6%': max_price - 0.236 * diff,
        '38.2%': max_price - 0.382 * diff,
        '50.0%': max_price - 0.5 * diff,
        '61.8%': max_price - 0.618 * diff,
        '100.0%': min_price
    }

    return levels

def decide_on_fibonacci_levels(df, predicted_close):
    levels = calculate_fibonacci_levels(df, predicted_close)

    current_price = df['Close'].iloc[-1]

    # Decide based on the closest Fibonacci level to the predicted close
    if predicted_close:
        closest_level = min(levels.items(), key=lambda x: abs(x[1] - predicted_close))
        if predicted_close > closest_level[1]:
            return f"Next predicted close ({predicted_close:.2f}) suggests a potential sell above {closest_level[0]} retracement level", "red", levels
        else:
            return f"Next predicted close ({predicted_close:.2f}) suggests a potential buy below {closest_level[0]} retracement level", "green", levels

    return "Hold", "gray", levels



