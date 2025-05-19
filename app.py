import streamlit as st
from prophet import Prophet
import pandas as pd
import yfinance as yf
import plotly.graph_objects as go
import auth  

# Initialize user database
auth.init_user_db()

def main_app():
    st.title("Stock Price Prediction Application")
    st.write("""
    This app predicts stock prices for Apple (AAPL), Microsoft (MSFT), Google (GOOGL), Amazon (AMZN), Tesla (TSLA), Reliance (RELIANCE.NS), Tata Motors (TATAMOTORS.NS), Zomato (ZOMATO.NS), and Bajaj Finance (BAJFINANCE.NS) using Facebook's Prophet library.
    """)

    st.sidebar.header("User Input")
    ticker_options = {
        "Apple": "AAPL",
        "Microsoft": "MSFT",
        "Google": "GOOGL",
        "Amazon": "AMZN",
        "Tesla": "TSLA",
        "Reliance": "RELIANCE.NS",
        "Tata Motors": "TATAMOTORS.NS",
        "Bajaj Finance": "BAJFINANCE.NS",
        "Zomato": "ZOMATO.NS"
    }
    selected_company = st.sidebar.selectbox("Select a Company", list(ticker_options.keys()))
    ticker = ticker_options[selected_company]
    period = st.sidebar.slider("Prediction Period (in days)", 30, 365, 120)

    try:
        st.subheader(f"Stock Data for {selected_company} ({ticker})")
        data = yf.download(ticker, period="5y")
        data.reset_index(inplace=True)
        st.write("Last 5 rows of stock data (with Open, Close, and Volume):")
        st.write(data[["Date", "Open", "Close", "Volume"]].tail())

        prophet_data = data[["Date", "Close"]]
        prophet_data.columns = ["ds", "y"]

        model = Prophet()
        model.fit(prophet_data)

        future = model.make_future_dataframe(periods=period)
        forecast = model.predict(future)

        st.subheader(f"Prediction Results for {selected_company} ({ticker})")
        fig1 = model.plot(forecast)
        st.write(fig1)

        st.subheader(f"Interactive Plot for {selected_company} ({ticker})")
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=prophet_data["ds"], y=prophet_data["y"], name="Actual"))
        fig.add_trace(go.Scatter(x=forecast["ds"], y=forecast["yhat"], name="Predicted", line=dict(color="green")))
        fig.update_layout(
            title=f"{selected_company} Stock Price Prediction",
            xaxis_title="Date",
            yaxis_title="Price",
            xaxis_rangeslider_visible=True,
            xaxis=dict(rangeselector=dict(
                buttons=list([
                    dict(count=1, label="1m", step="month", stepmode="backward"),
                    dict(count=6, label="6m", step="month", stepmode="backward"),
                    dict(count=1, label="1y", step="year", stepmode="backward"),
                    dict(step="all")
                ])
            ))
        )
        st.plotly_chart(fig)

        st.subheader("Forecasted Data (Date-Wise Table)")
        forecast["ds"] = pd.to_datetime(forecast["ds"])
        prophet_data["ds"] = pd.to_datetime(prophet_data["ds"])
        merged_data = pd.merge(forecast, prophet_data, on="ds", how="left")
        merged_data = merged_data.rename(columns={"ds": "Date", "y": "Actual Price", "yhat": "Predicted Price"})
        filtered_forecast = merged_data[["Date", "Actual Price", "Predicted Price"]]
        filtered_forecast = filtered_forecast[filtered_forecast["Date"] >= "2024-05-01"]
        st.dataframe(filtered_forecast, height=400)

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

# -login page logic ---
if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False
if "menu" not in st.session_state:
    st.session_state["menu"] = "🔑 Login"

st.sidebar.markdown("## 🚀 Navigation")
menu = st.sidebar.selectbox(
    "Go to",
    options=["🔑 Login", "📝 Register", "📈 App"],
    format_func=lambda x: x.split(" ", 1)[1],
    index=["🔑 Login", "📝 Register", "📈 App"].index(st.session_state["menu"])
)
st.session_state["menu"] = menu

if menu == "🔑 Login":
    auth.login()
elif menu == "📝 Register":
    auth.register()
elif menu == "📈 App":
    if st.session_state.get("logged_in", False):
        main_app()
    else:
        st.markdown(
            "⚠️ Please [log in first](#go-to) using the **Login** page from the sidebar.",
            unsafe_allow_html=True
        )
