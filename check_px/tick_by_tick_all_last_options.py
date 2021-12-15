from ibapi.client import EClient
from ibapi.wrapper import EWrapper
# types
from ibapi.common import *  # @UnusedWildImport
from ibapi.contract import * # @UnusedWildImport
import datetime

class TestApp(EWrapper, EClient):
    def __init__(self):
        EWrapper.__init__(self)
        EClient.__init__(self, wrapper=self)
        self.contract = Contract()
        self.CallContract = Contract()

    def nextValidId(self, orderId: int):
        # we can start now
        self.start()

    def start(self):
        # self.tickDataOperations_req()
        self.tickByTickOperations_req()
        print("Executing requests ... finished")

    def tickByTickOperations_req(self):
        # Create contract object
        # self.contract.symbol = 'NQ'
        # self.contract.secType = 'FUT'
        # self.contract.exchange = 'GLOBEX'
        # self.contract.currency = 'USD'
        # self.contract.lastTradeDateOrContractMonth = "202112"

        self.CallContract.symbol = 'TQQQ'
        self.CallContract.secType = 'OPT'
        self.CallContract.exchange = 'SMART'
        self.CallContract.currency = 'USD'
        self.CallContract.lastTradeDateOrContractMonth = '20211217'
        self.CallContract.strike = 155
        self.CallContract.right = "C"
        self.CallContract.multiplier = "100"

        # Request tick data
        self.reqTickByTickData(19002, self.CallContract, "MidPoint", 0, False)

    # Receive tick data
    def tickByTickAllLast(self, reqId: int, tickType: int, time: int, price: float,
                          size: int, tickAttribLast: TickAttribLast, exchange: str,
                          specialConditions: str):
        print('Time:', datetime.datetime.fromtimestamp(time),
              "Price:", "{:.2f}".format(price),
              'Size:', size)

def main():
    app = TestApp()
    app.connect("127.0.0.1", port=7497, clientId=102)
    print("serverVersion:%s connectionTime:%s" % (app.serverVersion(),app.twsConnectionTime()))
    app.run()

if __name__ == "__main__":
    main()