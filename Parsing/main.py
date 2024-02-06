from datetime import datetime, timedelta
import calendar
import influxdb_client
import parsers.parser1
from influxdb_config import org, url, token
from influxdb_client.client.write_api import SYNCHRONOUS


client = influxdb_client.InfluxDBClient(url=url,
                                        token=token,
                                        org=org)


bucket = "PetroTrackerTSDB"
measurement = "stock_data"


def main():
    write_api = client.write_api(write_options=SYNCHRONOUS)

    date_from = datetime(2023, 1, 1)
    date_to = datetime(2024, 2, 7)
    month = date_from.month
    day = date_from.day

    for year in range(date_from.year, date_to.year + 1):
        month = date_from.month if year == date_from.year else 1
        last_day = 1

        while not (last_day == date_to.day and datetime(year, month, last_day) == date_to):
            if year == date_to.year and month == date_to.month:
                last_day = date_to.day
            else:
                _, last_day = calendar.monthrange(year, month)

            record = parsers.parser1.parse_data_once_a_day(measurement, datetime(year, month, day), datetime(year, month, last_day)) # noqa
            write_api.write(bucket=bucket, org=org, record="\n".join(record))

            day = 1
            if (year, month) != (date_to.year, date_to.month) and month < 12:
                month = month + 1
            else:
                break

    client.close()


if __name__ == "__main__":
    main()
