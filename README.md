# Options Trading Analytics Dashboard

A Streamlit dashboard that generates sample options trading data, calculates portfolio risk metrics, and displays an options analytics dashboard in your browser.

## What It Does

- Generates sample options chain data
- Builds a sample options portfolio
- Calculates Black-Scholes option prices
- Calculates option delta
- Shows portfolio summary, Greeks, volatility smile, put/call ratio, and active option strikes

## Requirements

- Python 3.10 or newer
- pip

## Setup

Install dependencies:

```powershell
python -m pip install -r requirements.txt
```

## Run The App

```powershell
streamlit run app.py
```

Your browser will open the dashboard automatically. If it does not, copy the local URL shown in PowerShell and paste it into your browser.

## Notes

This app currently uses generated sample data. It does not connect to live market data yet.
