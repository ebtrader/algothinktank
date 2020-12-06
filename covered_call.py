from ibapi.client import EClient
from ibapi.wrapper import EWrapper
from ibapi.contract import Contract
from ibapi.order import *
from ibapi.utils import iswrapper

import threading
import time


class IBapi(EWrapper, EClient):
    def __init__(self):
        EClient.__init__(self, self)

    @iswrapper

    def nextValidId(self, orderId: int):
        super().nextValidId(orderId)
        self.nextorderId = orderId
        print('The next valid order id is: ', self.nextorderId)

    def orderStatus(self, orderId, status, filled, remaining, avgFullPrice, permId, parentId, lastFillPrice, clientId,
                    whyHeld, mktCapPrice):
        print('orderStatus - orderid:', orderId, 'status:', status, 'filled', filled, 'remaining', remaining,
              'lastFillPrice', lastFillPrice)

    def openOrder(self, orderId, contract, order, orderState):
        print('openOrder id:', orderId, contract.symbol, contract.secType, '@', contract.exchange, ':', order.action,
              order.orderType, order.totalQuantity, orderState.status)

    def execDetails(self, reqId, contract, execution):
        print('Order Executed: ', reqId, contract.symbol, contract.secType, contract.currency, execution.execId,
              execution.orderId, execution.shares, execution.lastLiquidity)


def run_loop():
    app.run()


app = IBapi()
app.connect('127.0.0.1', 7497, 123)

app.nextorderId = None

# Start the socket in a thread
api_thread = threading.Thread(target=run_loop, daemon=True)
api_thread.start()

# Check if the API is connected via orderid
while True:
    if isinstance(app.nextorderId, int):
        print('connected')
        print()
        break
    else:
        print('waiting for connection')
        time.sleep(1)


# Create order object - BUY AAPL STOCK QTY-100 -MKT ORDER
order = Order()
order.action = 'BUY'
order.totalQuantity = 100
order.orderType = 'MKT'
contract = Contract()
contract.symbol = 'AAPL'
contract.secType = 'STK'
contract.exchange = 'SMART'
contract.currency = 'USD'


# place order
app.placeOrder(app.nextorderId,contract, order)
app.nextorderId += 1

time.sleep(3)



# Create order object MKT order options-- SELL AAPL OPTIONS STRIKE 124 12/04 CALL
order = Order()
order.action = 'SELL'
order.totalQuantity = 1
order.orderType = 'MKT'
contract = Contract()
contract.symbol = 'AAPL'
contract.secType = 'OPT'
contract.exchange = 'SMART'
contract.currency = 'USD'
contract.lastTradeDateOrContractMonth = '20201211'
contract.strike = 124
contract.right = 'C'
contract.multiplier = '100'

# place order
app.placeOrder(app.nextorderId,contract, order)

app.nextorderId += 1

time.sleep(3)

# cancel order
# print('cancelling order')
# app.cancelOrder(app.nextorderId)

time.sleep(3)
app.disconnect()