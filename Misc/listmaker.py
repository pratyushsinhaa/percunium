import csv

# Read values from ticker column of first CSV file
with open('/Users/pratyushsinha/Github/quant/historical data usa/sp500-companies.csv', 'r') as csv_file:
    csv_reader = csv.DictReader(csv_file)
    tickers = [row['Ticker'] for row in csv_reader]

# Read values from Symbol column of second CSV file and append .NS to each symbol
with open('/Users/pratyushsinha/Github/quant/historical data ind/ind_nifty500list.csv', 'r') as csv_file:
    csv_reader = csv.DictReader(csv_file)
    symbols = [row['Symbol'] + ".NS" for row in csv_reader]

# Write tickers and symbols to a text file
with open('/Users/pratyushsinha/Github/quant/Misc/list.txt', 'w') as txt_file:
    txt_file.write('\n'.join(tickers) + '\n')
    txt_file.write('\n'.join(symbols) + '\n')

print("success")