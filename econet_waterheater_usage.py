import time
import sys
from datetime import datetime, timezone
from pyeconet.api import PyEcoNet
from tzlocal import get_localzone
import json
from influxdb import InfluxDBClient
from pprint import pprint

client = InfluxDBClient('localhost', 8086, 'root', 'root', 'home_metrics')

# make path to creds got passed in
if(len(sys.argv) != 2):
    print("You must specify a path to credentials.json as an argument")
    sys.exit(1)
# read our config.  It expects there to be an "econet" hash with a username
# and password
cfile = open(sys.argv[1])
creds = json.load(cfile)
if "econet" not in creds or "username" not in creds["econet"] or "password" not in creds["econet"]:
    print("didn't find expected credentials.  Exiting")
    sys.exit(1)

econet = PyEcoNet(creds["econet"]["username"], creds["econet"]["password"])
devices = econet.get_water_heaters()
for water_heater in devices:
    # print(water_heater.usage_unit)
    econet_data = json.loads(water_heater.dump_usage_json())
    
    # pprint(econet_data['energyUsage']['hours'])
    for hour in econet_data['energyUsage']['hours']:
        # for hour, used in usageDict:
        usage_object = [
            {
            "measurement": "water_heater",
            "tags": {
                "data_source": "econet",
                "location": "4126"
            },
            # Looks like timestamps are in UTC, so we'll append the
            # "Z" to the timestamp to make the right thing happen
            "time": hour + "T",
            "fields": {
                "usage": econet_data['energyUsage']['hours'][hour]
            }
            }
        ]

        client.write_points(usage_object)
        # pprint(usage_object)