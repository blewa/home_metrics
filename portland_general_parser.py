import csv
import sys
from datetime import datetime
from pprint import pprint
from influxdb import InfluxDBClient

client = InfluxDBClient('localhost', 8086, 'root', 'root', 'home_metrics')

if(len(sys.argv) != 2):
    print("You must specify a file to process as an argument")
    sys.exit(1)

csvfile = open(sys.argv[1])
filtered_csv = (line for line in csvfile if not line.isspace())
linereader = csv.reader(filtered_csv)
for row in linereader:
    # Validate that we're on a data line vs a header line
    if(row[0] != "Electric usage"):
        continue

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
    #for debugging:
    # pprint(usage_object)