import yfinance as yf

ticker = 'AAPL'
data = yf.download(ticker, start='2022-01-01', end='2022-12-31')

print(data)
