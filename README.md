# Home Metrics Utilities

Some utils I wrote to collect metrics from around the house.

## `portland_general_parser.py`

This script parses CSV files downloadable from the Portland General Electric usage portal and pushes them into a local InfluxDB instance.  Pushes data for cost as well as KW/h usage.

## `econet_waterheater_usage.py`

This script pulls hourly water heater power usage data from the Econet API and pushes it into InfluxDB.