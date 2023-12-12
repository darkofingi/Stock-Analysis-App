import streamlit as st


# This line configures the page, title and empty icon is beeing created
st.set_page_config(page_title="Mulitpage App", page_icon="")

# Introduction text
st.title("Stock Analysis App")
# Text is written to explain what the App does
st.write(
    "Welcome aboard the Stock Analysis App – your go-to companion for navigating the stock market! Here, simplicity meets power, offering you an array of tools to effortlessly analyze stocks and make informed decisions. \n\nTake a closer look at stock trends using our technical indicators. Whether it's moving averages or the relative strength index (RSI), we've got your back with straightforward insights into market movements. No need for complicated jargon – just clear, actionable information for all levels of investors. \n\nBut we're not stopping there. Our sentimental analysis goes beyond the numbers, giving you a feel for the market's emotions. Understand the vibes, anticipate shifts, and make decisions that align not just with data but also with the pulse of the market. \n\nNavigate through our user-friendly interface, designed to make your investment journey a breeze. Whether you're a seasoned investor or just starting, our app caters to you. \n\nSo, buckle up for a smarter way to invest. Welcome to the Stock Analysis App – where analyzing stocks is simple, decisions are informed, and your investment journey is seamlessly guided. Start exploring and make your moves with confidence!"
)


# Define a function for displaying the Watchlist section
def watchlist_section():
    # Use a Streamlit expander to create a collapsible section with the specified title
    with st.expander("How does the Watchlist work?"):
        # Display information about the Watchlist feature
        st.write("The Watchlist feature allows you to keep track of your favorite stocks. You can add and remove stocks from the watchlist, and it provides a quick overview of the latest information about the stocks you are interested in.")

# Define a function for displaying the Stock Analyzer section
def stock_analyzer_section():
    # Use a Streamlit expander to create a collapsible section with the specified title
    with st.expander("How does the Stock Analyzer work?"):
        # Display information about the Stock Analyzer feature
        st.write("The Stock Analyzer allows you to analyze historical stock data and visualize trends. You can input a stock symbol, select a date range, enable technical indicator and the analyzer will provide you with interactive charts and statistics to help you make informed decisions about the stock.")

# Define a function for displaying the Sentiment Analyzer section
def sentiment_analyzer_section():
    # Use a Streamlit expander to create a collapsible section with the specified title
    with st.expander("How does the Sentiment Analyzer work?"):
        # Display information about the Sentiment Analyzer feature
        st.write("With the Sentiment Analyzer, you can analyze the sentiment of news articles related to two stocks of your choice. Input the names of the two stocks in the provided text boxes. The program will then fetch recent news articles, perform sentiment analysis, and display the mean sentiment score along with the number of articles considered for both stocks. A bar chart is generated to visually compare the mean sentiment scores of the selected stocks.")

# Define a function for displaying the Portfolio Dashboard section
def portfolio_dashboard_section():
    # Use a Streamlit expander to create a collapsible section with the specified title
    with st.expander("How does the Portfolio Dashboard work?"):
        # Display information about the Portfolio Dashboard feature
        st.write("The Portfolio Dashboard allows you to track and manage your investment portfolio. You can add and remove stocks from your portfolio, specify the quantity of each stock, and the dashboard will display the stock allocations of your portfolio in a pie chart. Key metrics such as a comparison of your portfolio with the S&P 500 and the overall portfolio risk are included.")

# Define the main function
def main():
    # Set the title of the Streamlit app to "FAQ"
    st.title("FAQ")

    # Call each section function to display information about different features
    watchlist_section()
    stock_analyzer_section()
    sentiment_analyzer_section()
    portfolio_dashboard_section()

# Check if the script is being run directly (not imported as a module)
if __name__ == "__main__":
    # Call the main function to run the Streamlit app
    main()

