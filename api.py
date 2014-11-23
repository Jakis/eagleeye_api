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

#Authenticate
payload = {'username': apiuser, 'password': apipassword}
r = requests.post((apiURI + 'g/aaa/authenticate'), params=payload)

#Retreive auth token from json response.
jsonresponse = r.json()
authtoken = jsonresponse['token']

#Use the auth token to authenticate and retreive a cookie and session id
payload = {'token': authtoken}
r = requests.post((apiURI + 'g/aaa/authorize'), params=payload)
sessionid = r.cookies['videobank_sessionid']

"""/// Requests ///////////////////////////////////////////////////"""

#Now we can make requests.  Here's an example request for the user list.
payload = {'A': sessionid}
r = requests.get((apiURI + 'g/user/list'), params=payload)

response = r.json()
#print response
pprint(response)
