import os
from dotenv import load_dotenv

load_dotenv()

token = os.environ.get("INFLUXDB_TOKEN")
org = "National University of Oil and Gas «Gubkin University»"
url = "http://127.0.0.1:8086"
bucket = "PetroTrackerTSDB"
measurement = "stock_data"

if os.path.exists(".env"):
    trading_view_username = os.getenv("TV_USERNAME")
    trading_view_password = os.getenv("TV_PASSWORD")
else:
    trading_view_username = None
    trading_view_password = None

API_TOKEN = "SECRETAPITOKEN_12309876"
