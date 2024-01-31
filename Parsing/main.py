from datetime import datetime
import influxdb_client
from parsers.parser1 import parse_data
from influxdb_config import org, url, token
from influxdb_client.client.write_api import SYNCHRONOUS
from influxdb_client import WritePrecision


client = influxdb_client.InfluxDBClient(url=url,
                                        token=token,
                                        org=org)


bucket = "TSDB1"

write_api = client.write_api(write_options=SYNCHRONOUS)


def main():
    record = parse_data("my_measurment")

    # p = influxdb_client.Point("my_measurement").tag("location", "Moscow").field("temperature", 11.0)\
    #    .time(seconds, WritePrecision.S)
    write_api.write(bucket=bucket, org=org, record="\n".join(record))


if __name__ == "__main__":
    main()
