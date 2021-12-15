import pandas as pd
from ibapi.client import EClient
from ibapi.wrapper import EWrapper
from ibapi.contract import * # @UnusedWildImport
from ibapi.common import *  # @UnusedWildImport
from ibapi.ticktype import * # @UnusedWildImport

# available tick types
# https://interactivebrokers.github.io/tws-api/tick_types.html

class TestApp(EWrapper, EClient):
    def __init__(self):
        EWrapper.__init__(self)
        EClient.__init__(self, wrapper=self)
        self.CallContract = Contract()

    def nextValidId(self, orderId: int):
        super().nextValidId(orderId)
        print("NextValidId:", orderId)

        # we can start now
        self.start()


    def start(self):
        self.tickDataOperations_req()
        print("Executing requests ... finished")

    def tickDataOperations_req(self):
        self.CallContract.symbol = 'TQQQ'
        self.CallContract.secType = 'OPT'
        self.CallContract.exchange = 'SMART'
        self.CallContract.currency = 'USD'
        self.CallContract.lastTradeDateOrContractMonth = '20211217'
        self.CallContract.strike = 155
        self.CallContract.right = "C"
        self.CallContract.multiplier = "100"


        self.reqMktData(1002, self.CallContract, "", True, False, [])

    def tickPrice(self, reqId: TickerId, tickType: TickType, price: float,
                  attrib: TickAttrib):
        super().tickPrice(reqId, tickType, price, attrib)
        print("TickPrice. TickerId:", reqId, "tickType:", tickType,
              "Price:", price, "CanAutoExecute:", attrib.canAutoExecute,
              "PastLimit:", attrib.pastLimit, end=' ')

    def tickSize(self, reqId: TickerId, tickType: TickType, size: int):
        super().tickSize(reqId, tickType, size)
        print("TickSize. TickerId:", reqId, "TickType:", tickType, "Size:", size)
        self.disconnect()

def main():
    app = TestApp()
    app.connect("127.0.0.1", port=7497, clientId=102)
    print("serverVersion:%s connectionTime:%s" % (app.serverVersion(),app.twsConnectionTime()))
    app.run()

if __name__ == "__main__":
    main()