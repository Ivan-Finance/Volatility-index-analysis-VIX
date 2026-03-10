# VIX Index Trend Analysis

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

vix = pd.read_csv("vix-daily.csv")

vix.tail()

"""

Open  -> opening value of the index for that day
Close -> closing value of the index for that day
High  -> highest value reached during the day
Low   -> lowest value reached during the day

"""

vix.info()
vix.describe()

"""

The average VIX value is around 19–20, indicating normal or slightly elevated volatility over the long term.
The relatively high standard deviation shows that the index is highly variable and subject to frequent fluctuations.
The median is lower than the mean, indicating a right-skewed distribution. 

"""

vix["CLOSE"].skew()

# New variables

# Intraday volatility
vix['range'] = vix['HIGH'] - vix['LOW']
vix.tail()

# Daily percentage return
vix['ret_close'] = vix['CLOSE'].pct_change()

# Daily logarithmic return
vix['log_ret'] = np.log(vix['CLOSE'] / vix['CLOSE'].shift(1))

# 20-day moving average
vix['ma_20'] = vix['CLOSE'].rolling(20).mean()

# 20-day realized volatility
vix['vol_20'] = vix['CLOSE'].pct_change().rolling(20).std()

vix.tail()


# Sorting
vix_subset = vix[vix['range'] > 5]
vix_subset.head()

vix_sorted = vix.sort_values('CLOSE', ascending=False)
vix_sorted.head()

# Converting daily data to monthly frequency

vix['DATE'] = pd.to_datetime(vix['DATE'])
vix = vix.set_index('DATE')

vix_monthly = vix.resample('ME').last()
vix_monthly.head()

# Realized volatility calculation
vix['rv_10'] = (vix['log_ret']**2).rolling(10).sum()
vix['rv_30'] = (vix['log_ret']**2).rolling(30).sum()

# Volatility ratio calculation
vix['vol_ratio'] = vix['rv_10'] / vix['rv_30']

vix.tail()

"""

Volatility ratio interpretation:

≈ 1   -> recent volatility is similar to past volatility
< 1   -> recent volatility is lower than longer-term volatility
> 1   -> recent volatility is increasing, possibly indicating the start of a market stress phase

"""

# Volatility regimes

def volatility_classification(valore_vix):

    if valore_vix < 15:
        return "Low"
    elif valore_vix < 25:
        return "Mid"
    elif valore_vix < 40:
        return "High"
    else:
        return "Very high"

vix["Regime"] = vix["CLOSE"].apply(volatility_classification)

vix[["CLOSE", "Regime"]].head()

# Graphs

# Historical VIX trend
plt.figure(figsize=(12,5))
plt.plot(vix['CLOSE'])
plt.title('Historical VIX Trend', fontsize=14)
plt.xlabel('Year', fontsize=12)
plt.ylabel('VIX Close value', fontsize=12)
plt.grid(True, linestyle='--', alpha=0.5)
plt.show()

"""

# Major VIX spikes correspond to important financial events:

1997  -> Asian financial crisis
1998  -> Russian default and LTCM collapse risk
2002  -> Dot-com bubble collapse and corporate scandals
2008–2009 -> Global financial crisis and Lehman Brothers failure
2020–2021 -> COVID-19 pandemic and global lockdowns
2024–2025 -> geopolitical tensions and trade conflicts

"""

# Calculating 7-day and 90-day moving averages
vix["MA7"] = vix["CLOSE"].rolling(7).mean()
vix["MA90"] = vix["CLOSE"].rolling(90).mean()

# Graph
plt.figure(figsize=(12,4))
plt.plot(vix["CLOSE"], label="CLOSE", alpha=0.7)
plt.plot(vix["MA7"], label="MA7", alpha=0.9)
plt.plot(vix["MA90"], label="MA90", alpha=0.9)
plt.title("Close and rolling mean)", fontsize=14)
plt.xlabel("Data", fontsize=12)
plt.ylabel("Close", fontsize=12)
plt.legend()
plt.grid(axis='y', linestyle='--', alpha=0.5)
plt.show()

"""

The 7-day moving average highlights short-term fluctuations.
The 90-day moving average smooths noise and shows the medium to long-term trend.
Comparing the close series with moving averages helps identify regime shifts and extreme volatility peaks.

"""

# Return distributions

# Distribution of daily percentage returns
plt.figure(figsize=(10,4))
plt.hist(vix['ret_close'].dropna(), bins=50, edgecolor='black')
plt.title('Distribution of daily percentage returns', fontsize=14)
plt.xlabel('Daily return (%)', fontsize=12)
plt.ylabel('Frequency', fontsize=12)
plt.grid(axis='y', linestyle='--', alpha=0.5)
plt.show()

# Distribution of daily logarithmic returns
plt.figure(figsize=(10,4))
plt.hist(vix['log_ret'].dropna(), bins=50, edgecolor='black')
plt.title('Distribution of daily logarithmic returns', fontsize=14)
plt.xlabel('Daily log return', fontsize=12)
plt.ylabel('Frequency', fontsize=12)
plt.grid(axis='y', linestyle='--', alpha=0.5)
plt.show()

"""

The first histogram shows a right-skewed distribution with a long tail due to extreme movements.
Log returns produce a more symmetric distribution with reduced distortion from extreme values.

"""

# Comparison between standard returns and log returns
plt.figure(figsize=(12,4))
plt.plot(vix["ret_close"], label="ret_close", alpha=0.7)
plt.plot(vix["log_ret"], label="log_ret", alpha=0.7)
plt.title("Comparison between standard returns and log returns", fontsize=14)
plt.xlabel("Date", fontsize=12)
plt.ylabel("Return", fontsize=12)
plt.legend()
plt.grid(axis='y', linestyle='--', alpha=0.5)
plt.show()

# Descriptive statistics
print("\nDescriptive statistics for returns:")
print(vix["ret_close"].describe())

print("\nDescriptive statistics for log returns:")
print(vix["log_ret"].describe())


# Intraday volatility and extreme values

# Comparing daily range and returns
plt.figure(figsize=(10,4))
plt.scatter(vix['range'], vix['ret_close'], alpha=0.8)
plt.title('Daily range and returns comparison')
plt.xlabel('Range')
plt.ylabel('Daily return')
plt.grid(True)
plt.show()

# Volatility ratio

# Comparison between short-term (10-day) and long-term (30-day) volatility
plt.figure(figsize=(12,4))
plt.plot(vix['vol_ratio'], label='Volatility Ratio (RV10/RV30)')
plt.axhline(1, color='red', linestyle='--', label='Soglia 1')
plt.title('Volatility Ratio', fontsize=14)
plt.xlabel('Date', fontsize=12)
plt.ylabel('Volatility Ratio', fontsize=12)
plt.legend()
plt.grid(True, linestyle='--', alpha=0.5)
plt.show()

# Volatility regimes visualization

# Visual representation of volatility regimes
plt.figure(figsize=(12,3))
color_map = {'Low':'green','Mid':'yellow','High':'orange','Very high':'red'}
plt.scatter(vix.index, vix['CLOSE'], c=vix['Regime'].map(color_map), s=10)
plt.title('Volatility regimes visualization', fontsize=14)
plt.xlabel('Date', fontsize=12)
plt.ylabel('Close', fontsize=12)
plt.grid(True, linestyle='--', alpha=0.3)
plt.show()

# # Histogram showing the number of days for each volatility regime
vix['Regime'].value_counts().plot(kind='bar', color=['green','yellow','orange','red'])
plt.title('Number of days for each volatility regime', fontsize=14)
plt.ylabel('Days')
plt.show()

