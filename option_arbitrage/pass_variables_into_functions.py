import yfinance as yf


class StockDetails(object):
    def __init__(self):
        self.filepath = 'tickerlist.csv'
        self.symbol = None
        self.startdt = None
        self.period = None
        self.interval = None

    def tickerlist(self, file):
        line = [line for line in open(file)]
        stocksymbol = line[0].strip().split(',')
        return stocksymbol

    def yfinancedownload(self, symbol, startdt):  # , prd, int):
        df_data = yf.download(symbol, startdt)  # , period=prd, interval=int)
        return df_data

        # hist = ticker.history(period="1d", interval="5m")

    def analyze(self):
        startdt = '2010-01-01'
        stocksymbol = self.tickerlist(self.filepath)
        for symbol in stocksymbol:
            df = self.yfinancedownload(symbol, startdt)  # , period, interval)
            print(df)
            print('HOlding the data so that I can view the dataframe')


# ctrl+Alt+L

def main():
    app = StockDetails()
    app.analyze()


if __name__ == '__main__':
    main()
