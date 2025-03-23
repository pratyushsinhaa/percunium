import yfinance as yf
import pickle
import pandas as pd
from termcolor import cprint
def getsector(ticker, filename):
    data = pd.read_csv(filename)  # Read the CSV file
    filtered_data = data[data['Symbol'] == ticker]  # Filter the data for the given ticker
    if not filtered_data.empty:
        sector = filtered_data['Industry'].values[0]  # Get the sector value for the given ticker
        return sector
    else:
        raise ValueError(f"Ticker {ticker} not found in the CSV file.")

def avgval(filename, sec):
    with open(filename, "rb") as file:  # Open the file in binary read mode
         data = pickle.load(file)  # Load the pickle file content
    value = data[sec]["enterpriseToRevenue"]
    return value
        



# def analyze(ticker):
#     inf = yf.Ticker(ticker)
#     res = inf.info["enterpriseToRevenue"]
#     avgEVtoEBITDA = avgval("INDvalues.pkl")
#     aciton = 0
#     num_shares = 0
#     if res <avgEVtoEBITDA:
#         action = 1
#         num_shares = (avgEVtoEBITDA-res)*5
#     elif res>avgEVtoEBITDA:
#         action = -1
#         num_shares = (res-avgEVtoEBITDA)*5
        
#     return {
#         'action' : action,
#         'num_shares' : num_shares
#     }



def analyze_EtoR(ticker1, ticker2):
    res = {"action": 0, "num_shares": 0}  # Initialize res at the beginning
    try:
        dat = yf.Ticker(ticker2)
        sec = getsector(ticker1, "/Users/pratyushsinha/Github/quant/historical data ind/ind_nifty500list.csv")
        avg = avgval("/Users/pratyushsinha/Github/quant/averages/INDvalues.pkl", sec)
        inf = dat.info
        if inf['enterpriseToRevenue'] < avg:
            print("WOOOO BUY THIS STOCK HELL YEAH")
            res['action'] = 1
            res['num_shares'] = 20
        else:
            print("NOOOOOOO DON'T BUY THIS STOCK ")
            res['action'] = -1
            res['num_shares'] = 15
    except KeyError as e:
        cprint(f"Ticker not found or missing data: {e}", 'red', attrs=['bold'])
    except Exception as e:
        cprint(f"An error occurred: {e}", 'red', attrs=['bold'])
    return res

# Example usage
# result = analyze_EtoR("HCC.NS", "HCC")

        
