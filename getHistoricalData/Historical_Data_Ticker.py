from ibapi.client import EClient
from ibapi.wrapper import EWrapper
from ibapi.contract import Contract

stock_symbol = input("What ticker would you like?  ")
days_back = str(input("How many days back?   "))
minutes_period = str(input("How many minutes in each candle?   "))
days = days_back+" D"
minutes = minutes_period+" mins"

#print (days)

class TestApp(EWrapper, EClient):
    def __init__(self):
        EClient.__init__(self, self)

    def error(self, reqId, errorCode, errorString):
        print("Error: ", reqId, " ", errorCode, " ", errorString)

    def historicalData(self, reqId, bar):
        print("HistoricalData. ", reqId, " Date:", bar.date, "Open:", bar.open,
              "High:", bar.high, "Low:", bar.low, "Close:", bar.close, "Volume:", bar.volume,
              "Count:", bar.barCount, "WAP:", bar.average)


def main():
    app = TestApp()
    app.connect("127.0.0.1", 4002, 0)
    contract = Contract()
    contract.symbol = stock_symbol
    contract.secType = "STK"
    contract.exchange = "SMART"
    contract.currency = "USD"

    app.reqHistoricalData(1, contract, "", days, minutes, "MIDPOINT", 0, 1, False, [])
    app.run()


if __name__ == "__main__":
    main()