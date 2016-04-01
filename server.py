import sys
import time
import json
import urllib2
from SeleniumHelper import SeleniumHelper
from selenium import webdriver

class VolunteerController(SeleniumHelper):

	TIMEOUT = 7
	data = {}
	START_URL = 'http://helpfromhome.org/category/actions'

	SECTIONS = {}
	FIELDS = {}
	CONTAINER = {}

	CONTAINER['SEARCH'] = '#content'
	SECTIONS['SEARCH'] = {}
	SECTIONS['SEARCH']['LIST'] = {'quantity':'multiple', 'selector':'.cat-item'}
	FIELDS['SEARCH'] = {}
	FIELDS['SEARCH']['LIST'] = {}
	FIELDS['SEARCH']['LIST']['NAME'] = {'type':'text', 'selector':'a'}
	FIELDS['SEARCH']['LIST']['URL'] = {'attr':'href', 'type':'attr', 'selector':'a'}

	CONTAINER['RESULTS'] = '#content'
	SECTIONS['RESULTS'] = {}
	SECTIONS['RESULTS']['LIST'] = {'quantity':'multiple', 'selector':'.category-article'}
	FIELDS['RESULTS'] = {}
	FIELDS['RESULTS']['LIST'] = {}
	FIELDS['RESULTS']['LIST']['NAME'] = {'type':'text', 'selector':'h3 > a'}
	FIELDS['RESULTS']['LIST']['URL'] = {'attr':'href', 'type':'attr', 'selector':'h3 > a'}
	FIELDS['RESULTS']['LIST']['TIME'] = {'type':'text', 'selector':'li:nth-child(1)'}
	FIELDS['RESULTS']['LIST']['IMPACT'] = {'type':'text', 'selector':'li:nth-child(2)'}
	FIELDS['RESULTS']['LIST']['COST'] = {'type':'text', 'selector':'li:nth-child(3)'}
	FIELDS['RESULTS']['LIST']['RATING'] = {'type':'text', 'selector':'li:nth-child(4)'}
	FIELDS['RESULTS']['LIST']['CATEGORIES'] = {'type':'text', 'selector':'.post-meta > p'}

	CONTAINER['PAGE'] = '#content'
	SECTIONS['PAGE'] = {}
	SECTIONS['PAGE']['DESCRIPTION'] = {'quantity':'single', 'type':'text', 'selector':'#post-content p'}
	SECTIONS['PAGE']['ORGURL'] = {'quantity':'single', 'attr':'href', 'type':'attr', 'selector':'#post-content > center > a'}

	def extractVolunteers(self):
		print 'Loading'
		self.loadAndWait(self.START_URL, self.CONTAINER['SEARCH'])
		menu01 = self.extractSection('SEARCH')
		print 'Starting'
		for elem01 in menu01['LIST']:
			menu01Name = elem01['NAME']
			menu01URL = elem01['URL']
			print menu01Name
			self.data[menu01Name] = {}
			self.loadAndWait(menu01URL, self.CONTAINER['SEARCH'])
			menu02 = self.extractSection('SEARCH')
			for elem02 in menu02['LIST']:
				menu02Name = elem02['NAME']
				menu02URL= elem02['URL']
				print menu01Name + ' > ' + menu02Name
				self.data[menu01Name][menu02Name] = {}
				self.loadAndWait(menu02URL, self.CONTAINER['SEARCH'])
				menu03 = self.extractSection('SEARCH')
				for elem03 in menu03['LIST']:
					menu03Name = elem03['NAME']
					menu03URL= elem03['URL']
					print menu01Name + ' > ' + menu02Name + ' > ' + menu03Name
					self.data[menu01Name][menu02Name][menu03Name] = []
					self.loadAndWait(menu03URL, self.CONTAINER['RESULTS'])
					menu04 = self.extractSection('RESULTS')
					for elem04 in menu04['LIST']:
						menu04Name = elem04['NAME']
						menu04URL = elem04['URL']
						print menu01Name + ' > ' + menu02Name + ' > ' + menu03Name + ' > ' + menu04Name
						self.loadAndWait(menu03URL, self.CONTAINER['PAGE'])
						elem05 = self.extractSection('PAGE')
						elem04.update(elem05)
						self.data[menu01Name][menu02Name][menu03Name].append(elem04)
						print menu01Name + ' > ' + menu02Name + ' > ' + menu03Name + ' > ' + menu04Name + ' > OK'
						with open('results.json', 'w') as f:
							f.write(json.dumps(self.data))
		return self.data

	def __init__(self): 
		self.driver = webdriver.Firefox()
		self.driver.set_page_load_timeout(self.TIMEOUT)


volunteerTool = VolunteerController()
volunteers = volunteerTool.extractVolunteers()
print json.dumps(volunteers)