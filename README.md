# Options Trading Analytics Dashboard

A Python command-line app that generates sample options trading data, calculates portfolio risk metrics, and prints an options analytics dashboard in the terminal.

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

Clone the repository:

```powershell
git clone https://github.com/miandelco19-lang/my-python-app.git
cd my-python-app
Create a virtual environment:

```powershell
python -m venv .venv
```

Activate it on Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

Install dependencies:

```powershell
pip install -r requirements.txt
```

## Run The App

```powershell
python app.py
```

The dashboard output will appear in your terminal.

## Notes

This app currently uses generated sample data. It does not connect to live market data yet.
