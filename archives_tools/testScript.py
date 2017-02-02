import aspace as AS
import datetime

session = AS.getSession()

repo = "2"

"""
accession = AS.makeAccession()
accession.accession_date = "2002-01-01"
accession.id_0 = "2002.001"
accession.title = "Michelle Crone Papers"
accession.disposition = "Donor Name: Stephanie Madnick"
accession.provenance = "The collection includes material documenting the National March on Washington, Women's Encampment, Elword Productions, Gay Games, Full Circle Festival: Equinox '89, Lesbian & Gay Film & Video Festival, Rhythm Fest, and other events and groups."
accession.condition_description = "oversize posters in  need of preservation treatment are @ L-12-7"

accession.related_resources.append({"ref": "/repositories/2/resources/1513"})

accession = AS.makeExtent(accession, "21", "cubic ft.")

accession = AS.makeDate(accession, "1974-01-04", "1994-08-30")

AS.postAccession(session, repo, accession)
"""

CSEA = AS.makeResource()
resType = "Records"
CSEA.title = "Civil Service Employees Association (CSEA), AFSCME Local 1000" + " " + resType
CSEA.level = "collection"
CSEA.resource_type = resType.lower()
CSEA.publish = True
CSEA.ead_id = "nam_apap015"
CSEA.ead_location = "html"
CSEA.resource_date = datetime.datetime.now().isoformat().split("T")[0]

location = "H-16-3-1 through H-16-2-3 (last shelf has microfilm and CDs with images used for LUNA), G-8-1-1 - G-8-2-1, G-17-3-2, G-17-3-1, G-17-4-1 - G-17-4-7, G-10-4-1 - G-10-4-3, G-10-5-1 - G-10-5-8, C-12-2-1 - C-12-2-5, C-12-1-2 - C-12-1-3; SB 17 - o-15 (bound copies of Civil Service Leader digitized by Hudson Micro and returned in 2013, bound and unbound copies of The Public Sector, 1978-1998, digitized and returned in 2015, unbound copies of The Work Force, 1998 through 2012, also digitized); Cold 1-1 - 1-4, E-1-1, A-1-7 - A-1-8, A-1-5 - A-1-7, A-1-9, A-1-8, A-1-8 - A-1-9, A-5-1 - A-5-2, A-5-2 - A-5-3, A-4-9 - A-5-1, A-6-5, A-5-5, A-6-4 - A-6-5"

CSEA = CSEA.AS.addContainerLocation(CSEAm, "collection", location)

CSEA = AS.makeDate(CSEA, "1918", "2010")
CSEA = AS.makeExtent(CSEA, "55.05", "cubic ft.")

CSEA = AS.makeSingleNote(CSEA, "abstract", "The Civil Service Employees Association, Inc., or CSEA, is the largest public employees' union in New York State with over 260,000 members. CSEA began in Albany, New York in 1910 as a collective effort by a small group of state employees to secure better wages and working conditions. Originally known as the Association of State Civil Service Employees, the organization adopted its current name in November 1946. Between 1920 and 1940 the organization grew from a handful of workers to a membership of over 600. This increase in membership was largely based upon the admittance of non-competitive class civil service employees. By 1947 the organization admitted another class of state employees, local government workers, with the issuance of a charter to Westchester County employees. The records of the Civil Service Employees Association span from 1918 to the present.")

AS.postResource(session, repo, CSEA) #2034




#print AS.getResourceList(session, repo)

#collection = AS.getResource(session, repo, "1410")
#print collection.ead_id


"""
print collection.title
for note in collection.notes:
	if note.type == "abstract":
		print note.content[0]
"""
"""
for collection in AS.getResources(session, repo, "all"):
	if collection.ead_id.endswith("apap139"):
		print "found " + collection.title
		tree = AS.getTree(session, collection)
		for child in tree.children:
			print "	" + child.title
			for file in child.children:
				if "Cement" in file.title:
					print file.title
					print file.record_uri
					
					object = AS.getArchObj(session, file.record_uri)
					print object.title
					for date in object.dates:
						print date.expression
"""