import streamlit as st

# Custom CSS for styling
st.markdown(
    """
    <style>
    .main-title {
        font-size: 36px;
        font-weight: bold;
        color: #1E88E5; /* Bright blue for the title */
        text-align: center;
        margin-bottom: 20px;
    }
    .sub-title {
        font-size: 24px;
        font-weight: bold;
        color: #ADD8E6; /* Green for subtitles */
        margin-top: 20px;
    }
    .content {
        font-size: 18px;
        color: #FFFFFF; /* White for content text */
        line-height: 1.6;
    }
    .footer {
        font-size: 15px;
        color: #ACFFAC; /* Medium gray for footer */
        text-align: center;
        margin-top: 50px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Welcome page
st.markdown('<div class="main-title">Welcome to the Stock Price Prediction Application</div>', unsafe_allow_html=True)
st.markdown(
    """
    <div class="content">
        This application allows you to predict stock prices for major companies using advanced machine learning techniques.
    </div>
    """,
    unsafe_allow_html=True,
)

st.markdown('<div class="sub-title">Features:</div>', unsafe_allow_html=True)
st.markdown(
    """
    <div class="content">
    - User-Friendly Interface:- Easily select a company and prediction period.<br>
    - Interactive Visualizations:- View actual and predicted stock prices with interactive plots.<br>
    - Comprehensive Data:- Access up to 5 years of historical stock data for analysis.
    </div>
    """,
    unsafe_allow_html=True,
)

st.markdown('<div class="sub-title">Supported Companies:</div>', unsafe_allow_html=True)
st.markdown(
    """
    <div class="content">
    - Apple (AAPL)<br>
    - Microsoft (MSFT)<br>
    - Google (GOOGL)<br>
    - Amazon (AMZN)<br>
    - Tesla (TSLA)<br>
    - Reliance (RELIANCE.NS)<br>
    - Tata Motors (TATAMOTORS.NS)
    </div>
    """,
    unsafe_allow_html=True,
)

st.markdown('<div class="sub-title">Get Started!</div>', unsafe_allow_html=True)
st.markdown(
    """
    <div class="content">
        Click on the sidebar to select a company and start predicting stock prices.
    </div>
    """,
    unsafe_allow_html=True,
)

st.markdown('<div class="footer">Happy Predicting! 🚀</div>', unsafe_allow_html=True)