stl_tooltip = """

<h3>Understanding the STL Decomposition Chart</h3>
<p>The STL Decomposition chart presents three key components of your time series data—trend, seasonal, and residual. These components help in analyzing different aspects of the data, providing insights that are crucial for understanding underlying patterns and anomalies in stock prices or other financial metrics.</p>

<h4>What Each Component Represents:</h4>
<ol>
    <li><strong>Trend:</strong> This top subplot shows the trend component of the data. It represents the long-term progression or direction in the data, smoothing out short-term fluctuations. The trend line can help identify upward, downward, or stable trends in stock prices over time. A consistently rising trend might suggest a long-term increase in value, while a declining trend could indicate a decrease.</li>
    <li><strong>Seasonal:</strong> The middle subplot displays the seasonal component. This reflects regular, predictable patterns that repeat over a specific period, such as weekly, monthly, or quarterly cycles. For example, in stock market data, there might be typical end-of-quarter effects or monthly pay cycle impacts. Understanding these patterns can help in predicting when stocks are likely to perform well or poorly based on seasonal trends.</li>
    <li><strong>Residual:</strong> The bottom subplot features the residual component. These are the irregularities or 'noise' left after the trend and seasonal components have been removed from the data. Analyzing residuals can help identify outlying data points that do not fit the general pattern. Large residuals can indicate unexpected events or anomalies, such as a market shock or a significant news event impacting stock prices.</li>
</ol>

<h4>How to Use This Chart:</h4>
<ul>
    <li><strong>Zoom and Explore:</strong> Utilize interactive features to zoom in on specific time periods or details within each component. This can help you examine finer details or specific anomalies more closely.</li>
    <li><strong>Compare Components:</strong> By viewing all three components, you can compare how the underlying trends and seasonal patterns contribute to the observed data. This comparison can be crucial for forecasting and planning based on historical patterns.</li>
    <li><strong>Identify Anomalies:</strong> Pay special attention to unusual patterns in the residual plot, as these can indicate significant deviations from expected behavior. Investigating these anomalies can provide insights into potential risks or opportunities in the market.</li>
    <li><strong>Make Informed Decisions:</strong> Use insights from the trend and seasonal data to inform your investment or financial decisions. For instance, a strong upward trend might support a decision to invest in a particular stock, while significant seasonal dips could suggest optimal buying or selling times.</li>
</ul>

<h4>Tips for Interpreting the Chart:</h4>
<ul>
    <li><strong>Consistency is Key:</strong> Look for consistent patterns in the trend and seasonal plots over multiple cycles or periods, as these are more likely to repeat.</li>
    <li><strong>Context Matters:</strong> Always consider external factors that might influence the residuals, such as economic changes, industry shifts, or global events, which could affect the validity of seasonal and trend predictions.</li>
    <li><strong>Regular Updates:</strong> Regularly update and review the data to ensure that the patterns observed remain relevant and to adjust strategies based on new information.</li>
</ul>

"""

