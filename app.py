import streamlit as st
from prophet import Prophet
import pandas as pd
import yfinance as yf
import plotly.graph_objects as go

# App title
st.title("Stock Price Prediction Application")
st.write("""
This app predicts stock prices for Apple (AAPL), Microsoft (MSFT), Google (GOOGL), Amazon (AMZN), Tesla (TSLA), Reliance (RELIANCE.NS), and Tata Motors (TATAMOTORS.NS) using Facebook's Prophet library.
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
    "Tata Motors": "TATAMOTORS.NS"
}
selected_company = st.sidebar.selectbox("Select a Company", list(ticker_options.keys()))
ticker = ticker_options[selected_company]
period = st.sidebar.slider("Prediction Period (in days)", 30, 365, 90)

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

    # Interactive Plot with Plotly
    st.subheader(f"Interactive Plot for {selected_company} ({ticker})")
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=prophet_data["ds"], y=prophet_data["y"], name="Actual"))
    fig.add_trace(go.Scatter(x=forecast["ds"], y=forecast["yhat"], name="Predicted", line=dict(color="green")))
    fig.update_layout(title=f"{selected_company} Stock Price Prediction", xaxis_title="Date", yaxis_title="Price")
    st.plotly_chart(fig)

    # Display forecasted data in a scrollable table
    st.subheader("Forecasted Data (Date-Wise Table)")
    forecast["ds"] = pd.to_datetime(forecast["ds"])  # Ensure 'ds' is in datetime format
    filtered_forecast = forecast[forecast["ds"] >= "2024-05-01"]  # Filter data from May 2024 onward

    # Rename columns for better readability
    filtered_forecast = filtered_forecast.rename(columns={"ds": "Date", "yhat": "Predicted Price"})

    # Display the table
    st.dataframe(filtered_forecast[["Date", "Predicted Price"]], height=400)  # Scrollable table with a fixed height

except Exception as e:
    st.error(f"Error: {e}")