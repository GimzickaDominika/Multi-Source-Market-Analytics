import json
import time
import websocket
from kafka import KafkaProducer

FINNHUB_TOKEN = "token"
WS_URL = f"wss://ws.finnhub.io?token={FINNHUB_TOKEN}"

KAFKA_BOOTSTRAP = "localhost:9092"
TOPIC = "finnhub_trades"
SYMBOLS = [
    "AAPL",              # Apple
    "AMZN",              # Amazon
    "BINANCE:BTCUSDT",   # Bitcoin (Binance)
    "IC MARKETS:1",      # Twój istniejący symbol
    "BINANCE:ETHUSDT",   # Ethereum (Binance)
    "NVDA",              # NVIDIA
    "BRK.B",             # Berkshire Hathaway (Klasa B)
    "INTC",              # Intel
    "AMD"                # AMD
]
#SYMBOLS = ["AAPL", "AMZN", "BINANCE:BTCUSDT", "IC MARKETS:1"]

producer = KafkaProducer(
    bootstrap_servers=KAFKA_BOOTSTRAP,
    value_serializer=lambda v: json.dumps(v).encode("utf-8"),
    acks="all",
    retries=5,
    linger_ms=20,
)

def on_message(ws, message: str):
    try:
        payload = json.loads(message)
    except Exception:
        print("Not-JSON message:", message)
        return

    msg_type = payload.get("type")

    if msg_type == "ping":
        return

    # we want only trade messages
    if msg_type == "trade" and "data" in payload:
        for trade in payload["data"]:
            rowkey = f"{trade.get('s')}|{trade.get('t')}|{int(time.time()*1000)}"

            event = {
                "rowkey": rowkey,
                "source": "finnhub",
                "event_type": "trade",
                "received_at_ms": int(time.time() * 1000),
                "symbol": trade.get("s"),
                "price": trade.get("p"),
                "volume": trade.get("v"),
                "trade_ts_ms": trade.get("t"),
                "conditions": trade.get("c"),
                "raw": trade
            }

            # event = {
            #     "source": "finnhub",
            #     "event_type": "trade",
            #     "received_at_ms": int(time.time() * 1000),
            #     "symbol": trade.get("s"),
            #     "price": trade.get("p"),
            #     "volume": trade.get("v"),
            #     "trade_ts_ms": trade.get("t"),
            #     "conditions": trade.get("c"),
            #     "raw": trade,
            # }

            producer.send(TOPIC, value=event)
        producer.flush()

def on_error(ws, error):
    print("WS error:", error)


def on_close(ws, close_status_code, close_msg):
    print(f"### closed ### status={close_status_code}, msg={close_msg}")

def on_open(ws):
    for sym in SYMBOLS:
        ws.send(json.dumps({"type": "subscribe", "symbol": sym}))
    print("Subscribed:", SYMBOLS)

if __name__ == "__main__":
    websocket.enableTrace(False) #debugging off
    ws = websocket.WebSocketApp(
        WS_URL,
        on_open=on_open,
        on_message=on_message,
        on_error=on_error,
        on_close=on_close,
    )
    ws.run_forever(ping_interval=30, ping_timeout=10)
