# Import necessary libraries
import streamlit as st # Streamlit for creating web applications
import yfinance as yf # yfinance for fetching financial data
import pandas as pd # pandas for data manipulation
import plotly.graph_objects as go # plotly.graph_objects for creating interactive plots
import plotly.express as px # plotly.express for easy plotting

# Function named get_live_stock_price which retrieve the live stock prices for a given stock using Yahoo Finance API
def get_live_stock_price(ticker): # Defines the function (get_live_stock_price) that takes one argument, ticker
    try: # Tries to fetch historical stock data for the specified symbol using yfinance
        stock_info = yf.Ticker(ticker) # Creates a yfinance.Ticker object for the given stock symbol
        live_data = stock_info.history(period="1d") # Retrieves historical stock data for the last day (period="1d")
        live_price = live_data['Close'].iloc[-1] # Extracts the closing price of the last data point, considering it as the "live" price
        return live_price # Returns the live stock price if successful.
    except: # Initiates an exception block to handle errors
        return None #Returns None in case of an exception, providing a graceful error handling mechanism

# Defines a function named get_stock_data taking a stock symbol, start date, and end date as arguments
def get_stock_data(stock_symbol, start_date, end_date):
    # If start date and end date are the same, use live data
    if start_date == end_date:
        # Retrieves live stock price using the get_live_stock_price function
        live_price = get_live_stock_price(stock_symbol)
        # If live data is available, creates a DataFrame with the live price for a single date
        if live_price is not None:
            live_data = pd.DataFrame({'Close': [live_price]}, index=pd.to_datetime([start_date]))
            return live_data
        # If unable to retrieve live data, displays an error message and returns None
        else:
            st.error(f"Error retrieving live data for {stock_symbol}")
            return None
    else:
        # Uses historical data for the specified date range using yfinance's download function
        stock_data = yf.download(stock_symbol, start=start_date, end=end_date)
        return stock_data
    
# Function is beeing defined where the stock_data is beeing plotted
def plot_stock_chart(stock_data, indicators):
    fig = go.Figure() # Adds a ploty figure

    # Plot stock price as a line chart
    fig.add_trace(go.Scatter(x=stock_data.index, y=stock_data['Close'], mode='lines', name='Stock Price'))

    # Add indicators if selected
    for indicator in indicators:
        # If the current indicator is 'SMA', it calculates the 20-day Simple Moving Average (SMA) of the closing prices 
        if indicator == 'SMA':
            fig.add_trace(go.Scatter(x=stock_data.index, y=stock_data['Close'].rolling(window=20).mean(), mode='lines', name='SMA'))
        # If the current indicator is 'RSI', it calculates the Relative Strength Index (RSI) using a function called calculate_rsi and adds a line trace for RSI to the Plotly figure.
        elif indicator == 'RSI':
            rsi = calculate_rsi(stock_data['Close'])
            fig.add_trace(go.Scatter(x=stock_data.index, y=rsi, mode='lines', name='RSI'))
        # Similar to above
        elif indicator == 'MACD':
            macd, signal_line = calculate_macd(stock_data['Close'])
            fig.add_trace(go.Scatter(x=stock_data.index, y=macd, mode='lines', name='MACD'))
            fig.add_trace(go.Scatter(x=stock_data.index, y=signal_line, mode='lines', name='Signal Line'))
  
    return fig

# Defines the function to calculate the RSI. It takes a series of closing prices, calculates the gains and losses, computes the average gains and losses over a specified window, and then calculates the Relative Strength (RS) and RSI based on the provided formula. The resulting RSI values are returned as a Pandas Series
def calculate_rsi(close_prices, window=14):
    delta = close_prices.diff(1)
    gain = delta.where(delta > 0, 0)
    loss = -delta.where(delta < 0, 0)

    avg_gain = gain.rolling(window=window, min_periods=1).mean()
    avg_loss = loss.rolling(window=window, min_periods=1).mean()

    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))

    return rsi


# This function (calculate_macd) calculates the Moving Average Convergence Divergence (MACD) and 
# its signal line based on the stock's closing prices. It involves exponential 
# moving averages (EMAs) and their differences.
def calculate_macd(close_prices, short_window=12, long_window=26, signal_window=9):
    short_ema = close_prices.ewm(span=short_window, adjust=False).mean()
    long_ema = close_prices.ewm(span=long_window, adjust=False).mean()

    macd = short_ema - long_ema
    signal_line = macd.ewm(span=signal_window, adjust=False).mean()

    return macd, signal_line


# This function (plot_volume_chart) creates a Plotly bar chart for the stock's volume with a specified height.
def plot_volume_chart(stock_data, volume_height):
    fig = px.bar(stock_data, x=stock_data.index, y='Volume', labels={'Volume': 'Volume'})
    fig.update_layout(height=volume_height)
    return fig


# This function main function sets up the Streamlit web application, including a title, input parameters in 
# the sidebar, and a main page displaying the stock price chart and volume chart.
def main():
    st.title('Price Chart')

    # Creating the Sidebar
    st.sidebar.header('Input Parameters') # Creating the header for the sidebar with the str(Input Parameters)
    stock_symbol = st.sidebar.text_input('Enter Stock Symbol (e.g., AAPL)', 'AAPL')# Getting the user input as str() and let him enter a stock symbol
    start_date = st.sidebar.date_input('Start Date', pd.to_datetime('2020-01-01')) # This lets the user choose a start Date where the chart starts, pandas was used here for datetime
    end_date = st.sidebar.date_input('End Date', pd.to_datetime('2023-01-01'))# Same as above only difference is we let user choose End Date
    indicators = st.sidebar.multiselect('Indicators', ['SMA', 'RSI', 'MACD']) # This sidebar input let the user choose an Analysis 
    
    # Additional inputs for volume chart size, via slider. user can shoose the height oft the volume chart
    volume_height = st.sidebar.slider('Volume Chart Height', min_value=200, max_value=1000, value=200)

    # Gets stock data, with the inputs from the user in the sidebar
    stock_data = get_stock_data(stock_symbol, start_date, end_date)

    # Checks if stock_data is not None 
    if stock_data is not None:
        # Main page
        chart_height = 600  # Set a fixed height for the main price chart and plots it using Streamlit
        st.plotly_chart(plot_stock_chart(stock_data, indicators).update_layout(height=chart_height),
                        use_container_width=True)

        # Volume chart is plotted using Plotly
        st.plotly_chart(plot_volume_chart(stock_data, volume_height), use_container_width=True)


# The main() function will only be executed, if the scritp runs as the main programm, since the appication has multiple files.
if __name__ == '__main__':
    main()




