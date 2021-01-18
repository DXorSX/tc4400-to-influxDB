# tc4400-to-influxDB
Gather DOCSIS Data from a Technicolor TC4400 Cable Modem and send to influxDB

## Quickstart

### Setup influxDB as Docker instance

'docker run --name influxDB -v /PATH/influxdbv2:/root/.influxdbv2 -p 8086:8086 quay.io/influxdb/influxdb:v2.0.3 --reporting-disabled' 

Got to http://hostname:8086, create Org, a Bucket and a Token

### 

Install the needed python3 libraries via 'pip3'

'sudo pip3 install pandas'
'sudo pip3 install influxdb-client'

Edit the script and change values for the influxDB Connection and the IP Adress of your TC4400 Cable Modem.
Run the Script and explore the Data in your InfluxDB afterwards.

