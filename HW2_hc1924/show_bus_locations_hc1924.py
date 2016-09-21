#Author: Hongting Chen, NYU, Sep 2016
#Code for HW2 of PUI2016
#This code retrieves and reports information about active vehicle for a bus line.

from __future__ import print_function
import sys
import json
try:
    import urllib2 as urllib
except ImportError:
    import urllib.request as urllib

#download json file from an url
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

if __name__ == '__main__':
    
    # this line checks how many arguments are passed to python
    if not len(sys.argv) == 3:
        print("Invalid number of arguments. Run as python show_bus_locations_hc1924.py <MTA_KEY> <BUS_LINE>")
        sys.exit()

    jsonData = get_jsonparsed_data("http://bustime.mta.info/api/siri/vehicle-monitoring.json?key=" + sys.argv[1] +"&VehicleMonitoringDetailLevel=calls&LineRef=" + sys.argv[2])

    #get the active bus number and locations
    num = len(jsonData["Siri"]["ServiceDelivery"]["VehicleMonitoringDelivery"][0]['VehicleActivity'])
    buses = 0
    locations = []
    for i in range(num):
        item = jsonData["Siri"]["ServiceDelivery"]["VehicleMonitoringDelivery"][0]['VehicleActivity'][i]["MonitoredVehicleJourney"]
        buses += 1
        locations.append(item["VehicleLocation"])

    print ("Bus Line : {}".format(sys.argv[2]))
    print ("Number of Active Buses : {}".format(buses))
    for i in range(num):
        print ("Bus {} is at latitude {} and longitude {}".format(i,str(locations[i]["Latitude"]),str(locations[i]["Longitude"])))
