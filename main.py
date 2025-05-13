# pip install streamlit prophet yfinance plotly pandas
import streamlit as st
from datetime import date, timedelta
import yfinance as yf
from prophet import Prophet
from prophet.plot import plot_plotly
from plotly import graph_objs as go
import pandas as pd

# Define constants
TODAY = date.today().strftime("%Y-%m-%d")
START = (date.today() - timedelta(days=4 * 365)).strftime("%Y-%m-%d")  # Start date is 4 years ago

# Streamlit app title
st.title('Stock Price Prediction App')

# Stock selection
stocks = ('GOOG', 'AAPL', 'MSFT', 'GME')
selected_stock = st.selectbox('Select dataset for prediction', stocks)

# Prediction period (1 year)
n_years = st.slider('Years of prediction:', 1, 4)
period = n_years * 365

# Function to load data
@st.cache_data
def load_data(ticker):
    data = yf.download(ticker, START, TODAY)
    data.reset_index(inplace=True)
    return data

# Load data
data_load_state = st.text('Loading data...')
data = load_data(selected_stock)
data_load_state.text('Loading data... done!')

# Validate data
if data.empty:
    st.error("Failed to fetch data for the selected stock. Please try another stock.")
    st.stop()

# Ensure the 'Date' column is in datetime format
data['Date'] = pd.to_datetime(data['Date'])

# Display raw data
st.subheader('Raw data (Last 4 Years)')
st.write(data.tail())

# Plot raw data
def plot_raw_data():
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=data['Date'], y=data['Close'], mode='lines', name="Stock Close"))
    fig.update_layout(
        title='Stock Close Prices Over Time',
        xaxis_title='Date',
        yaxis_title='Close Price',
        xaxis_rangeslider_visible=True
    )
    st.plotly_chart(fig)

plot_raw_data()

# Prepare data for Prophet
df_train = data[['Date', 'Close']]

# Check for missing or non-numeric values in the 'Close' column
if df_train['Close'].isnull().sum() > 0:
    st.error("The 'Close' column contains missing values. Please try another stock.")
    st.stop()

# Ensure the 'Close' column is numeric
df_train['Close'] = pd.to_numeric(df_train['Close'], errors='coerce')

# Drop rows with missing or invalid values
df_train = df_train.dropna()

# Rename columns for Prophet
df_train = df_train.rename(columns={"Date": "ds", "Close": "y"})

# Train Prophet model
m = Prophet()
m.fit(df_train)

# Make future predictions
future = m.make_future_dataframe(periods=period)
forecast = m.predict(future)

# Filter forecast for the next 1 year
forecast_next_year = forecast[forecast['ds'] > TODAY]

# Display forecast data for the next 1 year
st.subheader('1-Year Forecast Data')
st.write(forecast_next_year[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].head(10))  # Display first 10 rows

# Plot forecast
st.write(f'Forecast plot for the next {n_years} years')
fig1 = plot_plotly(m, forecast)
st.plotly_chart(fig1)

# Plot forecast components
st.write("Forecast components")
fig2 = m.plot_components(forecast)
st.pyplot(fig2)