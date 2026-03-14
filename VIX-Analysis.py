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


# SP500 comparison
# Loading SP500 monthly dataset
sp500 = pd.read_csv(
    r"sp500.csv",
    sep=';',
    decimal=','
)
sp500.columns = sp500.columns.str.strip()
sp500.rename(columns={'Date':'DATE', 'Value':'CLOSE'}, inplace=True)
sp500['DATE'] = pd.to_datetime(sp500['DATE'])
sp500.set_index('DATE', inplace=True)
sp500.index = sp500.index.to_period('M').to_timestamp('M')

print(sp500.head())


vix_monthly_df = vix_monthly[['CLOSE']].rename(columns={'CLOSE':'VIX'})
sp500_df = sp500[['CLOSE']].rename(columns={'CLOSE':'SP500'})
data = pd.concat([vix_monthly_df, sp500_df], axis=1).dropna()

print(data.head())


data['VIX'] = pd.to_numeric(data['VIX'], errors='coerce')
data['SP500'] = pd.to_numeric(data['SP500'], errors='coerce')
data = data.dropna()

data['VIX_ret'] = np.log(data['VIX'] / data['VIX'].shift(1))
data['SP500_ret'] = np.log(data['SP500'] / data['SP500'].shift(1))
data_returns = data[['VIX_ret', 'SP500_ret']].dropna()


# Graph (normalized values) 
plt.figure(figsize=(12,5))
plt.plot(data['SP500']/data['SP500'].iloc[0], label='S&P500')
plt.plot(data['VIX']/data['VIX'].iloc[0], label='VIX')
plt.legend()
plt.grid(True)
plt.show()


# Graph (dual axis)
fig, ax1 = plt.subplots(figsize=(12,5))

ax1.plot(data['SP500'], color='blue', label='S&P500')
ax1.set_ylabel('S&P500', color='blue')
ax1.tick_params(axis='y', labelcolor='blue')

ax2 = ax1.twinx()
ax2.plot(data['VIX'], color='orange', label='VIX')
ax2.set_ylabel('VIX', color='orange')
ax2.tick_params(axis='y', labelcolor='orange')

plt.title('VIX vs S&P500 (dual axis)')
fig.tight_layout()
plt.show()

"""

In this plot, the S&P500 and the VIX are shown together over time, but on separate vertical axes to preserve
their natural scales. The S&P500 values are much larger than the VIX, so plotting them on the same axis
would make the VIX appear almost flat and hide its fluctuations. By assigning the S&P500 to the left
y-axis and the VIX to the right y-axis, each series retains its original range: the S&P500 rises from
a few thousand to several hundred thousand, while the VIX fluctuates between roughly 10 and 60. This
dual-axis approach makes both series fully visible, allowing one to observe the growth of the S&P500
alongside the oscillations of market volatility captured by the VIX, without distorting either series.

""" 

# Monthly log returns graph
plt.figure(figsize=(12,5))
plt.plot(data_returns['SP500_ret'], label='S&P500')
plt.plot(data_returns['VIX_ret'], label='VIX')
plt.title('Monthly log returns: VIX vs S&P500')
plt.xlabel('Date')
plt.ylabel('Log return')
plt.legend()
plt.grid(True)

plt.show()


print(data.head())
print(data.tail())
print(data.describe())
print(data.isna().sum())


# Scatter plot returns graph
plt.figure(figsize=(7,6))
colors = ['green' if r > 0 else 'red' for r in data_returns['SP500_ret']]

plt.scatter(data_returns['SP500_ret'], data_returns['VIX_ret'], 
            c=colors, s=50, alpha=0.6, edgecolors='k')
plt.title('VIX vs S&P500 monthly returns')
plt.xlabel('S&P500 return')
plt.ylabel('VIX return')
plt.grid(True)
plt.show()

"""

The scatter plot shows the relationship between monthly returns of the S&P500 (x-axis) and the VIX
(y-axis). Points are colored green for positive S&P500 months and red for negative months. The
pattern illustrates the typical inverse relationship: the VIX tends to rise when the S&P500 falls
(red points higher) and decline when the S&P500 rises (green points lower). Most points cluster
near the center, reflecting months with moderate returns for both indices, while the overall
rightward tilt shows the historical tendency of the stock market to produce more positive
than negative months.

"""


# Rolling correlation graph (12 months)
rolling_corr = data['SP500'].pct_change().rolling(12).corr(data['VIX'].pct_change())
plt.figure(figsize=(12,4))
plt.plot(rolling_corr)
plt.title('12-Month Rolling Correlation between S&P500 and VIX')
plt.xlabel('Date')
plt.ylabel('Correlation')
plt.grid(True, linestyle='--', alpha=0.5)
plt.show()

"""

The rolling 12-month correlation between the S&P500 and the VIX illustrates the typical inverse relationship
between equity markets and market volatility. Negative values indicate that when the S&P500 rises, the VIX
generally falls, reflecting lower perceived risk and market calm. Strongly negative periods, such as around
2003–2004, 2009, 2014, and 2020, correspond to episodes of market stress or rapid recoveries, where VIX
spikes sharply when the market drops. Positive or near-zero correlations, observed in periods like 1996
or 2018, reflect calmer market phases or temporary deviations from the usual inverse relationship.
Overall, this rolling correlation confirms that the VIX acts as a fear gauge, moving opposite to
the S&P500 in most market conditions.

"""


