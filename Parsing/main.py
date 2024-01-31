from parsers.parser1 import parse_data
from influxdb_config import org, url, token
import influxdb_client
from influxdb_client.client.write_api import SYNCHRONOUS


client = influxdb_client.InfluxDBClient(url=url,
                                        token=token,
                                        org=org)


bucket = "TSDB1"

write_api = client.write_api(write_options=SYNCHRONOUS)


def main():
    # Ваша основная логика здесь
    parse_data()

    p = influxdb_client.Point("my_measurement").tag("location", "Moscow").field("temperature", 11.0)
    write_api.write(bucket=bucket, org=org, record=p)


if __name__ == "__main__":
    main()
