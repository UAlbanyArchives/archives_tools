import os
import json
import requests
import ConfigParser
from datetime import datetime


#funtions for debugging
def pp(output):
	print (json.dumps(output, indent=2))
def serializeOutput(filename, output):
	__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
	f = open(os.path.join(__location__, filename + ".json"), "w")
	f.write(json.dumps(output, indent=2))
	f.close
	
#error handler
def handleError(response):
	log = open("aspace.log", "a")
	log.write("\n" + str(datetime.now()) + "  --  " + "ERROR: HTTP Response " + str(response.status_code) + "\n" + json.dumps(response.json(), indent=2))
	log.close()
	print ("ERROR: HTTP Response " + str(response.status_code))
	pp(response.json())
	

#basic function to get ASpace login details from a config file
def getLogin():

	__location__ = os.path.dirname(os.path.realpath(__file__))

	#load config file from same directory
	configPath = os.path.join(__location__, "local_settings.cfg")
	config = ConfigParser.ConfigParser()
	config.read(configPath)

	#dictionary with basic ASpace login info
	aspaceLogin = {'baseURL': config.get('ArchivesSpace', 'baseURL'), 'user': config.get('ArchivesSpace', 'user'), 'password': config.get('ArchivesSpace', 'password')}
	
	return aspaceLogin
	

#function to get an ArchivesSpace session
def getSession():

	#get dictionary of login details
	aspaceLogin = getLogin()
		
	#inital request for session
	r = requests.post(aspaceLogin["baseURL"] + "/users/" + aspaceLogin["user"]  + "/login", data = {"password":aspaceLogin["password"]})

	if r.status_code != 200:
		handleError(r)
	else:		
		print ("ASpace Connection Successful")
		sessionID = r.json()["session"]
		session = {'X-ArchivesSpace-Session':sessionID}
		return session

		
def fields(jsonObject):
	fieldList = ""
	for key, value in jsonObject.items():
		if isinstance(jsonObject[key], dict) or isinstance(jsonObject[key], list):
			field = key + " --> " listFields(jsonObject[key])
		else:
			field = key
		if len(fieldList) == 0:
			fieldList = "	" + field
		else:
			fieldList = fieldList + "\n	" + field
	return fieldList


		
def getRepositories(session):

	#get ASpace Login info
	aspaceLogin = getLogin()
	
	repoList = requests.get(aspaceLogin["baseURL"] + "/repositories",  headers=session)
	if repoList.status_code != 200:
		handleError(repoList)
	else:		
		return repoList.json()
		


def getResources(session, repo):

	#get ASpace Login info
	aspaceLogin = getLogin()
	
	repos = requests.get(aspaceLogin["baseURL"] + "/repositories",  headers=session).json()
	return repos