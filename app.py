import numpy as np
import pandas as pd
from datetime import datetime, timedelta
from scipy.stats import norm
import logging

class OptionsTradingDashboard:
    def __init__(self):
        logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
        self.logger = logging.getLogger(__name__)
        self.logger.info("Initializing OptionsTradingDashboard")
        try:
            self.options_data = self.generate_sample_data()
            self.logger.info("Sample options data generated successfully")
            self.portfolio = self.generate_sample_portfolio()
            self.logger.info("Sample portfolio generated successfully")
        except Exception as e:
            self.logger.error(f"Error during initialization: {e}")
            raise
        
    def generate_sample_data(self):
        self.logger.info("Generating sample options data")
        try:
            dates = []
            current_date = datetime.now()
            for i in range(20):
                dates.append(current_date + timedelta(days=i))
            
            data = []
            for date in dates:
                for strike in [90, 95, 100, 105, 110]:
                    price = 100 + np.random.normal(0, 5)
                    time_to_expiry = max(1/365, (dates[-1] - date).days/365)
                    iv = 0.2 + np.random.normal(0, 0.05)
                    
                    call_price = self.black_scholes(price, strike, time_to_expiry, iv, 'call')
                    put_price = self.black_scholes(price, strike, time_to_expiry, iv, 'put')
                    
                    call_delta = self.calculate_delta(price, strike, time_to_expiry, iv, 'call')
                    put_delta = self.calculate_delta(price, strike, time_to_expiry, iv, 'put')
                    
                    data.append({
                        'date': date,
                        'underlying_price': round(price, 2),
                        'strike': strike,
                        'expiry': dates[-1],
                        'type': 'CALL',
                        'premium': round(call_price, 2),
                        'implied_volatility': round(iv, 3),
                        'delta': round(call_delta, 3),
                        'volume': np.random.randint(100, 1000)
                    })
                    
                    data.append({
                        'date': date,
                        'underlying_price': round(price, 2),
                        'strike': strike,
                        'expiry': dates[-1],
                        'type': 'PUT',
                        'premium': round(put_price, 2),
                        'implied_volatility': round(iv, 3),
                        'delta': round(put_delta, 3),
                        'volume': np.random.randint(100, 1000)
                    })
            
            df = pd.DataFrame(data)
            self.logger.info(f"Generated {len(df)} sample option records")
            return df
        except Exception as e:
            self.logger.error(f"Error generating sample data: {e}")
            raise
    
    def generate_sample_portfolio(self):
        self.logger.info("Generating sample portfolio")
        try:
            portfolio_df = pd.DataFrame([
                {'symbol': 'AAPL', 'position': 5, 'option_type': 'CALL', 'strike': 100, 'expiry': datetime.now() + timedelta(days=30), 
                 'premium_paid': 3.50, 'current_value': 4.20, 'delta': 0.55, 'pnl': 35.00},
                {'symbol': 'TSLA', 'position': -3, 'option_type': 'PUT', 'strike': 800, 'expiry': datetime.now() + timedelta(days=45), 
                 'premium_paid': 25.00, 'current_value': 18.50, 'delta': -0.42, 'pnl': 195.00},
                {'symbol': 'GOOGL', 'position': 2, 'option_type': 'CALL', 'strike': 2800, 'expiry': datetime.now() + timedelta(days=60), 
                 'premium_paid': 45.00, 'current_value': 52.30, 'delta': 0.68, 'pnl': 146.00},
                {'symbol': 'MSFT', 'position': -1, 'option_type': 'PUT', 'strike': 350, 'expiry': datetime.now() + timedelta(days=15), 
                 'premium_paid': 8.50, 'current_value': 6.20, 'delta': -0.35, 'pnl': 23.00}
            ])
            self.logger.info(f"Generated portfolio with {len(portfolio_df)} positions")
            return portfolio_df
        except Exception as e:
            self.logger.error(f"Error generating sample portfolio: {e}")
            raise
    
    def black_scholes(self, S, K, T, sigma, option_type):
        try:
            d1 = (np.log(S/K) + (0.05 + sigma**2/2)*T) / (sigma*np.sqrt(T))
            d2 = d1 - sigma*np.sqrt(T)
            
            if option_type.lower() == 'call':
                price = S*norm.cdf(d1) - K*np.exp(-0.05*T)*norm.cdf(d2)
            else:
                price = K*np.exp(-0.05*T)*norm.cdf(-d2) - S*norm.cdf(-d1)
            
            result = max(price, 0)
            self.logger.debug(f"Black-Scholes: S={S}, K={K}, T={T}, sigma={sigma}, type={option_type} -> price={result}")
            return result
        except Exception as e:
            self.logger.error(f"Error in Black-Scholes calculation: {e}")
            raise
    
    def calculate_delta(self, S, K, T, sigma, option_type):
        try:
            d1 = (np.log(S/K) + (0.05 + sigma**2/2)*T) / (sigma*np.sqrt(T))
            
            if option_type.lower() == 'call':
                result = norm.cdf(d1)
            else:
                result = norm.cdf(d1) - 1
            
            self.logger.debug(f"Delta calculation: S={S}, K={K}, T={T}, sigma={sigma}, type={option_type} -> delta={result}")
            return result
        except Exception as e:
            self.logger.error(f"Error in delta calculation: {e}")
            raise
    
    def portfolio_summary(self):
        self.logger.info("Generating portfolio summary")
        try:
            total_pnl = self.portfolio['pnl'].sum()
            total_delta = (self.portfolio['delta'] * self.portfolio['position']).sum()
            total_theta = -0.15 * len(self.portfolio)
            
            summary = {
                'total_positions': len(self.portfolio),
                'total_pnl': round(total_pnl, 2),
                'portfolio_delta': round(total_delta, 3),
                'portfolio_theta': round(total_theta, 2),
                'unrealized_gain': round(total_pnl * 0.7, 2),
                'realized_gain': round(total_pnl * 0.3, 2)
            }
            self.logger.info(f"Portfolio summary: {summary}")
            return summary
        except Exception as e:
            self.logger.error(f"Error generating portfolio summary: {e}")
            raise
    
    def risk_metrics(self):
        self.logger.info("Calculating risk metrics")
        try:
            greeks = {'delta': 0, 'gamma': 0, 'theta': 0, 'vega': 0}
            
            for _, row in self.portfolio.iterrows():
                position = row['position']
                greeks['delta'] += position * row['delta']
                greeks['gamma'] += position * 0.04
                greeks['theta'] += position * -0.10
                greeks['vega'] += position * 0.25
            
            vol_skew = self.options_data.groupby('strike')['implied_volatility'].mean()
            vol_smile = {k: round(v, 3) for k, v in vol_skew.items()}
            
            risk_metrics = {
                'portfolio_greeks': {k: round(v, 3) for k, v in greeks.items()},
                'volatility_smile': vol_smile,
                'max_loss_scenario': round(-abs(greeks['delta']) * 100 * 0.1, 2),
                'var_95': round(abs(greeks['delta']) * 100 * 0.15 * 1.645, 2)
            }
            self.logger.info(f"Risk metrics calculated: {risk_metrics}")
            return risk_metrics
        except Exception as e:
            self.logger.error(f"Error calculating risk metrics: {e}")
            raise
    
    def market_analysis(self):
        self.logger.info("Performing market analysis")
        try:
            recent_data = self.options_data[self.options_data['date'] == self.options_data['date'].max()]
            
            put_call_ratio = (
                recent_data[recent_data['type'] == 'PUT']['volume'].sum() / 
                recent_data[recent_data['type'] == 'CALL']['volume'].sum()
            )
            
            avg_iv = recent_data['implied_volatility'].mean()
            
            most_active = (
                recent_data.groupby(['strike', 'type'])['volume'].sum()
                .sort_values(ascending=False).head(3)
            )
            
            market_analysis = {
                'put_call_ratio': round(put_call_ratio, 2),
                'average_iv': round(avg_iv, 3),
                'most_active_strikes': most_active.to_dict(),
                'total_volume': int(recent_data['volume'].sum()),
                'iv_percentile': 65 if avg_iv > 0.18 else 35
            }
            self.logger.info(f"Market analysis: {market_analysis}")
            return market_analysis
        except Exception as e:
            self.logger.error(f"Error in market analysis: {e}")
            raise
    
    def run_dashboard(self):
        self.logger.info("Running dashboard")
        try:
            summary = self.portfolio_summary()
            risk = self.risk_metrics()
            market = self.market_analysis()
            
            print("=" * 60)
            print("OPTIONS TRADING ANALYTICS DASHBOARD")
            print("=" * 60)
            print("\nPORTFOLIO SUMMARY:")
            print("-" * 40)
            for key, value in summary.items():
                print(f"{key.replace('_', ' ').title()}: {value}")
            
            print("\nRISK METRICS:")
            print("-" * 40)
            print("Portfolio Greeks:")
            for greek, value in risk['portfolio_greeks'].items():
                print(f" {greek.upper()}: {value}")
            print(f"Max 1-day Loss (10% move): ${risk['max_loss_scenario']}")
            print(f"95% VaR (1-day): ${risk['var_95']}")
            print("Volatility Smile:")
            for strike, iv in risk['volatility_smile'].items():
                print(f" Strike ${strike}: IV = {iv}")
            
            print("\nMARKET ANALYSIS:")
            print("-" * 40)
            print(f"Put/Call Ratio: {market['put_call_ratio']}")
            print(f"Average Implied Volatility: {market['average_iv']}")
            print(f"IV Percentile: {market['iv_percentile']}%")
            print(f"Total Daily Volume: {market['total_volume']:,}")
            print("\nMost Active Options:")
            for (strike, opt_type), volume in market['most_active_strikes'].items():
                print(f" ${strike} {opt_type}: {volume:,} contracts")
            
            print("\nPOSITIONS:")
            print("-" * 40)
            print(self.portfolio.to_string(index=False))
            
            expires_soon = self.portfolio[self.portfolio['expiry'] < datetime.now() + timedelta(days=7)]
            if len(expires_soon) > 0:
                warning_msg = f"{len(expires_soon)} positions expire within 7 days"
                print(f"\n❗ {warning_msg}")
                self.logger.warning(warning_msg)
            
            results = {
                'portfolio_summary': summary,
                'risk_metrics': risk,
                'market_analysis': market,
                'data': self.options_data,
                'portfolio': self.portfolio
            }
            self.logger.info("Dashboard run completed successfully")
            return results
        except Exception as e:
            self.logger.error(f"Error running dashboard: {e}")
            raise

if __name__ == "__main__":
    dashboard = OptionsTradingDashboard()
    results = dashboard.run_dashboard()