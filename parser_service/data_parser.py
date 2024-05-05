from influxdb_client.client.write_api import SYNCHRONOUS
import influxdb_client
from tvDatafeed import TvDatafeed, Interval

from influxdb_config import bucket, measurement, org, token, url, trading_view_password, trading_view_username


tv = TvDatafeed(password=trading_view_password, username=trading_view_username)
client = influxdb_client.InfluxDBClient(url=url,
                                        token=token,
                                        org=org)


def get_symbol_data_strings(symbol_data):
    symbol_data_strings = []
    for index, row in symbol_data.iterrows():
        exchange, symbol = row["symbol"].split(":")
        timestamp = int(row.name.timestamp() * 1e9)
        line = f'{measurement},EXCHANGE={exchange},TICKER={symbol} VALUE={row["volume"]},OPEN={row["open"]},LOW={row["low"]},HIGH={row["high"]},CLOSE={row["close"]} {timestamp}' # noqa
        # добавляем эту строку в общий запрос. В конечном итоге получаем один большой запрос на запись данных
        symbol_data_strings.append(line)

    return symbol_data_strings


def print_lost_exchanges(lost_exchanges):
    for exchange in lost_exchanges.keys():
        for symbol in lost_exchanges[exchange]:
            print(f"{exchange}:{symbol}")


def parse_data():
    write_api = client.write_api(write_options=SYNCHRONOUS)

    # пока нет Postgresql, где будут хранится биржи и их акции, использую словарь бирж(ключ) и их списка акций(значение)
    exchanges = {
        "MOEX": ["BANE", "BANEP", "VJGZ", "VJGZP", "GAZP", "RTGZ", "RTGZ", "EUTR", "LKOH", "MFGS", "MFGSP",
                 "NVTK", "CHGZ", "ROSN", "RNFT", "KRKN", "KRKNP", "JNOSP", "JNOS", "SNGS", "SNGSP", "TATN",
                 "TATNP", "TRNFP", "YAKG"],
        "NASDAQ": ["ACDC", "APA", "ARLP", "BANL", "BRY", "CHK", "CHKEL", "CHKEW", "CHKEZ", "CHRD", "CLMT",
                   "DMLP", "DWSN", "EPSN", "FANG", "HPK", "HPKEW", "MARPS", "NEXT", "PAA", "PAGP", "PFIE",
                   "PNRG", "PRTG", "PTEN", "RCON", "USEG", "VNOM"],
        "SSE": ["601918", "600688", "601015", "600121", "600256", "600997", "601857", "600971", "601101",
                "605090", "600395", "600546", "601011", "600968", "600985", "600123", "600777", "601898",
                "601666", "600348", "600758", "601001", "601699", "601225", "600180", "601088", "600938",
                "600792", "900948", "600725", "600740", "600508", "603619", "600403", "600188"]
    }
    lost_exchanges = dict()

    for exchange in exchanges.keys():
        lost_symbols = []
        exchange_data_strings = []  # список строк для БД, каждая содержит одну метку данных
        for symbol in exchanges[exchange]:
            symbol_data = None
            lost_counter = 0
            while (symbol_data is None or symbol_data.empty) and lost_counter < 3:
                symbol_data = tv.get_hist(symbol=symbol, exchange=exchange, interval=Interval.in_daily, n_bars=60)

            if lost_counter == 3:
                lost_symbols.append(symbol)
            else:
                exchange_data_strings.extend(get_symbol_data_strings(symbol_data=symbol_data))

        if lost_symbols:
            lost_exchanges[exchange] = lost_symbols
        write_api.write(bucket=bucket, org=org, record="\n".join(exchange_data_strings))

    client.close()

    print_lost_exchanges(lost_exchanges=lost_exchanges)


def clear_bucket_by_measurement():
    delete_api = client.delete_api()

    start = "1970-01-01T00:00:00Z"
    stop = "2024-05-05T00:00:00Z"
    delete_api.delete(start, stop, f'_measurement={measurement}', bucket=bucket, org=org)

    client.close()


if __name__ == "__main__":
    parse_data()
