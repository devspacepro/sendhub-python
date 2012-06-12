'''

Connection class to query SendHub resources

'''

from base import constants
from base.apiclient import APIClient

from message import Message, MessageResults
from contact import Contact

class Connection(object):
    
    def __init__(self, 
                 auth_user, 
                 api_key, 
                 server=constants.DEFAULT_SERVER,
                 version=constants.DEFAULT_VERSION):
        '''
        Initialize SendHub Connection
        
        '''
        
        # store settings in self
        self.auth_user      = auth_user
        self.auth_key       = api_key
        self.server         = server
        self.version        = version
        
        # initialize the apiclient
        self.apiclient      = APIClient(auth_user, api_key, server, version)
        
    def list_threads(self):
        '''
        Return a list of SendHub threads
        
        TODO: objectize threads
        
        '''
        id_list = []
        response = self.apiclient.get(constants.URL_INBOX)
        for message in response.objects:
            id = message.resource_uri.split('/')[3]
            id_list.append(id)
        return id_list
         
    def list_messages(self):
        '''
        Return a list of SendHub messages from all threads in Inbox
        '''
        message_list = []
        for thread_id in self.list_threads():
        
            thread = self.apiclient.get(constants.URL_THREADS + '/' + str(thread_id))
            
            for message in thread.objects:
                
                # rewrite contacts as objects
                contacts = message.pop('contacts')
                message['contacts'] = [Contact(c) for c in contacts]
                
                # yield message object
                message_list.append(Message(self, **message))
                                
        return MessageResults(self, message_list)