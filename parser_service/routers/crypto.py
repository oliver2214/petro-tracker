from pybit.unified_trading import HTTP
from datetime import datetime

from parser_service.config import TimeseriesConfig, bybit_config

def process_crypto(client, write_api, startdate_ms, enddate_ms):
    exchange_data_strings = []
    session = HTTP(
        testnet=False,
        api_key=bybit_config.api_key,
        api_secret=bybit_config.api_secret,
    )

    tickers=session.get_tickers(
        category="spot",
    )

    for t in tickers['result']['list']:
        history = session.get_kline(
            category="spot",
            symbol=t["symbol"],
            interval="D",
            start=startdate_ms,
            end=enddate_ms,
        )

        exchange_data_strings.extend(get_symbol_data_strings(symbol_data=history['result']))

    write_api.write(bucket=TimeseriesConfig.bucket, org=TimeseriesConfig.org,
        record="\n".join(exchange_data_strings))


def get_symbol_data_strings(symbol_data):
    symbol_data_strings = []
    for row in symbol_data['list']:
        line = f'{TimeseriesConfig.measurement},EXCHANGE=BYBIT{symbol_data['category'].upper()},TICKER={symbol_data['symbol']} VALUE={row[5]},OPEN={row[1]},LOW={row[3]},HIGH={row[2]},CLOSE={row[4]} {row[0]+"000000"}'
        symbol_data_strings.append(line)
    return symbol_data_strings
