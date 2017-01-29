import os
import requests
import ConfigParser


#basic function to get ASpace login details from a config file
def getLogin():

	__location__ = os.path.dirname(os.path.realpath(__file__))

	#load config file from same directory
	configPath = os.path.join(__location__, local_settings.cfg)
	config = ConfigParser.ConfigParser()
	config.read(configFilePath)

	#dictionary with basic ASpace login info
	aspaceLogin = {'baseURL': config.get('ArchivesSpace', 'baseURL'), 'user': config.get('ArchivesSpace', 'user'), 'password': config.get('ArchivesSpace', 'password')}
	
	return aspaceLogin
	

def getResources():

	#get ASpace Login info
	aspaceLogin = getLogin()
	
	print (aspaceLogin["user"])