import os
import json
import requests
import configparser
from easydict import EasyDict as edict
from datetime import datetime
from archives_tools.dacs import iso2DACS


#funtions for debugging
def pp(output):
	print (json.dumps(output, indent=2))
def serializeOutput(filePath, output):
	f = open(filePath, "w")
	f.write(json.dumps(output, indent=2))
	f.close
def fields(object):
	for key in object.keys():
		print (key)
	
	
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
	config = configparser.ConfigParser()
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
def getLogin(aspaceLogin = None):
	if aspaceLogin is None:
		config = readConfig()
		
		#make tuple with basic ASpace login info
		aspaceLogin = (config.get('ArchivesSpace', 'baseURL'), config.get('ArchivesSpace', 'user'), config.get('ArchivesSpace', 'password'))
		return aspaceLogin
	else:
		return aspaceLogin

	
#function to update the URL in the config file
def setURL(URL):
	config = readConfig()
	if not config.has_section("ArchivesSpace"):
		config.add_section('ArchivesSpace')
	config.set('ArchivesSpace', 'baseURL', URL)
	writeConfig(config)
	print ("URL path updated")

#function to update the user in the config file
def setUser(user):
	config = readConfig()
	if not config.has_section("ArchivesSpace"):
		config.add_section('ArchivesSpace')
	config.set('ArchivesSpace', 'user', user)
	writeConfig(config)
	print ("User updated")
	
#function to update the URL in the config file
def setPassword(password):
	config = readConfig()	
	if not config.has_section("ArchivesSpace"):
		config.add_section('ArchivesSpace')
	config.set('ArchivesSpace', 'password', password)
	writeConfig(config)
	print ("Password updated")

#function to get an ArchivesSpace session
def getSession(aspaceLogin = None):

	#get tuple of login details if not provided with one
	aspaceLogin = getLogin(aspaceLogin)
		
	#inital request for session
	r = requests.post(aspaceLogin[0] + "/users/" + aspaceLogin[1]  + "/login", data = {"password":aspaceLogin[2]})
	checkError(r)	
	print ("ASpace Connection Successful")
	sessionID = r.json()["session"]
	session = {'X-ArchivesSpace-Session':sessionID}
	return session
		

	
def makeObject(jsonData):
	#handles paginated returns
	if "results" in jsonData:
		jsonData = jsonData["results"]
		
	if isinstance(jsonData, list):
	
		itemList = []
		#checks if list of json objects or just a single one
		for thing in jsonData:
			object = edict(thing)
			#object.fields = fields(thing)
			#object.json = thing
			itemList.append(object)
		return itemList

	else:
		#single json object
		object = edict(jsonData)
		#object.fields = fields(jsonData)
		#object.json = jsonData
		return object
		
################################################################
#OBJECTS
################################################################	

class Accession(object):

	def __init__(self):
			
		#manditory stuff
		self.id = ""
		self.id_1 = ""
		self.id_2 = ""
		self.id_3 = ""
		self.date = ""
		
		#common stuff
		self.title = ""
		self.content = ""
		self.condition = ""
		self.provenance = ""
		
		#restrictions
		self.restrictionsApply = ""
		self.accessRestrictions = ""
		self.accessRestrictions = ""
		self.useRestrictions = ""
		self.useRestrictions = ""
		
		#if you really need them
		self.acquisitionType = ""
		self.resourceType = ""
		self.disposition = ""
		self.inventory = ""
		self.retentionRule = ""
		
		#full json set
		self.json = {}
		
	def toJSON(self):
		pass
		
	def fromJSON(self, jsonSet):
		pass
		




################################################################
#GETTING LIST OF LARGE SETS: ACCESSIONS, RESOURCES, etc.
################################################################	

def getResourceList(session, repo, aspaceLogin = None):

	#get ASpace Login info
	aspaceLogin = getLogin(aspaceLogin)
	
	resourceData= requests.get(aspaceLogin[0] + "/repositories/" + str(repo) + "/resources?all_ids=true",  headers=session)
	checkError(resourceData)
	return resourceData.json()
	
