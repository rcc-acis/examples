#!/usr/bin/python

'''
ACIS-WS Sample Code --> Spatial summary of grid data


Averages of daily maximum temperatures
spanning one year summarized
over the state Nevada.

The result is a time series of daily maximum
temperatures averaged over the area.
'''


#######################################
#Import modules required by Acis
import urllib2
import json
#######################################
#######################################
#Import plotting tools
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.ticker as ticker
import datetime
import numpy as np
#######################################
#Set Acis data server
base_url = "http://data.rcc-acis.org/"
#######################################
#Acis WebServices functions
#######################################
def make_request(url,params) :
    req = urllib2.Request(url,
    json.dumps(params),
    {"Content-Type":"application/json"})
    try:
        response = urllib2.urlopen(req)
        return json.loads(response.read())
    except urllib2.HTTPError as error:
        if error.code == 400 : print error.msg

def GridData(params) :
    return make_request(base_url+"GridData",params)
###################################################
#M A I N
###################################################
if __name__ == "__main__":
    #Set parameters for data request
    params = {
        "state":"nv",
        "sdate":"20130701",
        "edate":"20140701",
        "grid":"1",
        "elems":[{"name":"maxt","area_reduce":"state_mean"}],
    }
    #Obtain data
    data = GridData(params)

    #Generate time series
    dates = [datetime.datetime(int(d[0][0:4]),int(d[0][5:7]),int(d[0][8:10])) for d in data['data']]
    dates = np.array(dates)
    ave_maxt = np.array([d[1]["NV"] for d in data['data']])

    #Plotting
    fig, ax = plt.subplots()
    ax.plot(dates, ave_maxt)
    #Format the ticks
    ax.xaxis.set_major_locator(mdates.MonthLocator())
    ax.xaxis.set_minor_locator(mdates.MonthLocator(bymonthday=1))
    ax.xaxis.set_major_formatter(ticker.NullFormatter())
    ax.xaxis.set_minor_formatter(mdates.DateFormatter('%b'))
    ax.grid(True)
    ax.set_xlabel('2013/2014')
    ax.set_ylabel('Average Maximum Daily Temperature in Nevada')
    plt.show()


