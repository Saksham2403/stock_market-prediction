import streamlit as st
from prophet import Prophet
import pandas as pd
import yfinance as yf
import plotly.graph_objects as go

# App title
st.title("Stock Price Prediction Application")
st.write("""
This app predicts stock prices for Apple (AAPL), Microsoft (MSFT), Google (GOOGL), Amazon (AMZN), Tesla (TSLA), Reliance (RELIANCE.NS), Tata Motors (TATAMOTORS.NS), Zomato (ZOMATO.NS), and Bajaj Finance (BAJFINANCE.NS) using Facebook's Prophet library.
""")

# Sidebar for user input
st.sidebar.header("User Input")
ticker_options = {
    "Apple": "AAPL",
    "Microsoft": "MSFT",
    "Google": "GOOGL",
    "Amazon": "AMZN",
    "Tesla": "TSLA",
    "Reliance": "RELIANCE.NS",
    "Tata Motors": "TATAMOTORS.NS",
    "Zomato": "ZOMATO.NS",
    "Bajaj Finance": "BAJFINANCE.NS"
}
selected_company = st.sidebar.selectbox("Select a Company", list(ticker_options.keys()))
ticker = ticker_options[selected_company]
period = st.sidebar.slider("Prediction Period (in days)", 30, 365, 120)

# Fetch stock data
try:
    st.subheader(f"Stock Data for {selected_company} ({ticker})")
    # Fetch stock data for the last 5 years
    data = yf.download(ticker, period="5y")
    data.reset_index(inplace=True)

    # Display raw data (last 5 rows with Open, Close, and Volume)
    st.write("Last 5 rows of stock data (with Open, Close, and Volume):")
    st.write(data[["Date", "Open", "Close", "Volume"]].tail())

    # Prepare data for Prophet (only Date and Close are used for prediction)
    prophet_data = data[["Date", "Close"]]
    prophet_data.columns = ["ds", "y"]

    # Train Prophet model
    model = Prophet()
    model.fit(prophet_data)

    # Create future dataframe
    future = model.make_future_dataframe(periods=period)
    forecast = model.predict(future)

    # Plot results
    st.subheader(f"Prediction Results for {selected_company} ({ticker})")
    fig1 = model.plot(forecast)
    st.write(fig1)

    # Interactive Plot with Plotly (Zoom and Slide Enabled)
    st.subheader(f"Interactive Plot for {selected_company} ({ticker})")
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=prophet_data["ds"], y=prophet_data["y"], name="Actual"))
    fig.add_trace(go.Scatter(x=forecast["ds"], y=forecast["yhat"], name="Predicted", line=dict(color="green")))
    fig.update_layout(
        title=f"{selected_company} Stock Price Prediction",
        xaxis_title="Date",
        yaxis_title="Price",
        xaxis_rangeslider_visible=True,  # Enable range slider
        xaxis=dict(rangeselector=dict(  # Add zoom buttons
            buttons=list([
                dict(count=1, label="1m", step="month", stepmode="backward"),
                dict(count=6, label="6m", step="month", stepmode="backward"),
                dict(count=1, label="1y", step="year", stepmode="backward"),
                dict(step="all")
            ])
        ))
    )
    st.plotly_chart(fig)

    # Display forecasted data in a scrollable table
    st.subheader("Forecasted Data (Date-Wise Table)")

    # Ensure 'ds' is in datetime format for both datasets
    forecast["ds"] = pd.to_datetime(forecast["ds"])
    prophet_data["ds"] = pd.to_datetime(prophet_data["ds"])

    # Merge actual prices with forecasted data
    merged_data = pd.merge(forecast, prophet_data, on="ds", how="left")
    merged_data = merged_data.rename(columns={"ds": "Date", "y": "Actual Price", "yhat": "Predicted Price"})

    # Filter data to show only relevant columns and dates from May 2024 onward
    filtered_forecast = merged_data[["Date", "Actual Price", "Predicted Price"]]
    filtered_forecast = filtered_forecast[filtered_forecast["Date"] >= "2024-05-01"]

    # Display the table
    st.dataframe(filtered_forecast, height=400)  # Scrollable table with a fixed height

    # Add links to trusted stock trading platforms
    st.subheader("Proceed to Buy or Sell Stocks")
    st.write("You can buy or sell stocks on trusted platforms. Click the buttons below to proceed:")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("[![Robinhood](https://img.shields.io/badge/Robinhood-Trade-green?style=for-the-badge)](https://robinhood.com)")
    with col2:
        st.markdown("[![E*TRADE](https://img.shields.io/badge/E*TRADE-Trade-blue?style=for-the-badge)](https://us.etrade.com)")
    with col3:
        st.markdown("[![Zerodha](https://img.shields.io/badge/Zerodha-Trade-orange?style=for-the-badge)](https://zerodha.com)")

except Exception as e:
    st.error(f"Error: {e}")