#get a list of accession numbers
def getAccessionList(session, repo, aspaceLogin = None):

	#get ASpace Login info
	aspaceLogin = getLogin(aspaceLogin)
	
	accessionData= requests.get(aspaceLogin[0] + "/repositories/" + str(repo) + "/accessions?all_ids=true",  headers=session)
	checkError(accessionData)
	return accessionData.json()
	
#get a list of subjects
def getSubjectList(session, aspaceLogin = None):

	#get ASpace Login info
	aspaceLogin = getLogin(aspaceLogin)
	
	subjectData= requests.get(aspaceLogin[0] + "/subjects?all_ids=true",  headers=session)
	checkError(subjectData)
	return subjectData.json()
	
#get a list of locations
def getLocationList(session, aspaceLogin = None):

	#get ASpace Login info
	aspaceLogin = getLogin(aspaceLogin)
	
	locationData= requests.get(aspaceLogin[0] + "/locations?all_ids=true",  headers=session)
	checkError(locationData)
	return locationData.json()
		
################################################################
#REQUEST FUNCTIONS
################################################################	
		
def singleRequest(session, repo, number, requestType, aspaceLogin = None):
	#get ASpace Login info
	aspaceLogin = getLogin(aspaceLogin)

	requestData = requests.get(aspaceLogin[0] + "/repositories/" + str(repo) + "/" + requestType + "/" + str(number),  headers=session)
	checkError(requestData)
	returnList = makeObject(requestData.json())
	return returnList
		
def multipleRequest(session, repo, param, requestType, aspaceLogin = None):

	#get ASpace Login info
	aspaceLogin = getLogin(aspaceLogin)
	
	#get list of all resources and loop thorugh them
	if param.lower().strip() == "all":
		if requestType.lower() == "resources":
			numberSet = getResourceList(session, repo, aspaceLogin)
		elif requestType.lower() == "accessions":
			numberSet = getAccessionList(session, repo, aspaceLogin)
		elif requestType.lower() == "subjects":
			numberSet = getSubjectList(session, aspaceLogin)
		elif requestType.lower() == "locations":
			numberSet = getLocationList(session, aspaceLogin)
		returnList = []
		for number in numberSet:
			if  requestType.lower() == "subjects" or requestType.lower() == "locations":
				requestData = requests.get(aspaceLogin[0] + "/" + requestType + "/" + str(number),  headers=session)
			else:
				requestData = requests.get(aspaceLogin[0] + "/repositories/" + str(repo) + "/" + requestType + "/" + str(number),  headers=session)
			checkError(requestData)
			asObject = makeObject(requestData.json())
			returnList.append(asObject)
		return returnList
	else:
		if "-" in param:
			range = int(param.split("-")[1]) - int(param.split("-")[0])
			page = int(param.split("-")[0]) / range
			limiter = "page=" + str(page + 1) + "&page_size=" + str(range)
		elif "," in param:
			limiter = "id_set=" + param.replace(" ", "")
		else:
			print ("Invalid parameter, requires 'all', set (53, 75, 120), or paginated (1-100")
		
		if  requestType.lower() == "subjects":
			requestData= requests.get(aspaceLogin[0] + "/" + requestType + "?" + limiter,  headers=session)
		else:
			requestData= requests.get(aspaceLogin[0] + "/repositories/" + str(repo) + "/" + requestType + "?" + limiter,  headers=session)
		checkError(requestData)
		returnList = makeObject(requestData.json())
		return returnList
		
def postObject(session, object, aspaceLogin = None):

	#get ASpace Login info
	aspaceLogin = getLogin(aspaceLogin)
			
	uri = object.uri
	#del object['fields']
	#del object['json']
	objectString = json.dumps(object)
	
	postData = requests.post(aspaceLogin[0] + str(uri), data=objectString, headers=session)
	checkError(postData)
	return postData.status_code
		
def deleteObject(session, object, aspaceLogin = None):

	#get ASpace Login info
	aspaceLogin = getLogin(aspaceLogin)
	
	uri = object.uri
	deleteRequest = requests.delete(aspaceLogin[0] + str(uri),  headers=session)
	checkError(deleteRequest)
	return deleteRequest.status_code
		
		
