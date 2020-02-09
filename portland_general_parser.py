import csv
from datetime import datetime
from pprint import pprint
from influxdb import InfluxDBClient

client = InfluxDBClient('localhost', 8086, 'root', 'root', 'home_metrics')

with open('pgn_electric_interval_data_0200329289_2017-03-31_to_2020-02-08.csv') as csvfile:
    linereader = csv.reader(csvfile)
    for row in linereader:
        # Array Key
        # 0 - Usage Type
        # 1 - date
        # 2 - Time period start
        # 3 - Time Period End
        # 4 - Amount Used
        # 5 - Usage Unit
        # 6 - Cost
        reading_time = datetime.strptime(row[1] + " " + row[3] + " PST", "%Y-%m-%d %H:%M %Z")
        # stamp = row[1] + " " + row[3] + ":00Z"
        # pprint(reading_time.isoformat())

        usage_object = [
                {
                "measurement": "power_used",
                "tags": {
                    "provider": "portland_general",
                    "location": "4126"
                },
                "time": reading_time.isoformat(),
                "fields": {
                    "usage": row[4],
                    "cost": row[6][1:]
                }
            }
        ]

        client.write_points(usage_object)

        # pprint(cost_object)
        # pprint(usage_object)