import os
import json
import requests
import ConfigParser
from easydict import EasyDict as edict
from datetime import datetime


#funtions for debugging
def pp(output):
	print (json.dumps(output, indent=2))
def serializeOutput(filePath, output):
	f = open(filePath, "w")
	f.write(json.dumps(output, indent=2))
	f.close
	
#error handler
def handleError(response):
	log = open("aspace.log", "a")
	log.write("\n" + str(datetime.now()) + "  --  " + "ERROR: HTTP Response " + str(response.status_code) + "\n" + json.dumps(response.json(), indent=2))
	log.close()
	print ("ERROR: HTTP Response " + str(response.status_code))
	pp(response.json())
	
#reads config file for lower functions
def readConfig():
	__location__ = os.path.dirname(os.path.realpath(__file__))

	#load config file from same directory
	configPath = os.path.join(__location__, "local_settings.cfg")
	config = ConfigParser.ConfigParser()
	config.read(configPath)
	return config
	
#writes the config file back
def writeConfig(config):
	__location__ = os.path.dirname(os.path.realpath(__file__))

	#load config file from same directory
	configPath = os.path.join(__location__, "local_settings.cfg")
	with open(configPath, 'w') as f:
		config.write(f)
	
#basic function to get ASpace login details from a config file
def getLogin():
	config = readConfig()
	
	#make dictionary with basic ASpace login info
	aspaceLogin = {'baseURL': config.get('ArchivesSpace', 'baseURL'), 'user': config.get('ArchivesSpace', 'user'), 'password': config.get('ArchivesSpace', 'password')}
	return aspaceLogin

	
#function to update the URL in the config file
def setURL(URL):
	config = readConfig()	
	config.set('ArchivesSpace', 'baseURL', URL)
	writeConfig(config)
	print "URL path updated"

#function to update the user in the config file
def setUser(user):
	config = readConfig()	
	config.set('ArchivesSpace', 'user', user)
	writeConfig(config)
	print "User updated"
	
#function to update the URL in the config file
def setPassword(password):
	config = readConfig()	
	config.set('ArchivesSpace', 'password', password)
	writeConfig(config)
	print "Password updated"

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
	fieldsSet = ""
	def listFields(jsonObject, fieldList):
		for key, value in jsonObject.items():
		
			if isinstance(jsonObject[key], dict) or isinstance(jsonObject[key], list):
				field = key + "\n	" + listFields(jsonObject[key], "")
			else:
				field = key
				
			if len(fieldList) == 0:
				fieldList = "	" + field
			else:
				fieldList = fieldList + "\n	" + field
		return fieldList
	fieldsSet = listFields(jsonObject, fieldsSet)	
	return fieldsSet

	
def makeObject(response):
	if response.status_code != 200:
		handleError(response)
	else:
		list = []
		for thing in response.json():
			object = edict(thing)
			object.fields = fields(thing)
			object.json = thing
			list.append(object)
		return list

		
def getRepositories(session):

	#get ASpace Login info
	aspaceLogin = getLogin()
	
	repoData = requests.get(aspaceLogin["baseURL"] + "/repositories",  headers=session)
	repoList = makeObject(repoData)
	return repoList


def getResources(session, repo):

	#get ASpace Login info
	aspaceLogin = getLogin()
	
	resourceData= requests.get(aspaceLogin["baseURL"] + "/repositories/" + str(repo) + "/resources?all_ids=true",  headers=session)
	resourceList = makeObject(resourceData)
	return resourceList