################################################################
#REPOSITORIES
################################################################
		
def getRepositories(session, aspaceLogin = None):

	#get ASpace Login info
	aspaceLogin = getLogin(aspaceLogin)
	
	repoData = requests.get(aspaceLogin[0] + "/repositories",  headers=session)
	checkError(repoData)
	repoList = makeObject(repoData.json())
	return repoList


################################################################
#RESOURCES
################################################################
		

#returns a list of resources you can iterate though with all, a set, or a range of resource numbers
def getResources(session, repo, param, aspaceLogin = None):
	#get ASpace Login info
	aspaceLogin = getLogin(aspaceLogin)
	
	resourceList = multipleRequest(session, repo, param, "resources", aspaceLogin)
	return resourceList
		
#return resource object with number
def getResource(session, repo, number, aspaceLogin = None):
	#get ASpace Login info
	aspaceLogin = getLogin(aspaceLogin)
	
	resource = singleRequest(session, repo, number, "resources", aspaceLogin)
	return resource
	
#return a resource object by id_0 field using the index
def getResourceID(session, repo, id_0, aspaceLogin = None):
	#get ASpace Login info
	aspaceLogin = getLogin(aspaceLogin)

	response = requests.get(aspaceLogin[0] + "/repositories/" + str(repo) + "/search?page=1&aq={\"query\":{\"field\":\"identifier\", \"value\":\"" + id_0 + "\", \"jsonmodel_type\":\"field_query\"}}",  headers=session)
	checkError(response)
	if len(response.json()["results"]) < 1:
		print ("Error: could not find results for resource " + str(id_0))
	else:
		resourceID = response.json()["results"][0]["id"].split("/resources/")[1]
		
		resource = singleRequest(session, repo, resourceID, "resources", aspaceLogin)
		return resource
	
#creates an empty resource
def makeResource():
	resourceString = '{"jsonmodel_type":"resource","external_ids":[],"subjects":[],"linked_events":[],"extents":[],"dates":[],"external_documents":[],"rights_statements":[],"linked_agents":[],"restrictions":false,"revision_statements":[],"instances":[],"deaccessions":[],"related_accessions":[],"classifications":[],"notes":[],"title":"","id_0":"","level":"","language":"","ead_id":"","finding_aid_date":"","ead_location":""}'
	emptyResource = json.loads(resourceString)
	resourceObject = makeObject(emptyResource)
	return resourceObject
	
def postResource(session, repo, resourceObject, aspaceLogin = None):

	#get ASpace Login info
	aspaceLogin = getLogin(aspaceLogin)
	
	path = "/repositories/" + str(repo) + "/resources"
	if "uri" in resourceObject.keys():
		if len(resourceObject.uri) > 0:
			path = resourceObject.uri
			
	resourceString = json.dumps(resourceObject)
	
	postResource = requests.post(aspaceLogin[0] + path, data=resourceString, headers=session)
	checkError(postResource)
	return postResource.status_code

	
################################################################
#NAVIGATION
################################################################		
		
#return resource tree object from resource Object
def getTree(session, resourceObject, aspaceLogin = None):

	#get ASpace Login info
	aspaceLogin = getLogin(aspaceLogin)
	
	uri = resourceObject.uri	
	
	treeData = requests.get(aspaceLogin[0] + str(uri) + "/tree",  headers=session)
	checkError(treeData)
	treeObject = makeObject(treeData.json())
	return treeObject

#return a list of child objects from a Resource object or an Archival Object	
def getChildren(session, object, aspaceLogin = None):
	#get ASpace Login info
	aspaceLogin = getLogin(aspaceLogin)
	
	if object.jsonmodel_type == "archival_object":
		#get children of archival object
		aoURI = object.uri
		resourceURI = object.resource.ref
	
		childrenData = requests.get(aspaceLogin[0] + str(resourceURI) + "/tree",  headers=session)
		checkError(childrenData)
		#limit to only children below original archival object
		for child in childrenData.json()["children"]:
			if child["record_uri"] == aoURI:
				if len(child["children"]) < 1:
					print ("ERROR archival object has no children, uri: " + aoURI + " ref_id: " + aoURI.ref_id)
				else:
					childrenObject = makeObject(child["children"])
					return childrenObject
	else:
		#get children of a resource
		childrenData = getTree(session, object, aspaceLogin)
		return childrenData["children"]
		
	
