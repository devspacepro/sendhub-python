'''

Class for manipulating and representing SendHub messages

'''

class Message(object):
    
    def __init__(self,
                 connection,
                 text="", 
                 contacts=[],
                 acknowledgement=None,
                 created_at=None,
                 direction=None,
                 groups=None,
                 id=None,
                 resource_uri=None,
                 scheduled_at=None,
                 sent=None,
                 unread=None,
                 shortlink=None):
        
        '''
        Messages will rarely if ever need to be instantiated directly
        by the user.  Instead, use the Connection.send_message,
        Connection.get_message, and Connection.list_messages methods
        
        contacts       The list of contacts ids you would like to send to. Max 20.
        groups         The list of groups ids you would like to send to. Max 3.
        text           The text of the message. Max 500 chars.
        scheduled_at   If the message was scheduled, the UTC time it was scheduled.
        unread         If the message is inbound, is it unread.
        created_at     The UTC time this message was created. Read Only.
        sent           The UTC time the message was sent. Null if not yet sent. Read only.
        direction      The direction of the message. To = outbound, from = inbound. Read only.
        acknowledgment Information on your successful message sending request. Read only.
        resource_uri   The uri for this message. Read only.      
        shortlink      A small uri
        '''

        self.conn            = connection
        self.id              = id        
        self.text            = text
        self.contacts        = contacts
        self.acknowledgement = acknowledgement
        self.created_at      = created_at
        self.direction       = direction
        self.groups          = groups
        self.resource_uri    = resource_uri
        self.scheduled_at    = scheduled_at
        self.sent            = sent
        self.unread          = unread
        self.shortlink       = shortlink
         
    def __str__(self):
        return "<Message text=%s>" % self.text
    
    def __getitem__(self, key):
        return self.get_message()
    
class MessageResults(object):
    """
    An iterable results set object for Messages.

    This class implements dictionary- and list-like interfaces.
    """
    def __init__(self, conn, messages=list()):
        self._messages = messages
        self._names = [k.id for k in messages]
        self.conn = conn

    def __getitem__(self, key):
        return self._messages[key]

    def __getslice__(self, i, j):
        return [Message(self.conn, **k) for k in self._messages[i:j]]
    
    def __contains__(self, item):
        return item in self._names

    def __repr__(self):
        return 'MessageResults: %s Messages' % len(self._messages)
    __str__ = __repr__

    def __len__(self):
        return len(self._messages)

    def index(self, value, *args):
        """
        returns an integer for the first index of value
        """
        return self._names.index(value, *args)

    def count(self, value):
        """
        returns the number of occurrences of value
        """
        return self._names.count(value)
