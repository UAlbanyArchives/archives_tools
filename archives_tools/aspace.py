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
def checkError(response):
	if not response.status_code == 200:
		print ("ERROR: HTTP Response " + str(response.status_code))
		try:
			pp(response.json())
			log = open("aspace.log", "a")
			log.write("\n" + str(datetime.now()) + "  --  " + "ERROR: HTTP Response " + str(response.status_code) + "\n" + json.dumps(response.json(), indent=2))
			log.close()
		except:
			print (response.status_code)
			log = open("aspace.log", "a")
			log.write("\n" + str(datetime.now()) + "  --  " + "ERROR: HTTP Response " + str(response.status_code))
			log.close()
	
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
	if not config.has_section("ArchivesSpace"):
		config.add_section('ArchivesSpace')
	config.set('ArchivesSpace', 'baseURL', URL)
	writeConfig(config)
	print "URL path updated"

#function to update the user in the config file
def setUser(user):
	config = readConfig()
	if not config.has_section("ArchivesSpace"):
		config.add_section('ArchivesSpace')
	config.set('ArchivesSpace', 'user', user)
	writeConfig(config)
	print "User updated"
	
#function to update the URL in the config file
def setPassword(password):
	config = readConfig()	
	if not config.has_section("ArchivesSpace"):
		config.add_section('ArchivesSpace')
	config.set('ArchivesSpace', 'password', password)
	writeConfig(config)
	print "Password updated"

#function to get an ArchivesSpace session
def getSession():

	#get dictionary of login details
	aspaceLogin = getLogin()
		
	#inital request for session
	r = requests.post(aspaceLogin["baseURL"] + "/users/" + aspaceLogin["user"]  + "/login", data = {"password":aspaceLogin["password"]})
	checkError(r)	
	print ("ASpace Connection Successful")
	sessionID = r.json()["session"]
	session = {'X-ArchivesSpace-Session':sessionID}
	return session
		


#gets an indented list of keys from a ASpace json object
def fields(jsonObject):
	fieldsSet = ""
	def listFields(jsonObject, fieldList):
		if not isinstance(jsonObject, dict):
			for item in jsonObject:
				for key, value in item.items():
					if key.lower() == "type":
						fieldList = fieldList + "\n		" + key + ": " + value
					else:
						fieldList = fieldList + "\n		" + key
		else:
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

	
def makeObject(jsonData):
	#handles paginated returns
	if "results" in jsonData:
		jsonData = jsonData["results"]
		
	if isinstance(jsonData, list):
	
		itemList = []
		#checks if list of json objects or just a single one
		for thing in jsonData:
			object = edict(thing)
			object.fields = fields(thing)
			object.json = thing
			itemList.append(object)
		return itemList

	else:
		#single json object
		object = edict(jsonData)
		object.fields = fields(jsonData)
		object.json = jsonData
		return object
		
def getRepositories(session):

	#get ASpace Login info
	aspaceLogin = getLogin()
	
	repoData = requests.get(aspaceLogin["baseURL"] + "/repositories",  headers=session)
	checkError(repoData)
	repoList = makeObject(repoData.json())
	return repoList


def getResourceList(session, repo):

	#get ASpace Login info
	aspaceLogin = getLogin()
	
	resourceData= requests.get(aspaceLogin["baseURL"] + "/repositories/" + str(repo) + "/resources?all_ids=true",  headers=session)
	checkError(resourceData)
	return resourceData.json()
		

#returns a list of resources you can iterate though with all, a set, or a range of resource numbers
def getResources(session, repo, param):

	#get ASpace Login info
	aspaceLogin = getLogin()
	
	#get list of all resources and loop thorugh them
	if param.lower().strip() == "all":
		resourceNumbers = getResourceList(session, repo)
		resourceList = []
		for number in resourceNumbers:
			resourceData= requests.get(aspaceLogin["baseURL"] + "/repositories/" + str(repo) + "/resources/" + str(number),  headers=session)
			checkError(resourceData)
			resourceObject = makeObject(resourceData.json())
			resourceList.append(resourceObject)
		return resourceList
	else:
		if "-" in param:
			range = int(param.split("-")[1]) - int(param.split("-")[0])
			page = int(param.split("-")[0]) / range
			limiter = "page=" + str(page + 1) + "&page_size=" + str(range)
		elif "," in param:
			limiter = "id_set=" + param.replace(" ", "")
		else:
			print ("Invalid parameter, requires 'all', set (53, 75, 120), or paginated (1-100")
		
		resourceData= requests.get(aspaceLogin["baseURL"] + "/repositories/" + str(repo) + "/resources?" + limiter,  headers=session)
		checkError(resourceData)
		resourceList = makeObject(resourceData.json())
		return resourceList
		
#return resource object with number
def getResource(session, repo, number):

	#get ASpace Login info
	aspaceLogin = getLogin()

	resourceData= requests.get(aspaceLogin["baseURL"] + "/repositories/" + str(repo) + "/resources/" + str(number),  headers=session)
	checkError(resourceData)
	resourceList = makeObject(resourceData.json())
	return resourceList
	
#post a resourse object back to archivesspace
def postResource(session, resourceObject):

	#get ASpace Login info
	aspaceLogin = getLogin()
	
	uri = resourceObject.uri
	del resourceObject['fields']
	del resourceObject['json']
	resourceString = json.dumps(resourceObject)
	
	resourceData = requests.post(aspaceLogin["baseURL"] + str(URI), data=resourceString, headers=session)
	checkError(resourceData)
	if resourceData.status_code == 200:
		print ("Resource " + str(uri) + " posted back to ArchivesSpace")
		
#Delete a resourse object
def deleteResource(session, resourceObject):

	#get ASpace Login info
	aspaceLogin = getLogin()
	
	uri = resourceObject.uri
	del resourceObject['fields']
	del resourceObject['json']
	resourceString = json.dumps(resourceObject)
	
	deleteResource = requests.delete(aspaceLogin["baseURL"] + str(uri),  headers=session)
	checkError(deleteResource)
	if deleteResource.status_code == 200:
		print ("Resource " + str(URI) + " Deleted")


#return resource tree object
def getTree(session, resourceObject):

	#get ASpace Login info
	aspaceLogin = getLogin()
	
	uri = resourceObject.uri	
	
	treeData = requests.get(aspaceLogin["baseURL"] + str(uri) + "/tree",  headers=session)
	checkError(treeData)
	treeObject = makeObject(treeData.json())
	return treeObject
	
#return resource tree object
def getArchObj(session, recordUri):

	#get ASpace Login info
	aspaceLogin = getLogin()
	
	aoData = requests.get(aspaceLogin["baseURL"] + str(recordUri),  headers=session)
	checkError(aoData)
	aoObject = makeObject(aoData.json())
	return aoObject