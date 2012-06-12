import unittest
import sys
import os

# fix paths so we can import source
sys.path.append(os.path.join(os.path.dirname(__file__), '../..'))

# import test items
from sendhub.base.apiclient import APIClient
from sendhub.base import constants

class APIBasicTests(unittest.TestCase):
	'''
	Basic tests that will exercise the APIClient
	'''
	
	def setUp(self):
		'''
		Setup for test cases
		'''
		
		# initialize the api client
		self.apiclient = APIClient(auth_user=constants.TEST_USER,
								   auth_key=constants.TEST_KEY,
								   server=constants.TEST_SERVER,
								   version=constants.TEST_VERSION)
		

	def tearDown(self):
		'''
		Teardown for test cases
		'''
		pass
	
	def test_view_inbox(self):
		'''
		Tests we can see our inbox
		'''
		
		inbox = self.apiclient.get(constants.URL_INBOX)
		self.failUnlessEqual(type(inbox.objects), type([]), "Expect to find an list of inbox elements")

