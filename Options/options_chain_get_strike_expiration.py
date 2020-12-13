from ibapi.client import EClient
from ibapi.wrapper import EWrapper
from ibapi.contract import Contract
from threading import Timer

stock_symbol = input("What ticker would you like?  ")
strike_number = float(input("What strike?   "))
expiration = float(input("What expiration (yyyymmdd)?   "))

class TestApp(EWrapper, EClient):

    def __init__(self):
        EClient.__init__(self, self)

    def error(self, reqId, errorCode, errorString):
        print("Error: ", reqId, " ", errorCode, " ", errorString)

    def nextValidId(self, orderId):
        self.start()

    def contractDetails(self, reqID, contractDetails):
        print("contractDetails: ", reqID, " ", contractDetails, "\n")

    def contractDetailsEnd(self, reqId):
        print("\ncontractDetails End\n")

    def start(self):
        contract = Contract()
        contract.symbol = stock_symbol
        contract.secType = "OPT"
        contract.exchange = "SMART"
        contract.currency = "USD"
        contract.strike = strike_number
        contract.lastTradeDateOrContractMonth = expiration

        self.reqContractDetails(1, contract)

    def stop(self):
        self.done = True
        self.disconnect()

def main():
    app = TestApp()
    app.nextOrderID = 0
    app.connect("127.0.0.1", 7497, 0)

    Timer(4, app.stop).start()
    app.run()

if __name__ == "__main__":
    main()
