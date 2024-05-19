from datetime import datetime
from typing import Annotated

from fastapi import APIRouter, HTTPException, Header, status
import influxdb_client
from influxdb_client.client.write_api import SYNCHRONOUS
from tvDatafeed import TvDatafeed, Interval

from config import API_TOKEN, TimeseriesConfig
from db.queries import get_exchanges_and_securities
from schemes.parser_schemes import ParseResponse, ParseRequest

router = APIRouter()

tv = TvDatafeed(password=TimeseriesConfig.trading_view_password, username=TimeseriesConfig.trading_view_username)


def get_symbol_data_strings(symbol_data):
    symbol_data_strings = []
    for index, row in symbol_data.iterrows():
        exchange, symbol = row["symbol"].split(":")
        timestamp = int(row.name.timestamp() * 1e9)
        line = f'{TimeseriesConfig.measurement},EXCHANGE={exchange},TICKER={symbol} VALUE={row["volume"]},OPEN={row["open"]},LOW={row["low"]},HIGH={row["high"]},CLOSE={row["close"]} {timestamp}'
        symbol_data_strings.append(line)
    return symbol_data_strings


@router.post("/parse_historic_data/", response_model=ParseResponse, status_code=status.HTTP_201_CREATED)
def parse_historic_data(request: ParseRequest,
                        api_token: Annotated[str, Header()] = None):
    try:
        if api_token != API_TOKEN:
            raise HTTPException(status_code=401, detail="Unauthorized")

        client = influxdb_client.InfluxDBClient(url=TimeseriesConfig.url, token=TimeseriesConfig.token,
                                                org=TimeseriesConfig.org)
        write_api = client.write_api(write_options=SYNCHRONOUS)

        exchanges = get_exchanges_and_securities()
        lost_exchanges = dict()

        for exchange in exchanges.keys():
            lost_symbols = []
            exchange_data_strings = []
            for symbol in exchanges[exchange]:
                symbol_data = None
                lost_counter = 0
                while (symbol_data is None or symbol_data.empty) and lost_counter < 3:
                    symbol_data = tv.get_hist(symbol=symbol, exchange=exchange, interval=Interval.in_daily, n_bars=request.n_bars)
                    lost_counter += 1

                if lost_counter == 3:
                    lost_symbols.append(symbol)
                else:
                    exchange_data_strings.extend(get_symbol_data_strings(symbol_data=symbol_data))

            if lost_symbols:
                lost_exchanges[exchange] = lost_symbols
            if exchange_data_strings:
                write_api.write(bucket=TimeseriesConfig.bucket, org=TimeseriesConfig.org,
                                record="\n".join(exchange_data_strings))

        client.close()

        if lost_exchanges:
            return ParseResponse(status="partial success", lost_exchanges=lost_exchanges)
        return ParseResponse(status="success")

    except Exception as e:
        client.close()
        raise HTTPException(status_code=500)


@router.delete("/clear_data/", status_code=status.HTTP_204_NO_CONTENT)
def clear_bucket_by_measurement(start: datetime = "1970-01-01T00:00:00Z",
                                stop: datetime = datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ"),
                                api_token: Annotated[str, Header()] = None):

    if api_token != API_TOKEN:
        raise HTTPException(status_code=401, detail="Unauthorized")

    try:
        client = influxdb_client.InfluxDBClient(url=TimeseriesConfig.url,
                                                token=TimeseriesConfig.token, org=TimeseriesConfig.org)
        delete_api = client.delete_api()

        delete_api.delete(start, stop, f'_measurement={TimeseriesConfig.measurement}',
                          bucket=TimeseriesConfig.bucket, org=TimeseriesConfig.org)
        client.close()

    except Exception as e:
        client.close()
        raise HTTPException(status_code=500)