################################################################
#ARCHIVAL OBJECTS
################################################################
	
#return archival object by id
def getArchObj(session, recordUri, aspaceLogin = None):

	#get ASpace Login info
	aspaceLogin = getLogin(aspaceLogin)
	
	aoData = requests.get(aspaceLogin[0] + str(recordUri),  headers=session)
	checkError(aoData)
	aoObject = makeObject(aoData.json())
	return aoObject
	
#return archival object by Ref ID
def getArchObjID(session, repo, refID, aspaceLogin = None):

	#get ASpace Login info
	aspaceLogin = getLogin(aspaceLogin)
	
	params = {"ref_id[]": refID}
	aoData = requests.get(aspaceLogin[0] + "/repositories/" + repo + "/find_by_id/archival_objects", headers=session, params=params)
	checkError(aoData)
	if len(aoData.json()["archival_objects"]) < 1:
		print ("ERROR cound not find archival object for ref ID " + refID)
	else:
		recordUri = aoData.json()["archival_objects"][0]["ref"]
		aoObject = getArchObj(session, recordUri, aspaceLogin)
		return aoObject
		
#creates an empty resource
def makeArchObj():
	objectString = '{"jsonmodel_type":"archival_object","external_ids":[],"subjects":[],"linked_events":[],"extents":[],"dates":[],"external_documents":[],"rights_statements":[],"linked_agents":[],"restrictions_apply":false,"instances":[],"notes":[],"title":"","level":""}'
	emptyArchObj = json.loads(objectString)
	aoObject = makeObject(emptyArchObj)
	return aoObject

def postArchObj(session, repo, aoObject, aspaceLogin = None):
	#get ASpace Login info
	aspaceLogin = getLogin(aspaceLogin)
			
	aoString = json.dumps(aoObject)
	if "ref_id" in aoObject:
		aoID = aoObject.uri.split("/archival_objects/")[1]
		postArchObj = requests.post(aspaceLogin[0] + "/repositories/" + str(repo) + "/archival_objects/" + aoID, data=aoString, headers=session)
	else:
		postArchObj = requests.post(aspaceLogin[0] + "/repositories/" + str(repo) + "/archival_objects", data=aoString, headers=session)
	checkError(postArchObj)
	return postArchObj.status_code
	
################################################################
#ACCESSIONS
################################################################

#returns a list of accessions you can iterate though with all, a set, or a range of resource numbers
def getAccessions(session, repo, param, aspaceLogin = None):
	#get ASpace Login info
	aspaceLogin = getLogin(aspaceLogin)

	accessionList = multipleRequest(session, repo, param, "accessions", aspaceLogin)
	return accessionList

#return accession object with number
def getAccession(session, repo, number, aspaceLogin = None):
	#get ASpace Login info
	aspaceLogin = getLogin(aspaceLogin)
	
	resourceObject = singleRequest(session, repo, number, "accessions", aspaceLogin)
	return resourceObject
	
#makes an empty accession object
def makeAccession():
	accessionString = '{"external_ids":[], "related_accessions":[], "classifications":[], "subjects":[], "linked_events":[], "extents":[], "dates":[], "external_documents":[], "rights_statements":[], "deaccessions":[], "related_resources":[], "restrictions_apply":false, "access_restrictions":false, "use_restrictions":false, "linked_agents":[], "instances":[], "id_0":"", "id_1":"", "title":"","content_description":"","condition_description":"","accession_date":""}'
	emptyAccession = json.loads(accessionString)
	accessionObject = makeObject(emptyAccession)
	accessionObject.accession_date = datetime.now().isoformat().split("T")[0]
	return accessionObject
	
def postAccession(session, repo, accessionObject, aspaceLogin = None):

	#get ASpace Login info
	aspaceLogin = getLogin(aspaceLogin)
			
	accessionString = json.dumps(accessionObject)
	
	postAccession = requests.post(aspaceLogin[0] + "/repositories/" + str(repo) + "/accessions", data=accessionString, headers=session)
	checkError(postAccession)
	return postAccession.status_code
		
		
