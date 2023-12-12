# Import necessary libraries
import streamlit as st # Streamlit for creating web applications
import pandas as pd # pandas for data manipulation
import yfinance as yf # yfinance for fetching financial data
import numpy as np # numpy for numerical operations
import matplotlib.pyplot as plt # matplotlib for plotting



# The get_user_input function collects user input for the stock portfolio, including assets and amounts, as well as the starting date for the analysis.
def get_user_input():
    st.title("Portfolio Dashboard")
    # Input for assets (comma-separated) with a default value
    assets = st.text_input("Enter your assets and amounts (comma-separated: AAPL:100, GOOGL:50, MSFT:75)", "AAPL:100, GOOGL:50, MSFT:75")
    # Input for the starting date of the analysis with a default value
    start_date = st.date_input("Pick a starting date for your analysis", pd.to_datetime('2022-06-01'))
    # Split input to separate assets and amounts
    assets_and_amounts = [item.strip().split(':') for item in assets.split(',')]
    # Create separate lists for assets and amounts
    assets_list, amounts_list = zip(*assets_and_amounts)
    # Replace NaN with 0 for any missing values
    amounts = np.nan_to_num(amounts_list).astype(float)
    return assets_list, start_date, amounts

# Function to download stock data and optional benchmark data
def download_data(assets, start_date):
    # Download adjusted close prices for user-provided assets
    data = yf.download(assets, start=start_date)['Adj Close']
    # Attempt to download benchmark data (S&P 500) and handle exceptions
    benchmark_data = None
    try:
        benchmark_data = yf.download('^GSPC', start=start_date)['Adj Close']
    except Exception as e:
        st.warning("Benchmark data not available: " + str(e))
    return data, benchmark_data

# Function to calculate daily returns and cumulative returns of the portfolio
def calculate_returns(data):
    # Calculate daily returns and cumulative returns
    ret_df = data.pct_change()
    cumul_ret = (ret_df + 1).cumprod() - 1
    pf_cumul_ret = cumul_ret.mean(axis=1)
    return ret_df, pf_cumul_ret

# Function to calculate the portfolio standard deviation (risk)
def calculate_portfolio_risk(ret_df, amounts=None):
    # If amounts are not provided, use equal weights
    if amounts is None:
        amounts = np.ones(len(ret_df.columns))
    # Calculate weights based on user-provided or equal amounts
    weights = amounts / sum(amounts)
    # Calculate portfolio standard deviation using the covariance matrix
    pf_std = (weights.dot(ret_df.cov()).dot(weights)) ** (1/2)
    return pf_std

# Function to get user input for the amount of each stock in the portfolio
def get_stock_amounts(assets):
    st.subheader("Enter the Amount of Each Stock")
    # Collect user input for the amount of each stock
    amounts = []
    for asset in assets.split(','):
        amount = st.number_input(f"Amount of {asset.strip()}", min_value=0.0, value=0.0, step=1.0)
        amounts.append(amount)
    # Replace NaN with 0 for any missing values
    amounts = np.nan_to_num(amounts)
    return np.array(amounts)


# Function to plot the portfolio composition as a pie chart
def plot_portfolio_composition(ret_df, amounts, show_chart=True):
    if show_chart:
        # Calculate weights based on user-provided or equal amounts
        weights = amounts / sum(amounts)
        # Create a pie chart with stock labels and percentages
        fig, ax = plt.subplots(facecolor='#ffffff')
        ax.pie(weights, labels=ret_df.columns, autopct='%1.1f%%', textprops={'color': 'black'})
        st.subheader("Portfolio composition")
        st.pyplot(fig)


# Function to plot the portfolio performance against the benchmark (S&P 500)
def plot_portfolio_vs_index(bench_dev, pf_cumul_ret, show_chart=True):
    if show_chart:
        # Combine benchmark and portfolio cumulative returns into a DataFrame
        tog = pd.concat([bench_dev, pf_cumul_ret], axis=1)
        tog.columns = ['S&P500 Performance', 'Portfolio Performance']
        st.subheader("Portfolio Performance vs. S&P500 Performance")
        st.line_chart(data=tog)


# Function to display portfolio risk. display_portfolio_risk function displays the calculated portfolio risk if specified.
def display_portfolio_risk(pf_std, show_risk=True):
    if show_risk:
        st.subheader("Portfolio Risk")
        st.write("Portfolio Risk:", pf_std)



# Main function to orchestrate the entire dashboard
def main():
    # Get user input for assets, start date, and stock amounts
    assets, start_date, amounts = get_user_input()
    # Download stock data and benchmark data
    data, benchmark_data = download_data(assets, start_date)
    # Calculate daily returns and cumulative returns of the portfolio
    ret_df, pf_cumul_ret = calculate_returns(data)
    # Calculate risk with user-provided stock amounts
    pf_std = calculate_portfolio_risk(ret_df, amounts)
    # Checkboxes to enable/disable charts and risk display
    with st.sidebar:
        show_portfolio_composition = st.checkbox("Show Portfolio Composition", True)
        show_portfolio_vs_index = st.checkbox("Show Portfolio vs. Index", True)
        show_portfolio_risk = st.checkbox("Show Portfolio Risk", True)
    # Plot portfolio composition
    plot_portfolio_composition(ret_df, amounts, show_portfolio_composition)
    # If benchmark data is available, compare portfolio performance to S&P 500
    if benchmark_data is not None:
        bench_ret = benchmark_data.pct_change()
        bench_dev = (bench_ret + 1).cumprod() - 1
        plot_portfolio_vs_index(bench_dev, pf_cumul_ret, show_portfolio_vs_index)
    # Display portfolio risk
    display_portfolio_risk(pf_std, show_portfolio_risk)
# Entry point for running the Streamlit app
if __name__ == "__main__":
    main()
