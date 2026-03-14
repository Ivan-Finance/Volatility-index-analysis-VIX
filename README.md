# 📉 VIX Analysis & S&P500 Comparison
**A quantitative study of market volatility and equity behavior using Python.**

This project analyzes the CBOE Volatility Index (VIX) from 1990 to 2025 and compares it with the S&P500 to identify volatility regimes and their interaction with the stock market.

## Key Analyses
- **Volatility Regimes:** Classification of market states (Calm vs. Stress) using thresholds on the VIX.
- **Returns & Dynamics:** Daily and monthly log returns, intraday ranges, and realized volatility capture market fluctuations.
- **Trend Smoothing:** Moving averages highlight long-term trends and filter noise.
- **S&P500 Comparison:** Monthly VIX and S&P500 returns are analyzed, showing the typical inverse relationship; dual-axis plots preserve scale for visual clarity.
- **Correlation:** 12-month rolling correlation quantifies how the VIX reacts to stock market movements over time.

## Visualizations
<p align="center">
  <img src="./images/Historical_VIX_Trend.png" width="700">
</p>

<p align="center">
  <img src="./images/Volatility_regimes_visualization.png" width="1000">
</p>

<p align="center">
  <img src="./images/vix_vs_sp500.jpeg" width="700">
</p>

<p align="center">
  <img src="./images/monthly_returns.jpeg" width="700">
</p>

## Data & Sources

### VIX
- **Source:** CBOE Volatility Index time series available on [GitHub finance-vix dataset](https://github.com/datasets/finance-vix). 
- **Dataset file used in this project:** is available [here](./vix-daily.csv).

### S&P500
- **Source:** S&P 500 index historical monthly data on [Macrotrends](https://www.macrotrends.net/2324/sp-500-historical-chart-data#google_vignette).  
- **Dataset file used in this project:**  is available [here](./sp500.csv).
