import streamlit as st
import yfinance as yf
import pandas as pd
import time

# Function to retrieve the live stock prices for a given stock using Yahoo Finance API
def get_live_stock_price(ticker): #ticker, represents the stock symbol
    try: # Tries to execute the following statement
        stock_info = yf.Ticker(ticker) #.Ticker allows us to access ticker data 
        # Retrieves histrotical stock data for defined period
        live_data = stock_info.history(period="1d") 
         # Extracting the last closing prices, which represents the live price
        live_price = live_data['Close'].iloc[-1]
        return live_price # Returns price
    except:
        return None
    
# Main function to orchestrate the entire watchlist
def main():
    st.title('Stock Price Watchlist')# Title for watchlist

    st.sidebar.header('User Input')# Creats sidebar for user input
    # Let the user choose ticker symbol and stores it in variable ticker
    ticker = st.sidebar.text_input('Enter Stock Symbol (e.g., AAPL)', 'AAPL')

    # Fetch live price
    live_price = get_live_stock_price(ticker)

    if live_price is not None:
        st.header(f'Live Stock Price for {ticker}: ${live_price:.2f}')# Shows the live price
    else:
        # If ticker symbol not available gives message
        st.warning(f"Couldn't retrieve live stock price for {ticker}. Please check the ticker symbol.")

    # Display additional information about the stock
    stock_info = yf.Ticker(ticker).info
    st.subheader(f"Additional Information for {ticker}")
    st.write(f"**Company Name:** {stock_info['longName']}")# Company name
    st.write(f"**Exchange:** {stock_info['exchange']}")# Which Exchange
    st.write(f"**Sector:** {stock_info['sector']}")# Sector
    st.write(f"**Industry:** {stock_info['industry']}")# Industry
    st.write(f"**Website:** {stock_info['website']}")# Website

    # Initialize session state
    if 'watchlist_data' not in st.session_state:
        st.session_state.watchlist_data = {'Ticker': [], 'Live Price': []}

    # Allow the user to add the stock to the watchlist
    if st.button('Add to Watchlist'): # Executes if button is clicked
        # Retrieves the current watchlist data stored in the session state.
        watchlist_data = st.session_state.watchlist_data 
        # Appends the ticker to the watchlist
        watchlist_data['Ticker'].append(ticker)
        watchlist_data['Live Price'].append(live_price) # Same for live prices
        # Updates the session state with the modified watchlist data
        st.session_state.watchlist_data = watchlist_data

    # Creating a Pandas DataFrame with the watchlist data
    watchlist_df = pd.DataFrame(st.session_state.watchlist_data)
    st.header('Stock Price Watchlist')
    st.table(watchlist_df.set_index('Ticker'))# Display the table

    # Manually refresh live prices with a button
    if st.button('Refresh Prices'):
        update_live_prices()

# Defining a function to update the prices
def update_live_prices():
    # Update live prices in the watchlist
    watchlist_data = st.session_state.watchlist_data # Retrieving watchlist data
    for i in range(len(watchlist_data['Ticker'])):
        # Retrieves the stock ticker at the current index[i] in the loop
        ticker = watchlist_data['Ticker'][i]
        # Calls the function to get the live prices
        live_price = get_live_stock_price(ticker)
        # Updates the live prices
        watchlist_data['Live Price'][i] = live_price
    # Updates watchlist data    
    st.session_state.watchlist_data = watchlist_data

# The main() function will only be executed, if the scritp runs as the main programm, since the appication has multiple files
if __name__ == '__main__':
    main()










