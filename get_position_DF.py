from ibapi.client import EClient
from ibapi.wrapper import EWrapper
from ibapi.contract import Contract
from ibapi.utils import *
from ibapi.order import *
from threading import Timer
import pandas as pd

class TestApp(EWrapper, EClient):
    def __init__(self):
        EClient.__init__(self, self)
        self.df = pd.DataFrame(columns=['symbol', 'sectype', 'position'])

    @iswrapper
    def error(self, reqId, errorCode, errorString):
        print("Error: ", reqId, " ", errorCode, " ", errorString)

    @iswrapper
    def nextValidId(self, orderId):
        self.start()

    @iswrapper
    def updatePortfolio(self, contract: Contract, position: float,
                        marketPrice: float, marketValue: float,
                        averageCost: float, unrealizedPNL: float,
                        realizedPNL: float, accountName: str):
        print("UpdatePortfolio.", "Symbol:", contract.symbol, "SecType:", contract.secType, "Exchange:",
              contract.exchange,
              "Position", position, "MarketPrice:", marketPrice, "MarketValue:", marketValue, "AverageCost:",
              averageCost,
              "UnrealizedPNL:", unrealizedPNL, "RealizedPNL:", realizedPNL, "AccountName:", accountName)

        self.df.loc[len(self.df)] = [contract.symbol, contract.secType, position]
        self.df.to_csv('position.csv')

    def start(self):
        self.reqAccountUpdates(True, "")

    def stop(self):
        self.reqAccountUpdates(False, "")
        self.done = True
        self.disconnect()


#execute the classes
def main():

    app2 = TestApp()
    # app2.connect("127.0.0.1", 4002, 9)  # IB Gateway PaperTrading
    app2.connect("127.0.0.1", 7497, 9)  # TWS PaperTrading
    Timer(3, app2.stop).start()
    app2.run()


if __name__ == "__main__":
    main()