bollinger_tooltip = """
    <div class="chart-description">
    <h3>Understanding the 'Bollinger Bands and Predicted Close' Chart</h3>
    <p>This visualization provides insights into the financial data using Bollinger Bands, the Simple Moving Average (SMA), and trading signals across a time series of stock prices. It includes trends, potential buy/sell opportunities, and a forecasted future closing price.</p>

    <h4>Chart Components:</h4>
    <ul>
        <li><strong>Close Price (Blue Line):</strong> Represents the actual closing prices of the stock over time, crucial for tracking day-to-day movements and the overall trend direction.</li>
        <li><strong>Simple Moving Average (SMA) - Orange Line:</strong> Averages the closing prices over a specified period to identify the trend direction by smoothing out price data.</li>
        <li><strong>Upper and Lower Bollinger Bands (Green and Red Lines):</strong> These bands set the standard deviations away from the SMA, indicating potential upper resistance and lower support levels.
            <ul>
                <li><strong>Band Fill (Grey Area):</strong> The area between the upper and lower bands is shaded to visually represent volatility. The width indicates the volatility level, with wider bands suggesting higher volatility.</li>
            </ul>
        </li>
        <li><strong>Predicted Close (Purple Marker):</strong> Shows the predicted closing price for the next trading day, providing a forecast based on historical data trends.</li>
        <li><strong>Buy and Sell Signals (Green and Red Markers):</strong> Indicate potential buying or selling opportunities based on the Bollinger Band strategy.
            <ul>
                <li><strong>Buy Signal (Green Marker):</strong> Suggests a buying opportunity when the price is low or undervalued.</li>
                <li><strong>Sell Signal (Red Marker):</strong> Indicates a selling point where the stock might be overvalued or expected to decline.</li>
            </ul>
        </li>
        <li><strong>Squeeze Points (Black Markers):</strong> Identified when the bands are notably close, indicating low volatility, which often precedes significant price movements.</li>
    </ul>

    <h4>How to Use This Chart:</h4>
    <ul>
        <li><strong>Trend Analysis:</strong> Evaluate the close price in relation to the SMA and Bollinger Bands to understand the market trend.</li>
        <li><strong>Volatility Assessment:</strong> Use the width of the bands to gauge market volatility and potential upcoming movements.</li>
        <li><strong>Trade Decision Support:</strong> Combine Buy and Sell Signals with other analytical tools to support trading decisions.</li>
        <li><strong>Predictive Insight:</strong> Consider the Predicted Close as a tool for short-term trading strategies, while being mindful of broader market conditions.</li>
    </ul>

    <h4>Tips for Interpreting the Chart:</h4>
    <ul>
        <li><strong>Consistency and Context:</strong> Always use Bollinger Bands in combination with other indicators for a more comprehensive analysis.</li>
        <li><strong>Responsive Strategy:</strong> Adapt strategies to reflect sudden market changes or during periods of unexpected volatility.</li>
        <li><strong>Regular Updates and Review:</strong> Continuously update and review your analytical approaches to align with current market conditions.</li>
    </ul>
</div>

"""

stochastic_tooltip = """
<div class="chart-description">
    <h3>Understanding the 'Stochastic Oscillator with Signals' Chart</h3>
    <p>This chart displays the Stochastic Oscillator, a momentum indicator that compares a particular closing price of a security to a range of its prices over a certain period of time. The oscillator is used to generate overbought and oversold trading signals, represented by two lines: %K (the stochastic line) and %D (the signal line).</p>

    <h4>Key Components:</h4>
    <ul>
        <li><strong>%K Line (Blue):</strong> This line represents the current value of the stochastic indicator. It's calculated based on the latest closing prices and shows the momentum of the price as it compares to the highs/lows over a given period.</li>
        <li><strong>%D Line (Orange):</strong> This line is the simple moving average of the %K line. It acts as a trigger line for buy or sell signals.</li>
        <li><strong>Buy Signals (Green Markers):</strong> These are shown when the %K line crosses up through the %D line while below the oversold level (20), suggesting a potential upward movement in price.</li>
        <li><strong>Sell Signals (Red Markers):</strong> These occur when the %K line crosses down through the %D line while above the overbought level (80), indicating a potential downward movement in price.</li>
    </ul>

    <h4>Important Levels:</h4>
    <ul>
        <li><strong>Oversold Line:</strong> Drawn at 20, it indicates that the security may be getting oversold and could be gearing up for an upward reversal.</li>
        <li><strong>Overbought Line:</strong> Drawn at 80, it suggests that the security might be overbought and could be preparing for a price decline.</li>
    </ul>

    <h4>How to Use This Chart:</h4>
    <ul>
        <li><strong>Identifying Market Trends:</strong> Observing where the lines intersect can help predict the short-term direction of the market prices.</li>
        <li><strong>Trading Decisions:</strong> Buy when the %K line crosses above the %D line from below 20 as it indicates buying pressure. Sell when the %K line crosses below the %D line from above 80 as it signals selling pressure.</li>
        <li><strong>Confirmation with Other Indicators:</strong> While stochastic signals can be powerful, they should ideally be used in conjunction with other indicators and analysis techniques to confirm trading signals.</li>
    </ul>

    <h4>Tips for Interpreting the Chart:</h4>
    <ul>
        <li><strong>Watch for False Signals:</strong> Sometimes, the stochastic oscillator can produce false signals particularly in volatile markets; hence, always seek confirmation from other sources.</li>
        <li><strong>Avoid Overtrading:</strong> Overrelying on stochastic signals for frequent trading can lead to significant transaction costs and risks. It's essential to use these signals as part of a broader strategy.</li>
        <li><strong>Regular Review:</strong> Regularly review your strategies and keep yourself updated with market conditions that can affect the effectiveness of these indicators.</li>
    </ul>
</div>


"""
