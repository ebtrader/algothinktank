from ibapi.client import EClient
from ibapi.wrapper import EWrapper
# types
from ibapi.contract import * # @UnusedWildImport
from ibapi.order import Order
from datetime import datetime
import pause

# https://stackoverflow.com/questions/11523918/python-start-a-function-at-given-time
# https://stackoverflow.com/questions/15088037/python-script-to-do-something-at-the-same-time-every-day

class TestApp(EWrapper, EClient):
    def __init__(self):
        EWrapper.__init__(self)
        EClient.__init__(self, wrapper=self)
        self.nextValidOrderId = None
        self.permId2ord = {}
        self.contract = Contract()

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
        self.check_and_send_order()
        print("Executing requests ... finished")

    def sendOrder(self, action):
        # Create contract object
        self.contract.symbol = 'TQQQ'
        self.contract.secType = 'OPT'
        self.contract.exchange = 'SMART'
        self.contract.currency = 'USD'
        self.contract.lastTradeDateOrContractMonth = "20210827"
        self.contract.strike = 135
        self.contract.right = "C"
        self.contract.multiplier = "100"

        order = Order()
        order.action = action
        order.totalQuantity = 1
        order.orderType = "MKT"
        self.placeOrder(self.nextOrderId(), self.contract, order)

    def check_and_send_order(self):
        pause.until(datetime(2021, 8, 22, 18, 31, 0))  # this is the time at which you can buy shares
        self.sendOrder('SELL')
        pause.until(datetime(2021, 8, 22, 18, 31, 15))
        self.sendOrder('SELL')
        self.disconnect()

def main():
    app = TestApp()
    app.connect("127.0.0.1", port=7497, clientId=108)
    print("serverVersion:%s connectionTime:%s" % (app.serverVersion(),app.twsConnectionTime()))
    app.run()

if __name__ == "__main__":
    main()