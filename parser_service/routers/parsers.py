from datetime import datetime
from typing import Annotated
from fastapi import APIRouter, HTTPException, Header, status
import influxdb_client
from influxdb_client.client.write_api import SYNCHRONOUS
from tvDatafeed import TvDatafeed, Interval
from config import API_TOKEN, bucket, measurement, org, url, token, trading_view_password, trading_view_username
from schemes.parser_schemes import ParseResponse, ParseRequest

router = APIRouter()

tv = TvDatafeed(password=trading_view_password, username=trading_view_username)


def get_symbol_data_strings(symbol_data):
    symbol_data_strings = []
    for index, row in symbol_data.iterrows():
        exchange, symbol = row["symbol"].split(":")
        timestamp = int(row.name.timestamp() * 1e9)
        line = f'{measurement},EXCHANGE={exchange},TICKER={symbol} VALUE={row["volume"]},OPEN={row["open"]},LOW={row["low"]},HIGH={row["high"]},CLOSE={row["close"]} {timestamp}'
        symbol_data_strings.append(line)
    return symbol_data_strings


@router.post("/parse_historic_data/", response_model=ParseResponse, status_code=status.HTTP_201_CREATED)
def parse_historic_data(request: ParseRequest,
                        api_token: Annotated[str, Header()] = None):

    if api_token != API_TOKEN:
        raise HTTPException(status_code=401, detail="Unauthorized")

    client = influxdb_client.InfluxDBClient(url=url, token=token, org=org)
    write_api = client.write_api(write_options=SYNCHRONOUS)

    exchanges = {
        "MOEX": ["BANE", "BANEP", "VJGZ", "VJGZP", "GAZP", "RTGZ", "RTGZ", "EUTR", "LKOH", "MFGS", "MFGSP", "NVTK", "CHGZ", "ROSN", "RNFT", "KRKN", "KRKNP", "JNOSP", "JNOS", "SNGS", "SNGSP", "TATN", "TATNP", "TRNFP", "YAKG"],
        "NASDAQ": ["ACDC", "APA", "ARLP", "BANL", "BRY", "CHK", "CHKEL", "CHKEW", "CHKEZ", "CHRD", "CLMT", "DMLP", "DWSN", "EPSN", "FANG", "HPK", "HPKEW", "MARPS", "NEXT", "PAA", "PAGP", "PFIE", "PNRG", "PRTG", "PTEN", "RCON", "USEG", "VNOM"],
        "SSE": ["601918", "600688", "601015", "600121", "600256", "600997", "601857", "600971", "601101", "605090", "600395", "600546", "601011", "600968", "600985", "600123", "600777", "601898", "601666", "600348", "600758", "601001", "601699", "601225", "600180", "601088", "600938", "600792", "900948", "600725", "600740", "600508", "603619", "600403", "600188"]
    }
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
            write_api.write(bucket=bucket, org=org, record="\n".join(exchange_data_strings))

    client.close()

    if lost_exchanges:
        return ParseResponse(status="partial success", lost_exchanges=lost_exchanges)
    return ParseResponse(status="success")


@router.delete("/clear_data/", status_code=status.HTTP_204_NO_CONTENT)
def clear_bucket_by_measurement(start: datetime = "1970-01-01T00:00:00Z",
                                stop: datetime = datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ"),
                                api_token: Annotated[str, Header()] = None):

    if api_token != API_TOKEN:
        raise HTTPException(status_code=401, detail="Unauthorized")

    try:
        client = influxdb_client.InfluxDBClient(url=url, token=token, org=org)
        delete_api = client.delete_api()

        delete_api.delete(start, stop, f'_measurement={measurement}', bucket=bucket, org=org)
        client.close()

    except Exception as e:
        client.close()
        raise HTTPException(status_code=500)
