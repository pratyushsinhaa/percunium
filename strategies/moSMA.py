import yfinance as yf # type: ignore
from termcolor import colored,cprint
import sys

def analyze_sma(ticker):
    """
    Calculates SMAs for 1d, 5d, 1mo, 3mo, 6mo, and 1y for the given ticker.
    Prints whether each period indicates a buy or sell in green or red.
    """
    # Download historical data for the past year
    historical_data = yf.download(ticker, period="1y")["Close"]
    
    # Define periods for SMA calculation
    periods = {'1d': 1, '5d': 5, '1mo': 30, '3mo': 90, '6mo': 180, '1y': 365}
    
    buy_signals = 0
    sell_signals = 0
    
    # Most recent closing price
    market_price = historical_data.iloc[-1]
    
    for period, days in periods.items():
        # Calculate SMA for the period
        sma = historical_data.tail(days).mean()
        
        # Determine buy or sell signal
        if market_price > sma:
            buy_signals += 1
            print(colored(f"{period} SMA indicates a BUY signal.", "green"))
        elif market_price < sma:
            sell_signals += 1
            print(colored(f"{period} SMA indicates a SELL signal.", "red"))
    
    # Overall decision based on counts of buy/sell signals
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
    return {
      'action': action,
      'num_shares': num_shares
  }

