import pandas as pd
from ..utils.load_data import load_data
from .technical_indicators import *
from ..charts.price import create_price_chart
from ..charts.rsi import create_rsi_chart
from ..charts.bollinger import plot_bollinger_bands
from ..charts.stochastic_oscillator import plot_stochastic_signals
from ..charts.average_true_range import *
from ..charts.plotting_obv import *
from ..charts.fibonacci_levels import *
from ..utils.plotToHtml import plot_to_html
from ..charts.stl import *
from .linear_regression_predict_price import predict_next_day_close_linear_regression
from .tensorflow_predict_price import predict_price_tensorflow
from .random_forest import *
from .gradient_boost import *
from .armia import *
from ..utils.openai import *
from ..utils.llama3 import *
from ..utils.seasonal_time_series import *
from ..utils.tooltips import *

def indicators_result(filepath, timeframe, stock_symbol):
     # First load the data and insert headers
    df = load_data(filepath)

    original_df = df.copy()
    # Predict next day close using linear regression 
    # Linear regression require a lot of data
    next_day_close_linear_regression = predict_next_day_close_linear_regression(df)

    # 2. Calculate the time frame
    if timeframe == 'short':
        window_settings = {'short_window': 15, 'long_window': 45}  # Example settings for short-term
        df = df.tail(45)
    elif timeframe == 'medium':
        window_settings = {'short_window': 30, 'long_window': 90}
        df = df.tail(90)
    else:  # Long term
        window_settings = {'short_window': 60, 'long_window': 180}
        df = df.tail(180)

    print("shape++++++++++++++++++++++++++++++++++++++++++++++++++++", df.shape)
    arima_df = df.copy()

    # Predict price close using TensorFlow
    next_day_close_tensorflow = predict_price_tensorflow(df, stock_symbol, timeframe)

    # 3. Run the indicators with the time frames
    df = add_technical_indicators(df, **window_settings)

     # Create plots
    price_chart = create_price_chart(df)
    rsi_chart = create_rsi_chart(df)

    # Convert plots to HTML
    price_chart_html = plot_to_html(price_chart)
    rsi_chart_html = plot_to_html(rsi_chart)

    last_close = df['Close'].iloc[-1]
    percent_change_tensorflow = ((next_day_close_tensorflow - last_close) / last_close) * 100
    tensorflow_color = get_color_for_percantage(percent_change_tensorflow)
    percent_change_linear_regrission = ((next_day_close_linear_regression - last_close) / last_close) * 100
    linear_regression_color = get_color_for_percantage(percent_change_linear_regrission)

    # Stochastic oscillator
    df = calculate_stochastic_oscillator(df)
    stochastic_buy_sell, stochastic_color, stochastic_percent_k, stochastic_percent_d = stochastic_signal(df)
    stochastic_chart = plot_stochastic_signals(df)


    # Average true range
    df = calculate_atr(df)
    atr_buy_sell, atr_stop_lose, atr_color = make_trading_decision(df, last_close)
    atr_chart = plot_atr(df)

    # On-Balance Volume 
    df = calculate_obv(df)
    obv_buy_sell, obv_color = make_obv_decision(df)
    obv_chart = plot_obv(df)

    # Fibonacci
    fib_buy_sell, fib_color, fib_levels = decide_on_fibonacci_levels(df, next_day_close_tensorflow)
    fib_chart = plot_fibonacci_levels(df, fib_levels, next_day_close_tensorflow)

    # Random Forest
    X, y = prepare_data_random_forest(original_df)
    random_forest_predicted_price= predicted_price_random_forest(stock_symbol, timeframe, X, y)
    random_forest_percent_change = ((random_forest_predicted_price - last_close) / last_close) * 100
    random_forest_color = get_color_for_percantage(random_forest_percent_change)

    # Gradient Boosting
    X, y = gradient_boost_prepare_data(original_df)
    gradient_boost_predicted_price= gradient_boosting_predicted_price(stock_symbol, timeframe, X, y)
    gradient_boost_percent_change = ((gradient_boost_predicted_price - last_close) / last_close) * 100
    gradient_boost_color = get_color_for_percantage(gradient_boost_percent_change)


    # ARIMA
    arima_model = train_arima_model(arima_df)
    arima_next_day_close = predict_next_day_close_arima(arima_model)
    arima_percent_change = ((arima_next_day_close - last_close) / last_close) * 100
    arima_color = get_color_for_percantage(arima_percent_change)

    #bollinger bands
    df = calculate_bollinger_bands(df)
    bollinger_buy_sell, bollinger_color = predict_next_day_bollinger(df, next_day_close_tensorflow)
    bollinger_chart = plot_bollinger_bands(df, next_day_close_tensorflow)

    ## Generate summary:
    input_to_openai = (
        f"For {stock_symbol} in EGX market, the output from models and indicators was as follows:\n"
        f"    LinearRegression next_close_price {next_day_close_linear_regression}, percentage {percent_change_linear_regrission}.\n"
        f"    Tensorflow next_close_price {next_day_close_tensorflow}, percentage {percent_change_tensorflow}.\n"
        f"    RandomForest next_close_price {random_forest_predicted_price}, percentage {random_forest_percent_change}.\n"
        f"    GradientBoosting next_close_price {gradient_boost_predicted_price}, percentage {gradient_boost_percent_change}.\n"
        f"    Autoregressive Integrated Moving Average (ARIMA) next_close_price {arima_next_day_close}, percentage {arima_percent_change}."
        f"Should I buy or sell and explain in details?"
    )
    summary = ''
    #summary = summarize_output(input_to_openai)
    #summary = summarize_with_llama3(input_to_openai)


    ## Seasonal Timer Series
    trend, seasonal, resid = decompose_time_series(original_df, 12)
    stl_chart = plot_stl_decomposition(trend, seasonal, resid, original_df.index)

    ## build models object

    context = {
        'symbol': stock_symbol,
        'summary': summary,
        'last_close_price': last_close,
        'linear_regression': {
            'percentage': percent_change_linear_regrission,
            'price': next_day_close_linear_regression,
            'color': linear_regression_color
        },
        'tensorflow': {
            'price': next_day_close_tensorflow,
            'percentage': percent_change_tensorflow,
            'color': tensorflow_color
        },
        'rf': {
            'price': random_forest_predicted_price,
            'percentage': random_forest_percent_change,
            'color': random_forest_color
        },
        'gs': {
            'price': gradient_boost_predicted_price,
            'percentage': gradient_boost_percent_change,
            'color': gradient_boost_color
        },
        'arima': {
           'price': arima_next_day_close,
            'percentage': arima_percent_change,
            'color': arima_color
        },
        'bollinger':{
            'buy_sell': bollinger_buy_sell,
            'chart': bollinger_chart,
            'color': bollinger_color,
            'description': bollinger_tooltip
        },
        'stl':{
            'buy_sell': bollinger_buy_sell,
            'chart': stl_chart,
            'color': bollinger_color,
            'description': stl_tooltip
        },
        'stochastic': {
            'buy_sell': stochastic_buy_sell,
            'color': stochastic_color,
            'percent_k': stochastic_percent_k,
            'percent_d': stochastic_percent_d,
            'chart': stochastic_chart
        },
        'atr': {
            'buy_sell': atr_buy_sell,
            'stop_lose': atr_stop_lose,
            'color': atr_color,
            'chart': atr_chart
        },
        'obv': {
            'buy_sell': obv_buy_sell,
            'color': obv_color,
            'chart': obv_chart
        },
        'fib': {
            'buy_sell': fib_buy_sell,
            'color': fib_color,
            'chart': fib_chart
        },
        'price_chart': price_chart_html,
        'rsi_chart': rsi_chart_html,
        'price_chart_explanation': 'This chart shows the closing price of the stock over time.',
        'rsi_chart_explanation': 'RSI values above 70 indicate overbought conditions, while values below 30 indicate oversold conditions.'
    }


    return context
    

def get_color_for_percantage(percntage):
    if (percntage >= 0):
        color = 'green'
    else:
        color = 'red'
    return color