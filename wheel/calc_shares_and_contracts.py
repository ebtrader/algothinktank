import pandas as pd
from ibapi.client import EClient
from ibapi.wrapper import EWrapper
from ibapi.contract import * # @UnusedWildImport
from ibapi.common import *  # @UnusedWildImport
from ibapi.ticktype import * # @UnusedWildImport
import math

class TestApp(EWrapper, EClient):
    def __init__(self):
        EWrapper.__init__(self)
        EClient.__init__(self, wrapper=self)
        self.contract = Contract()
        self.data = []
        self.df = pd.DataFrame()
        self.cash_value = 0
        self.recent_px = 0
        self.shares_to_buy = 0
        self.num_contracts = 0

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
        self.contract.symbol = 'NQ'
        self.contract.secType = 'FUT'
        self.contract.exchange = 'GLOBEX'
        self.contract.currency = 'USD'
        self.contract.lastTradeDateOrContractMonth = "202109"

        self.reqMktData(1002, self.contract, "", True, False, [])

    def tickPrice(self, reqId: TickerId, tickType: TickType, price: float,
                  attrib: TickAttrib):
        super().tickPrice(reqId, tickType, price, attrib)
        # print("TickPrice. TickerId:", reqId, "tickType:", tickType,
        #       "Price:", price, "CanAutoExecute:", attrib.canAutoExecute,
        #       "PastLimit:", attrib.pastLimit, end=' ')
        self.data.append([tickType, price])
        self.df = pd.DataFrame(self.data, columns=['TickType', 'Price'])

    def tickSize(self, reqId: TickerId, tickType: TickType, size: int):
        super().tickSize(reqId, tickType, size)
        # print("TickSize. TickerId:", reqId, "TickType:", tickType, "Size:", size)

    def tickSnapshotEnd(self, reqId: int):
        super().tickSnapshotEnd(reqId)
        print("TickSnapshotEnd. TickerId:", reqId)
        self.get_px()

    def get_px(self):
        print(self.df)
        self.recent_px = self.df.loc[0, 'Price']
        print(f'recent price: {self.recent_px}')
        self.accountOperations_req()

    def accountOperations_req(self):
        # Requesting accounts' summary
        # ! [reqaaccountsummary]
        self.reqAccountSummary(9002, "All", "$LEDGER")
        # ! [reqaaccountsummary]

        # ! [accountsummary]

    def accountSummary(self, reqId: int, account: str, tag: str, value: str,
                       currency: str):
        super().accountSummary(reqId, account, tag, value, currency)
        # print("AccountSummary. ReqId:", reqId, "Account:", account,
        #       "Tag: ", tag, "Value:", value, "Currency:", currency)
        self.data.append([tag, value])
        self.df = pd.DataFrame(self.data, columns=['Account', 'Value'])

    def accountSummaryEnd(self, reqId: int):
        super().accountSummaryEnd(reqId)
        print("AccountSummaryEnd. ReqId:", reqId)
        self.get_cash()

    def get_cash(self):
        print(self.df)
        self.df.to_csv('acct_value.csv')
        self.cash_value = self.df.loc[self.df['Account'] == 'CashBalance', 'Value'].iloc[0]
        print(f'cash value: {self.cash_value}')
        self.calc_contracts()

    def calc_contracts(self):
        num_shares = float(self.cash_value) / (self.recent_px / 100)
        safety_num_shares = 0.75 * num_shares
        self.shares_to_buy = math.floor(safety_num_shares / 100) * 100
        print(f'shares to buy: {self.shares_to_buy}')
        self.num_contracts = self.shares_to_buy / 100
        print(f'number of contracts: {self.num_contracts}')

        self.disconnect()

def main():
    app = TestApp()
    app.connect("127.0.0.1", port=7497, clientId=102)
    print("serverVersion:%s connectionTime:%s" % (app.serverVersion(),app.twsConnectionTime()))
    app.run()

if __name__ == "__main__":
    main()