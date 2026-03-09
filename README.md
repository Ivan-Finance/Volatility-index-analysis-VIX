# Volatility-index-analysis-VIX
A python based study on the correlation between the VIX Index and the S\&P 500 returns to identify market regimes. 

The VIX measures the market's expectations of future volatility for the S\&P 500 over the coming weeks. 

When investors anticipate large price movements, the VIX rises; when markets are calm, the VIX declines. Low values (around 10–15) usually correspond to stable market conditions, where investors expect limited price fluctuations. High values (above 30–40) typically occur during periods of financial stress, when uncertainty about future asset prices increases. 

This project analyzes the historical evolution of the VIX on a daily basis. The analysis focuses on identifying volatility spikes, examining the statistical distribution of daily movements, and observing how the index behaves during periods of market stress. Additional variables such as daily range, returns, moving averages, and realized volatility are constructed to better interpret the dynamics of market uncertainty. 

The goal is to study long-term volatility behavior, identify statistical patterns and anomalies, and understand how financial markets react during crisis periods. 

The dataset used in this project contains daily VIX values from January 2, 1990 to November 14, 2025 and is analyzed using pandas for data manipulation and matplotlib for visualization.

Dataset source: https://github.com/datasets/finance-vix

Work in progress
