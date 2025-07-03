from fastapi import FastAPI, WebSocket
from app.models import Order
from app.order_book import OrderBook
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import json

app = FastAPI()
order_book = OrderBook()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/submit_order")
async def submit_order(order: Order):
    trades = order_book.match_order(order)
    return {"trades": [trade.dict() for trade in trades]}

@app.get("/bbo/{symbol}")
async def get_bbo(symbol: str):
    bid, ask = order_book.get_bbo()
    return {"symbol": symbol, "best_bid": bid, "best_ask": ask}

@app.get("/order_book/{symbol}")
async def order_book_depth(symbol: str):
    depth = order_book.get_order_book_depth()
    return {"symbol": symbol, **depth}

@app.websocket("/ws/market_data")
async def market_data_stream(websocket: WebSocket):
    await websocket.accept()
    while True:
        depth = order_book.get_order_book_depth()
        await websocket.send_text(json.dumps({
            "symbol": "BTC-USDT",
            "asks": depth["asks"],
            "bids": depth["bids"]
        }))
