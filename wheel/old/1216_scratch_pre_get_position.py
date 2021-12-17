# ibkr packages
from ibapi.client import EClient
from ibapi.wrapper import EWrapper
# types
from ibapi.contract import * # @UnusedWildImport
from ibapi.order import Order
from ibapi.common import *  # @UnusedWildImport
from ibapi.ticktype import * # @UnusedWildImport
# other packages
import pandas as pd
from datetime import datetime, date, timedelta
import math
import pause
import time

STOCK_SYMBOL = 'QQQ'
PERCENTAGE_OF_CASH_TO_USE = 0.4

DESIGNATED_DAY_TO_MAKE_THE_TRADE = 1 # 0=Mon, 1=Tues, 2=Wed, 3=Thu, 4=Fri
TRADE_EXECUTION_HOUR = 8
TRADE_EXECUTION_MIN = 9
TRADE_EXECUTION_SEC = 45

class TestApp(EWrapper, EClient):
    def __init__(self):
        EWrapper.__init__(self)
        EClient.__init__(self, wrapper=self)

        # this is for trading
        self.nextValidOrderId = None
        self.permId2ord = {}

        # this is for calcs of share and contracts
        self.contract = Contract()
        self.CallContract = Contract()
        self.data_px = []
        self.data = []
        self.df_px = pd.DataFrame()
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

    def next_weekday(self, weekday):  # 0=Mon, 1=Tues, 2=Wed, 3=Thu, 4=Fri
        d = date.today()
        days_ahead = weekday - d.weekday()

        if days_ahead < 0:  # target day already happened this week also try <=
            days_ahead += 7

        return d + timedelta(days_ahead)

    def start(self):
        # calculate next Monday/weekday
        next_weekday = self.next_weekday(DESIGNATED_DAY_TO_MAKE_THE_TRADE) # 0=Mon, 1=Tues, 2=Wed, 3=Thu, 4=Fri
        year = next_weekday.year
        month = next_weekday.month
        day = next_weekday.day

        # pause until trigger time on coming Monday/weekday
        print("Pausing until designated trade time...")
        pause.until(datetime(year, month, day, TRADE_EXECUTION_HOUR, TRADE_EXECUTION_MIN, TRADE_EXECUTION_SEC))
        self.tickDataOperations_req()

    def tickDataOperations_req(self):
        self.contract.symbol = STOCK_SYMBOL
        self.contract.secType = 'STK'
        self.contract.exchange = 'SMART'
        self.contract.currency = 'USD'

        self.reqMktData(1002, self.contract, "", True, False, [])

    def tickPrice(self, reqId: TickerId, tickType: TickType, price: float,
                  attrib: TickAttrib):
        super().tickPrice(reqId, tickType, price, attrib)
        # print("TickPrice. TickerId:", reqId, "tickType:", tickType,
        #       "Price:", price, "CanAutoExecute:", attrib.canAutoExecute,
        #       "PastLimit:", attrib.pastLimit, end=' ')
        self.data_px.append([tickType, price])
        self.df_px = pd.DataFrame(self.data_px, columns=['TickType', 'Price'])

    def tickSize(self, reqId: TickerId, tickType: TickType, size: int):
        super().tickSize(reqId, tickType, size)
        # print("TickSize. TickerId:", reqId, "TickType:", tickType, "Size:", size)

    def tickSnapshotEnd(self, reqId: int):
        super().tickSnapshotEnd(reqId)
        print("TickSnapshotEnd. TickerId:", reqId)
        self.get_px()

    def get_px(self):
        print(self.df_px)
        self.recent_px = self.df_px.loc[self.df_px['TickType'] == 4, 'Price'].iloc[0]
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
        # print("AccountSummaryEnd. ReqId:", reqId)
        self.get_cash()

    def get_cash(self):
        # print(self.df)
        # self.df.to_csv('acct_value.csv')
        self.cash_value = self.df.loc[self.df['Account'] == 'CashBalance', 'Value'].iloc[0]
        print(f'cash value: {self.cash_value}')
        self.calc_contracts()

    def calc_contracts(self):
        num_shares = float(self.cash_value) / (self.recent_px) # get rid of  / 100
        percentage_of_cash_to_use = PERCENTAGE_OF_CASH_TO_USE
        safety_num_shares = percentage_of_cash_to_use * num_shares # this is percentage of cash
        self.shares_to_buy = math.floor(safety_num_shares / 100) * 100
        print(f'shares to buy: {self.shares_to_buy}')
        self.num_contracts = self.shares_to_buy / 100
        print(f'number of contracts: {self.num_contracts}')
        self.check_and_send_order()

    def sendOrder(self, action):
        order = Order()
        order.action = action
        order.totalQuantity = self.shares_to_buy
        # order.orderType = "MKT"

        # use these next 2 lines for limit orders
        order.orderType = "LMT"
        order.lmtPrice = self.recent_px

        self.placeOrder(self.nextOrderId(), self.contract, order)

    def sendCallOrder(self, action):
        # calculate the strike
        strike = int(self.recent_px)

        # calculate coming fri expiration
        next_friday = self.next_weekday(4)  # 0=Mon, 1=Tues, 2=Wed, 3=Thu, 4=Fri
        year = next_friday.year
        month = next_friday.month
        day = next_friday.day
        coming_fri_expiration = str(year) + str(month) + str(day)

        self.CallContract.symbol = STOCK_SYMBOL
        self.CallContract.secType = 'OPT'
        self.CallContract.exchange = 'SMART'
        self.CallContract.currency = 'USD'
        self.CallContract.lastTradeDateOrContractMonth = coming_fri_expiration
        self.CallContract.strike = str(strike)
        self.CallContract.right = "C"
        self.CallContract.multiplier = "100"

        order = Order()
        order.action = action
        order.totalQuantity = self.num_contracts
        # order.orderType = "MKT"

        # use these next 2 lines for limit orders
        order.orderType = "LMT"
        order.lmtPrice = 1

        self.placeOrder(self.nextOrderId(), self.CallContract, order)

    def check_and_send_order(self):
        self.sendOrder('BUY')
        time.sleep(5)
        self.sendCallOrder('SELL')

        self.disconnect()

def main():
    app = TestApp()
    app.connect("127.0.0.1", port=7497, clientId=102)
    print("serverVersion:%s connectionTime:%s" % (app.serverVersion(),app.twsConnectionTime()))
    app.run()

if __name__ == "__main__":
    main()