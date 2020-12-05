from ib_insync import *

#https://github.com/erdewit/ib_insync/blob/master/notebooks/option_chain.ipynb

ib = IB()
ib.connect('127.0.0.1', 7497, clientId=12)

#stock_symbol = 'TQQQ'
stock_symbol = input("what stock ticker do you want an option chain for?  ")
number_of_strikes = float(input("how many strikes?   "))

spx = Stock(stock_symbol, 'CBOE')

print(ib.qualifyContracts(spx))

ib.reqMarketDataType(4)

[ticker] = ib.reqTickers(spx)

#print(ticker)

spxValue = ticker.marketPrice()
#print(spxValue)

chains = ib.reqSecDefOptParams(spx.symbol, '', spx.secType, spx.conId)

#print(util.df(chains))

chain = next(c for c in chains if c.tradingClass == stock_symbol and c.exchange == 'SMART')
#print(chain)

util.df(chains).to_csv("opt_chain.csv")

strikes = [strike for strike in chain.strikes
        if strike % 5 == 0
        and spxValue - number_of_strikes < strike < spxValue + number_of_strikes]
expirations = sorted(exp for exp in chain.expirations)[:3]
rights = ['P', 'C']

contracts = [Option(stock_symbol, expiration, strike, right, 'SMART', tradingClass=stock_symbol)
        for right in rights
        for expiration in expirations
        for strike in strikes]

contracts = ib.qualifyContracts(*contracts)
#print(len(contracts))

#print(contracts[0])

lst = []

lst = contracts

#print(lst)

print(*lst, sep='\n')

#tickers = ib.reqTickers(*contracts)

#print (tickers[0])

ib.disconnect()