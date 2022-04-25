import pandas as pd
import numpy as np
from datetime import datetime
import matplotlib.pyplot as plt
import streamlit as st 
import pandas_datareader as web
import yfinance as yf


# Page Settings
st.set_page_config(
     page_title="Algo Trading",
     page_icon="",
     layout="wide"
 )


# Drop down options for streamlit display
# the bottom one is the default. 
# Having multiple default assets is buggy
tickeroptions = st.multiselect(
     'Select at Least Two Assets - 10B >',
    ['ETH-USD',   'BTC-USD', 'SOL-USD', 'FTT-USD', 'AVAX-USD', 'BNB-USD', 'LINK-USD', 'LUNA1-USD', 'RAY-USD', 'SRM-USD', 'UNI-USD', 'ATLAS-USD', 'POLIS-USD'],
    ['BTC-USD'])


# Downloading pricedata from yahoo finance
# If you change a period and nothing shows up you probably selected an incompatible time period or interval
price_data = yf.download(tickers=tickeroptions, period = '7d', interval = '90m')


# Setting price data to datetime index
price_data.reset_index(level=0, inplace=True)


# Indicators, equations are copied from the interweb
# The ewm() function is used to provide exponential weighted functions.
exp1 = price_data.Close.ewm(span=12, adjust=False).mean()
exp2 = price_data.Close.ewm(span=26, adjust=False).mean()
price_data['MACD'] = exp1-exp2
price_data['Signal Line'] = price_data['MACD'].ewm(span=9, adjust=False).mean()


# Basic Streamlit table.
# You can make this a 'st.dataframe(your dataframe)' which is interactive



# This is the format for making a complex streamlit chart
# Copy paste and input if you need to replicate 
# for more basic charts you can also use st.line_char(your data variable) or st.bar_chart(your data variable)
fig2, ax1 = plt.subplots()
plt.rcParams["figure.figsize"] = (8,3)
ax2 = ax1.twinx()
ax1.plot(price_data['MACD'], label = 'MACD')
ax1.plot(price_data['Signal Line'], label = 'Signal Line')
ax2.plot(price_data.Close, 'g-', label = 'BTC')
ax1.set_xlabel('Intervals')
ax1.set_ylabel(' ')
ax1.legend(loc='upper left')
ax1.axis() 
st.pyplot(fig2)


# Where the magic Happens!
# When you look at the chart you can see when the signal line is < than the MACD line the asset trends upwards
# the last numbers are if true say '1' if false say '0'
price_data['Long'] = np.where( price_data['Signal Line'] < price_data['MACD'], 1, 0 )


# Where the magic Happens!
# When you look at the chart you can see when the signal line is > than the MACD line the asset trends downwards
# the last numbers are if true say '1' if false say '0'
price_data['Short'] = np.where( price_data['Signal Line'] > price_data['MACD'], 1, 0 )


# Very basic equation for returns 
#This equations only works for dataframes. Not with arrays 
price_data['Returns']=price_data['Close'].pct_change()


# Finding returns off we have to multiply the pricedata because we need to exclude instances where our if then statement was negative aka '0'
short_returns= ((price_data['Returns']*-1) * price_data['Short'])
long_returns = (price_data['Returns']) * price_data['Long']


# Finding sums
long_returns=long_returns.sum()
short_returns=short_returns.sum()
total = short_returns + long_returns


# Portfolio value after time period and constant trading within the intervals
total = (total.round(3) +1)
st.metric(value =total, label = 'Portfolio Total')
