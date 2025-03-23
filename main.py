import yfinance as yf         #type: ignore
import numpy as np
import pickle
import sys
import math
import pandas
import os
from termcolor import colored, cprint
from termcolor import colored
from importlib import import_module
from strategies.moSMA import analyze_sma
from strategies.moEMA import analyze_ema
from strategies.trailPE import analyze_trailPE
from strategies.enterprisetoEBITDA import analyze_EtoEB
from strategies.enterpriseToRevenue import analyze_EtoR
from Misc.autocorrect import autocorrect
from features.check_nyse_open import nyse_market_is_open  
from features.check_nifty_open import nifty_market_is_open 


global india_market_status       #used along with check nifty to allow/disallow buying/selling
global america_market_status     # used with check_nyse to allow/disallow buying/selling


def master(user_choice, portfol):           # used to either display current portfolio, otherwise proceed with analysis
  if user_choice == 1:
    update_portfolio(portfol)
  else:
    print('okay here it is')


#------------------------------------------------STRAT CODE------------------------------------------------------------------------
def sma(analyze_result, ticker, initial_capital, portfolio):         # driver code for simple moving averages calculated in a diff directory 
  if analyze_result['action'] == 1:
    print("Exponential moving averages recommend BUYING this stock, therefore:")
  else:
    print("Exponential moving averages recommend SELLING this stock, therefore:")
  buy_or_sell_stock(ticker, initial_capital, portfolio, analyze_result['action'], analyze_result['num_shares'])


def ema(analyze_result, ticker, initial_capital, portfolio):
  if analyze_result['action'] == 1:
    print("Exponential moving averages recommend BUYING this stock, therefore:")
  else:
    print("Exponential moving averages recommend SELLING this stock, therefore:")
  buy_or_sell_stock(ticker, initial_capital, portfolio, analyze_result['action'], analyze_result['num_shares'])


def trailPE(analyze_trailPE, ticker, initial_capital, portfolio):
  if analyze_trailPE['action'] == 1:
    print("TRAIL PRICE TO EARNINGS recommend BUYING this stock, therefore:")
  elif analyze_trailPE['action'] == -1:
    print("TRAIL PRICE TO EARNINGS recommend SELLING this stock, therefore:")
  elif analyze_trailPE['action'] == 0:
    print("TRAIL PRICE TO EARNINGS RECOMMENDS HOLDING THIS STOCK")
  buy_or_sell_stock(ticker, initial_capital, portfolio, analyze_trailPE['action'], analyze_trailPE['num_shares'])


def EtoEB(analyze_EtoEB, ticker, initial_capital, portfolio):
  if analyze_EtoEB['action'] == 1:
    print("ENTERPRISE TO EBITDA recommend BUYING this stock, therefore:")
  elif analyze_EtoEB['action'] == -1:
    print("ENTERPRISE TO EBITDA recommend SELLING this stock, therefore:")
  else:
    print("ENTERPRISE TO EBITDA RECOMMENDS HOLDING THIS STOCK")
  buy_or_sell_stock(ticker, initial_capital, portfolio, analyze_EtoEB['action'], analyze_EtoEB['num_shares'])


def EtoR(analyze_EtoR, ticker, initial_capital, portfolio):
  if analyze_EtoR['action'] == 1:
    print("ENTERPRISE TO Revenue recommend BUYING this stock, therefore:")
  elif analyze_EtoR['action'] == -1:
    print("ENTERPRISE TO Revenue recommend SELLING this stock, therefore:")
  else:
    print("ENTERPRISE TO Revenue RECOMMENDS HOLDING THIS STOCK")
  buy_or_sell_stock(ticker, initial_capital, portfolio, analyze_EtoR['action'], analyze_EtoR['num_shares'])


#--------------------------------------------STRAT CODE OVER----------------------------------------------------------------

