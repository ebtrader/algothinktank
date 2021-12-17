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
        self.CallContract1 = Contract()
        self.data = []
        self.df = pd.DataFrame()

    def nextValidId(self, orderId: int):
        super().nextValidId(orderId)
        self.nextValidOrderId = orderId
        print("NextValidId:", orderId)

        # we can start now
        self.start()

    def nextOrderId(self):
        oid = self.nextValidOrderId
        self.nextValidOrderId += 1
        return oid

    def start(self):
        self.tickDataOperations_req()
        print("Executing requests ... finished")

    def tickDataOperations_req(self):
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

        self.CallContract1.symbol = 'TQQQ'
        self.CallContract1.secType = 'OPT'
        self.CallContract1.exchange = 'SMART'
        self.CallContract1.currency = 'USD'
        self.CallContract1.lastTradeDateOrContractMonth = '20211217'
        self.CallContract1.strike = 154
        self.CallContract1.right = "C"
        self.CallContract1.multiplier = "100"

        # self.reqRealTimeBars(3001, self.CallContract, 5, "MIDPOINT", True, [])
        self.reqRealTimeBars(3002, self.CallContract, 5, "BID", True, [])
        self.reqRealTimeBars(3003, self.CallContract, 5, "ASK", True, [])
        self.reqRealTimeBars(3004, self.CallContract1, 5, "BID", True, [])
        self.reqRealTimeBars(3005, self.CallContract1, 5, "ASK", True, [])

    def realtimeBar(self, reqId: TickerId, time: int, open_: float, high: float, low: float, close: float,
                    volume: int, wap: float, count: int):
        super().realtimeBar(reqId, time, open_, high, low, close, volume, wap, count)
        print("RealTimeBar. TickerId:", reqId, RealTimeBar(time, -1, open_, high, low, close, volume, wap, count))

    # ! [realtimebar]

def main():
    app = TestApp()
    app.connect("127.0.0.1", port=7497, clientId=102)
    print("serverVersion:%s connectionTime:%s" % (app.serverVersion(),app.twsConnectionTime()))
    app.run()

if __name__ == "__main__":
    main()