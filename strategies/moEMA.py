import yfinance as yf
from termcolor import colored,cprint
import sys


def analyze_ema(ticker):
    """
    Analyzes the given stock ticker using exponential moving averages (EMA) to determine buy, sell, or hold action.

    Args:
        ticker: String representing the stock ticker symbol.

    Returns:
        A dictionary containing:
            'action': Positive integer for buy, negative integer for sell, 0 for hold.
            'num_shares': Number of shares to buy/sell (positive for buy, negative for sell all).
    """
    # Download historical data for the past year
    historical_data = yf.download(ticker, period="1y")["Close"]
    
    # Define periods for EMA calculation in days
    periods = {'5d': 5, '1mo': 30, '3mo': 90, '6mo': 180, '1y': 365}
    
    buy_signals = 0
    sell_signals = 0
    
    # Most recent closing price
    market_price = historical_data.iloc[-1]
    
    for period_name, days in periods.items():
        # Calculate EMA for the period
        ema = historical_data.ewm(span=days, adjust=False).mean().iloc[-1]
        
        # Determine buy or sell signal
        if market_price > ema:
            buy_signals += 1
            print(colored(f"{period_name} EMA indicates a BUY signal.", "green"))
        elif market_price < ema:
            sell_signals += 1
            print(colored(f"{period_name} EMA indicates a SELL signal.", "red"))
    
    # Determine overall action based on counts of buy/sell signals
    if buy_signals > sell_signals:
        cprint("Overall Decision: BUY THE STOCK", "green", attrs=["bold"], file=sys.stderr)
        action = 1
    elif sell_signals > buy_signals:
        cprint("Overall Decision: SELL THE STOCK", "red", attrs=["bold"], file=sys.stderr)
        action = -1
    else:
        cprint("Overall Decision: HOLD THE STOCK", "gray", attrs=["bold"], file=sys.stderr)
        action = 0
    num_shares = abs((buy_signals - sell_signals)*5)
    
    return {'action': action, 'num_shares': num_shares}

# Example usage
