import urllib, urllib2
import requests
import json
# call data using web servies
input_dict = {"county":"22033","sdate":"2014-06-01","edate":"2014-06-30","meta":"name,sids","elems":[{"name":"pcpn","interval":"mly","duration":"mly","reduce":{"reduce":"sum","add":"mcnt"},"maxmissing":3,"smry":{"reduce":"sum","add":"mcnt"}},{"name":"pcpn","interval":"mly","duration":"mly","reduce":{"reduce":"sum","add":"mcnt"},"maxmissing":3,"smry":{"reduce":"sum","add":"mcnt"},"normal":"departure"}]}
params = urllib.urlencode({'params':json.dumps(input_dict)})
req = urllib2.Request('http://data.rcc-acis.org/MultiStnData', params, {'Accept':'application/json'})
response = urllib2.urlopen(req)
a = response.read()
z= json.loads(a)
b=z['data']
x=0
w=0
# extract just the GHCN Station IDs
stnid=[]
for x in range (0,len(b)):
	for w in range (0,len(b[x]['meta']['sids'])):
		if b[x]['meta']['sids'][w][len(b[x]['meta']['sids'][w])-1]=='6':
			stnid.append(b[x]['meta']['sids'][w])
	w=0
stnname=[]  # create empty list to hold the station names
mpcpn=[]    # create empty list to hold the precip data
depart=[]   # create empty list to hold the precip dfn data
v=0
for v in range (0,len(b)):
         stnname.append((b[v]['meta']['name']))   # populate the three lists
         mpcpn.append(b[v]['smry'][0][0])
         depart.append(b[v]['smry'][1][0])
         if depart[v]=='M':     # check to see if there is a normals value for the stn
                depart[v]='N/A' # if not, assign the value as 'not available'
# print out the data in a formatted text table
i=0
print 'Monthly Precipitation Totals (inches) In East Baton Rouge Parish for June, 2014'
print ''
print ''
print "%-12s %-25s %6s %7s"% ('GHCN Stn ID','Station Name','Precipitation','DFN*')
print ''
for i in range (0,len(stnname)):
         print "%-12s %-25s %8s %11s"% (stnid[i][:-2],stnname[i],mpcpn[i],depart[i])
print ''
print '* DFN - Departure from the 1981-2010 Climate Normals'
