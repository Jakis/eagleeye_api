#! /usr/bin/python
import requests
import os
import json
from pprint import pprint

"""/// Reading Creds from Config file /////////////////////////////"""

configFile = './eagleeye.json'
json_data = open(configFile)
data = json.load(json_data)

apiuser = (data["apicreds"]["username"])
apipassword = (data["apicreds"]["password"])
apiURI = (data["apicreds"]["authURI"])

json_data.close()

"""/// Connecting to API //////////////////////////////////////////"""

# Authenticate
payload = {'username': apiuser, 'password': apipassword}
r = requests.post((apiURI + 'g/aaa/authenticate'), params=payload)

# Retreive auth token from json response.
jsonresponse = r.json()
authtoken = jsonresponse['token']

# Use the auth token to authenticate and retreive a cookie and session id.
payload = {'token': authtoken}
r = requests.post((apiURI + 'g/aaa/authorize'), params=payload)
sessionid = r.cookies['videobank_sessionid']

"""/// Requests ///////////////////////////////////////////////////"""

# Now we can make requests.  Here's an example request for the user list.
payload = {'A': sessionid}
r = requests.get((apiURI + 'g/user/list'), params=payload)

# Store user list
userlist = r.json()

# Store device list
payload = {'A': sessionid}
r = requests.get((apiURI + 'g/device/list'), params=payload)
devicelist = r.json()

"""/// Retreive list of Cameras and their ID's /////////////////////"""
cameraIDlist = []
for item in devicelist:
    cameraIDlist.append(item[1])
    #print "Camera ID : %r" % (item[1])
    cameraIDlist.append(item[2])
    #print "Camera Label : %r" % (item[2])
    #print ""

# Targeting the first camera to collect metrics on:
targetCamera = devicelist[0][1]

poll_string = { 'cameras': { '10097da5': { "resource": ["pre"] } } }
post_json = json.dumps(poll_string)
params = {'A': sessionid}
r = requests.post((apiURI + '/poll'), data=post_json, params=params)
print r
