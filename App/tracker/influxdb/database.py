# Файл для подключения и описания запросов на чтение к InfluxDB

from datetime import datetime
import influxdb_client
from .influxdb_config import org, url, token, bucket, measurement


client = influxdb_client.InfluxDBClient(url=url,
                                        token=token,
                                        org=org)
query_api = client.query_api()


def data_market(date: datetime):
    """
    Функция для предоставления информации на страницу market.
    Для работы требуется поднять сервер для работы с БД
    C:\Program Files\InfluxData\influxdb

    Возвращает данные по рынку в формате списка словарей или False в случае ошибки.

    Parameters:
    - date (datetime): Дата, для которой необходимо получить информацию.

    Returns:
    - list of dict: Список словарей с данными по рынку или пустой список, если данных нет.
    - False: В случае ошибки подключения к базе данных.
    """
    try:
        data = []

        # Даты начала и конца считывания данных формат:2021-05-22T23:30:00Z
        # В данном случае берется текущий день с промежутком с 00:00 до 23:59, чтобы захватить все временные точки
        date_from = date.strftime("%Y-%m-%dT00:00:00Z")
        date_to = date.strftime("%Y-%m-%dT23:59:00Z")

        # Формирование запроса
        query_market_by_ticker = f"""from(bucket: "{bucket}")
        |> range(start: {date_from}, stop: {date_to})
        |> filter(fn: (r) => r._measurement == "{measurement}")
        |> group(columns: ["_time", "TICKER"])
    """
        # Выполнение запроса и получение ответа
        tables = query_api.query(query_market_by_ticker, org=org)

        # Форматирование ответа для view в формат списка словарей
        for table in tables:
            data_dict = {
                "TICKER": table.records[0]["TICKER"],
                table.records[0]["_field"]: table.records[0]["_value"],
                table.records[1]["_field"]: table.records[1]["_value"],
                table.records[2]["_field"]: table.records[2]["_value"],
                table.records[3]["_field"]: table.records[3]["_value"],
                table.records[4]["_field"]: table.records[4]["_value"],
            }

            data.append(data_dict)

        return data

    except Exception as e:
        # Исключение при проблеме с подключением с БД
        return False


def data_security(exchange, ticker):
    try:
        data = []

        date_from = "1970-01-01T00:00:00Z"
        date_to = datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ")

        # Формирование запроса
        query_market_by_ticker = f"""from(bucket: "{bucket}")
        |> range(start: {date_from}, stop: {date_to})
        |> filter(fn: (r) => r["EXCHANGE"] == "{exchange.upper()}")
        |> filter(fn: (r) => r["TICKER"] == "{ticker}")
        |> filter(fn: (r) => r["_field"] == "CLOSE" or r["_field"] == "HIGH" or r["_field"] == "LOW" \
            or r["_field"] == "OPEN" or r["_field"] == "VALUE")
        |> group(columns: ["_time", "_measurement"])
    """
        # Выполнение запроса и получение ответа
        tables = query_api.query(query_market_by_ticker, org=org)

        # Форматирование ответа для view в формат списка списков [date, open, close, lowest, highest, value]
        for table in tables:
            data_row = [
                table.records[0]["_time"].strftime("%Y-%m-%d"),
                table.records[3]["_value"],
                table.records[0]["_value"],
                table.records[2]["_value"],
                table.records[1]["_value"],
                table.records[4]["_value"],
            ]

            data.append(data_row)

        return data

    except Exception as e:
        # Исключение при проблеме с подключением с БД
        return False
