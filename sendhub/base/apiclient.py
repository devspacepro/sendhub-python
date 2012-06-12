'''
Created on June 11, 2012

@author: alan
'''

import base64
import constants
import json
import errors
import httplib
import httplib, mimetypes
import restclient
import sys
from log import log
from restclient.errors import ResourceNotFound
from restclient.rest import url_quote
from sendhub.contrib.storify import Storify
from decorators import retry_wrapper

class APIClient(object):
    '''
    This is the API helper toolkit to access to the rest based
    SendHub API. 
    
    The primary purposes is to catch api errors, provide uniform logging
    and raise them in a uniform fashion, handle silent retries 
    (up until a predetermined point), and silently append 
    authentication to all requests.
    '''

    def __init__(self, auth_user, auth_key, server, version=constants.DEFAULT_VERSION):
        '''
        Initialize APIClient Service
        '''
        
        # store parameters to self
        self.auth_user   = auth_user
        self.auth_key    = auth_key
        self.server      = server
        self.version     = version
        
        # initialize remote http resource
        self.resource = restclient.Resource(self.server)
        
    @retry_wrapper(constants.MAX_API_RETRIES)
    def get(self, *args, **kwargs):
        '''Wrapper for Resource.get that adds basic authorization'''

        # add version and authentication url and params requested
        args, kwargs = self._rewrite_url(*args)
        
        log.debug("=> GET %s: %r (sent body payload: %s)", args[0], kwargs, kwargs.get('payload', False) is not False)

        if 'headers' not in kwargs:
            kwargs['headers'] = self._default_headers()

        if 'payload' in kwargs:
            
            # grab payload and type
            payload         = kwargs.pop('payload', False)
            payload_json    = kwargs.pop('payload_json', False)
            
            connection = httplib.HTTPSConnection(self.server.replace('https://',''))

            if payload_json:
                payload = json.dumps(payload)
            
            connection.request("GET", args[0], payload, kwargs['headers'])
            
            response = connection.getresponse().read()

        else:
            
            try:

                response = self.resource.get(*args, **kwargs)
                
                
            # check for 404
            except ResourceNotFound:
                raise errors.SendHubNotFoundException("Failed to GET non-existent resource %s " % args[0])

                
            # ensure 200 response
            if self.resource.status != 200:
                raise errors.SendHubAPIException("Failed to GET %s" % args[0])
        
        # determine where we should expect and process json
        # we also storify the results so we can access
        # nested elements with class dot notation
        expect_json = kwargs['headers'].get('Accept', False)

        log.debug("<= GET %s: %s" % (args[0], response))
                
        # if we sent headers expecting json, then we enforce json
        if expect_json:
            try:
                json_response = json.loads(response)
            except:
                raise errors.SendHubAPIException("Failed to GET %s: expected JSON response but got %s" % (args[0], response))
            
            # return storified json response list
            return Storify(json_response)   
             
        else:
            return response
    
    @retry_wrapper(constants.MAX_API_RETRIES)        
    def post(self, *args, **kwargs):
        '''Wrapper for Resource.post that adds basic authorization'''

        # add authentication and version to url requested
        args, kwargs = self._rewrite_url(*args, **kwargs)

        log.debug("=> POST %s: %r (sent body payload: %s)", args[0], kwargs, kwargs.get('payload', False) is not False)

        if 'headers' not in kwargs:
            kwargs['headers'] = self._default_headers()

        sent_json = False
        
        if kwargs.get('json', False):
            
            # pop json param
            kwargs.pop('json')
            
            # note we are sending json
            sent_json = True
            
            # make a copy of our kwargs
            kwargs_copy = kwargs
            
            # throw away argument
            headers     = kwargs_copy.pop('headers')
            
            # convert kwargs to json
            post_payload = json.dumps(kwargs_copy)
            
            # debug
            log.debug("=> POST %s Sending JSON: %r", args[0], post_payload)
            
            # post a payload
            response = self.resource.post(args[0], payload=post_payload, headers=headers)
        
        else:
            
            # do a normal form post
            response = self.resource.post(*args, **kwargs)
            
        if self.resource.status not in [200, 201, 202]:
            raise errors.SendHubAPIException("Received non-success http code (%s) during POST %s: %s" % (self.resource.status, args[0], response))

        # determine where we should expect and process json
        # by assuming that if we sent json, we will expect
        # a json response, otherwise, if we sent a header
        # accepting json, then we would also expect a
        # json response

        if sent_json:
            expect_json = True
        
        else: 
            if kwargs['headers'].get('Accept', False) == 'application/json':
                expect_json = True
        
        # debug api activity
        log.debug("<= POST %s: %s" % (args[0], response))
        
        # if we sent headers expecting json, then we enforce json
        if expect_json:
            try:
                json_response = json.loads(response)
            except:
                raise errors.SendHubAPIException("Failed to POST %s: expected JSON response but got %s" % (args[0], response))
            
            # if it is json, and we find a success field
            # ensure we were successful
            status = json_response.get('status', 'success')
            if status != 'success':
                raise errors.SendHubAPIException("Failed to POST %s: %s" % (args[0], response))
            
            # return storified json response list which allows us to access
            # attributes as class properties instead of that gnarly dict
            # syntax          
            return Storify(json_response)
        else:
            return response

    @retry_wrapper(constants.MAX_API_RETRIES)
    def put(self, *args, **kwargs):
        '''Wrapper for Resource.put that adds basic authorization'''

        # add authentication and version to url requested
        args, kwargs = self._rewrite_url(*args, **kwargs)

        log.debug("=> PUT %s: %r (sent body payload: %s)", args[0], kwargs, kwargs.get('payload', False) is not False)


        if 'headers' not in kwargs:
            kwargs['headers'] = self._default_headers()

        sent_json = False
        if kwargs.get('json', False):
            
            # pop json param
            kwargs.pop('json')
            
            # note we are sending json
            sent_json = True
            
            # make a copy of our kwargs
            kwargs_copy = kwargs
            
            # throw away argument
            headers     = kwargs_copy.pop('headers')
            
            # convert kwargs to json
            put_payload = json.dumps(kwargs_copy)
            
            # debug
            log.debug("Sending PUT JSON: %s" % put_payload)
            
            # post a payload
            response = self.resource.post(args[0], payload=put_payload, headers=headers)
        
        else:
            
            # do a normal form post
            response = self.resource.put(*args, **kwargs)
            
        if self.resource.status not in [200, 201, 202]:
            raise errors.SendHubAPIException("Received non-success http code (%s) during PUT %s: %s" % (self.resource.status, args[0], response))

        # determine where we should expect and process json
        # by assuming that if we sent json, we will expect
        # a json response, otherwise, if we sent a header
        # accepting json, then we would also expect a
        # json response

        if sent_json:
            expect_json = True
        
        else: 
            if kwargs['headers'].get('Accept', False) == 'application/json':
                expect_json = True
        
        # debug api activity
        log.debug("<= PUT %s: %s" % (args[0], response))
        
        # if we sent headers expecting json, then we enforce json
        if expect_json:
            try:
                json_response = json.loads(response)
            except:
                raise errors.SendHubAPIException("Failed to PUT %s: expected JSON response but got %s" % (args[0], response))
            
            # if it is json, and we find a success field
            # ensure we were successful
            status = json_response.get('status', 'success')
            if status != 'success':
                raise errors.SendHubAPIException("Failed to PUT %s: %s" % (args[0], response))
            
            # return storified json response list which allows us to access
            # attributes as class properties instead of that gnarly dict
            # syntax          
            return Storify(json_response)
        else:
            return response
    
    @retry_wrapper(constants.MAX_API_RETRIES)    
    def delete(self, *args, **kwargs):
        '''Wrapper for Resource.delete that adds basic authorization'''

        # add authentication and version to url requested
        args, kwargs = self._rewrite_url(*args, **kwargs)
        
        if 'headers' not in kwargs:
            kwargs['headers'] = self._default_headers()
        response = self.resource.delete(*args, **kwargs)
        if self.resource.status not in [200, 201, 202]:
            raise errors.SendHubAPIException("Failed to DELETE %s" % args[0])
        return response
        
    def _default_headers(self):
        '''
        Creates default headers necessary to ensure
        json return data
        '''
        
        # construct default headers
        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
        }
        return headers
    
    def _rewrite_url(self, *args, **kwargs):
        '''
        Rewrite the url specified so it includes
        the version requested by the user and the
        appropriate authorization parameters
        '''
        url = args[0]
        
        new_url = '/%s/%s/' % (self.version,
                               url)
        
        # add version to url
        new_args = list(args)
        new_args[0] = new_url
        
        # add authentication to params
        kwargs['username']  = self.auth_user
        kwargs['api_key']   = self.auth_key

        return tuple(new_args), kwargs
