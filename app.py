import logging
from datetime import datetime, timedelta

import numpy as np
import pandas as pd
import streamlit as st
from scipy.stats import norm


class OptionsTradingDashboard:
    def __init__(self):
        logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
        self.logger = logging.getLogger(__name__)
        self.logger.info("Initializing OptionsTradingDashboard")
        self.options_data = self.generate_sample_data()
        self.portfolio = self.generate_sample_portfolio()

    def generate_sample_data(self):
        dates = []
        current_date = datetime.now()
        for i in range(20):
            dates.append(current_date + timedelta(days=i))

        data = []
        for date in dates:
            for strike in [90, 95, 100, 105, 110]:
                price = 100 + np.random.normal(0, 5)
                time_to_expiry = max(1 / 365, (dates[-1] - date).days / 365)
                iv = 0.2 + np.random.normal(0, 0.05)

                call_price = self.black_scholes(price, strike, time_to_expiry, iv, "call")
                put_price = self.black_scholes(price, strike, time_to_expiry, iv, "put")
                call_delta = self.calculate_delta(price, strike, time_to_expiry, iv, "call")
                put_delta = self.calculate_delta(price, strike, time_to_expiry, iv, "put")

                data.append(
                    {
                        "date": date,
                        "underlying_price": round(price, 2),
                        "strike": strike,
                        "expiry": dates[-1],
                        "type": "CALL",
                        "premium": round(call_price, 2),
                        "implied_volatility": round(iv, 3),
                        "delta": round(call_delta, 3),
                        "volume": np.random.randint(100, 1000),
                    }
                )
                data.append(
                    {
                        "date": date,
                        "underlying_price": round(price, 2),
                        "strike": strike,
                        "expiry": dates[-1],
                        "type": "PUT",
                        "premium": round(put_price, 2),
                        "implied_volatility": round(iv, 3),
                        "delta": round(put_delta, 3),
                        "volume": np.random.randint(100, 1000),
                    }
                )

        return pd.DataFrame(data)

    def generate_sample_portfolio(self):
        return pd.DataFrame(
            [
                {
                    "symbol": "AAPL",
                    "position": 5,
                    "option_type": "CALL",
                    "strike": 100,
                    "expiry": datetime.now() + timedelta(days=30),
                    "premium_paid": 3.50,
                    "current_value": 4.20,
                    "delta": 0.55,
                    "pnl": 35.00,
                },
                {
                    "symbol": "TSLA",
                    "position": -3,
                    "option_type": "PUT",
                    "strike": 800,
                    "expiry": datetime.now() + timedelta(days=45),
                    "premium_paid": 25.00,
                    "current_value": 18.50,
                    "delta": -0.42,
                    "pnl": 195.00,
                },
                {
                    "symbol": "GOOGL",
                    "position": 2,
                    "option_type": "CALL",
                    "strike": 2800,
                    "expiry": datetime.now() + timedelta(days=60),
                    "premium_paid": 45.00,
                    "current_value": 52.30,
                    "delta": 0.68,
                    "pnl": 146.00,
                },
                {
                    "symbol": "MSFT",
                    "position": -1,
                    "option_type": "PUT",
                    "strike": 350,
                    "expiry": datetime.now() + timedelta(days=15),
                    "premium_paid": 8.50,
                    "current_value": 6.20,
                    "delta": -0.35,
                    "pnl": 23.00,
                },
            ]
        )

    def black_scholes(self, S, K, T, sigma, option_type):
        d1 = (np.log(S / K) + (0.05 + sigma**2 / 2) * T) / (sigma * np.sqrt(T))
        d2 = d1 - sigma * np.sqrt(T)

        if option_type.lower() == "call":
            price = S * norm.cdf(d1) - K * np.exp(-0.05 * T) * norm.cdf(d2)
        else:
            price = K * np.exp(-0.05 * T) * norm.cdf(-d2) - S * norm.cdf(-d1)

        return max(price, 0)

    def calculate_delta(self, S, K, T, sigma, option_type):
        d1 = (np.log(S / K) + (0.05 + sigma**2 / 2) * T) / (sigma * np.sqrt(T))
        if option_type.lower() == "call":
            return norm.cdf(d1)
        return norm.cdf(d1) - 1

    def portfolio_summary(self):
        total_pnl = self.portfolio["pnl"].sum()
        total_delta = (self.portfolio["delta"] * self.portfolio["position"]).sum()
        total_theta = -0.15 * len(self.portfolio)

        return {
            "total_positions": len(self.portfolio),
            "total_pnl": round(total_pnl, 2),
            "portfolio_delta": round(total_delta, 3),
            "portfolio_theta": round(total_theta, 2),
            "unrealized_gain": round(total_pnl * 0.7, 2),
            "realized_gain": round(total_pnl * 0.3, 2),
        }

    def risk_metrics(self):
        greeks = {"delta": 0, "gamma": 0, "theta": 0, "vega": 0}
        for _, row in self.portfolio.iterrows():
            position = row["position"]
            greeks["delta"] += position * row["delta"]
            greeks["gamma"] += position * 0.04
            greeks["theta"] += position * -0.10
            greeks["vega"] += position * 0.25

        vol_skew = self.options_data.groupby("strike")["implied_volatility"].mean()
        vol_smile = {k: round(v, 3) for k, v in vol_skew.items()}

        return {
            "portfolio_greeks": {k: round(v, 3) for k, v in greeks.items()},
            "volatility_smile": vol_smile,
            "max_loss_scenario": round(-abs(greeks["delta"]) * 100 * 0.1, 2),
            "var_95": round(abs(greeks["delta"]) * 100 * 0.15 * 1.645, 2),
        }

    def market_analysis(self):
        recent_data = self.options_data[self.options_data["date"] == self.options_data["date"].max()]
        put_call_ratio = (
            recent_data[recent_data["type"] == "PUT"]["volume"].sum()
            / recent_data[recent_data["type"] == "CALL"]["volume"].sum()
        )
        avg_iv = recent_data["implied_volatility"].mean()
        most_active = recent_data.groupby(["strike", "type"])["volume"].sum().sort_values(ascending=False).head(3)

        return {
            "put_call_ratio": round(put_call_ratio, 2),
            "average_iv": round(avg_iv, 3),
            "most_active_strikes": most_active.to_dict(),
            "total_volume": int(recent_data["volume"].sum()),
            "iv_percentile": 65 if avg_iv > 0.18 else 35,
        }

    def run_dashboard(self):
        return {
            "portfolio_summary": self.portfolio_summary(),
            "risk_metrics": self.risk_metrics(),
            "market_analysis": self.market_analysis(),
            "data": self.options_data,
            "portfolio": self.portfolio,
        }

    def print_terminal_dashboard(self):
        results = self.run_dashboard()
        summary = results["portfolio_summary"]
        risk = results["risk_metrics"]
        market = results["market_analysis"]

        print("=" * 60)
        print("OPTIONS TRADING ANALYTICS DASHBOARD")
        print("=" * 60)
        print("\nPORTFOLIO SUMMARY:")
        for key, value in summary.items():
            print(f"{key.replace('_', ' ').title()}: {value}")

        print("\nRISK METRICS:")
        for greek, value in risk["portfolio_greeks"].items():
            print(f"{greek.upper()}: {value}")
        print(f"Max 1-day Loss: ${risk['max_loss_scenario']}")
        print(f"95% VaR: ${risk['var_95']}")

        print("\nMARKET ANALYSIS:")
        print(f"Put/Call Ratio: {market['put_call_ratio']}")
        print(f"Average IV: {market['average_iv']}")
        print(f"IV Percentile: {market['iv_percentile']}%")
        print(f"Total Volume: {market['total_volume']:,}")
        print("\nTo open the browser dashboard, run: streamlit run app.py")