################################################################
#EXTENTS AND DATES
################################################################

#adds an extent object
def makeExtent(object, number, type):
	extent = {"jsonmodel_type":"extent", "portion":"whole","number":str(number),"extent_type":str(type)}
	if object.extents is None:
		object.extents = [extent]
	else:
		object.extents.append(extent)
	return object


#adds a date object
def makeDate(object, dateBegin, dateEnd = None, displayDate = None):
	if displayDate is None:
		displayDate = ""
	if dateEnd is None:
		dateEnd = ""
	if len(dateEnd) > 0:
		if len(displayDate) > 0:
			date = {"jsonmodel_type":"date","date_type":"inclusive","label":"creation","begin":str(dateBegin),"end":str(dateEnd),"expression":str(displayDate)}
		else:
			date = {"jsonmodel_type":"date","date_type":"inclusive","label":"creation","begin":str(dateBegin),"end":str(dateEnd),"expression":iso2DACS(str(dateBegin) + "/" + str(dateEnd))}
	else:
		if len(displayDate) > 0:
			date = {"jsonmodel_type":"date","date_type":"single","label":"creation","begin":str(dateBegin),"expression":str(displayDate)}
		else:
			date = {"jsonmodel_type":"date","date_type":"single","label":"creation","begin":str(dateBegin),"expression":iso2DACS(str(dateBegin))}
		
	if object.dates is None:
		object.dates = [date]
	else:
		object.dates.append(date)
	return object

################################################################
#NOTES
################################################################
	
#adds a single part notes
def makeSingleNote(object, type, text):
	note = {"type": type, "jsonmodel_type": "note_singlepart", "publish": True, "content": [text]}
	if object.notes is None:
		object.notes = [note]
	else:
		object.notes.append(note)
	return object
	
#adds a single part notes
def makeMultiNote(object, type, text):
	note = {"type": type, "jsonmodel_type": "note_multipart", "publish": True,"subnotes": [{"content": text, "jsonmodel_type": "note_text", "publish": True}]}
	if object.notes is None:
		object.notes = [note]
	else:
		object.notes.append(note)
	return object
	
################################################################
#SUBJECTS
################################################################

#gets a set of subjects you can iterate though
def getSubjects(session, param, aspaceLogin = None):

	subjectList = multipleRequest(session, "", param, "subjects")
	return subjectList


#adds a subject reference
def addSubject(session, object, subjectRef):

	if object.subjects is None:
		object.subjects = [{"ref": subjectRef}]
	else:
		object.subjects.append({"ref": subjectRef})
	return object
			



################################################################
#CONTAINERS AND LOCATIONS
################################################################

#takes a container uri string and returns a container Object
def getContainer(session, containerURI, aspaceLogin = None):
	#get ASpace Login info
	aspaceLogin = getLogin(aspaceLogin)
	
	containerData = requests.get(aspaceLogin[0] + str(containerURI),  headers=session)
	checkError(containerData)
	containerObject = makeObject(containerData.json())
	return containerObject

#takes a archival object and adds reference to an existing top container via a uri string	
def addToContainer(session, fileObject, boxUri, type2 = None, indicator2 = None, aspaceLogin = None):
	#get ASpace Login info
	aspaceLogin = getLogin(aspaceLogin)
	
	boxObject = getContainer(session, boxUri, aspaceLogin)
	boxType = boxObject.type
	boxIndicator = boxObject.indicator
	boxLocations = boxObject.container_locations
	newInstance = {"Jsonmodel_type": "instance", "instance_type": "mixed_materials", "is_representative": True, "container": {"indicator_1": boxIndicator, "type_1": boxType, "container_locations": boxLocations}, "sub_container": {"jsonmodel_type": "sub_container", "top_container": {"ref": boxUri}}}
	if not type2 is None:
		newInstance["container"]["type_2"] = type2
		newInstance["sub_container"]["type_2"] = type2
	if not indicator2 is None:
		newInstance["container"]["indicator_2"] = indicator2
		newInstance["sub_container"]["indicator_2"] = indicator2
	fileObject.instances.append(newInstance)
	
	return fileObject
	
