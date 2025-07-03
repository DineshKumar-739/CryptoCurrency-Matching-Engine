# CryptoCurrency-Matching-Engine


## How to Run

1. Install dependencies:

```bash
pip install -r requirements.txt
```

2. Run the app:

```bash
uvicorn app.main:app --reload
```

3. Endpoints:
- POST `/submit_order`
- GET `/bbo/{symbol}`
- GET `/order_book/{symbol}`
- WebSocket: `/ws/market_data`

## Developed for Assignment:
- REG NMS-based matching logic
- Price-time priority
- BBO calculation
- Real-time WebSocket for order book
