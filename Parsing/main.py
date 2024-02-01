import influxdb_client
import parsers.parser1
from influxdb_config import org, url, token
from influxdb_client.client.write_api import SYNCHRONOUS


client = influxdb_client.InfluxDBClient(url=url,
                                        token=token,
                                        org=org)


bucket = "PetroTrackerTSDB"
measurement = "stock_data"

write_api = client.write_api(write_options=SYNCHRONOUS)


def main():
    record = parsers.parser1.parse_data_once_a_day(measurement)
    write_api.write(bucket=bucket, org=org, record="\n".join(record))


if __name__ == "__main__":
    main()
