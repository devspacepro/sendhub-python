import unittest
import sys
import os

# fix paths so we can import source
sys.path.append(os.path.join(os.path.dirname(__file__), '../..'))

# import test items
from sendhub.connection import Connection
from sendhub.base import constants

from sendhub.message import Message
from sendhub.contact import Contact


class MessageTests(unittest.TestCase):
	'''
	Basic tests that will exercise SendHub Message Objects
	'''
	
	def setUp(self):
		'''
		Setup for test cases
		'''
		
		# initialize the api client
		self.conn = Connection(auth_user=constants.TEST_USER,
							   api_key=constants.TEST_KEY,
							   server=constants.TEST_SERVER,
							   version=constants.TEST_VERSION)
		

	def tearDown(self):
		'''
		Teardown for test cases
		'''
		pass
	
	def test_list_messages_type_verification(self):
		'''
		Tests we can read our messages and they return the appropriate
		pythonic types
		'''
		
		messages = self.conn.list_messages()
		self.failUnlessEqual(len(messages), 1, "We expect a single message in our test account")
		
		for m in messages:
			self.failUnlessEqual(type(m), Message, "Message returned should be of type 'Message'")
			self.failUnlessEqual(type(m.contacts[0]), Contact, "Contact associated with message should be of type 'Contact'")
