'''
Created on Dec 8, 2009

@author: alan
'''

class Storify(dict):
    '''
    This class is defined here to return storage objects.  When
    we return a Storage instance we can access the stored
    information either as a dictionary or as an element of the
    class.  Basically, it makes things look cleaner.
    '''

    def __getattr__(self, key):
        try:
            if isinstance(self[key], dict):
                return Storify(self[key])
            elif isinstance(self[key], list):
                return [Storify(elem) for elem in self[key]]
            else:
                return self[key]
        except KeyError, k:
            raise AttributeError, k

    def __setattr__(self, key, value):
        self[key] = value

    def __delattr__(self, key):
        try:
            del self[key]
        except KeyError, k:
            raise AttributeError, k
       
    def __repr__(self):
        return '<Storify ' + dict.__repr__(self) + '>'