def render_streamlit_dashboard():
    st.set_page_config(page_title="Options Trading Analytics Dashboard", layout="wide")
    st.title("Options Trading Analytics Dashboard")
    st.caption("Sample options portfolio analytics powered by Black-Scholes calculations.")

    dashboard = OptionsTradingDashboard()
    results = dashboard.run_dashboard()
    summary = results["portfolio_summary"]
    risk = results["risk_metrics"]
    market = results["market_analysis"]
    options_data = results["data"]
    portfolio = results["portfolio"]

    summary_cols = st.columns(4)
    summary_cols[0].metric("Total Positions", summary["total_positions"])
    summary_cols[1].metric("Total P&L", f"${summary['total_pnl']:,.2f}")
    summary_cols[2].metric("Portfolio Delta", summary["portfolio_delta"])
    summary_cols[3].metric("Portfolio Theta", summary["portfolio_theta"])

    market_cols = st.columns(4)
    market_cols[0].metric("Put/Call Ratio", market["put_call_ratio"])
    market_cols[1].metric("Average IV", market["average_iv"])
    market_cols[2].metric("IV Percentile", f"{market['iv_percentile']}%")
    market_cols[3].metric("Total Volume", f"{market['total_volume']:,}")

    tab_portfolio, tab_risk, tab_market, tab_data = st.tabs(
        ["Portfolio", "Risk Metrics", "Market Analysis", "Raw Data"]
    )

    with tab_portfolio:
        st.subheader("Current Positions")
        st.dataframe(portfolio, use_container_width=True)
        st.subheader("Profit and Loss by Symbol")
        st.bar_chart(portfolio[["symbol", "pnl"]].set_index("symbol"))

    with tab_risk:
        greek_cols = st.columns(4)
        for index, (greek, value) in enumerate(risk["portfolio_greeks"].items()):
            greek_cols[index].metric(greek.upper(), value)

        risk_cols = st.columns(2)
        risk_cols[0].metric("Max 1-Day Loss", f"${risk['max_loss_scenario']:,.2f}")
        risk_cols[1].metric("95% VaR", f"${risk['var_95']:,.2f}")

        vol_smile = pd.DataFrame(
            {
                "strike": list(risk["volatility_smile"].keys()),
                "implied_volatility": list(risk["volatility_smile"].values()),
            }
        ).set_index("strike")
        st.subheader("Volatility Smile")
        st.line_chart(vol_smile)

    with tab_market:
        most_active = pd.DataFrame(
            [
                {"strike": strike, "type": option_type, "volume": volume}
                for (strike, option_type), volume in market["most_active_strikes"].items()
            ]
        )
        st.subheader("Most Active Options")
        st.dataframe(most_active, use_container_width=True)

        daily_volume = options_data.groupby(["date", "type"])["volume"].sum().reset_index()
        daily_volume["date"] = daily_volume["date"].dt.date
        volume_pivot = daily_volume.pivot(index="date", columns="type", values="volume")
        st.subheader("Daily Call and Put Volume")
        st.line_chart(volume_pivot)

    with tab_data:
        st.subheader("Generated Options Chain")
        st.dataframe(options_data, use_container_width=True)


def is_running_with_streamlit():
    try:
        from streamlit.runtime.scriptrunner import get_script_run_ctx

        return get_script_run_ctx() is not None
    except Exception:
        return False


if __name__ == "__main__":
    if is_running_with_streamlit():
        render_streamlit_dashboard()
    else:
        dashboard = OptionsTradingDashboard()
        dashboard.print_terminal_dashboard()
