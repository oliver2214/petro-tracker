import os
from dotenv import load_dotenv

# Загрузка переменных окружения из файла .env, если он существует
if os.path.exists(".env"):
    load_dotenv(".env")


class TimeseriesConfig:
    token = "rim6Bm2UQwCr0o6Z-JZfGcFc_ropA1VnDLsaT3S98uOAmrjbRcG0tCVvS9f18VcsG6Nx64-AJd78LbEiShQ6EQ=="
    org = "National University of Oil and Gas «Gubkin University»"
    url = "http://influxdb:8086"
    bucket = "PetroTrackerTSDB"
    measurement = "stock_data"
    trading_view_username = os.getenv("TV_USERNAME")
    trading_view_password = os.getenv("TV_PASSWORD")


API_TOKEN = "SECRETAPITOKEN_12309876"


class DatabaseConfig:
    dbname = os.getenv('DB_NAME', 'petrotracker_db')
    user = os.getenv('DB_USER', 'postgres')
    password = os.getenv('DB_PASSWORD', '12354lbvf')
    host = os.getenv('DB_HOST', 'db')
    port = int(os.getenv('DB_PORT', 5432))


db_config = DatabaseConfig()


DATABASE_CONFIG = {
    'dbname': db_config.dbname,
    'user': db_config.user,
    'password': db_config.password,
    'host': db_config.host,
    'port': db_config.port,
}