def buy_or_sell_stock(ticker, initial_capital, portfolio, action, num_shares):
  num_shares = math.ceil(num_shares)

  if action not in (1, -1, 0):
    print(f"Invalid action. Please enter 1 to buy or -1 to sell.")
    return

  stock_data = yf.download(ticker, period="1d")["Close"].iloc[0]
  stock_price = round(stock_data, 2)
  total_cost = num_shares * stock_price

  if action == 1:
    if num_shares <= 0:
      print("Invalid number of shares. Please enter a positive number to buy.")
      return

    if total_cost <= initial_capital:
      if ticker in portfolio:
        portfolio[ticker]["Shares"] += num_shares
        portfolio[ticker]["Price"].append(stock_price)
        initial_capital -= total_cost
      else:
        portfolio[ticker] = {'Price': [stock_price], 'Shares': num_shares}
        initial_capital -= total_cost

      shares_to_buy = num_shares
      print(f"Bought {shares_to_buy} shares of {ticker} at {curr}{stock_price:.2f} per share.")
      average_price = sum(portfolio[ticker]["Price"]) / len(portfolio[ticker]["Price"])
      print(f"Average Buying Price: {curr}{average_price:.2f}")
      print(f"Remaining portfolio value: {curr}{initial_capital:.2f}")
      update_capital(initial_capital, "INDcapital.pkl") if indian else update_capital(initial_capital, "UScapital.pkl")
    else:
      print(f"Insufficient funds to buy {num_shares} shares of {ticker}.")
      print(f"Your remaining capital is {curr}{initial_capital:.2f}.")
      print(f"Consider buying fewer shares or using a smaller portion of your capital.")
      update_capital(initial_capital, "INDcapital.pkl") if indian else update_capital(initial_capital, "UScapital.pkl")
  elif action == -1:
    if ticker not in portfolio or portfolio[ticker]["Shares"] <= 0:
      print(f"No shares of {ticker} to sell in the portfolio.")
      return

    if num_shares < 0:
      num_shares = portfolio[ticker]["Shares"]

    if num_shares > portfolio[ticker]["Shares"]:
      print(f"Not enough shares to sell. You have {portfolio[ticker]['Shares']} shares of {ticker}.")
      return

    total_sale_value = num_shares * stock_price
    initial_capital += total_sale_value
    portfolio[ticker]["Shares"] -= num_shares
    if portfolio[ticker]["Shares"] == 0:
      del portfolio[ticker]

    print(f"Sold {num_shares} shares of {ticker} at {curr}{stock_price:.2f} per share.")
    print(f"Total sale value: {curr}{total_sale_value:.2f}")
    print(f"Updated portfolio value: {curr}{initial_capital:.2f}")
    update_capital(initial_capital, "INDcapital.pkl") if indian else update_capital(initial_capital, "UScapital.pkl")
  elif action == 0:
    if ticker in portfolio:
      print(f"Holding {portfolio[ticker]['Shares']} shares of {ticker}.")
      print(f"Average Buying Price: {curr}{sum(portfolio[ticker]['Price']) / len(portfolio[ticker]['Price']):.2f}")
    else:
      print(f"Not holding any shares of {ticker} in the portfolio.")


def update_portfolio(portfolio):
  if portfolio is None or not isinstance(portfolio, dict):
    print("Error: Portfolio is not initialized correctly.")
    return

  total_value = 0
  initial_capital = load_capital("INDcapital.pkl") if indian else load_capital("UScapital.pkl")
  for ticker, stock_info in portfolio.items():
    average_price = sum(portfolio[ticker]["Price"]) / len(portfolio[ticker]["Price"])
    current_price = round(yf.download(ticker, period="1d")["Close"].iloc[0], 2)
    current_value = current_price * stock_info["Shares"]
    profit_loss = current_value - (average_price * stock_info["Shares"])
    total_value += current_value

    print(f"\nStock: {ticker}")
    print(f"Average Buying Price: {curr}{average_price:.2f}")
    print(f"  - Shares: {stock_info['Shares']}")
    print(f"  - Current Price: {curr}{current_price:.2f}")
    if profit_loss < 0:
      cprint(f"  - Profit/Loss: {curr}{profit_loss:.2f}", "red", attrs=["blink"])
    else:
      cprint(f"  - Profit/Loss: {curr}{profit_loss:.2f}", "green", attrs=["blink"])

  total_portfolio_value = total_value + initial_capital
  print(f"\nTotal Portfolio Value (including stock holdings): {curr}{total_portfolio_value:.2f}")
  total_profit_loss = total_portfolio_value - 1000000
  percentage_profit_loss = (total_profit_loss / (1000000.1 - initial_capital)) * 100
  if total_profit_loss > 0:
    cprint(f"Profit/Loss: {curr}{total_profit_loss:.2f}", "green", attrs=["bold"])
    cprint(f"Profit/Loss Percentage: {percentage_profit_loss:.2f}%", "green", attrs=["bold"])
  else:
    cprint(f"Profit/Loss: {curr}{total_profit_loss:.2f}", "red", attrs=["bold"])
    cprint(f"Profit/Loss Percentage: {percentage_profit_loss:.2f}%", "red", attrs=["bold"])


def save_portfolio(portfolio, filename):
  with open(filename, 'wb') as handle:
    pickle.dump(portfolio, handle)


def load_portfolio(filename):
  try:
    with open(filename, 'rb') as handle:
      return pickle.load(handle)
  except FileNotFoundError:
    print("Portfolio file not found. Creating a new portfolio.")
    return {}


def load_capital(filename):
  try:
    with open(filename, 'rb') as handle:
      return pickle.load(handle)
  except FileNotFoundError:
    print("Capital file not found. Using default initial capital.")
    return 1000000


def update_capital(capital, filename):
  print("Your total left capital is: ", curr, capital)
  with open(filename, 'wb') as handle:
    pickle.dump(capital, handle)