#Make a new container
def makeEmptyContainer(type = None, indicator = None):
	boxObject = {"jsonmodel_type": "top_container", "container_locations": [], "restricted": False, "active_restrictions": []}
	if not type is None:
		boxObject["type"] = str(type)
	if not indicator is None:
		boxObject["indicator"] = str(indicator)
	return boxObject
	
	
#post a container object back to Aspace
def postContainer(session, repo, boxObject, aspaceLogin = None):
	#get ASpace Login info
	aspaceLogin = getLogin(aspaceLogin)
	
	boxID	= boxObject.uri.split("/top_containers/")[1]
	boxString = json.dumps(boxObject)
	
	postBox = requests.post(aspaceLogin[0] + "/repositories/" + str(repo) + "/top_containers/" + boxID, data=boxString, headers=session)
	checkError(postBox)
	return postBox.status_code
	
#make a new container and add a file object to itemList
def makeContainer(session, repo, type, indicator, aspaceLogin = None):
	#get ASpace Login info
	aspaceLogin = getLogin(aspaceLogin)
	
	boxObject = makeEmptyContainer(str(type), str(indicator))
	boxString = json.dumps(boxObject)
	postBox = requests.post(aspaceLogin[0] + "/repositories/" + str(repo) + "/top_containers", data=boxString, headers=session)
	checkError(postBox)
	
	boxURI = postBox.json()["uri"]
	boxObject = getContainer(session, boxURI, aspaceLogin)
	
	return boxObject

#takes a location uri string and returns a location Object
def getLocations(session, repo, param, aspaceLogin = None):
	#get ASpace Login info
	aspaceLogin = getLogin(aspaceLogin)
	
	resourceList = multipleRequest(session, repo, param, "locations", aspaceLogin)
	return resourceList
	
#takes a location uri string and returns a location Object
def getLocation(session, locationURI, aspaceLogin = None):
	#get ASpace Login info
	aspaceLogin = getLogin(aspaceLogin)
	
	locationData = requests.get(aspaceLogin[0] + str(locationURI),  headers=session)
	checkError(locationData)
	locationObject = makeObject(locationData.json())
	return locationObject
	
#add a location to a container object
def addToLocation(boxObject, locationURI, locationNote = None, locationStatus = None, locationEndDate = None):
	if locationStatus is None:
		newLocation = {"status": "current", "jsonmodel_type": "container_location", "start_date": datetime.now().isoformat().split("T")[0], "ref": locationURI}
	else:
		newLocation = {"status": locationStatus, "jsonmodel_type": "container_location", "start_date": datetime.now().isoformat().split("T")[0], "end_date": locationEndDate, "ref": locationURI}
	if not locationNote is None:
		newLocation["note"] = locationNote
	boxObject.container_locations.append(newLocation)
	return boxObject

# Search by title for location and return location URI
def findLocation(session, locTitle, aspaceLogin = None):
	#get ASpace Login info
	aspaceLogin = getLogin(aspaceLogin)
	location = requests.get(aspaceLogin[0] + "/search?page=1&page_size=100&q=%22" + locTitle + "%22",  headers=session)
	checkError(location)
	foundSwitch = False
	for result in location.json()["results"]:
		if result["title"].strip().lower() == locTitle.strip().lower():
			foundSwitch = True
			locationURI = result["uri"]
	if foundSwitch is False:
		print ("Error1: could not find location " + locTitle)
		if len(location.json()["results"]) > 0:
			pp(location.json())
	else:
		return locationURI
		
#post a location object back to Aspace
def postLocation(session, locationObject, aspaceLogin = None):
	#get ASpace Login info
	aspaceLogin = getLogin(aspaceLogin)
	
	locationURI = locationObject.uri
	locationString = json.dumps(locationObject)
	
	postLoc = requests.post(aspaceLogin[0] + locationURI, data=locationString, headers=session)
	checkError(postLoc)
	return postLoc.status_code
	
	
