# percunium
Paper trading platform with dual market support along with sentiment analysis and value investing formulae implemented.

Please note this is a work in progress as I make the code executable directly by downloading. 
I will add all the features in due time from the private repo.

## Setup

### Required Packages
- yfinance
- numpy
- pandas
- sys
- termcolor
- transformers

### Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/yourusername/percunium.git
    cd percunium
    ```

2. Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

### Running the Application

After you're done downloading these, you're pretty much set to go. Just run your main file and do what you wish with your new portfolio!
In general, if all you do is run the program and then input tickers, It's going to use simple moving averages formulae, exponential moving avergaes, some value investing formulae like EV/EBITDA, EV/R, trailPE so far. The sentiment analysis file uses siebert roberta large english model to fnd a ticker in the "hot" posts from r/WallStreetBets and then analyse it as either positive or negative. 


```bash
python main.py