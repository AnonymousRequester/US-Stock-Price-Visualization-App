import pandas as pd
import yfinance as yf
import altair as alt
import streamlit as st

st.title('US Stock Price Visualization App')

st.sidebar.write("""
# GAFA stock prices
This is a stock price visualization tool. 
You can specify the display years and price range from the following options.
""")

st.sidebar.write("""
## Display Years Selection
""")
years = st.sidebar.slider('Years', 1, 20, 10)

st.write(f"""
### GAFA stock prices for the past {years} years.
""")

@st.cache_data
def get_data(yeas, tickers):
    df = pd.DataFrame()
    for company in tickers.keys():
        tkr = yf.Ticker(tickers[company])
        hist = tkr.history(period=f'{years}y')
        hist.index = hist.index.strftime('%d %B %Y')
        hist = hist[['Close']]
        hist.columns = [company]
        hist = hist.T
        hist.index.name = 'Name'
        df = pd.concat([df, hist])
    return df
try:
    st.sidebar.write("""
    ## Specify the stock price range
    """)

    ymin, ymax = st.sidebar.slider('Please specify the range.', 0.0, 3500.0, (0.0, 3500.0))

    tickers = {
        'Google': 'GOOG',
        'Amazon': 'AMZN',
        'Meta': 'META',
        'Apple': 'AAPL',
        'Microsoft': 'MSFT',
        'Netflix': 'NFLX'
    }

    df = get_data(years, tickers)
    companies = st.multiselect(
        'Please select a company name.',
        list(df.index),
        list(df.index)
    )

    if not companies:
        st.error('Please select at least one company.')  
    else:
        data = df.loc[companies]
        st.write("### Stock Prices(USD)", data.sort_index())
        data = data.T.reset_index()
        data = pd.melt(data, id_vars=['Date']).rename(
            columns = {'value': 'Stock Prices(USD)'} 
        )

        chart = (
            alt.Chart(data)
            .mark_line(opacity=0.8, clip=True)
            .encode(
                x="Date:T",
                y=alt.Y("Stock Prices(USD):Q", stack=None, scale=alt.Scale(domain=[ymin, ymax])),
                color='Name:N'
            )
        )
        st.altair_chart(chart, use_container_width=True)
except:
    st.error(
        "Error!"
    )