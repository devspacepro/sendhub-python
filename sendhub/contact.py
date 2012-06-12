'''

Class for manipulating and representing SendHub contacts

'''

class Contact(object):
    
    def __init__(self,
                 connection,
                 name="", 
                 number="",
                 groups=None,
                 date_created=None,
                 date_modified=None,
                 id=None,
                 blocked=None,
                 resource_uri=None):
        
        '''
        Contacts will rarely if ever need to be instantiated directly
        by the user.  Instead, use the Connection.create_contact,
        Connection.get_contact, and Connection.list_contacts methods

        id            The unique identifier of your new contact. Read only.
        name          The name of your new contact.
        number        The new contacts cell phone number.
        groups        The list of group ids to which this contact will be added
        resource_uri  The uri to access this contacts data.
        blocked       Boolean. True if this contact has blocked your number. Read only.
        date_created  The UTC time this contact was created. Read only.
        date_modified The UTC time this contact was last changed. Read only.
        '''

        self.id              = id        
        self.name            = name
        self.number          = number
        self.groups          = groups
        self.resource_uri    = resource_uri
        self.blocked         = blocked
        self.date_created    = date_created
        self.date_modified   = date_modified
