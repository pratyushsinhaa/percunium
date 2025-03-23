import pandas as pd
from transformers import pipeline
import re
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def read_text_file(filename):
    with open(filename, 'r') as file:
        lines = file.readlines()
    return lines

titles_path = os.path.join(BASE_DIR, "scrape", "titles.txt")
companies_path = os.path.join(BASE_DIR, "historical data usa", "sp500-companies.csv")

data = read_text_file(titles_path)
data = [line.strip("\n") for line in data]

try:
    sentiment_analysis = pipeline("sentiment-analysis", model="siebert/sentiment-roberta-large-english", device=0)
except Exception as e:
    print(f"Error initializing sentiment analysis pipeline: {e}")
    sentiment_analysis = pipeline("sentiment-analysis", model="siebert/sentiment-roberta-large-english")

try:
    df = pd.read_csv(companies_path, encoding='ISO-8859-1')
except Exception as e:
    print(f"Error reading CSV file: {e}")
    df = pd.DataFrame()

if not df.empty:
    ticknames = dict(zip(df["Ticker"], df["Name"]))
else:
    ticknames = {}

for line in data:
    for ticker, name in ticknames.items():
        if re.search(rf'\b{ticker}\b', line):
            try:
                result = sentiment_analysis(line)
                print(result[0]['label'], ticker, name, "\n\tthe line is ----", line)
            except Exception as e:
                print(f"Error performing sentiment analysis on line '{line}': {e}")