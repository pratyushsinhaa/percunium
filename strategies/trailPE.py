import yfinance as yf
from termcolor import cprint


def analyze_trailPE(ticker):
    tick = yf.Ticker(ticker)
    try:
        pe = tick.info['trailingPE']
        res = {"action":0, "num_shares": 0}
        if pe>30:
            cprint("THE PRICE TO EARNINGS IS VERY HIGH, THEREFORE THIS STOCK is RECOMMENDED TO BE SOLD",color = "red",attrs=['blink'])
            res["action"] = -1
            res["num_shares"] = (pe-30)*5
        elif pe>20 and pe<30:
            cprint("THE PRICE TO EARNINGS IS DECENT, THEREFORE THIS STOCK is RECOMMENDED TO BE HELD",color = "grey",attrs=['blink'])
            res["action"] = 0
        else:
            cprint("THE PRICE TO EARNINGS IS SUFFICIENTLY LOW, THEREFORE THIS STOCK is RECOMMENDED TO BE BOUGHT",color = "green",attrs=['blink'])
        
            res["action"] = 1
            res["action"] = (20-pe)*5
        
        return res
    except KeyError:
        cprint("THE TRAILING PROFIT TO EARNINGS FOR THIS TICKER COULD NOT BE FOUND, THEREFORE THIS METHOD OF EVALUATION CANNOT BE USED",color = "magenta")
        res = {"action":0, "num_shares": 0}
        return res



