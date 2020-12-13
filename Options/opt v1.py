from ibapi.client import EClient
from ibapi.wrapper import EWrapper
from ibapi.contract import Contract
from ibapi.order import *
from threading import Timer


class TradeFire1(EWrapper, EClient):

    def __init__(self):
        EClient.__init__(self, self)
        self.done = False
        self.nextOrderId = ""

    def error(self, reqId, errorCode, errorString):
        print("Error: ", reqId, " ", errorCode, " ", errorString)

    def nextValidId(self, orderId):
        self.nextOrderId = orderId
        self.start()

    def orderStatus(self, orderId, status, filled, remaining, avgFillPrice, permId, parentId, lastFillPrice, clientId,
                    whyHeld, mktCapPrice):
        print("OrderStatus. Id: ", orderId, ", Status: ", status, ", Filled:", filled, ", Remaining: ", remaining,
              ", LastFillPrice: ", lastFillPrice)

    def openOrder(self, orderId, contract, order, orderState):
        print("OpenOrder. ID:", orderId, contract.symbol, contract.secType, "@", contract.exchange, ":", order.action,
              order.orderType, order.totalQuantity, orderState.status)

    def execDetails(self, reqId, contract, execution):
        print("ExecDetails. ", reqId, contract.symbol, contract.secType, contract.currency, execution.execId,
              execution.orderId, execution.shares, execution.lastLiquidity)

    def buyStock(self, sym, qty, contract):
        print("Buy stock of X qty")
        contract.secType = "STK"
        contract.symbol = sym
        order = Order()
        order.totalQuantity = qty
        order.action = "SELL"
        order.orderType = "MKT"
        self.placeOrder(self.nextOrderId, contract, order)

    def sellCall(self, sym, expirationDate, strike, size, contract):
        contract.symbol = sym
        contract.secType = "OPT"
        contract.lastTradeDateOrContractMonth = expirationDate
        contract.strike = strike
        contract.right = "C"
        contract.multiplier = "100"
        order = Order()
        order.action = "SELL"
        order.totalQuantity = size
        order.orderType = "MKT"
        self.placeOrder(self.nextOrderId, contract, order)

    def start(self):
        # contract = Contract()
        # contract.exchange = "SMART"
        # contract.currency = "USD"
        # print("Buy Stock")
        # self.buyStock("TQQQ", 100, contract)

        contract = Contract()
        contract.exchange = "SMART"
        contract.currency = "USD"
        print("Sell call")
        self.sellCall("TQQQ", "20201204", 150, 1, contract)

    def stop(self):
        self.done = True
        self.disconnect()


def main():
    app1 = TradeFire1()
    app1.nextOrderId = 1
    app1.connect("127.0.0.1", 7497, 9)  # IB Gateway PaperTrading
    Timer(3, app1.stop).start()
    app1.run()


if __name__ == "__main__":
    main()
