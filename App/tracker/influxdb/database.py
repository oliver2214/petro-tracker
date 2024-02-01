import influxdb_client
from .influxdb_config import org, url, token, bucket, measurement


client = influxdb_client.InfluxDBClient(url=url,
                                        token=token,
                                        org=org)
query_api = client.query_api()


def data_market():
    data = []
    query_market_by_secid = f"""from(bucket: "{bucket}")
    |> range(start: -2d)
    |> filter(fn: (r) => r._measurement == "{measurement}")
    |> group(columns: ["_time", "SECID"])
"""

    tables = query_api.query(query_market_by_secid, org=org)

    for table in tables:
        data_dict = {
            "SECID": table.records[0]["SECID"],
            "SHORTNAME": table.records[0]["SHORTNAME"].strip('"'),
            table.records[0]["_field"]: table.records[0]["_value"],
            table.records[1]["_field"]: table.records[1]["_value"],
            table.records[2]["_field"]: table.records[2]["_value"],
            table.records[3]["_field"]: table.records[3]["_value"],
            table.records[4]["_field"]: table.records[4]["_value"],
            table.records[5]["_field"]: table.records[5]["_value"],
        }

        data.append(data_dict)

    return data
