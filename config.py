import os
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("TOKEN")
exchanges = ["exmo", "binance", "huobi"]
