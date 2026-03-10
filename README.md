# Volatility index (VIX) Analysis with Python
This project analyzes the historical behavior of the VIX (Volatility Index) using Python. The VIX measures market expectations of future volatility for the S&P 500 and is often referred to as the fear index.

When investors anticipate large market movements the VIX rises, while during stable market conditions it tends to decline. Values around 10–15 usually indicate calm markets, while values above 30–40 are typically associated with periods of financial stress.

The analysis focuses on the daily evolution of the VIX, identifying volatility spikes and examining the statistical properties of its movements. Several indicators are constructed to better understand market uncertainty, including:

- daily range (intraday volatility)
- percentage and logarithmic returns
- moving averages
- realized volatility
- volatility ratio

These variables help identify different volatility regimes and highlight periods of extreme market tension.

The dataset contains daily VIX values from January 2, 1990 to November 14, 2025 and is analyzed using pandas for data manipulation and matplotlib for visualization.

* Source: Data was retrieved from [Yahoo Finance](https://github.com/datasets/finance-vix).
* Dataset: The specific CSV file used in this analysis is available [here](./vix-daily.csv).
  
## Visualizations
![VIX Historical Trend](./images/Historical_VIX_Trend.png) 

![Volatility regimes visualization](./images/Volatility_regimes_visualization.png)
