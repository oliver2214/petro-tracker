import os
from dotenv import load_dotenv

load_dotenv()

token = os.environ.get("INFLUXDB_TOKEN")
org = "National University of Oil and Gas «Gubkin University»"
url = "http://127.0.0.1:8086"
bucket = "TSDB1"
"PetroTrackerTSDB"
measurement = "stock_data"

trading_view_username = os.getenv("TV_USERNAME")
trading_view_password = os.getenv("TV_PASSWORD")
