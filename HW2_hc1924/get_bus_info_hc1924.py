#Author: Hongting Chen, NYU, Sep 2016
#Code for HW2 of PUI2016
#This code displays information on the next stop location of all busses of a given line.

from __future__ import print_function
import sys
import json
try:
    import urllib2 as urllib
except ImportError:
    import urllib.request as urllib

if not len(sys.argv) == 4:
    print("Invalid number of arguments. Run as python show_bus_info_hc1924.py <MTA_KEY> <BUS_LINE> <BUS_LINE>.csv")
    sys.exit()

#http://bustime.mta.info/api/siri/vehicle-monitoring.json?key=93f33afe-1590-4ad3-8244-ac31bea8204b&VehicleMonitoringDetailLevel=calls&LineRef=B52

def get_jsonparsed_data(url):
    """
    from http://stackoverflow.com/questions/12965203/how-to-get-json-from-webpage-into-python-script
    Receive the content of ``url``, parse it as JSON and return the object.

    Parameters
    ----------
    url : str

    Returns
    -------
    dict
    """
    response = urllib.urlopen(url)
    data = response.read().decode("utf-8")
    return json.loads(data)

jsonData = get_jsonparsed_data("http://bustime.mta.info/api/siri/vehicle-monitoring.json?key=" + sys.argv[1] +"&VehicleMonitoringDetailLevel=calls&LineRef=" + sys.argv[2])

num = len(jsonData["Siri"]["ServiceDelivery"]["VehicleMonitoringDelivery"][0]['VehicleActivity'])
fout = open(sys.argv[3], "w")
fout.write("Latitude,Longitude,Stop Name,Stop Status\n")

for i in range(num):
    item = jsonData["Siri"]["ServiceDelivery"]["VehicleMonitoringDelivery"][0]['VehicleActivity'][i]["MonitoredVehicleJourney"]  
    if item["OnwardCalls"] != []: 
        StopPointName = item["OnwardCalls"]["OnwardCall"][0]["StopPointName"]
        PresentableDistance = item["OnwardCalls"]["OnwardCall"][0]["Extensions"]["Distances"]["PresentableDistance"]
    else: 
        # When the OnwordCalls field is empty, output "N/A" as values for both the "Stop Name" and "Stop Status" fields.
        StopPointName = "N/A"
        PresentableDistance = "N/A"
    Latitude = item["VehicleLocation"]["Latitude"]
    Longitude = item["VehicleLocation"]["Longitude"]

    info = str(Latitude) + "," + str(Longitude) + "," + str(StopPointName) + "," + str(PresentableDistance)+ "\n" 
    fout.write(info)