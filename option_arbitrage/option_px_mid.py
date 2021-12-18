import pandas as pd
from ibapi.client import EClient
from ibapi.wrapper import EWrapper
from ibapi.contract import * # @UnusedWildImport
from ibapi.common import *  # @UnusedWildImport
from ibapi.ticktype import * # @UnusedWildImport

# available tick types
# https://interactivebrokers.github.io/tws-api/tick_types.html
# https://cmdlinetips.com/2018/01/how-to-create-pandas-dataframe-from-multiple-lists/

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
        self.dict = {}
        self.df = pd.DataFrame()
        self.tick1 = 3004   # NQ bid
        self.tick2 = 3005   # NQ ask
        self.tick3 = 3006   # ES bid
        self.tick4 = 3007   # ES ask
        self.NQ_bid = 0
        self.NQ_ask = 0
        self.ES_bid = 0
        self.ES_ask = 0
        self.NQ_mid = 0
        self.ES_mid = 0

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

    def assign_variables(self, reqId, close: float):
        if reqId == self.tick1:
            self.NQ_bid = close
        elif reqId == self.tick2:
            self.NQ_ask = close
        elif reqId == self.tick3:
            self.ES_bid = close
        elif reqId == self.tick4:
            self.ES_ask = close
        else:
            print("Error")

    def calculate_mid_px(self):
        self.NQ_mid = (self.NQ_bid + self.NQ_ask) / 2
        self.ES_mid = (self.ES_bid + self.ES_ask) / 2

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

        # self.reqRealTimeBars(3002, self.contract, 5, "BID", True, [])
        # self.reqRealTimeBars(3003, self.contract, 5, "ASK", True, [])
        self.reqRealTimeBars(self.tick1, self.contract, 5, "BID", False, []) # False for after-hours and True for market hours
        self.reqRealTimeBars(self.tick2, self.contract, 5, "ASK", False,[])  # False for after-hours and True for market hours
        self.reqRealTimeBars(self.tick3, self.contract1, 5, "BID", False, []) # False for after-hours and True for market hours
        self.reqRealTimeBars(self.tick4, self.contract1, 5, "ASK", False, [])  # False for after-hours and True for market hours

    def realtimeBar(self, reqId: TickerId, time: int, open_: float, high: float, low: float, close: float,
                    volume: int, wap: float, count: int):
        super().realtimeBar(reqId, time, open_, high, low, close, volume, wap, count)
        # print("RealTimeBar. TickerId:", reqId, RealTimeBar(time, -1, open_, high, low, close, volume, wap, count), self.data1, self.data, self.dict)
        # print("RealTimeBar. TickerId:", reqId, RealTimeBar(time, -1, open_, high, low, close, volume, wap, count),
        #       f'NQ_bid: {self.NQ_bid} NQ_ask: {self.NQ_ask} ES_bid: {self.ES_bid} ES_ask: {self.ES_ask}' )
        print("TickerId:", reqId,
              f'NQ_mid: {self.NQ_mid} NQ_bid: {self.NQ_bid} NQ_ask: {self.NQ_ask} ES_mid: {self.ES_mid} ES_bid: {self.ES_bid} ES_ask: {self.ES_ask}')

        self.assign_variables(reqId, close)
        self.calculate_mid_px()

    # ! [realtimebar]

def main():
    app = TestApp()
    app.connect("127.0.0.1", port=7497, clientId=102)
    print("serverVersion:%s connectionTime:%s" % (app.serverVersion(),app.twsConnectionTime()))
    app.run()

if __name__ == "__main__":
    main()