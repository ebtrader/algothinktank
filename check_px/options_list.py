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
        self.contract = Contract()
        self.contract1 = Contract()
        self.data = []
        self.data1 = []
        self.data_counter = 0
        self.data1_counter = 0
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

    def running_list(self, close: float):
        self.data.append(close)
        self.data_counter += 1
        if self.data_counter < 7:
            return
        while len(self.data) > 7:
            self.data.pop(0)

    def id_list(self, reqId):
        self.data1.append(reqId)
        self.data1_counter += 1
        if self.data1_counter < 7:
            return
        while len(self.data1) > 7:
            self.data1.pop(0)

    def tickDataOperations_req(self):
        self.contract.symbol = 'NQ'
        self.contract.secType = 'FUT'
        self.contract.exchange = 'GLOBEX'
        self.contract.currency = 'USD'
        self.contract.lastTradeDateOrContractMonth = "202112"

        self.contract1.symbol = 'ES'
        self.contract1.secType = 'FUT'
        self.contract1.exchange = 'GLOBEX'
        self.contract1.currency = 'USD'
        self.contract1.lastTradeDateOrContractMonth = "202112"

        tick1 = 3004
        tick2 = 3005
        tick3 = 3006
        tick4 = 3007

        # self.reqRealTimeBars(3002, self.contract, 5, "BID", True, [])
        # self.reqRealTimeBars(3003, self.contract, 5, "ASK", True, [])
        self.reqRealTimeBars(tick1, self.contract, 5, "BID", False, []) # False for after-hours and True for market hours
        self.reqRealTimeBars(tick2, self.contract, 5, "ASK", False,[])  # False for after-hours and True for market hours
        self.reqRealTimeBars(tick3, self.contract1, 5, "BID", False, []) # False for after-hours and True for market hours
        self.reqRealTimeBars(tick4, self.contract1, 5, "ASK", False, [])  # False for after-hours and True for market hours

    def realtimeBar(self, reqId: TickerId, time: int, open_: float, high: float, low: float, close: float,
                    volume: int, wap: float, count: int):
        super().realtimeBar(reqId, time, open_, high, low, close, volume, wap, count)
        print("RealTimeBar. TickerId:", reqId, RealTimeBar(time, -1, open_, high, low, close, volume, wap, count), self.data1, self.data)

        self.id_list(reqId)
        self.running_list(close)


    # ! [realtimebar]

def main():
    app = TestApp()
    app.connect("127.0.0.1", port=7497, clientId=102)
    print("serverVersion:%s connectionTime:%s" % (app.serverVersion(),app.twsConnectionTime()))
    app.run()

if __name__ == "__main__":
    main()