#-------------------------------------------Driver Code-----------------------------------------------------------

dictionary_file = os.path.join(os.path.dirname(__file__), "Misc", "list.txt")
print("ENTER THE TICKER YOU WANT ANALYSIS FOR, add .NS for indian stock and input 1 FOR BUYING A STOCK AND ENTER 0 FOR SELLING A STOCK-")
ticker = input()

corrected_ticker = autocorrect(ticker, dictionary_file)
if corrected_ticker != ticker:
  print(f"Did you mean '{corrected_ticker}'?")
  confirm = input()
  if confirm.lower() in ["y", "yes"]:
    print("okay continuing with program")
  else:
    print("Please try again")
    sys.exit()

ticker = corrected_ticker

if ticker[-3:] in [".NS", ".BO"]:
  american = False
  indian = True
  curr = "₹"
  portfolio = load_portfolio("INDportfolio.pkl")
  initial_capital = load_capital("INDcapital.pkl")
else:
  indian = False
  american = True
  curr = "$"
  portfolio = load_portfolio("USportfolio.pkl")
  initial_capital = load_capital("UScapital.pkl")

if ticker == "1":
  if indian and nifty_market_is_open() == 0:
    cprint("The Indian market is currently closed. Cannot execute buy orders.", "yellow")
    cprint("1: View current portfolio", "green")
    cprint("2: Exit program", "red")
    choice = input("Enter your choice: ")
    if choice == "1":
      update_portfolio(portfolio)
    sys.exit()
  elif american and nyse_market_is_open() == 0:
    cprint("The US market is currently closed. Cannot execute buy orders.", "yellow")
    cprint("1: View current portfolio", "green")
    cprint("2: Exit program", "red")
    choice = input("Enter your choice: ")
    if choice == "1":
      update_portfolio(portfolio)
    sys.exit()

  print("Enter the Ticker you wish to buy and in a new line the number of shares")
  direct_ticker = input()
  numOfShares = int(input())
  buy_or_sell_stock(direct_ticker, initial_capital, portfolio, 1, numOfShares)

elif ticker == "0":
  print("Enter the Ticker you wish to sell and in a new line the number of shares")
  direct_ticker = input()
  numOfShares = int(input())
  buy_or_sell_stock(direct_ticker, initial_capital, portfolio, -1, numOfShares)

print("If you wish to see the portfolio, press 1 else press any other number")
choice = int(input())
master(choice, portfolio)

if indian:
  save_portfolio(portfolio, "INDportfolio.pkl")
else:
  save_portfolio(portfolio, "USportfolio.pkl")

analyze_result_sma = analyze_sma(ticker)
sma(analyze_result_sma, ticker, initial_capital, portfolio)
if indian:
  save_portfolio(portfolio, "INDportfolio.pkl")
  initial_capital = load_capital("INDcapital.pkl")
elif american:
  save_portfolio(portfolio, "USportfolio.pkl")
  initial_capital = load_capital("UScapital.pkl")
update_portfolio(portfolio)

analyze_result_ema = analyze_ema(ticker)
ema(analyze_result_ema, ticker, initial_capital, portfolio)
if indian:
  save_portfolio(portfolio, "INDportfolio.pkl")
  initial_capital = load_capital("INDcapital.pkl")
elif american:
  save_portfolio(portfolio, "USportfolio.pkl")
  initial_capital = load_capital("UScapital.pkl")
update_portfolio(portfolio)

analyze_result_trailPE = analyze_trailPE(ticker)
trailPE(analyze_result_trailPE, ticker, initial_capital, portfolio)
if indian:
  save_portfolio(portfolio, "INDportfolio.pkl")
  initial_capital = load_capital("INDcapital.pkl")
elif american:
  save_portfolio(portfolio, "USportfolio.pkl")
  initial_capital = load_capital("UScapital.pkl")
update_portfolio(portfolio)

temp = ticker[:-3]
analyze_result_EtoEB = analyze_EtoEB(temp, ticker)
EtoEB(analyze_result_EtoEB, ticker, initial_capital, portfolio)
if indian:
  save_portfolio(portfolio, "INDportfolio.pkl")
  initial_capital = load_capital("INDcapital.pkl")
elif american:
  save_portfolio(portfolio, "USportfolio.pkl")
  initial_capital = load_capital("UScapital.pkl")
update_portfolio(portfolio)

temp = ticker[:-3]
analyze_result_EtoR = analyze_EtoR(temp, ticker)
EtoR(analyze_result_EtoR, ticker, initial_capital, portfolio)
if indian:
  save_portfolio(portfolio, "INDportfolio.pkl")
  initial_capital = load_capital("INDcapital.pkl")
elif american:
  save_portfolio(portfolio, "USportfolio.pkl")
  initial_capital = load_capital("UScapital.pkl")
update_portfolio(portfolio)
