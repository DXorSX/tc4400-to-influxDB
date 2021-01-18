# Imports
import requests
import re
from requests.auth import HTTPBasicAuth
import lxml.html as lh
import pandas as pd
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS

# Config
bolDebug=False   # if true, print debug messages 
bolTestrun=False # if true, nothing will be send to DB

# Define InfluxDB Connection
token="Udk_sdiczhLeRv0sPpzt1gvSo2IV7NN8Dt7wQwT-6ebWbASSbThQQmhePMSdVf8FzBMnyfpITN4u9UJlHfp1ow=="
org = "Home"
bucket = "tc4400-DOCSIS-Monitor"
client = InfluxDBClient(url="http://wolf.unterwelt.lan:8086", token=token)

# Define TC4400 WebInterface
url='http://192.168.0.1/cmconnectionstatus.html'
httpuser='admin'
httppass='bEn2o#US9s'

page = requests.get(url, auth=HTTPBasicAuth(httpuser, httppass))
tables = pd.read_html(page.content)

if bolDebug:
    print("There are : ",len(tables)," tables")
    print("Take look at table 1 - Downstream")
    print(tables[1])
    print("Take look at table 2 - Upstream")
    print(tables[2])

#########################################################################################
# Parsing Table "Downstream Channel Status" & send to influxDB
for row_num in range(1, len(tables[1])):
    write_api = client.write_api(write_options=SYNCHRONOUS)
    datastring = ""

    # Formatting some data, remove whitespaces + unit (Hz, kHz etc.)
    strSNR = tables[1].iloc[row_num,7]
    strSNR = re.sub('\s.*', '', strSNR)
    strReceivedLevel = tables[1].iloc[row_num,8]
    strReceivedLevel = re.sub('\s.*', '', strReceivedLevel)       
    strCenterFrequency = tables[1].iloc[row_num,5]
    strCenterFrequency = re.sub('\s.*', '', strCenterFrequency)
    strChannelWidth = tables[1].iloc[row_num,6]
    strChannelWidth = re.sub('\s.*', '', strChannelWidth)

    # Build datastring, send to influxDB
    datastring = datastring + "tc4400,provider=vodafone,stream=DS,channelID=" + tables[1].iloc[row_num,1] + \
        " lockStatus=\"" + tables[1].iloc[row_num,2] + \
        "\",channelType=\"" + tables[1].iloc[row_num,3] + \
        "\",bondingStatus=\"" + tables[1].iloc[row_num,4] + \
        "\",centerFrequency-Hz=" + strCenterFrequency + \
        ",channelWidth-Hz=" + strChannelWidth + \
        ",SNR-dB=" + strSNR + \
        ",receivedLevel-dBmV=" + strReceivedLevel + \
        ",profileID=\"" + tables[1].iloc[row_num,9] + \
        "\",unerroredCodewords=" + tables[1].iloc[row_num,10] + \
        ",correctedCodewords=" + tables[1].iloc[row_num,11] + \
        ",uncorrectableCodewords=" + tables[1].iloc[row_num,12]
    if bolDebug:
        print(datastring)

    if not bolTestrun:
        write_api.write(bucket, org, datastring)
    else:
        print("Testrun Downstream Channel Status: No write to influxDB")
#########################################################################################


#########################################################################################
# Parsing Table "Upstream Channel Status" & send to influxDB
for row_num in range(1, len(tables[2])):
    write_api = client.write_api(write_options=SYNCHRONOUS)
    datastring = ""

    # Formatting some data, remove whitespaces + unit (Hz, kHz etc.)
    strTransmitLevel = tables[2].iloc[row_num,7]
    strTransmitLevel = re.sub('\s.*', '', strTransmitLevel)
    strCenterFrequency = tables[2].iloc[row_num,5]
    strCenterFrequency = re.sub('\s.*', '', strCenterFrequency)
    
    # Build datastring, send to influxDB
    datastring = datastring + "tc4400,provider=vodafone,stream=US,channelID=" + tables[2].iloc[row_num,1] + \
        " lockStatus=\"" + tables[2].iloc[row_num,2] + \
        "\",channelType=\"" + tables[2].iloc[row_num,3] + \
        "\",bondingStatus=\"" + tables[2].iloc[row_num,4] + \
        "\",centerFrequency-Hz=" + strCenterFrequency + \
        ",transmitLevel-dBmV=" + strTransmitLevel + \
        ",profileID=\"" + tables[2].iloc[row_num,8] + "\""
    if bolDebug:
        print(datastring)

    if not bolTestrun:
        write_api.write(bucket, org, datastring)
    else:
        print("Testrun Upstream Channel Status: No write to influxDB")
#########################################################################################



