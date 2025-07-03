from collections import deque, defaultdict
from app.models import Order, Trade
from uuid import uuid4
from datetime import datetime

class OrderBook:
    def __init__(self):
        self.bids = defaultdict(deque)
        self.asks = defaultdict(deque)
        self.trades = []

    def get_bbo(self):
        best_bid = max(self.bids.keys(), default=None)
        best_ask = min(self.asks.keys(), default=None)
        return best_bid, best_ask

    def match_order(self, order: Order):
        trades = []
        book = self.bids if order.side == "sell" else self.asks
        opposing_book = self.asks if order.side == "buy" else self.bids
        sorted_prices = sorted(opposing_book.keys(), reverse=(order.side == "buy"))

        quantity_remaining = order.quantity

        for price in sorted_prices:
            if (order.side == "buy" and order.order_type != "market" and price > order.price) or                (order.side == "sell" and order.order_type != "market" and price < order.price):
                break

            level_orders = opposing_book[price]
            while level_orders and quantity_remaining > 0:
                existing_order = level_orders[0]
                traded_qty = min(quantity_remaining, existing_order.quantity)
                trade = Trade(
                    trade_id=str(uuid4()),
                    symbol=order.symbol,
                    price=price,
                    quantity=traded_qty,
                    aggressor_side=order.side,
                    maker_order_id=existing_order.order_id,
                    taker_order_id=order.order_id,
                    timestamp=datetime.utcnow().isoformat()
                )
                trades.append(trade)
                self.trades.append(trade)

                quantity_remaining -= traded_qty
                existing_order.quantity -= traded_qty

                if existing_order.quantity <= 0:
                    level_orders.popleft()
            if quantity_remaining <= 0:
                break

        if order.order_type == "limit" and quantity_remaining > 0:
            order.quantity = quantity_remaining
            if order.side == "buy":
                self.bids[order.price].append(order)
            else:
                self.asks[order.price].append(order)

        return trades

    def get_order_book_depth(self):
        return {
            "asks": [[price, sum(order.quantity for order in orders)]
                     for price, orders in sorted(self.asks.items())][:10],
            "bids": [[price, sum(order.quantity for order in orders)]
                     for price, orders in sorted(self.bids.items(), reverse=True)][:10]
        }
