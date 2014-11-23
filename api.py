#! /usr/bin/python
import requests
import os
import json
from pprint import pprint

# apiURI = 'https://login.eagleeyenetworks.com/g/aaa/authenticate'
# apiuser = 'demo4@eagleeyenetworks.com'
# apipassword = 'password'

configFile = './eagleeye.json'
json_data = open(configFile)
data = json.load(json_data)

apiuser = (data["apicreds"]["username"])
apipassword = (data["apicreds"]["password"])
apiURI = (data["apicreds"]["authURI"])

json_data.close()

#Authenticate
authenticateURI = apiURI + 'g/aaa/authenticate'
payload = {'username': apiuser, 'password': apipassword}
r = requests.post(authenticateURI, params=payload)

#Retreive auth token from json response.
jsonresponse = r.json()
authtoken = jsonresponse['token']

#Use the auth token to authenticate and retreive a cookie and session id
#authurl = 'https://login.eagleeyenetworks.com/g/aaa/authorize'
authorizeURI = apiURI + 'g/aaa/authorize'
payload = {'token': authtoken}
r = requests.post(authorizeURI, params=payload)
sessionid = r.cookies['videobank_sessionid']

payload = {'A': sessionid}
r = requests.get('https://login.eagleeyenetworks.com/g/user/list', params=payload)

response = r.json()
print response
pprint(response)
