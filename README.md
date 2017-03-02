# archives_tools
Python libraries for working with archives data

# aspace
A Python library for working with the ArchivesSpace API

* This is a partially complete library I've added to as I write scripts. I set this up to avoid writing requests multiple times and hopefully serve as an example for a community-directed library. There are more functions that are not yet documented. Any suggestions are welcome.

## Requirements

* Python 2.7 or Python 3.4+
* ArchivesSpace version 1.5+

## Setup

* you can clone the repo, and install with setup.py:


	git clone https://github.com/UAlbanyArchives/archives_tools
	python setup.py install


* aspace can optionally be set up to us local config file called local_settings.cfg which places itself in you Python lib directory. Three values stored there can be edited in the .cfg file manually or by using the library:


	from archives_ tools import aspace as AS
		
	AS.setURL("http://localhost:8089")
	AS.setUser("admin")
	AS.setPassword("admin")


* This prevents you from having to re-enter credentials each time, but you can also pass a tuple with each function

* Keep in mind that these values are stored in plain text in your python library directory

## Principles

* Lower the complexity of working with the ArchivesSpace API
* Write commonly used code once, making it faster and easier to write scripts in the future
* Be consistent and transparent about what the library is doing
* Maintain the full functionality of the API in as much as possible

## Usage

### Authentication

* Once these values are stored, you can connect with ArchivesSpace by using `AS.getSession()`:


	from archives_tools import aspace as AS

	session = AS.getSession()

* As with all functions you can also use a tuple each time:


	from archives_tools import aspace as AS

	loginData = ("http://localhost:8089", "admin", "admin")	
	session = AS.getSession(loginData)


## Get Data from ArchivesSpace

### Using Data Objects

* Data objects returned from ArchivesSpace can use dot syntax (`collection.title`) but are also a dictionary of native ASpace API data, so you can also use that syntax (`collection["title"]`) and get a list of fields with `collection.keys()`.

* There are a few functions for viewing the API data:
	* `AS.pp(collection)` pretty prints the native JSON to the console
	* `AS.fields(collection)` prints all of the data fields on different lines
	* `AS.serializeData(collection, "/output/path/data.json")` writes the data to a pretty printed JSON file to the output file path entered as a string

### Repositories

* Returns a repository object


	from archives_tools import aspace as AS

	session = AS.getSession()

	repository = AS.getRepository(session)
	print (repository.title)

	> M. E. Grenander Department of Special Collections & Archives

### Resources

* `getResource()` returns a single resource object
	* Can iterate through child objects using same keys as JSON API
	* Requires:
		* `session`
		* login data tuple is optional second argument
		* Repository number as a string


	from archives_tools import aspace as AS

	session = AS.getSession()
	repo = "2"

	collection = AS.getResource(session, repo, "512")
	print (collection.uri)

	> /repositories/2/resources/512

	for note in collection.notes:
		if note.type == "accessrestrict":
			note.publish = True
			for subnote in note:
				subnote.publish = True


* `getResources()` returns a list of resource objects, limited by parameter
	* Can iterate through child objects using same keys as JSON API
	* Requires:
		* `session`
		* Repository number as a string
		* Limiting parameter such as:
			* "all" for all resources (may be problematic for large repositories)
			* A string of comma separated resoruce numbers: "334, 352, 445, 707" 
			* A range of the total resources for pagination: "50-100"
				* Note that these are not resource numbers, but the second set of 50 resoruces


	from archives_tools import aspace as AS

	session = AS.getSession()
	repo = "2"

	for collection in AS.getResources(session, repo, "all"):
		if collection.title == "David Baldus Papers":
			print (collection.ead_id)
			for note in collection.notes:
				if note.type == "abstract":
					print (note.content)

	>apap329
	>Consists of records from legal scholar and death penalty researcher David C. Baldus whose work informed the 1987 McCleskey v. Kemp decision.


* `getTree()` returns a object that lists the arrangement of archival objects assigned to a resource object
	* Can be iterated over to get basic archival object information and to retrieve archival object uris to call with `getArchObj()`
		* Requires:
			* 

