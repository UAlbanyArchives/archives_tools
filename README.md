# archives_tools
Python libraries for working with archives data

# aspace
A Python library for working with the ArchivesSpace API

## Requirements

* Python 2.7 or Python 3.4+
* ArchivesSpace version 1.5+

## Setup

* aspace uses a local config file called local_settings.cfg which places itself in you Python lib directory. Three values stored there can be edited manually or by using the library:

`

	import aspace as AS
		
	AS.setURL("http://localhost:8080")
	AS.setUser("admin")
	AS.setPassword("admin")


* Keep in mind that these values are stored in pain text in you python library directory

## Principles

* Lower the complexity of working with the ArchivesSpace API
* Write commonly used code once, making it faster and easier to write scripts in the future
* Be consistent and transparent about what the library is doing
* Maintain the full functionality of the API in as much as possible

## Usage

### Authentication

* Once these values are stored, you can connect with ArchivesSpace by using `AS.getSession()`:

`

	import aspace as AS

	session = AS.getSession()


### Repositories

* Returns a repository object

`

	import aspace as AS

	session = AS.getSession()

	repository = AS.getRepository(session)
	print (repository.title)

	> M. E. Grenander Department of Special Collections & Archives

### Resources

* `getResource()` returns a single resource object
	* Can iterate through child objects using same keys as JSON API
	* Requires:
		* `session`
		* Repository number as a string

`

	import aspace as AS

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

`

	import aspace as AS

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

